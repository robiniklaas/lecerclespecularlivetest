import ast
import datetime
import html
import random
from pathlib import Path

# Reuse the four existing phrase lists without duplicating or changing them.
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
    """Create 80 sequences with 2, 3, or 4 speaking voices.

    Every voice speaks exactly 40 times across the 80-slot cycle.
    Half the sequences have 2 speakers, one quarter have 3, and one
    quarter have 4, for 160 total speaking turns.
    """
    # Start with 20 sequences of each balanced pair. This gives every voice
    # 20 speaking turns. Then add 40 extra speaking turns: 20 single
    # additions (creating 20 three-voice sequences) and 20 double additions
    # (creating 20 four-voice sequences). The additions are balanced so each
    # voice receives exactly 20 more turns.
    pairings = [
        (0, 1), (2, 3),
        (0, 2), (1, 3),
    ] * 20
    rng.shuffle(pairings)

    schedule = [
        (1 << a) | (1 << b)
        for a, b in pairings
    ]

    # Ten singleton additions per voice -> 40 additions total, but to get a
    # controlled mix of 3- and 4-voice sequences we use 20 single additions
    # and 10 pair additions. Each voice gets 10 additions from each category.
    single_additions = [v for v in range(4) for _ in range(5)]
    rng.shuffle(single_additions)

    # Pair additions: the four-cycle pairs each occur 5 times, giving every
    # voice 10 additional turns.
    pair_additions = [
        (0, 1), (1, 2), (2, 3), (3, 0)
    ] * 5
    rng.shuffle(pair_additions)

    # Apply 20 single additions to 20 pair sequences, then 20 pair additions
    # to another 20 pair sequences. This creates 20 triples and 20 quadruples.
    for index, voice in enumerate(single_additions):
        base_index = index
        mask = schedule[base_index]
        if mask & (1 << voice):
            # If the chosen voice is already present, rotate until absent.
            for candidate in range(4):
                if not (mask & (1 << candidate)):
                    voice = candidate
                    break
        schedule[base_index] = mask | (1 << voice)

    for index, (a, b) in enumerate(pair_additions):
        base_index = 20 + index
        mask = schedule[base_index]
        # The pair must both be absent to create a four-voice sequence.
        # If not, choose the missing voices instead; every base has exactly 2.
        missing = [v for v in range(4) if not (mask & (1 << v))]
        if len(missing) == 2:
            schedule[base_index] = mask | (1 << missing[0]) | (1 << missing[1])
        else:
            schedule[base_index] = 15

    rng.shuffle(schedule)

    # Verify the invariants before returning.
    counts = [sum((mask >> v) & 1 for mask in schedule) for v in range(4)]
    if counts != [40, 40, 40, 40]:
        raise RuntimeError(f"Répartition invalide : {counts}")
    if any(mask.bit_count() < 2 or mask.bit_count() > 4 for mask in schedule):
        raise RuntimeError("Chaque séquence doit avoir entre 2 et 4 voix")
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
        order = list(range(40))
        random.Random(cycle * 100 + voice_index).shuffle(order)
        speaks_before = sum((schedule[s] >> voice_index) & 1 for s in range(position))

        if (mask >> voice_index) & 1:
            text = phrases[order[speaks_before]]
        else:
            text = "..."
        selected.append((author, text))

    # The four voice entries change order from one sequence to the next.
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
