#!/usr/bin/env python3
# Cercle Specular — prototype V4.10 : collisions locales
# Lecture seule de generate_rss.py ; aucun fichier source ou feed n'est modifié.

import ast
import csv
import random
import re
from collections import Counter, deque
from pathlib import Path

SEED = 20261025
N_TURNS = 80
OUTDIR = Path("prototype_v4_10_results")
VOICES = ["BLAKE", "LEI", "SOREL", "ANAYA"]

# Fonctions de composition attribuées manuellement aux phrases pivots et aux
# familles de phrases. Les règles lexicales complètent ces annotations.
MANUAL_OPS = {
    "BLAKE": {
        "decrire": set(range(1, 8)) | set(range(9, 27)) | {28, 29},
        "rompre": {8, 27},
        "suspendre": {30},
    },
    "LEI": {
        "deplacer": set(range(1, 3)) | set(range(4, 31)),
        "contester": {3, 22},
        "suspendre": {31},
        "rompre": {32},
    },
    "SOREL": {
        "contester": {1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 17, 18, 19, 20, 22, 24, 25, 27, 29, 30},
        "decrire": {7, 11, 13, 15, 21, 26},
        "rompre": {14, 23, 28, 31},
    },
    "ANAYA": {
        "transformer": set(range(1, 31)),
        "suspendre": {7, 25, 31, 32},
        "rompre": {32},
    },
}

# Concepts détectés dans le texte. Plusieurs concepts peuvent coexister.
CONCEPT_PATTERNS = {
    "regard": ["regard", "regarder", "vision", "perçois", "perception", "voir", "vois"],
    "dispositif": ["dispositif", "système", "structure", "cadre", "organisation", "fonctionne"],
    "position": ["position", "point de vue", "point de départ", "place que", "point déjà"],
    "absence_presence": ["absence", "présence", "corps", "visible", "visibilité", "effacement"],
    "image_representation": ["image", "représentation", "reflet", "miroir", "surface", "transparence", "flou", "netteté"],
    "sujet_observateur": ["sujet", "observateur", "celui qui regarde", "tu es", "tu arrives", "tu regardes"],
    "distance": ["distance", "dehors", "extérieur", "extériorité", "proximité", "séparation"],
    "retour_coincidence": ["retour", "revient", "revenir", "coïncidence", "correspondance", "circularité"],
    "transformation": ["transforme", "transformation", "autrement", "déplacé", "déplacement", "devient", "passage", "traverse", "mouvement"],
    "rupture_totalite": ["oublié la question", "attends", "perdu le fil", "recharger la page", "monde comme totalité", "presque", "déjà fini"],
}

TRANSITIONS = {
    "decrire": {"contester": 3.1, "deplacer": 2.6, "transformer": 2.1, "suspendre": 1.4, "rompre": 1.2, "decrire": 0.7},
    "deplacer": {"decrire": 2.1, "contester": 1.9, "transformer": 2.9, "suspendre": 1.5, "rompre": 1.4, "deplacer": 0.7},
    "contester": {"decrire": 1.8, "deplacer": 2.1, "transformer": 2.5, "suspendre": 1.9, "rompre": 1.8, "contester": 0.65},
    "transformer": {"decrire": 1.3, "deplacer": 1.9, "contester": 1.8, "suspendre": 1.9, "rompre": 1.4, "transformer": 0.65},
    "suspendre": {"decrire": 0.9, "deplacer": 1.4, "contester": 1.1, "transformer": 1.7, "rompre": 1.2, "suspendre": 0.55},
    "rompre": {"decrire": 0.7, "deplacer": 1.0, "contester": 1.0, "transformer": 1.4, "suspendre": 1.8, "rompre": 0.5},
}

# Uniquement des pivots : ils augmentent la probabilité d'une suspension,
# sans imposer systématiquement un silence.
PIVOTS = {
    ("BLAKE", 27),   # le système semble avoir oublié la question
    ("BLAKE", 30),   # tout est en place, sauf l'essentiel
    ("LEI", 32),     # attends... non
    ("SOREL", 14),   # recommencer / recharger la page
    ("SOREL", 23),   # nous avons perdu le fil
    ("SOREL", 28),   # la critique ne trouve plus de point d'appui
    ("SOREL", 31),   # il n'y a pas de monde comme totalité
    ("ANAYA", 31),   # nous y étions presque
    ("ANAYA", 32),   # peut-être que c'était déjà fini
}

# V4.6 : registres lexicaux très grossiers, utilisés uniquement pour proposer
# des collisions. Ils ne décrivent pas le sens profond des phrases.
REGISTER_PATTERNS = {
    "technique": ["système", "dispositif", "fonctionne", "recharger", "page", "paramètres", "génère", "validation"],
    "philosophique": ["totalité", "sujet", "origine", "condition", "présence", "absence", "coïncidence", "extériorité", "distinction"],
    "spatial": ["distance", "dehors", "point", "place", "cadre", "surface", "passage", "ailleurs", "position"],
    "affectif": ["manques", "perds", "accueille", "t’habites", "te traverse", "tu es là", "presque", "fini"],
    "perceptif": ["regard", "voir", "vois", "image", "reflet", "miroir", "visible", "flou", "netteté"],
    "rupture": ["attends", "non", "oublié", "perdu le fil", "recommencer", "presque", "déjà fini"],
}

def registers(phrase):
    p = norm(phrase)
    found = [name for name, terms in REGISTER_PATTERNS.items()
             if any(norm(term) in p for term in terms)]
    return found or ["indéterminé"]

def norm(text):
    return re.sub(r"\s+", " ", text.lower().replace("’", "'")).strip()

def load_corpus():
    tree = ast.parse(Path("generate_rss.py").read_text(encoding="utf-8"))
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.lower() in {
                    "blake", "lei", "sorel", "anaya"
                }:
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        continue
                    if isinstance(value, list) and all(isinstance(x, str) for x in value):
                        result[target.id.upper()] = value
    if set(result) != set(VOICES):
        raise RuntimeError(
            "Impossible d'identifier les quatre listes dans generate_rss.py. "
            "Le fichier source n'a pas été modifié."
        )
    return result

def operations(voice, index, phrase):
    found = [op for op, numbers in MANUAL_OPS[voice].items() if index in numbers]
    if found:
        return found
    # Complément lexical pour les phrases non explicitement annotées.
    p = norm(phrase)
    if any(x in p for x in ["ne peut pas", "impossible", "annule", "exclusion", "n'est pas", "suppose"]):
        return ["contester"]
    return [{"BLAKE": "decrire", "LEI": "deplacer", "SOREL": "contester", "ANAYA": "transformer"}[voice]]

def concepts(phrase):
    p = norm(phrase)
    tags = [tag for tag, patterns in CONCEPT_PATTERNS.items()
            if any(norm(pattern) in p for pattern in patterns)]
    return tags or ["indetermine"]

def make_items(corpus):
    items = []
    for voice in VOICES:
        for index, phrase in enumerate(corpus[voice], 1):
            items.append({
                "voice": voice, "index": index, "phrase": phrase,
                "ops": operations(voice, index, phrase),
                "concepts": concepts(phrase),
                "key": (voice, index),
            })
    return items

def weighted_choice(options, weights, rng):
    if not options:
        raise RuntimeError("Aucun candidat disponible.")
    return rng.choices(options, weights=[max(0.001, w) for w in weights], k=1)[0]

def choose_silence_positions(rng):
    """Tire huit positions réparties dans toute la séquence.

    La répartition est souple : chaque quart de séquence reçoit entre un et
    trois silences, avec huit au total et au moins cinq tours entre eux.
    Les positions sont aléatoires, pas fixées à des tours prédéterminés.
    """
    blocks = [(1, 20), (21, 40), (41, 60), (61, 80)]
    for _ in range(10000):
        counts = [2, 2, 2, 2]
        # Petites redistributions aléatoires : chaque bloc garde 1 à 3 silences.
        for _move in range(rng.randint(0, 4)):
            donors = [i for i, c in enumerate(counts) if c > 1]
            receivers = [i for i, c in enumerate(counts) if c < 3]
            if donors and receivers:
                d = rng.choice(donors)
                r = rng.choice([x for x in receivers if x != d] or receivers)
                if d != r:
                    counts[d] -= 1
                    counts[r] += 1
        positions = []
        valid = True
        for (lo, hi), count in zip(blocks, counts):
            candidates = list(range(lo, hi + 1))
            rng.shuffle(candidates)
            chosen = []
            for pos in candidates:
                if all(abs(pos - other) >= 5 for other in positions + chosen):
                    chosen.append(pos)
                    if len(chosen) == count:
                        break
            if len(chosen) != count:
                valid = False
                break
            positions.extend(chosen)
        if valid and len(positions) == 8 and all(
            b - a >= 5 for a, b in zip(sorted(positions), sorted(positions)[1:])
        ):
            return set(positions)
    raise RuntimeError("Impossible de répartir les huit silences.")

def choose_participants(size, remaining, future_active_turns, previous_op, rng):
    mandatory = [v for v in VOICES if remaining[v] > future_active_turns]
    if len(mandatory) > size:
        raise RuntimeError("L'équilibre des voix est devenu impossible.")
    chosen = mandatory[:]
    pool = [v for v in VOICES if v not in chosen and remaining[v] > 0]
    while len(chosen) < size:
        weights = []
        for voice in pool:
            weight = remaining[voice] ** 1.2
            if previous_op:
                # Favorise une voix susceptible de déplacer l'opération précédente,
                # sans imposer une alternance fixe.
                best = max(TRANSITIONS.get(previous_op, {}).values())
                weight *= 0.8 + 0.4 * best
            weight *= rng.uniform(0.8, 1.2)
            weights.append(weight)
        chosen_voice = weighted_choice(pool, weights, rng)
        chosen.append(chosen_voice)
        pool.remove(chosen_voice)
    return chosen

def concept_overlap(a, b):
    aa, bb = set(a), set(b)
    return len(aa & bb) / max(1, len(aa | bb))

def relation_function(item, previous):
    """Heuristique locale : estime la fonction de la phrase face à la précédente.
    Ce n'est pas une analyse sémantique ; les étiquettes servent à auditer la séquence.
    """
    if previous is None:
        return "ouverture"
    overlap = concept_overlap(item["concepts"], previous["concepts"])
    ops = set(item["ops"])
    prev_ops = set(previous["ops"])
    if "rompre" in ops or "suspendre" in ops:
        return "interruption"
    if overlap >= 0.5 and ({"contester", "rompre"} & ops):
        return "contestation"
    if overlap >= 0.34 and ({"deplacer", "transformer"} & ops):
        return "déplacement"
    if overlap >= 0.5:
        return "écho"
    if ops & {"rompre", "contester"} and prev_ops & {"decrire", "transformer"}:
        return "contrepoint"
    if overlap < 0.2:
        return "bifurcation"
    return "prolongement"


def phrase_score(item, recent_items, recent_texts, previous_voice, previous_op,
                 used_keys, phrase_use_counts, recent_concepts, turn_no, mode="moyenne",
                 turn_items=None, rupture_charge=0, rupture_memory=None):
    if item["key"] in used_keys:
        return 0.0
    weight = 1.0
    p = norm(item["phrase"])
    if p in recent_texts:
        weight *= 0.005

    # Mémoire globale des phrases : ne pas laisser quelques formules dominer.
    # Les répétitions restent possibles quand le corpus d'une voix a été parcouru.
    uses = phrase_use_counts.get(item["key"], 0)
    if uses == 1:
        weight *= 0.22
    elif uses >= 2:
        weight *= 0.07

    if previous_voice == item["voice"]:
        # Même voix permise, mais une répétition immédiate n'est pas favorisée.
        weight *= 0.62

    if previous_op:
        best = max(TRANSITIONS.get(previous_op, {}).get(op, 1.0) for op in item["ops"])
        weight *= best

    # Mémoire conceptuelle plus large : les 8 dernières interventions et un
    # compteur des motifs dominants dans la séquence entière.
    for previous in recent_items[-8:]:
        overlap = concept_overlap(item["concepts"], previous["concepts"])
        same_voice = item["voice"] == previous["voice"]
        if overlap >= 0.5:
            if "contester" in item["ops"] or "rompre" in item["ops"]:
                weight *= 1.22  # reprise polémique possible
            elif "transformer" in item["ops"] or "deplacer" in item["ops"]:
                weight *= 0.78  # déplacement d'un motif déjà présent
            else:
                weight *= 0.34  # répétition explicative à éviter
        elif overlap >= 0.34:
            weight *= 0.64
        if same_voice and overlap >= 0.34:
            weight *= 0.65

    # Pénalise les champs conceptuels déjà surreprésentés dans la séquence.
    for concept in item["concepts"]:
        count = recent_concepts.get(concept, 0)
        if count >= 10:
            weight *= 0.72
        elif count >= 7:
            weight *= 0.86

    # Évite une phrase lexicalement trop proche d'une des dernières, sans l'interdire.
    words = set(re.findall(r"[a-zà-ÿ']+", p))
    stop = {"le", "la", "les", "un", "une", "des", "de", "du", "et", "ou", "que",
            "qui", "ce", "ça", "tu", "te", "t", "en", "dans", "est", "ne", "pas",
            "sans", "ici", "comme", "ceci", "mais", "plus", "pour", "par"}
    words -= stop
    for prev in recent_items[-4:]:
        prev_words = set(re.findall(r"[a-zà-ÿ']+", norm(prev["phrase"]))) - stop
        jaccard = len(words & prev_words) / max(1, len(words | prev_words))
        if jaccard > 0.28:
            weight *= 0.72

    # V4.5 : un tour n'est pas une simple juxtaposition. Les phrases déjà
    # prononcées dans le tour courant sont les deux dernières entrées de
    # recent_items quand elles existent. On favorise une relation distincte
    # (déplacement, contestation, bifurcation) et on pénalise l'écho explicatif.
    if recent_items:
        previous = recent_items[-1]
        overlap = concept_overlap(item["concepts"], previous["concepts"])
        ops = set(item["ops"])
        if overlap >= 0.5 and not ({"contester", "rompre"} & ops):
            weight *= 0.55
        elif overlap >= 0.34 and ({"deplacer", "transformer"} & ops):
            weight *= 1.18
        elif overlap < 0.2:
            weight *= 1.12
        if item["voice"] != previous["voice"] and (
            ("contester" in ops and "decrire" in previous["ops"])
            or ("rompre" in ops)
        ):
            weight *= 1.20

    # V4.10 : collision explicite entre deux prises de parole du même tour.
    # On ne cherche pas seulement une phrase éloignée du contexte global :
    # on favorise une rencontre locale entre des registres et des champs différents.
    # Les niveaux règlent la force de cette préférence, sans garantir un effet sémantique.
    if turn_items:
        previous_in_turn = turn_items[-1]
        pair_overlap = concept_overlap(item["concepts"], previous_in_turn["concepts"])
        candidate_regs = set(registers(item["phrase"]))
        previous_regs = set(registers(previous_in_turn["phrase"]))
        register_collision = bool(candidate_regs and previous_regs and not (candidate_regs & previous_regs))
        collision_strength = {"faible": 2.0, "moyenne": 5.0, "forte": 10.0}.get(mode, 5.0)

        # Collision nette : peu de concepts communs ET registres distincts.
        if pair_overlap < 0.20 and register_collision:
            weight *= collision_strength
        # Déplacement partiel : un peu de terrain commun, mais changement de registre.
        elif pair_overlap < 0.35 and register_collision:
            weight *= 1.5 + collision_strength * 0.35
        # Évite que la seconde voix ne reformule simplement la première.
        elif pair_overlap >= 0.50 and not register_collision:
            weight *= {"faible": 0.65, "moyenne": 0.35, "forte": 0.18}.get(mode, 0.35)
        elif pair_overlap >= 0.35 and not register_collision:
            weight *= {"faible": 0.88, "moyenne": 0.65, "forte": 0.42}.get(mode, 0.65)

        # Une collision n'est pas un pur tirage au hasard : garder un petit
        # résidu conceptuel peut permettre qu'un événement se forme entre les phrases.
        if 0.10 <= pair_overlap <= 0.30:
            weight *= 1.25

    return max(weight, 0.001)

def choose_phrase(items, voice, rng, recent_items, recent_texts,
                  previous_voice, previous_op, used_keys, phrase_use_counts,
                  recent_concepts, turn_no, mode="moyenne", turn_items=None, rupture_charge=0, rupture_memory=None):
    candidates = [item for item in items if item["voice"] == voice and item["key"] not in used_keys]
    weights = [
        phrase_score(item, recent_items, recent_texts, previous_voice, previous_op,
                     used_keys, phrase_use_counts, recent_concepts, turn_no, mode, turn_items, rupture_charge, rupture_memory)
        for item in candidates
    ]
    return weighted_choice(candidates, weights, rng)

def main(mode="moyenne", outdir=None):
    rng = random.Random(SEED)
    outdir = Path(outdir) if outdir else OUTDIR
    corpus = load_corpus()
    items = make_items(corpus)
    outdir.mkdir(exist_ok=True, parents=True)

    # 80 tours : 8 silences, 10 solos, 40 duos, 18 trios, 4 tours à quatre voix.
    # Cela donne 160 prises de parole et exactement 40 apparitions par voix.
    shape_counts = Counter({
        "silence": 8, "solo": 10, "duo": 40, "trio": 18, "quatre_voix": 4
    })
    silence_positions = choose_silence_positions(rng)
    remaining_shapes = shape_counts.copy()
    remaining_voice_uses = {voice: 40 for voice in VOICES}
    active_turns_left = 72

    recent_items = deque(maxlen=12)
    recent_texts = deque(maxlen=32)
    phrase_use_counts = Counter()
    recent_concepts = Counter()
    rows = []
    previous_voice = None
    previous_op = None
    previous_was_pivot = False
    previous_shape = None
    silence_turns = []
    turns_since_silence = 10
    collision_events = []
    collision_pairs = 0
    rupture_charge = 0  # argument conservé pour compatibilité avec la signature du prototype
    rupture_memory = None

    for turn_no in range(1, N_TURNS + 1):
        if turn_no in silence_positions:
            shape = "silence"
        else:
            available = [name for name, count in remaining_shapes.items()
                         if count > 0 and name != "silence"]
            shape = weighted_choice(
                available,
                [remaining_shapes[name] * (1.25 if name == "duo" else 1.0)
                 for name in available],
                rng,
            )
        remaining_shapes[shape] -= 1

        if shape == "silence":
            rows.append({
                "tour": turn_no, "type": shape, "voix": "",
                "numero_phrase": "", "operation": "silence",
                "concepts": "", "relation": "silence", "phrase": "[silence]",
            })
            previous_op = "suspendre"
            previous_was_pivot = False
            silence_turns.append(turn_no)
            turns_since_silence = 0
            previous_shape = "silence"
            continue

        active_turns_left -= 1
        size = {"solo": 1, "duo": 2, "trio": 3, "quatre_voix": 4}[shape]
        participants = choose_participants(
            size, remaining_voice_uses, active_turns_left, previous_op, rng
        )

        # Réordonne les voix présentes : la première intervention est choisie
        # selon le contexte précédent ; les autres restent libres de se déplacer.
        if previous_op and len(participants) > 1:
            lead_weights = []
            for voice in participants:
                w = 1.0
                if previous_voice == voice:
                    w *= 0.6
                lead_weights.append(w * rng.uniform(0.8, 1.2))
            lead = weighted_choice(participants, lead_weights, rng)
            participants.remove(lead)
            participants.insert(0, lead)

        used_keys = set()
        turn_items = []
        for voice in participants:
            item = choose_phrase(
                items, voice, rng, list(recent_items), list(recent_texts),
                previous_voice, previous_op, used_keys, phrase_use_counts,
                recent_concepts, turn_no, mode, turn_items, rupture_charge, rupture_memory
            )
            prior_item = recent_items[-1] if recent_items else None
            relation = relation_function(item, prior_item)
            used_keys.add(item["key"])
            remaining_voice_uses[voice] -= 1
            recent_items.append(item)
            recent_texts.append(norm(item["phrase"]))
            phrase_use_counts[item["key"]] += 1
            for concept in item["concepts"]:
                recent_concepts[concept] += 1
            turn_items.append(item)

            rows.append({
                "tour": turn_no, "type": shape, "voix": voice,
                "numero_phrase": item["index"],
                "operation": "+".join(item["ops"]),
                "concepts": "; ".join(item["concepts"]),
                "registres": "; ".join(registers(item["phrase"])),
                "perturbation": "",
                "relation": relation,
                "phrase": item["phrase"],
            })
            previous_voice = voice
            previous_op = item["ops"][0]
            previous_was_pivot = (voice, item["index"]) in PIVOTS

            # V4.10 : mesure une collision effective avec la prise précédente du même tour.
            if len(turn_items) >= 2:
                left = turn_items[-2]
                right = turn_items[-1]
                overlap_pair = concept_overlap(left["concepts"], right["concepts"])
                regs_left = set(registers(left["phrase"]))
                regs_right = set(registers(right["phrase"]))
                reg_collision = bool(regs_left and regs_right and not (regs_left & regs_right))
                if overlap_pair < 0.20 and reg_collision:
                    collision_pairs += 1
                    collision_events.append({
                        "tour": turn_no,
                        "voix_a": left["voice"], "phrase_a": left["phrase"],
                        "voix_b": right["voice"], "phrase_b": right["phrase"],
                        "recouvrement": round(overlap_pair, 3),
                        "registres_a": ", ".join(sorted(regs_left)),
                        "registres_b": ", ".join(sorted(regs_right)),
                    })

        previous_shape = shape
        turns_since_silence += 1

    if any(remaining_voice_uses[v] != 0 for v in VOICES):
        raise RuntimeError(f"Équilibre des voix incorrect : {remaining_voice_uses}")
    if len([r for r in rows if r["type"] != "silence"]) != 160:
        raise RuntimeError("Le nombre de prises de parole actives n'est pas 160.")

    grouped = {}
    for row in rows:
        grouped.setdefault(row["tour"], []).append(row)
    active = [r for r in rows if r["type"] != "silence"]
    voice_counts = Counter(r["voix"] for r in active)
    exact_repeat_count = sum(
        1 for i, row in enumerate(active)
        if norm(row["phrase"]) in {norm(prev["phrase"]) for prev in active[max(0, i-24):i]}
    )
    same_turn_duplicates = []
    for n, group in grouped.items():
        voices = [r["voix"] for r in group if r["voix"]]
        if len(voices) != len(set(voices)):
            same_turn_duplicates.append(n)

    fields = ["tour", "type", "voix", "numero_phrase", "operation", "concepts", "registres", "perturbation", "relation", "phrase"]
    with (outdir / "sequence_80_tours.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with (outdir / "inventaire_annote.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["voix", "numero_phrase", "operations", "concepts", "registres", "relation", "phrase"])
        writer.writeheader()
        for item in items:
            writer.writerow({
                "voix": item["voice"], "numero_phrase": item["index"],
                "operations": "; ".join(item["ops"]),
                "concepts": "; ".join(item["concepts"]),
                "registres": "; ".join(registers(item["phrase"])),
                "relation": "à évaluer en contexte",
                "phrase": item["phrase"],
            })

    with (outdir / f"rapport_v4_10_{mode}.txt").open("w", encoding="utf-8") as f:
        f.write("CERCLE SPECULAR — PROTOTYPE V4.10\n")
        f.write(f"Mode : {mode}\n")
        f.write("Principe : sélection locale de collisions entre phrases d’un même tour, selon le recouvrement conceptuel et les registres lexicaux détectés.\n")
        f.write("Les étiquettes de registre sont heuristiques ; une collision lexicale ne garantit pas un événement de sens.\n")
        f.write(f"Graine aléatoire : {SEED}\n")
        f.write("Source : generate_rss.py (lecture seule)\n")
        f.write("Corpus source et feed.xml non modifiés.\n\n")
        f.write("RÉPARTITION DES 80 TOURS\n")
        for shape in ["silence", "solo", "duo", "trio", "quatre_voix"]:
            f.write(f"  {shape}: {shape_counts[shape]}\n")
        f.write(f"\nPositions des silences : {sorted(silence_positions)}\n")
        f.write(f"Prises de parole actives : {len(active)}\n")
        f.write(f"Répétitions exactes dans les 24 dernières phrases actives : {exact_repeat_count}\n")
        f.write(f"Apparitions par voix : {dict(voice_counts)}\n")
        f.write(f"Voix répétées dans un même tour : {same_turn_duplicates or 'aucune'}\n")
        relation_counts = Counter(r["relation"] for r in active)
        f.write(f"Étiquettes relationnelles heuristiques : {dict(relation_counts)}\n")
        f.write(f"Collisions locales détectées : {collision_pairs}\n")
        f.write("Paires détectées (faible recouvrement conceptuel + registres distincts) :\n")
        for event in collision_events:
            f.write(f"  tour {event['tour']:02d} — {event['voix_a']} : {event['phrase_a']}\n")
            f.write(f"                 → {event['voix_b']} : {event['phrase_b']}\n")
            f.write(f"    recouvrement={event['recouvrement']} ; registres={event['registres_a']} / {event['registres_b']}\n")
        f.write("\nSÉQUENCE\n")
        for n in range(1, N_TURNS + 1):
            f.write(f"\nTOUR {n:02d} [{grouped[n][0]['type']}]\n")
            for r in grouped[n]:
                relation = f" <{r['relation']}>" if r['voix'] else ""
                f.write(f"  {r['voix'] or '—'}{relation}: {r['phrase']}\n")

    print(f"Prototype V4.10 ({mode}) terminé. Corpus source inchangé.")
    print(f"Phrases du corpus : {len(items)}")
    print(f"Positions des silences : {sorted(silence_positions)}")
    print(f"Prises de parole : {len(active)}")
    print(f"Apparitions par voix : {dict(voice_counts)}")
    print(f"Voix répétées dans un même tour : {same_turn_duplicates or 'aucune'}")
    print(f"Résultats : {outdir.resolve()}")
    print(f"Collisions locales détectées : {collision_pairs}")
    print(f"Fichiers : sequence_80_tours.csv, rapport_v4_10_{mode}.txt, inventaire_annote.csv")
    print("La sélection favorise les collisions locales ; le corpus source reste inchangé.")

if __name__ == "__main__":
    corpus_check = load_corpus()
    print(f"Corpus détecté : {sum(len(v) for v in corpus_check.values())} phrases.")
    for mode, folder in [
        ("faible", "A_collision_faible"),
        ("moyenne", "B_collision_moyenne"),
        ("forte", "C_collision_forte"),
    ]:
        main(mode, Path("prototype_v4_10_results") / folder)
