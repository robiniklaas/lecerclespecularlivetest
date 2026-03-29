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
"la perception est structurée par une dissociation irréductible",
"le dispositif configure une expérience où le sujet ne peut pas apparaître comme tel",
"l’image fonctionne sans jamais se stabiliser dans une forme définitive",
"le dispositif maintient une séparation opératoire entre ce qui est perçu et ce qui perçoit",
"la perception est contrainte par une organisation qui la dépasse",
"le cadre impose une organisation qui précède toute expérience perceptive",
"l’image maintient sa cohérence en excluant toute inscription du sujet",
"le système produit une visibilité qui n’autorise aucune réflexivité",
"l’image ne permet aucune intégration du point de vue qui la rend possible",
"le dispositif organise une dissociation stable entre ce qui est vu et celui qui voit",
"le système produit une séparation entre perception et identification du sujet"
]

lei = [
"tu arrives... quand la position n’est déjà plus disponible",
"ce que tu vois se décide... avant ton regard",
"la netteté serait un contresens ici...",
"le retour a lieu... mais pas dans ta direction",
"ce n’est pas toi qui manques... c’est la place que tu crois occuper",
"tu regardes depuis un point déjà déplacé",
"le cadre a changé... sans que tu le voies",
"le système te précède désormais",
"ce que tu perçois se forme... ailleurs que là où tu te tiens",
"le point existe... mais il ne t’est jamais donné",
"tu vois... mais depuis un décalage irréductible",
"le cadre agit... avant que tu n’y entres",
"tu es pris dans ce qui ne te renvoie rien",
"l’absence est déjà là... avant ton regard",
"tu ne peux pas confirmer ce que tu vois",
"ce qui te dépasse agit déjà en toi...",
"la distance est déjà en place... avant ton geste",
"tu ne peux pas t’installer dans ce que tu vois",
"tu es déjà engagé... avant même de regarder",
"ce que tu vois s’établit... sans toi",
"tu ne peux pas revenir sur ce qui est déjà là",
"le regard ne coïncide jamais avec ce qu’il voit",
"tu restes dehors... même en regardant",
"aucun point de départ ne t’est accessible",
"tu peux te reconnaître... sans jamais t’y fixer",
"la séparation reste... même quand tu t’en approches",
"tu es là... et déjà ailleurs",
"ce que tu vois ne s’arrête jamais vraiment",
"ce que tu perçois se forme... ailleurs",
"le retour existe... mais ne revient pas"
]

sorel = [
"tu continues à parler de miroir, alors que rien ici ne remplit les conditions du reflet",
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
"la proximité perceptive est une illusion produite",
"l’identification fonctionne comme une opération toujours incomplète",
"la résolution est empêchée par la condition même du dispositif",
"la réflexivité est rendue structurellement impossible",
"l’origine est neutralisée par la logique du dispositif",
"la condition d’apparition repose sur l’impossibilité de se voir soi-même",
"la coïncidence est annulée par le fonctionnement du dispositif",
"la présence du sujet est exclue comme condition de cohérence",
"la tension n’est pas un effet mais une condition",
"l’appropriation est neutralisée par la structure du dispositif",
"la forme excède toujours ce qu’elle prétend être",
"la condition de vision implique une perte préalable de présence",
"la critique ne trouve plus de point d’appui",
"la distinction sujet objet devient inopérante",
"le dispositif annule les distinctions qu’il semblait produire"
]

anaya = [
"ce qui apparaît t’inclut... sans jamais te contenir",
"tu es là... mais déjà pris dans ce qui t’échappe",
"la surface ne fixe rien... elle laisse passer",
"le cercle existe... mais il ne se referme pas sur toi",
"tu es déjà impliqué... autrement que visible",
"la position devient un passage que tu ne peux pas fixer",
"tout reste... mais autrement",
"tu fais déjà partie de ce qui te dépasse",
"tu es là, mais déjà déplacé dans ce qui apparaît",
"ce que tu perds te relie autrement",
"la distance ne sépare pas... elle transforme",
"ce qui précède te porte sans se montrer",
"tu es inclus... autrement que visible",
"ce qui manque ouvre un passage",
"tu continues pourtant à être là",
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
"ce qui apparaît ne demande rien et pourtant te traverse"
]

# --- MÉLANGE CONTRAINT SANS RÉPÉTITION ---

pools = {
    "BLAKE :": blake.copy(),
    "LEI :": lei.copy(),
    "SOREL :": sorel.copy(),
    "ANAYA :": anaya.copy()
}

# mélange interne
for key in pools:
    random.shuffle(pools[key])

items = []
last_author = None

while any(pools.values()):
    available = [a for a in pools if pools[a]]

    # tri pour équilibrer
    available.sort(key=lambda a: len(pools[a]), reverse=True)

    # choisir un auteur différent du précédent
    chosen = None
    for author in available:
        if author != last_author:
            chosen = author
            break

    # sécurité absolue (ne devrait jamais arriver)
    if chosen is None:
        for author in available:
            if author != last_author:
                chosen = author
                break

    text = pools[chosen].pop()
    items.append((chosen, text))
    last_author = chosen

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
