import ast
import datetime
import html
import random
from pathlib import Path

source_text = Path("generate_rss.py").read_text(encoding="utf-8")
tree = ast.parse(source_text)
phrase_lists = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {"blake", "lei", "sorel", "anaya"}:
                phrase_lists[target.id] = ast.literal_eval(node.value)

sources = [
    (">_ BLAKE :", phrase_lists["blake"]),
    (">_ LEI :", phrase_lists["lei"]),
    (">_ SOREL :", phrase_lists["sorel"]),
    (">_ ANAYA :", phrase_lists["anaya"]),
]

# The four voice corpora may now contain different numbers of phrases.
# The dialogue uses the longest corpus length and wraps shorter corpora,
# so no phrase is discarded and no voice can cause an index error.
if not all(phrases for _, phrases in sources):
    raise ValueError("Chaque voix doit contenir au moins une phrase")

DIALOGUE_UNIT_COUNT = max(len(phrases) for _, phrases in sources)
dialogue_units = list(range(DIALOGUE_UNIT_COUNT))


def make_speech_schedule(rng):
    """80 slots: 10 singles, 62 duos, 6 trios, 2 quads; 40 turns/voice.

    All six possible voice pairings are represented. We begin with 80 duos,
    balanced so that every voice appears 40 times, then convert 10 to singles,
    6 to trios and 2 to quads while preserving the final 40 turns per voice.
    """
    pairings = (
        [(0, 1)] * 14 + [(2, 3)] * 14 +
        [(0, 2)] * 13 + [(0, 3)] * 13 +
        [(1, 2)] * 13 + [(1, 3)] * 13
    )
    rng.shuffle(pairings)
    schedule = [(1 << a) | (1 << b) for a, b in pairings]

    removal_voices = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3]
    addition_voices = [0, 0, 1, 1, 2, 3]
    quad_additions = [(0, 1), (2, 3)]
    rng.shuffle(removal_voices)
    rng.shuffle(addition_voices)
    rng.shuffle(quad_additions)
    used = set()

    for voice in removal_voices:
        candidates = [i for i, mask in enumerate(schedule)
                      if i not in used and (mask & (1 << voice))]
        index = rng.choice(candidates)
        used.add(index)
        schedule[index] &= ~(1 << voice)

    for voice in addition_voices:
        candidates = [i for i, mask in enumerate(schedule)
                      if i not in used and not (mask & (1 << voice))]
        index = rng.choice(candidates)
        used.add(index)
        schedule[index] |= 1 << voice

    for a, b in quad_additions:
        candidates = [i for i, mask in enumerate(schedule)
                      if i not in used and not (mask & (1 << a)) and not (mask & (1 << b))]
        index = rng.choice(candidates)
        used.add(index)
        schedule[index] |= (1 << a) | (1 << b)

    rng.shuffle(schedule)
    counts = [sum((mask >> v) & 1 for mask in schedule) for v in range(4)]
    size_counts = {size: sum(mask.bit_count() == size for mask in schedule) for size in range(1, 5)}
    if counts != [40, 40, 40, 40] or size_counts != {1: 10, 2: 62, 3: 6, 4: 2}:
        raise RuntimeError(f"Répartition invalide : voices={counts}, sizes={size_counts}")
    return schedule


def make_voice_phrase_schedules(cycle):
    """Build one balanced 40-turn phrase schedule for each voice.

    Each voice speaks exactly 40 times per 80-slot cycle. Its own corpus is
    balanced independently, so corpora with 30 and 32 phrases do not create
    modulo bias. Every phrase appears at least once per cycle; the remainder
    is distributed randomly among phrases.
    """
    schedules = {}
    for voice_index, (_, phrases) in enumerate(sources):
        rng = random.Random(cycle * 1000003 + 31 + voice_index * 1009)
        base = list(range(len(phrases)))
        occurrences = []
        while len(occurrences) < 40:
            batch = base[:]
            rng.shuffle(batch)
            occurrences.extend(batch)
        occurrences = occurrences[:40]
        rng.shuffle(occurrences)
        schedules[voice_index] = occurrences
    return schedules


def generate_feed():
    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    schedule = make_speech_schedule(random.Random(cycle * 10000 + 17))
    mask = schedule[position]
    voice_phrase_schedules = make_voice_phrase_schedules(cycle)

    # Count the turn number of each voice up to this position. The phrase
    # schedule is independent for each voice, so only that voice's own turns
    # advance its phrase sequence.
    selected = []
    turns_so_far = [0, 0, 0, 0]
    for previous_mask in schedule[:position]:
        for voice_index in range(4):
            if (previous_mask >> voice_index) & 1:
                turns_so_far[voice_index] += 1

    for voice_index, (author, phrases) in enumerate(sources):
        if (mask >> voice_index) & 1:
            phrase_index = voice_phrase_schedules[voice_index][turns_so_far[voice_index]]
            text = phrases[phrase_index]
            turns_so_far[voice_index] += 1
        else:
            text = "..."
        selected.append((author, text))
    random.Random(slot).shuffle(selected)

    selected_phrases = {(author, text) for author, text in selected if text != "..."}
    remaining = []
    for author, phrases in sources:
        for phrase in phrases:
            if (author, phrase) not in selected_phrases:
                remaining.append((author, phrase))
    random.Random(slot + 1).shuffle(remaining)
    items = selected + remaining

    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss_items = []
    for index, (author, text) in enumerate(items):
        rss_items.append(f'''<item>
<title>{html.escape(author)}</title>
<description>{html.escape(text)}</description>
<pubDate>{pub_date}</pubDate>
<guid isPermaLink="false">{slot}-{index:03d}</guid>
</item>''')

    rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>cercle specular — inter_view</title>
<description>flux evolutif — {now.isoformat()}</description>
<link>https://example.com</link>

{chr(10).join(rss_items)}

</channel>
</rss>
'''
    Path("feed.xml").write_text(rss, encoding="utf-8")


generate_feed()
