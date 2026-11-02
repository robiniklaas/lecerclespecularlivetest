#!/usr/bin/env python3
"""Daily public sequence generator for experimental Cercle Specular V4.11.

Uses prototype_cercle_v4_11.py in a temporary copy. The source prototype,
V4.10 files and generate_rss.py remain unchanged.
"""
import csv
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOTYPE = ROOT / "prototype_cercle_v4_11.py"
ARCHIVE_ROOT = ROOT / "observations_v4_11"
PUBLIC_JSON = ROOT / "circle_daily.json"
VOICES = ["BLAKE", "LEI", "SOREL", "ANAYA"]


def main():
    day = datetime.now(timezone.utc).date().isoformat()
    seed_base = int(day.replace("-", "")) * 1000
    archive = ARCHIVE_ROOT / day
    source = PROTOTYPE.read_text(encoding="utf-8")
    source, count = re.subn(
        r"^SEED = \\d+\\s*$", "SEED = {seed}", source,
        count=1, flags=re.M
    )
    if count != 1:
        raise RuntimeError("Impossible de remplacer la graine dans V4.11.")

    source, count = re.subn(
        r'if __name__ == "__main__":\\s*corpus_check = load_corpus\\(\\).*\\Z',
        'if __name__ == "__main__":\\n    main("forte", Path(sys.argv[1]))\\n',
        source, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Impossible de préparer l'exécution V4.11 forte.")
    source = "import sys\\n" + source

    last_error = ""
    for attempt in range(1, 101):
        seed = seed_base + attempt - 1
        with tempfile.TemporaryDirectory(prefix="cercle-v411-") as temp:
            temp_path = Path(temp)
            patched = source.replace("SEED = {seed}", f"SEED = {seed}", 1)
            runner = temp_path / "prototype_run.py"
            output = temp_path / "result"
            runner.write_text(patched, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(runner), str(output)],
                cwd=ROOT, capture_output=True, text=True, timeout=120,
            )
            if proc.returncode != 0:
                last_error = (proc.stderr or proc.stdout)[-2000:]
                continue

            sequence_file = output / "sequence_80_tours.csv"
            if not sequence_file.exists():
                last_error = "Séquence CSV absente."
                continue
            with sequence_file.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))

            grouped = {}
            for row in rows:
                grouped.setdefault(int(row["tour"]), []).append(row)
            if len(grouped) != 80:
                last_error = f"Nombre de tours inattendu : {len(grouped)}"
                continue

            active = [r for r in rows if r["type"] != "silence"]
            counts = Counter(r["voix"] for r in active)
            absent = [v for v in VOICES if counts[v] == 0]
            if sum(1 for r in rows if r["type"] == "silence") != 8:
                last_error = "La séquence ne comporte pas exactement 8 silences."
                continue
            if len(absent) not in (0, 1, 2):
                last_error = f"Nombre de voix absentes invalide : {absent}"
                continue
            expected_active = 120 if len(absent) == 2 else 160
            if len(active) != expected_active:
                last_error = f"Nombre de prises inattendu : {len(active)} au lieu de {expected_active}."
                continue
            if counts and max(counts.values()) - min(counts.values()) > 1:
                last_error = f"Répartition des voix déséquilibrée : {dict(counts)}"
                continue
            duplicate_turns = []
            for number, group in grouped.items():
                present = [r["voix"] for r in group if r["voix"]]
                if len(present) != len(set(present)):
                    duplicate_turns.append(number)
            if duplicate_turns:
                last_error = f"Voix répétées dans un même tour : {duplicate_turns}"
                continue

            if archive.exists():
                shutil.rmtree(archive)
            archive.mkdir(parents=True, exist_ok=True)
            for filename in ["sequence_80_tours.csv", "inventaire_annote.csv"]:
                shutil.copy2(output / filename, archive / filename)
            report = next(output.glob("rapport_v4_11_*.txt"))
            shutil.copy2(report, archive / "rapport_v4_11_forte.txt")

            turns = []
            for number in range(1, 81):
                group = grouped[number]
                turns.append({
                    "turn": number,
                    "type": group[0]["type"],
                    "entries": [
                        {"voice": row["voix"], "text": row["phrase"]}
                        for row in group if row["voix"]
                    ],
                })

            payload = {
                "date": day,
                "version": "V4.11 expérimentale",
                "seed": seed,
                "absent_voices": absent,
                "turns": turns,
                "stats": {
                    "turns": 80,
                    "silences": 8,
                    "active_utterances": len(active),
                    "voices": dict(counts),
                    "absent_voices": absent,
                },
            }
            PUBLIC_JSON.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\\n",
                encoding="utf-8",
            )
            (archive / "observation.txt").write_text(
                "Cercle Specular — V4.11 expérimentale\\n"
                f"Date UTC : {day}\\nGraine : {seed} (essai {attempt})\\n"
                f"Voix absentes : {', '.join(absent) if absent else 'aucune'}\\n"
                f"Prises de parole : {len(active)}\\n"
                f"Répartition : {dict(counts)}\\n"
                f"Silences : {[n for n, g in grouped.items() if g[0]['type'] == 'silence']}\\n"
                "Corpus source generate_rss.py : lecture seule\\n"
                "Prototype V4.10 et corpus source : inchangés\\n",
                encoding="utf-8",
            )
            print(
                f"V4.11 publiée pour {day}; graine {seed}; "
                f"voix absentes {absent}; {len(active)} prises."
            )
            return

    raise RuntimeError("Échec après 100 graines. Dernière erreur : " + last_error)


if __name__ == "__main__":
    main()
