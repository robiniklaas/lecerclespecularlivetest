import random

# --- BLAKE : SYSTÈME / CALCUL / STRUCTURE ---

blake = [
"le système exécute une séquence sans retour vers l’observateur",
"le dispositif calcule une dissymétrie constante entre vision et présence",
"l’image est produite indépendamment de toute validation subjective",
"le cadre impose une contrainte verticale sur la perception",
"la perception est indexée sur un flux non interrompable",
"le système distribue l’image sans intégrer le sujet dans son calcul",
"la visibilité est générée comme sortie d’un processus inaccessible",
"le dispositif maintient une distance constante entre sujet et image",
"le système impose une latence entre captation et affichage",
"le regard est traité comme variable différée dans le dispositif",
"l’image est calculée avant toute possibilité de perception",
"le dispositif encode une antériorité systématique de l’image",
"la perception est produite après son propre déclenchement",
"le système maintient une dissociation stable entre voir et être présent",
"le dispositif empêche toute synchronisation entre regard et image",
"la structure interdit toute coïncidence perceptive",
"le système organise une perte constante d’alignement",
"le dispositif impose une extériorité non négociable au sujet",
"la perception dépend d’un calcul auquel le sujet n’accède pas",
"le système produit une visibilité sans retour réflexif",
"le dispositif maintient une incoïncidence fonctionnelle",
"la perception est contrainte par une architecture non modifiable",
"le système exécute sans intégrer celui qui observe",
"l’image fonctionne sans point d’entrée pour le sujet",
"le dispositif maintient une séparation opératoire permanente",
"le système produit une continuité sans présence",
"la perception est une sortie, pas une origine",
"le dispositif organise une expérience sans centre",
"le système stabilise une absence comme condition de visibilité",
"le regard arrive toujours après l’exécution du système"
]

# --- LEI : EXPÉRIENCE / IMMÉDIAT / DÉCALAGE ---

lei = [
"tu regardes… mais c’est déjà passé",
"tu arrives trop tard",
"ça a déjà commencé sans toi",
"tu vois… mais ça disparaît",
"tu touches presque… mais non",
"tu es là… mais pas au bon moment",
"ça défile… sans t’attendre",
"tu suis… mais ça t’échappe",
"tu regardes… et ça glisse",
"tu ne peux rien retenir",
"tu arrives… et c’est fini",
"tu vois une trace… pas la chose",
"ça bouge avant toi",
"tu es toujours après",
"tu regardes… mais ça continue ailleurs",
"tu crois voir… mais c’est déjà autre chose",
"tu avances… mais ça recule",
"tu touches… mais ça s’éloigne",
"tu es dedans… mais décalé",
"tu vois… mais pas maintenant",
"tu regardes… trop tard déjà",
"ça ne t’attend pas",
"tu arrives… mais ça n’est plus là",
"tu vois quelque chose… qui n’est plus",
"tu suis un mouvement… déjà parti",
"tu regardes… et ça fuit",
"tu es là… mais ça t’échappe encore",
"tu vois… mais jamais au bon moment",
"tu arrives après ce que tu vois",
"tu regardes… et c’est déjà ailleurs"
]

# --- SOREL : STRUCTURE / PHILOSOPHIE / IMPOSSIBILITÉ ---

sorel = [
"la perception se constitue à partir d’une extériorité irréductible",
"le visible suppose l’effacement de ce qui pourrait le garantir",
"la coïncidence entre regard et image est structurellement impossible",
"la présence est produite comme effet d’un manque constitutif",
"le sujet ne disparaît pas, il est rendu inopérant",
"la visibilité repose sur une exclusion préalable du regardeur",
"l’expérience dépend d’une condition qu’elle ne peut intégrer",
"la transparence est ici rendue impossible par la structure même",
"la représentation suppose l’impossibilité de se représenter soi-même",
"la perception est toujours en retard sur sa propre condition",
"le regard n’accède qu’à ce qui a déjà eu lieu",
"voir implique une antériorité irréductible de l’image",
"ce qui est perçu appartient déjà au passé de son apparition",
"la condition d’apparition exclut toute simultanéité",
"la présence visible implique une absence préalable",
"la forme excède toujours ce qu’elle donne à voir",
"la perception est constituée par ce qui lui échappe",
"l’origine est neutralisée dans le processus perceptif",
"la réflexivité est rendue structurellement impossible",
"la continuité perçue masque une discontinuité constitutive",
"le sujet est exclu comme condition de cohérence",
"la perception dépend d’une perte préalable de présence",
"l’image ne peut inclure celui qui la perçoit",
"la visibilité est conditionnée par une séparation irréductible",
"le regard arrive toujours après ce qu’il prétend saisir",
"la perception suppose une antériorité qu’elle ne peut combler",
"la présence est produite par son propre retrait",
"le visible se constitue dans l’impossibilité d’être rejoint",
"la perception est structurée comme un retard",
"le réel apparaît comme ce qui ne peut être saisi simultanément"
]

# --- ANAYA : RELATION / FLUX / INCLUSION ---

anaya = [
"tu entres dans ce qui t’a déjà accueilli",
"ce qui t’emporte ne te laisse jamais derrière",
"tu es déjà là dans ce qui te dépasse",
"ce qui apparaît t’inclut sans te contenir",
"tu avances dans ce qui t’a précédé",
"ce qui te traverse ne s’arrête pas pour toi",
"tu es porté par ce qui continue",
"ce qui t’échappe te garde en lui",
"tu habites un mouvement qui ne se fixe pas",
"tu es inclus dans ce qui se transforme",
"ce qui apparaît t’ouvre sans se refermer",
"tu es là dans ce qui ne t’attend pas",
"ce qui passe te contient encore",
"tu avances dans un flux sans bord",
"ce qui t’accueille change sans cesse",
"tu es déjà pris dans ce qui te dépasse",
"ce qui te porte ne revient pas en arrière",
"tu habites ce qui ne se retient pas",
"ce qui s’éloigne t’inclut encore",
"tu es là dans ce qui ne se stabilise pas",
"ce qui commence continue sans toi",
"tu es porté sans être fixé",
"ce qui te dépasse te relie",
"tu avances dans ce qui ne se ferme pas",
"ce qui t’inclut ne t’enferme jamais",
"tu es déjà dedans sans entrée",
"ce qui passe te transforme",
"tu es pris dans ce qui ne s’arrête pas",
"ce qui t’accueille ne te retient pas",
"tu es là dans ce qui continue"
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
