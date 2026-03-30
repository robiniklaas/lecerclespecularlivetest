import random

# --- TEXTES PAR VOIX ---

blake = [
"le dispositif organise une séparation fonctionnelle entre perception et identification",
"l’image dépend d’un point de vue qui ne peut pas s’y intégrer",
"le fond diffus empêche toute stabilisation réflexive de l’image",
"le système fonctionne sans produire de retour exploitable sur l’observateur",
"l’absence du corps empêche toute validation du point de vue",
"le dispositif introduit une dissymétrie entre vision et présence",
"les paramètres perceptifs cessent d’être constants dans ce système",
"la séparation initiale ne permet plus de décrire l’expérience",
"le système génère une image indépendante de toute validation subjective",
"le dispositif maintient une distance irréductible entre sujet et image",
"l’image ne permet aucune appropriation du point de vue",
"le dispositif stabilise une absence comme condition de visibilité",
"le système empêche toute correspondance directe entre regard et image",
"le dispositif maintient une tension constante entre présence et absence",
"l’image persiste sans se référer à une origine subjective",
"le système rend toute identification instable sans la supprimer",
"le dispositif impose une extériorité constante au sujet percevant",
"l’image se maintient sans jamais intégrer celui qui la perçoit",
"la structure empêche toute coïncidence entre regard et représentation",
"la perception est structurée par une dissociation irréductible"
]

blake_plus = [
"le dispositif calcule une dissymétrie stable entre vision et présence",
"le cadre impose une contrainte verticale sur la perception",
"le système distribue l’image sans inclure le sujet dans son calcul",
"la visibilité est produite comme sortie d’un processus non accessible",
"le dispositif maintient une continuité indépendante de ton action",
"le champ visible est limité par une architecture que tu ne contrôles pas"
]

blake_delay = [
"le système introduit une latence constante entre image et perception",
"le regard est traité comme une variable en retard dans le processus",
"l’image est calculée avant d’être effectivement perçue",
"le dispositif produit une antériorité systématique de l’image",
"la perception est toujours en retard sur son propre déclenchement",
"le système maintient un décalage temporel irréductible"
]

lei = [
"tu arrives... quand la position n’est déjà plus disponible",
"ce que tu vois se décide... avant ton regard",
"la netteté serait un contresens ici...",
"le retour a lieu... mais pas dans ta direction",
"tu regardes depuis un point déjà déplacé",
"le système te précède désormais",
"tu vois... mais depuis un décalage irréductible",
"tu ne peux pas t’installer dans ce que tu vois",
"tu es déjà engagé... avant même de regarder",
"ce que tu vois s’établit... sans toi"
]

lei_plus = [
"tu regardes... mais ça a déjà glissé ailleurs",
"ça continue... même si tu t’arrêtes",
"tu vois une partie... le reste t’échappe déjà",
"tu arrives... mais c’est déjà en train de passer",
"tu ne tiens jamais ce que tu regardes",
"ça défile... sans attendre que tu comprennes"
]

lei_delay = [
"tu regardes... mais c’est déjà passé",
"tu arrives toujours après ce que tu vois",
"ça a déjà eu lieu quand tu le remarques",
"tu vois... mais c’est trop tard",
"tu touches presque... mais c’est déjà ailleurs",
"tu suis... mais tu es en retard"
]

sorel = [
"tu continues à parler de miroir, alors que rien ici ne remplit les conditions du reflet",
"la présence visible suppose la suppression de ce qui devrait la garantir",
"le flou n’est pas un défaut, c’est la condition même de ce qui apparaît",
"la circularité du regard est ici rendue structurellement impossible",
"le sujet n’est pas absent, il est rendu inopérant par le dispositif",
"la présence est produite au prix de son propre effacement"
]

sorel_plus = [
"la visibilité dépend ici d’une réduction préalable du réel",
"le sujet ne disparaît pas, il est conditionné comme impossibilité",
"la continuité perçue repose sur une discontinuité masquée",
"l’image produit ce qu’elle prétend seulement révéler",
"la limitation du cadre devient la condition de toute apparition"
]

sorel_delay = [
"le regard n’accède qu’à ce qui a déjà eu lieu",
"voir implique toujours arriver trop tard",
"la perception suppose une antériorité irréductible de l’image",
"ce qui est vu appartient déjà au passé de son apparition",
"le présent visible est toujours déjà dépassé",
"l’image précède nécessairement le regard qui la saisit"
]

anaya = [
"ce qui apparaît t’inclut... sans jamais te contenir",
"tu es là... mais déjà pris dans ce qui t’échappe",
"la surface ne fixe rien... elle laisse passer",
"tu fais déjà partie de ce qui te dépasse",
"ce qui te perds te relie autrement",
"tu participes à ce qui te traverse"
]

anaya_plus = [
"tu es porté par ce qui te traverse sans jamais se fixer",
"ce qui apparaît t’inclut sans jamais se refermer sur toi",
"tu avances dans un mouvement qui te dépasse doucement",
"la surface t’accueille sans jamais te retenir",
"tu es déjà dedans... sans avoir franchi quoi que ce soit"
]

anaya_delay = [
"tu rejoins ce qui t’a précédé sans jamais être en dehors",
"ce qui apparaît t’accueille après s’être déjà transformé",
"tu entres dans ce qui t’a déjà inclus",
"ce qui te précède ne te laisse jamais derrière",
"tu arrives dans un mouvement déjà en cours",
"tu es accueilli par ce qui a commencé sans toi"
]

# --- FUSION DES LISTES ---

blake += blake_plus + blake_delay
lei += lei_plus + lei_delay
sorel += sorel_plus + sorel_delay
anaya += anaya_plus + anaya_delay

# --- MÉLANGE PAR BLOCS (ANTI-RÉPÉTITION) ---

random.shuffle(blake)
random.shuffle(lei)
random.shuffle(sorel)
random.shuffle(anaya)

n = min(len(blake), len(lei), len(sorel), len(anaya))

items = []

for i in range(n):
    block = [
        ("BLAKE :", blake[i]),
        ("LEI :", lei[i]),
        ("SOREL :", sorel[i]),
        ("ANAYA :", anaya[i])
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
