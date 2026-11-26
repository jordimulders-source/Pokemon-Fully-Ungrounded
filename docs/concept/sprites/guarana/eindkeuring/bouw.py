# Guarana fase 1, eindkeuring (Dragonfly Cave: schaduw + belijning + kleurtinten). Leest r4 in, verandert alleen tinten binnen het
# bevroren silhouet (alpha-diff 0 bewezen met assert), oogwit/pupil onaangeroerd. Gebruik (vanuit docs/concept/sprites/guarana):
#   python3 eindkeuring/bouw.py
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); import gemeen
R4={'guarana_ek.png':'sprite_r4/guarana_r4.png','guarana_ek_ogen_groter.png':'sprite_r4/r4_ogen_groter.png'}
HOOFD=np.array(Image.open('sprite_r4/guarana_r4.png')).astype(int)
# 1. Palet groen: stappen r4 82/109/136/163 (27 per tint, onder de +-30-40 van SPRITE_KERN en de maatstaf: Skinguin 22/36/44,
#    Dundragoon 37/38/54) -> 73/104/140/178 (31/36/38); verzadiging iets op (40-45 -> 45-50 %, blijft olijf zoals het model);
#    hue shift sterker: lijn 102, schaduw 99 (koeler), midden 88, licht 81 (warmer). Rood blijft (55/90/120/163, hue 357->14).
PAL=list(gemeen.PAL)
PAL[2]=(120,28,32)                       # zoals r4 (bouw.py r4 zet deze; gemeen.PAL zelf heeft nog de r1-waarde)
PAL[6]=(58,86,46); PAL[7]=(84,122,64); PAL[8]=(122,160,80); PAL[9]=(166,198,108)
# 2. Schaduw tros uit de modelhelderheid (model_op_schaal, L): idx 2 lijn, 3 schaduw, 4 midden, 5 licht.
#    Alleen pixels die in r4 nog de oude waarde hebben (dus nooit een oogrand of oogpixel van de variant).
P={
 # rechtsondervrucht: rechterrand stond als lijnrood (L55) pal naast de zwarte buitenlijn = 2 px lijn; model is daar
 # schaduwtoon (L 90-109, de vrucht zelf 116-173) -> schaduwsikkel die van rechtsboven langs de rand naar de onderrand (24-27,32) loopt
 (27,27):(2,3),(27,28):(2,3),(27,29):(2,3),(28,29):(2,3),(28,30):(2,3),(27,31):(2,3),
 # naad boven die vrucht: (25,27) was licht maar het model is daar donker (L63, naad) -> lijn; (26,27) model L96 -> schaduw
 (25,27):(5,2),(26,27):(2,3),
 # vrucht rechts van het bovenoog: onderkant rechts model L74/L86 -> korte diagonale sikkel
 (24,26):(4,3),(23,27):(4,3),
 # middelste vrucht: onderkant model L56/L88 -> sikkel (in de variant is (18,27) oogrand: daar overgeslagen, (19,27) dan ook)
 (18,27):(4,3),(19,27):(4,3),
}
for uit,bron in R4.items():
    o=np.array(Image.open(bron)).astype(int); r4=o.copy(); log=[]
    for (X,Y),(oud,nieuw) in P.items():
        if o[Y,X]==oud and HOOFD[Y,X]==oud: o[Y,X]=nieuw; log.append((X,Y,oud,nieuw))
    if 'ogen' in uit and o[27,18]==2: o[27,19]=r4[27,19]; log=[l for l in log if l[:2]!=(19,27)]
    assert ((o>0)==(r4>0)).all(), 'silhouet gewijzigd'
    assert (o[np.isin(r4,(10,11))]==r4[np.isin(r4,(10,11))]).all() and ((o==1)==(r4==1)).all(), 'oog/zwart gewijzigd'
    p=Image.fromarray(o.astype('uint8'),'P'); flat=[v for c in PAL for v in c]; p.putpalette(flat+[0]*(768-len(flat)))
    p.save('eindkeuring/'+uit,transparency=0)
    print(uit,'pixels anders dan r4:',len(log),log)
