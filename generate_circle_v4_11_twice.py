#!/usr/bin/env python3
"""Two daily experimental V4.11 sequences, isolated from the V4.10 feed."""
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
VOICES = ["BLAKE", "LEI", "SOREL", "ANAYA"]
SLOTS = {"matin": 7, "soir": 19}


def main():
    now = datetime.now(timezone.utc)
    slot = "matin" if now.hour < 13 else "soir"
    day = now.date().isoformat()
    seed_base = int(day.replace("-", "")) * 1000 + (0 if slot == "matin" else 500)
    archive = ARCHIVE_ROOT / day / slot

    source = PROTOTYPE.read_text(encoding="utf-8")
    source, count = re.subn(r"^SEED = \d+\s*$", "SEED = {seed}", source, count=1, flags=re.M)
    if count != 1:
        raise RuntimeError("Impossible de remplacer la graine dans V4.11.")

    source, count = re.subn(
        r'if __name__ == "__main__":\s*corpus_check = load_corpus\(\).*\Z',
        'if __name__ == "__main__":\n    main("forte", Path(sys.argv[1]))\n',
        source, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Impossible de préparer l'exécution V4.11.")
    source = "import sys\n" + source

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
            turns = {}
            for row in rows:
                turns.setdefault(int(row["tour"]), []).append(row)
            active = [r for r in rows if r["type"] != "silence"]
            counts = Counter(r["voix"] for r in active)
            absent = [v for v in VOICES if counts[v] == 0]
            if len(turns) != 80 or sum(1 for r in rows if r["type"] == "silence") != 8:
                last_error = "La séquence ne comporte pas 80 tours et 8 silences."
                continue
            if len(absent) not in (0, 1, 2):
                last_error = f"Nombre de voix absentes invalide : {absent}"
                continue
            if any(len([r for r in group if r["voix"]]) > len(VOICES) - len(absent)
                   for group in turns.values()):
                last_error = "Un tour dépasse le nombre de voix présentes."
                continue

            if archive.exists():
                shutil.rmtree(archive)
            archive.mkdir(parents=True, exist_ok=True)
            for filename in ["sequence_80_tours.csv", "inventaire_annote.csv"]:
                shutil.copy2(output / filename, archive / filename)
            report = next(output.glob("rapport_v4_11_*.txt"))
            shutil.copy2(report, archive / "rapport_v4_11_forte.txt")

            payload = {
                "date": day, "slot": slot, "version": "V4.11 expérimentale",
                "seed": seed, "absent_voices": absent,
                "turns": [
                    {"turn": n, "type": group[0]["type"],
                     "entries": [{"voice": r["voix"], "text": r["phrase"]}
                                 for r in group if r["voix"]]}
                    for n, group in sorted(turns.items())
                ],
                "stats": {"turns": 80, "silences": 8,
                          "active_utterances": len(active),
                          "voices": dict(counts), "absent_voices": absent},
            }
            (archive / "sequence.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            (archive / "observation.txt").write_text(
                f"Cercle Specular — V4.11 expérimentale\nDate UTC : {day}\n"
                f"Tirage : {slot}\nGraine : {seed} (essai {attempt})\n"
                f"Voix absentes : {', '.join(absent) if absent else 'aucune'}\n"
                f"Prises de parole : {len(active)}\n"
                f"Répartition : {dict(counts)}\n"
                "Corpus source generate_rss.py : lecture seule\n",
                encoding="utf-8",
            )
            print(f"V4.11 {slot} publiée pour {day}; graine {seed}; absences {absent}.")
            return

    raise RuntimeError("Échec après 100 graines. Dernière erreur : " + last_error)


if __name__ == "__main__":
    main()
