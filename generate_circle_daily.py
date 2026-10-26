#!/usr/bin/env python3
"""Daily public sequence generator for Cercle Specular V4.10 forte.

Keeps prototype_cercle_v4_10.py and generate_rss.py unchanged.
Retries deterministic seeds until the prototype produces a balanced sequence.
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
PROTOTYPE = ROOT / "prototype_cercle_v4_10.py"
ARCHIVE_ROOT = ROOT / "observations_v4_10_forte"
PUBLIC_JSON = ROOT / "circle_daily.json"
VOICES = ["BLAKE", "LEI", "SOREL", "ANAYA"]


def main():
    day = datetime.now(timezone.utc).date().isoformat()
    seed_base = int(datetime.now(timezone.utc).strftime("%Y%m%d"))
    archive = ARCHIVE_ROOT / day
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    source = PROTOTYPE.read_text(encoding="utf-8")
    source, count = re.subn(r"^SEED = \d+\s*$", "SEED = {seed}", source, count=1, flags=re.M)
    if count != 1:
        raise RuntimeError("Impossible de remplacer la graine dans le prototype V4.10.")

    # Keep the prototype source unchanged; run a temporary copy in forte mode only.
    source, count = re.subn(
        r'if __name__ == "__main__":\s*corpus_check = load_corpus\(\).*\Z',
        'if __name__ == "__main__":\n    main("forte", Path(sys.argv[1]))\n',
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("Impossible de préparer l'exécution V4.10 forte.")
    source = "import sys\n" + source

    if archive.exists():
        shutil.rmtree(archive)

    last_error = ""
    for attempt in range(1, 101):
        seed = seed_base + attempt - 1
        with tempfile.TemporaryDirectory(prefix="cercle-v410-") as temp:
            temp_path = Path(temp)
            patched = source.replace("SEED = {seed}", f"SEED = {seed}", 1)
            runner = temp_path / "prototype_run.py"
            output = temp_path / "result"
            runner.write_text(patched, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(runner), str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if proc.returncode != 0:
                last_error = (proc.stderr or proc.stdout)[-2000:]
                continue

            sequence_file = output / "sequence_80_tours.csv"
            if not sequence_file.exists():
                last_error = "Le prototype n'a pas produit sequence_80_tours.csv."
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
            if len(active) != 160 or any(counts[v] != 40 for v in VOICES):
                last_error = f"Équilibre incorrect : {len(active)} prises, {dict(counts)}"
                continue

            archive.mkdir(parents=True, exist_ok=True)
            for filename in [
                "sequence_80_tours.csv",
                "inventaire_annote.csv",
                "rapport_v4_10_forte.txt",
            ]:
                shutil.copy2(output / filename, archive / filename)

            turns = []
            for number in range(1, 81):
                group = grouped[number]
                turn_type = group[0]["type"]
                entries = []
                for row in group:
                    if row["voix"]:
                        entries.append({"voice": row["voix"], "text": row["phrase"]})
                turns.append({
                    "turn": number,
                    "type": turn_type,
                    "entries": entries,
                })

            payload = {
                "date": day,
                "version": "V4.10 forte",
                "seed": seed,
                "turns": turns,
                "stats": {
                    "turns": 80,
                    "silences": sum(1 for t in turns if t["type"] == "silence"),
                    "active_utterances": len(active),
                    "voices": dict(counts),
                },
            }
            PUBLIC_JSON.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            (archive / "observation.txt").write_text(
                f"Observation quotidienne du Cercle Specular — V4.10 forte\n"
                f"Date UTC : {day}\nGraine utilisée : {seed} (essai {attempt})\n"
                f"Corpus source : generate_rss.py (lecture seule)\n"
                f"Corpus détecté : 125 phrases attendues\n"
                f"Prises de parole : {len(active)}\n"
                f"Apparitions par voix : {dict(counts)}\n"
                f"Silences : {[t['turn'] for t in turns if t['type'] == 'silence']}\n"
                f"Prototype source inchangé : oui\n",
                encoding="utf-8",
            )
            print(f"Séquence V4.10 forte publiée pour {day}; graine {seed}; essai {attempt}.")
            print(f"80 tours; 160 prises de parole; répartition {dict(counts)}.")
            return

    raise RuntimeError("Aucune séquence équilibrée après 100 essais. Dernière erreur : " + last_error)


if __name__ == "__main__":
    main()
