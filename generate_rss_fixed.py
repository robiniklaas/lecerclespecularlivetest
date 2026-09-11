import ast
import datetime
import html
import random
from pathlib import Path

# Reuse the four existing phrase lists from generate_rss.py.
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

for author, phrases in sources:
    if len(phrases) < 40:
        raise ValueError(f"Chaque voix doit contenir au moins 40 phrases : {author} en contient {len(phrases)}")


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


def generate_feed():
    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    schedule = make_speech_schedule(random.Random(cycle * 10000 + 17))
    mask = schedule[position]

    selected = []
    for voice_index, (author, phrases) in enumerate(sources):
        # A cycle has 40 speaking turns per voice. The corpus is never
        # truncated: if a voice has more than 40 phrases, exactly two phrases
        # are left for the next cycles. The omitted pair rotates, so every
        # phrase is eventually spoken and no phrase is permanently excluded.
        omitted_a = cycle % len(phrases)
        omitted_b = (omitted_a + 1) % len(phrases)
        omitted = {omitted_a, omitted_b}
        order = [i for i in range(len(phrases)) if i not in omitted]
        rng = random.Random(cycle * 100 + voice_index)
        rng.shuffle(order)
        speaks_before = sum((schedule[s] >> voice_index) & 1 for s in range(position))

        if (mask >> voice_index) & 1:
            text = phrases[order[speaks_before]]
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
