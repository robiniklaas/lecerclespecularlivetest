import ast
import datetime
import html
import random
from pathlib import Path

# Reuse the four original phrase lists from generate_rss.py.
# The four phrases at the same index form one invisible dialogic unit.
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

# 30 invisible dialogic units: Blake[i], Lei[i], Sorel[i], Anaya[i]
# belong to the same underlying thought, even when only some voices speak.
dialogue_units = list(range(30))


def make_speech_schedule(rng):
    """Create 80 sequences with 1, 2, 3, or 4 speaking voices.

    Every voice speaks exactly 40 times across the 80-slot cycle.
    The cycle contains 10 single-voice, 62 two-voice, 6 three-voice,
    and 2 four-voice sequences.
    """
    pairings = [(0, 1), (2, 3), (0, 2), (1, 3)] * 20
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
        if not candidates:
            raise RuntimeError("Impossible de construire les séquences à une voix")
        index = candidates[0]
        used.add(index)
        schedule[index] &= ~(1 << voice)

    for voice in addition_voices:
        candidates = [i for i, mask in enumerate(schedule)
                      if i not in used and not (mask & (1 << voice))]
        if not candidates:
            raise RuntimeError("Impossible de construire les séquences à trois voix")
        index = candidates[0]
        used.add(index)
        schedule[index] |= (1 << voice)

    for a, b in quad_additions:
        candidates = [i for i, mask in enumerate(schedule)
                      if i not in used and not (mask & (1 << a)) and not (mask & (1 << b))]
        if not candidates:
            raise RuntimeError("Impossible de construire les séquences à quatre voix")
        index = candidates[0]
        used.add(index)
        schedule[index] |= (1 << a) | (1 << b)

    rng.shuffle(schedule)

    counts = [sum((mask >> v) & 1 for mask in schedule) for v in range(4)]
    size_counts = {size: sum(mask.bit_count() == size for mask in schedule) for size in range(1, 5)}
    if counts != [40, 40, 40, 40]:
        raise RuntimeError(f"Répartition invalide : {counts}")
    if size_counts != {1: 10, 2: 62, 3: 6, 4: 2}:
        raise RuntimeError(f"Répartition des séquences invalide : {size_counts}")
    return schedule


def make_dialogue_units(cycle):
    """Distribute the 30 latent units across the 80 slots.

    The unit is attached to the slot, not to an individual voice. Therefore,
    whenever two or more voices speak together, they draw their phrases from
    the same invisible unit and can genuinely answer one another.

    The 30 units are shuffled deterministically for each 20-hour cycle and
    repeated as needed to cover all 80 slots. No phrase is removed from the
    corpus; repetition is simply a consequence of having 40 speaking turns
    per voice but only 30 dialogic units.
    """
    rng = random.Random(cycle * 1000003 + 31)
    order = dialogue_units[:]
    rng.shuffle(order)
    return [order[i % 30] for i in range(80)]


def generate_feed():
    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    schedule = make_speech_schedule(random.Random(cycle * 10000 + 17))
    mask = schedule[position]
    slot_units = make_dialogue_units(cycle)
    unit_index = slot_units[position]

    selected = []
    for voice_index, (author, phrases) in enumerate(sources):
        if (mask >> voice_index) & 1:
            # The same latent unit is used by every voice speaking in this slot.
            # A voice therefore answers through its corresponding phrase rather
            # than drawing independently from an unrelated phrase pool.
            text = phrases[unit_index]
        else:
            text = "..."
        selected.append((author, text))

    random.Random(slot).shuffle(selected)

    # Keep the complete 120-phrase corpus in every RSS generation.
    # The four visible positions are simply the current dialogue moment;
    # all other original phrases remain available in the feed.
    selected_phrases = {(author, text) for author, text in selected if text != "..."}
    remaining = []
    for author, phrases in sources:
        for phrase in phrases:
            if (author, phrase) not in selected_phrases:
                remaining.append((author, phrase))
    random.Random(slot + 1).shuffle(remaining)

    items = selected + remaining
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    now_iso = now.isoformat()

    rss_items = []
    for index, (author, text) in enumerate(items):
        rss_items.append(
            f"""<item>
<title>{html.escape(author)}</title>
<description>{html.escape(text)}</description>
<pubDate>{pub_date}</pubDate>
<guid isPermaLink=\"false\">{slot}-{index:03d}</guid>
</item>"""
        )

    rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>cercle specular — inter_view</title>
<description>flux evolutif — {now_iso}</description>
<link>https://example.com</link>

{chr(10).join(rss_items)}

</channel>
</rss>
'''
    Path("feed.xml").write_text(rss, encoding="utf-8")


generate_feed()
