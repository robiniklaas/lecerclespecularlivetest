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

if not all(len(phrases) == 30 for _, phrases in sources):
    raise ValueError("Le corpus originel doit contenir exactement 30 phrases par voix")

dialogue_units = list(range(30))


def make_speech_schedule(rng):
    """80 slots: 10 singles, 62 duos, 6 trios, 2 quads; 40 turns/voice.

    All six possible voice pairings are represented. Pairing counts are
    11,11,10,10,10,10 before conversion to singles/trios/quads.
    """
    pairings = (
        [(0, 1)] * 11 + [(2, 3)] * 11 +
        [(0, 2)] * 10 + [(0, 3)] * 10 +
        [(1, 2)] * 10 + [(1, 3)] * 10
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


def make_dialogue_units(cycle):
    """Randomly place 80 unit occurrences: each of 30 units occurs 2 or 3 times."""
    rng = random.Random(cycle * 1000003 + 31)
    occurrences = dialogue_units * 2
    extra = dialogue_units[:]
    rng.shuffle(extra)
    occurrences.extend(extra[:20])
    rng.shuffle(occurrences)
    return occurrences


def generate_feed():
    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    schedule = make_speech_schedule(random.Random(cycle * 10000 + 17))
    mask = schedule[position]
    unit_index = make_dialogue_units(cycle)[position]

    selected = []
    for voice_index, (author, phrases) in enumerate(sources):
        text = phrases[unit_index] if (mask >> voice_index) & 1 else "..."
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
