import random

# --- TEXTES PAR VOIX (ÉQUILIBRÉS) ---

blake = [
"le dispositif organise une séparation fonctionnelle entre perception et identification",
"l’image dépend d’un point de vue qui ne peut pas s’y intégrer",
"le système fonctionne sans produire de retour exploitable sur l’observateur",
"le dispositif introduit une dissymétrie entre vision et présence",
"les paramètres perceptifs cessent d’être constants dans ce système",
"le dispositif maintient une distance irréductible entre sujet et image",
"le système empêche toute correspondance directe entre regard et image",
"le dispositif maintient une tension constante entre présence et absence",
"le système rend toute identification instable sans la supprimer",
"le dispositif impose une extériorité constante au sujet percevant",
"la structure empêche toute coïncidence entre regard et représentation",
"la perception est structurée par une dissociation irréductible",
"le dispositif configure une expérience où le sujet ne peut pas apparaître comme tel",
"le dispositif maintient une séparation opératoire entre ce qui est perçu et ce qui perçoit",
"la perception est contrainte par une organisation qui la dépasse",
"le cadre impose une organisation qui précède toute expérience perceptive",
"le système produit une visibilité qui n’autorise aucune réflexivité",
"le dispositif organise une dissociation stable entre ce qui est vu et celui qui voit",
"le dispositif calcule une dissymétrie stable entre vision et présence",
"le cadre impose une contrainte verticale sur la perception",
"le système distribue l’image sans inclure le sujet dans son calcul",
"le dispositif maintient une continuité indépendante de ton action",
"le champ visible est limité par une architecture que tu ne contrôles pas",
"le système impose une séquence sans retour possible vers l’origine",
"la perception est indexée sur un flux que tu ne peux pas interrompre",
"le dispositif encode une distance constante entre toi et ce qui apparaît",
"le système introduit une latence constante entre image et perception",
"le regard est traité comme une variable en retard dans le processus",
"l’image est calculée avant d’être effectivement perçue",
"la perception est toujours en retard sur son propre déclenchement",
"l’image est calculée avant toute possibilité de perception",
"la perception est une sortie, pas une origine",
"le dispositif empêche toute synchronisation entre regard et image",
"le système exécute une séquence sans retour vers l’observateur",
"le regard arrive toujours après l’exécution du système",
"le dispositif organise une expérience sans point d'ancrage"
]

lei = [
"tu arrives quand la position n’est déjà plus disponible",
"ce que tu vois se décide avant ton regard",
"le retour a lieu mais pas dans ta direction",
"tu regardes depuis un point déjà déplacé",
"le système te précède désormais",
"tu vois... mais depuis un décalage irréductible",
"tu ne peux pas t’installer dans ce que tu vois",
"tu es déjà engagé... avant même de regarder",
"ce que tu vois s’établit... sans toi",
"tu ne peux pas revenir sur ce qui est déjà là",
"tu restes dehors... même en regardant",
"tu peux te reconnaître... sans jamais t’y fixer",
"tu es là... et déjà ailleurs",
"ce que tu vois ne s’arrête jamais vraiment",
"tu regardes... mais ça a déjà glissé ailleurs",
"ça continue... même si tu t’arrêtes",
"tu vois une partie... le reste t’échappe déjà",
"tu arrives... mais c’est déjà en train de passer",
"tu ne tiens jamais ce que tu regardes",
"ça défile... sans attendre que tu comprennes",
"tu touches presque... mais non",
"tu es là... mais jamais au bon moment",
"ce que tu vois commence sans toi",
"tu suis... mais rien ne t’attend",
"tu regardes... mais c’est déjà passé",
"tu arrives toujours après ce que tu vois",
"ça a déjà eu lieu quand tu le remarques",
"tu vois... mais c’est trop tard",
"tu suis... mais tu es en retard",
"tu regardes... et ça t’échappe déjà",
"tu arrives trop tard",
"tu vois quelque chose… qui n’est plus",
"ça bouge avant toi",
"tu arrives et c’est fini",
"ça défile… sans t’attendre"
]

sorel = [
"la présence visible suppose la suppression de ce qui devrait la garantir",
"le flou n’est pas un défaut, c’est la condition même de ce qui apparaît",
"la circularité du regard est ici rendue structurellement impossible",
"le sujet n’est pas absent, il est rendu inopérant par le dispositif",
"la présence est produite au prix de son propre effacement",
"la stabilité apparente masque une transformation des conditions",
"il n’y a jamais eu de point extérieur à ce dispositif",
"la visibilité repose ici sur une exclusion constitutive du sujet",
"la transparence supposée est ici structurellement impossible",
"la structure précède ce que tu crois vivre immédiatement",
"la représentation suppose ici l’effacement de celui qui regarde",
"la présence est produite par un manque constitutif",
"la validation est rendue impossible par la logique même du dispositif",
"l’expérience dépend d’une extériorité irréductible",
"l’identification fonctionne comme une opération toujours incomplète",
"la réflexivité est rendue structurellement impossible",
"l’origine est neutralisée par la logique du dispositif",
"la condition d’apparition repose sur l’impossibilité de se voir soi-même",
"la coïncidence est annulée par le fonctionnement du dispositif",
"la tension n’est pas un effet mais une condition",
"l’appropriation est neutralisée par la structure du dispositif",
"la forme excède toujours ce qu’elle donne à voir",
"la condition de vision implique une perte préalable de présence",
"ce que tu perçois n’apparaît qu’à travers la restriction de son propre champ",
"la continuité perçue repose sur une discontinuité masquée",
"l’image produit ce qu’elle prétend seulement révéler",
"la perception se constitue dans ce qui lui échappe",
"le regard n’accède qu’à ce qui a déjà eu lieu",
"voir implique toujours arriver trop tard",
"ce qui est vu appartient déjà au passé de son apparition",
"la perception suppose une antériorité irréductible de l’image",
"la perception est structurée comme un retard",
"la présence est produite par son propre retrait",
"l’image ne peut inclure celui qui la perçoit",
"la perception dépend d’une perte préalable de présence"
]

anaya = [
"ce qui apparaît t’inclut... sans jamais te contenir",
"tu es là... mais déjà pris dans ce qui t’échappe",
"la surface ne fixe rien... elle laisse passer",
"tu fais déjà partie de ce qui te dépasse",
"ce que tu perds te relie autrement",
"tu participes à ce qui te traverse",
"ce qui semble proche est déjà ailleurs",
"tu passes... sans pouvoir retenir",
"tu habites cette distance",
"tu es présent... autrement que visible",
"ce dehors t’habite déjà",
"tout commence... sans commencer",
"tu es en mouvement dans ce qui te définit",
"tu es séparé... sans être isolé",
"les deux coexistent sans se résoudre",
"tu avances dans ce qui ne revient pas",
"tout continue... sans fin stable",
"la surface relie sans jamais fixer",
"tu es déjà là... autrement",
"tu es porté par ce qui te traverse sans jamais se fixer",
"ce qui apparaît t’inclut sans jamais se refermer sur toi",
"tu avances dans un mouvement qui te dépasse doucement",
"la surface t’accueille sans jamais te retenir",
"tu es déjà dedans... sans avoir franchi quoi que ce soit",
"ce qui glisse t’emporte sans te perdre",
"tu habites ce passage sans pouvoir l’arrêter",
"tout te relie sans jamais te fixer",
"tu es pris dans un flux qui ne t’exclut pas",
"tu rejoins ce qui t’a précédé sans jamais être en dehors",
"tu arrives dans un mouvement déjà en cours",
"ce qui apparaît t’accueille après s’être déjà transformé",
"tu es accueilli par ce qui a commencé sans toi",
"ce qui te précède ne te laisse jamais derrière",
"tu avances dans un flux sans bord",
"tu es là dans ce qui ne t’attend pas"
]

# --- MÉLANGE PAR BLOCS (ANTI-RÉPÉTITION) ---

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

# --- GÉNÉRATION RSS ---

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
