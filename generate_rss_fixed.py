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
    if len(phrases) != 40:
        raise ValueError(f"Chaque voix doit contenir 40 phrases : {author} en contient {len(phrases)}")


def make_speech_schedule(rng):
    """Create 80 non-empty sequences with exactly 40 turns per voice."""
    remaining = [40, 40, 40, 40]
    schedule = []

    for position in range(80):
        left = 79 - position
        possible = []

        # A mask is valid if it speaks for at least one voice, never speaks
        # for a voice with no turns left, and leaves every voice enough
        # positions to use all its remaining turns.
        for mask in range(1, 16):
            if any(((mask >> v) & 1) > remaining[v] for v in range(4)):
                continue
            if any(remaining[v] - ((mask >> v) & 1) > left for v in range(4)):
                continue
            possible.append(mask)

        if not possible:
            raise RuntimeError("Impossible de construire le cycle de parole")

        mask = rng.choice(possible)
        schedule.append(mask)
        for v in range(4):
            remaining[v] -= (mask >> v) & 1

    if remaining != [0, 0, 0, 0]:
        raise RuntimeError("Le cycle n'utilise pas exactement 40 prises de parole par voix")
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
