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

if not all(phrases for _, phrases in sources):
    raise ValueError("Chaque voix doit contenir au moins une phrase")

DIALOGUE_UNIT_COUNT = max(len(phrases) for _, phrases in sources)

def make_speech_schedule(rng):
    """80 slots: 10 singles, 62 duos, 6 trios, 2 quads; 40 turns/voice."""
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


def _make_one_voice_sequence(voice_index, cycle, previous_tail=None):
    """Create 40 phrase indices with a 15/16-turn exact-repeat cooldown.

    The sequence is balanced over the whole cycle, but a phrase cannot recur
    while it is still inside the recent-memory window. The tail of the
    previous cycle is carried into the next cycle, so the boundary does not
    reset the memory and immediately repeat yesterday's phrases.
    """
    phrases = sources[voice_index][1]
    count = len(phrases)
    cooldown = min(16, count // 2)
    rng = random.Random(cycle * 1000003 + 31 + voice_index * 1009)

    # Start with one randomized pass through the whole corpus. This guarantees
    # that every phrase is represented at least once without forcing the same
    # phrase to recur at a fixed position in every cycle.
    first_pass = list(range(count))
    rng.shuffle(first_pass)
    sequence = []
    recent = list(previous_tail or [])[-cooldown:]

    def choose_candidate(candidates):
        candidates = [x for x in candidates if x not in recent]
        if not candidates:
            candidates = [x for x in range(count) if x not in recent]
        choice = rng.choice(candidates)
        sequence.append(choice)
        recent.append(choice)
        del recent[:-cooldown]
        return choice

    for phrase_index in first_pass:
        if phrase_index not in recent:
            choose_candidate([phrase_index])
        else:
            choose_candidate([x for x in first_pass if x not in sequence])

    while len(sequence) < 40:
        choose_candidate(list(range(count)))

    return sequence


def make_voice_phrase_schedules(cycle):
    """Build balanced phrase schedules with recent-use memory per voice."""
    schedules = {}
    for voice_index, (_, phrases) in enumerate(sources):
        previous = _make_one_voice_sequence(voice_index, cycle - 1) if cycle > 0 else []
        cooldown = min(16, len(phrases) // 2)
        schedules[voice_index] = _make_one_voice_sequence(
            voice_index, cycle, previous_tail=previous[-cooldown:]
        )
    return schedules


def generate_feed():
    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    schedule = make_speech_schedule(random.Random(cycle * 10000 + 17))
    mask = schedule[position]
    voice_phrase_schedules = make_voice_phrase_schedules(cycle)

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
