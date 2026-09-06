import ast
import datetime
import html
import random

# Reuse the four existing phrase lists without duplicating them.
with open("generate_rss.py", "r", encoding="utf-8") as f:
    source = f.read()

tree = ast.parse(source)
namespace = {}
for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        exec(compile(ast.Module(body=[node], type_ignores=[]), "generate_rss.py", "exec"), namespace)
    elif isinstance(node, ast.Assign):
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        if any(name in {"blake", "lei", "sorel", "anaya"} for name in names):
            exec(compile(ast.Module(body=[node], type_ignores=[]), "generate_rss.py", "exec"), namespace)

blake = namespace["blake"]
lei = namespace["lei"]
sorel = namespace["sorel"]
anaya = namespace["anaya"]


def make_speech_schedule(rng):
    """Return 80 non-empty masks with exactly 40 speaking slots per voice."""
    remaining = [40, 40, 40, 40]
    schedule = []

    for position in range(80):
        slots_left_after = 79 - position
        possible = []

        # A non-empty subset of the four voices is valid if it does not
        # consume a voice's final remaining slot too early.
        for mask in range(1, 16):
            selected = [(mask >> v) & 1 for v in range(4)]
            if any(selected[v] > remaining[v] for v in range(4)):
                continue
            if any(remaining[v] - selected[v] > slots_left_after for v in range(4)):
                continue
            possible.append(mask)

        mask = rng.choice(possible)
        schedule.append(mask)
        for v in range(4):
            remaining[v] -= (mask >> v) & 1

    assert remaining == [0, 0, 0, 0]
    return schedule


def generate_feed():
    sources = [
        (">_ BLAKE :", blake),
        (">_ LEI :", lei),
        (">_ SOREL :", sorel),
        (">_ ANAYA :", anaya),
    ]

    for author, phrases in sources:
        if len(phrases) != 40:
            raise ValueError(f"Chaque voix doit contenir 40 phrases : {author} en contient {len(phrases)}")

    now = datetime.datetime.now(datetime.timezone.utc)
    slot = int(now.timestamp() // (15 * 60))
    cycle = slot // 80
    position = slot % 80

    # One deterministic 80-sequence cycle: each voice speaks 40 times,
    # remains silent 40 times, and no sequence is completely silent.
    schedule_rng = random.Random(cycle * 10000 + 17)
    schedule = make_speech_schedule(schedule_rng)
    mask = schedule[position]

    selected = []
    for voice_index, (author, phrases) in enumerate(sources):
        phrase_order = list(range(40))
        phrase_rng = random.Random(cycle * 100 + voice_index)
        phrase_rng.shuffle(phrase_order)

        speaks_before = sum((schedule[s] >> voice_index) & 1 for s in range(position))
        if (mask >> voice_index) & 1:
            selected.append((author, phrases[phrase_order[speaks_before]]))
        else:
            selected.append((author, "..."))

    # The four visible entries change order from one sequence to the next.
    display_rng = random.Random(slot)
    display_rng.shuffle(selected)

    selected_phrases = {(author, text) for author, text in selected if text != "..."}
    remaining = []
    for author, phrases in sources:
        for phrase in phrases:
            if (author, phrase) not in selected_phrases:
                remaining.append((author, phrase))

    display_rng.shuffle(remaining)
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

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss)


generate_feed()
