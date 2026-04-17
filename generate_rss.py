import random

# --- BLAKE : système / compact / computationnel ---

blake = [
"le dispositif organise une séparation fonctionnelle entre perception et identification",
"l’image dépend d’un point de vue non intégrable",
"le système fonctionne sans retour exploitable sur l’observateur",
"le dispositif introduit une dissymétrie stable entre vision et présence",
"les paramètres perceptifs deviennent variables dans le système",
"le dispositif maintient une distance irréductible entre sujet et image",
"le système empêche toute correspondance directe entre regard et image",
"le dispositif maintient une tension entre présence et absence",
"le système rend l’identification instable sans la supprimer",
"le dispositif impose une extériorité constante au sujet percevant",
"la structure empêche toute coïncidence entre regard et représentation",
"la perception relève d’une dissociation irréductible",
"le dispositif configure une expérience sans apparition du sujet",
"le dispositif maintient une séparation entre perception et perceptible",
"la perception est contrainte par une organisation préalable",
"le cadre impose une organisation antérieure à l’expérience",
"le système produit une visibilité qui ne coïncide pas avec sa réflexivité",
"le dispositif organise une dissociation entre vision et identification",
"le dispositif calcule une dissymétrie entre vision et présence",
"le cadre impose une contrainte verticale à la perception",
"le système distribue l’image sans inclure le sujet",
"le dispositif maintient une continuité indépendante de l’action",
"le champ visible est limité par une architecture non accessible",
"le système impose une séquence sans retour vers l’origine",
"la perception est indexée sur un flux non interruptible",
"le dispositif encode une distance constante au visible",
"le système introduit une latence entre image et perception",
"le regard est une variable différée du processus",
"l’image est calculée avant perception",
"la perception est différée de son déclenchement",
"la perception est une sortie du système",
"le dispositif empêche toute synchronisation entre regard et image",
"le système exécute une séquence sans retour vers l’observateur",
"le regard intervient après exécution",
"le dispositif organise une expérience sans point d’ancrage",
"la perception n’intervient pas dans la production du visible",
"le regard n’est pas requis dans l’exécution",
"le système maintient une image indépendante de la perception",
"l’image se produit comme processus autonome",
"l’image persiste sans instance de regard",

# 👉 AJOUT
"le cadre vertical contraint la perception dans un format opératoire"
]

# --- LEI : fragmenté / instable / vécu ---

lei = [
"tu arrives… mais la place n’est déjà plus là",
"tu vois… mais ça s’est décidé avant",
"le retour a lieu… mais pas vers toi",
"tu regardes… depuis ailleurs déjà",
"le système t’a précédé",
"tu vois… mais ça glisse",
"tu ne peux pas rester dans ce que tu vois",
"tu es déjà pris… avant même de regarder",
"ça apparaît… sans toi",
"tu ne peux pas revenir",
"tu te reconnais… sans t’attraper",
"tu es là… et ailleurs",
"ça ne s’arrête pas vraiment",
"tu regardes… et ça a déjà bougé",
"ça continue… sans toi",
"tu vois un peu… le reste s’échappe",
"tu arrives… mais c’est déjà en train de passer",
"tu ne tiens rien",
"ça défile… sans attendre",
"tu touches… presque",
"tu es là… mais pas au bon moment",
"ça commence sans toi",
"tu suis… mais rien ne t’attend",
"tu regardes… trop tard",
"tu arrives après",
"tu remarques… mais c’est déjà passé",
"tu vois… mais c’est fini",
"tu suis… en retard",
"tu regardes… et ça disparaît",
"tu arrives trop tard",
"tu vois quelque chose… déjà perdu",
"ça bouge avant toi",
"tu arrives… et c’est fini",
"ça passe… sans toi",
"tu es dedans… sans regarder",
"tu regardes… mais ça ne dépend pas de toi",
"ça apparaît… puis autre chose",
"tu passes… rien ne tient",
"tu regardes en avançant… et ça se déplace avec toi",

# 👉 AJOUT
"tu regardes… mais ça n’existe nulle part où tu pourrais le toucher"
]

# --- SOREL : dense / théorique / structuré ---

sorel = [
"la présence visible suppose la suppression de ce qui devrait la garantir",
"le flou constitue la condition même de l’apparition",
"la circularité du regard est structurellement impossible",
"le sujet est rendu inopérant par le dispositif",
"la présence est produite au prix de son effacement",
"la stabilité masque une transformation des conditions",
"aucun point extérieur au dispositif n’est pensable",
"la visibilité repose sur l’exclusion constitutive du sujet",
"la transparence est structurellement impossible",
"la structure précède toute immédiateté supposée",
"la représentation implique l’effacement du regardant",
"la présence se constitue comme manque",
"la validation est impossible dans ce dispositif",
"l’expérience dépend d’une extériorité irréductible",
"l’identification demeure structurellement incomplète",
"la réflexivité est rendue impossible",
"l’origine est neutralisée",
"la condition d’apparition exclut la possibilité de se voir",
"la coïncidence est annulée",
"la tension constitue la condition même du visible",
"l’appropriation est neutralisée",
"la forme excède ce qu’elle donne à voir",
"la condition de vision implique une perte préalable",
"le champ perceptif est conditionné par sa restriction",
"la continuité repose sur une discontinuité masquée",
"l’image produit ce qu’elle prétend révéler",
"la perception se constitue dans ce qui lui échappe",
"le regard n’accède qu’à ce qui a déjà eu lieu",
"voir implique d’arriver trop tard",
"ce qui est vu appartient déjà au passé",
"la perception suppose une antériorité irréductible",
"la perception est structurée comme retard",
"la présence se constitue dans son retrait",
"l’image n’inclut pas celui qui la perçoit",
"la perception dépend d’une perte de présence",
"aucune instance de regard n’est nécessaire",
"le regard fonctionne comme fiction",
"l’apparition ne s’adresse à personne",
"il n’y a pas de monde comme totalité",
"le réel se donne comme dispersion",

# 👉 AJOUT
"la perception est orientée par un cadre qui détermine à la fois son format et sa limite"
]

# --- ANAYA : fluide / respirant / relationnel ---

anaya = [
"ce qui apparaît t’inclut... sans jamais te contenir",
"tu es là... mais déjà pris dans ce qui t’échappe",
"la surface ne fixe rien... elle laisse passer",
"tu fais déjà partie de ce qui te dépasse",
"ce que tu perds t’ouvre autrement",
"tu participes à ce qui te traverse",
"ce qui semble proche est déjà ailleurs",
"tu passes... sans pouvoir retenir",
"tu habites cette distance",
"tu es présent autrement",
"ce dehors t’habite déjà",
"tout commence sans commencer",
"tu es en mouvement dans ce qui te définit",
"tu es séparé sans être isolé",
"les deux coexistent sans se résoudre",
"tu avances dans ce qui ne revient pas",
"tout continue sans fin stable",
"la surface relie sans jamais fixer",
"tu es déjà là autrement",
"tu es porté sans te fixer",
"ce qui apparaît t’inclut sans se refermer",
"tu avances doucement dans ce qui te dépasse",
"la surface t’accueille sans te retenir",
"tu es déjà dedans sans entrer",
"ce qui glisse t’emporte doucement",
"tu habites le passage sans l’arrêter",
"tout te relie sans te fixer",
"tu es pris dans un flux ouvert",
"tu rejoins ce qui t’a précédé",
"tu arrives dans un mouvement déjà là",
"ce qui apparaît se transforme encore",
"tu es accueilli sans avoir commencé",
"ce qui te précède te porte encore",
"tu avances sans bord",
"tu es là dans ce qui ne t’attend pas",
"tu es dans ce qui apparaît sans distance",
"tu fais partie de ce qui se voit",
"tu es dans ce qui se montre sans destinataire",
"tu es porté par ce qui ne se rassemble pas",

# 👉 AJOUT
"tu regardes en avançant… et ça se déplace avec toi"
]

# --- MÉLANGE PAR BLOCS ---

random.shuffle(blake)
random.shuffle(lei)
random.shuffle(sorel)
random.shuffle(anaya)

n = min(len(blake), len(lei), len(sorel), len(anaya))

items = []

for i in range(n):
    block = [
        (">_ BLAKE :", blake[i]),
        (">_ LEI :", lei[i]),
        (">_ SOREL :", sorel[i]),
        (">_ ANAYA :", anaya[i])
    ]
    random.shuffle(block)
    items.extend(block)

# --- RSS ---

rss_items = ""
for author, text in items:
    rss_items += f'<item><title>{author}</title><description>{text}</description></item>\n'

rss = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>cercle specular — inter_view</title>
<description>flux evolutif</description>
<link>https://example.com</link>

{rss_items}

</channel>
</rss>
'''

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)
