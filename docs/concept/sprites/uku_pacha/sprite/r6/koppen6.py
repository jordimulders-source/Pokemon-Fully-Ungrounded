# Uku Pacha r6: alleen Jordi's punten op r5 (per pixel tegen het natieve model)
R=[list(l.rstrip('\n')) for l in open('../r5/raster_af.txt')][:64]
def zet(x,y,c,oud):
    assert R[y][x]==oud,(x,y,R[y][x],oud); R[y][x]=c
# 1. tong linkerkop: model = steel uit de bek (16-17,38) schuin naar linksonder, vork bij (11,41):
#    linkertip (9,42) -> sprite (3,26), ondertip (12,42-43) -> (5,27), zwart tussen de tips (10-11,42) -> (4,27).
#    In r5 brak de K op (4,26) de steel van de tips af; (5,26) is in het model donker (K 1,17 van 2,1).
zet(4,26,'P','K'); zet(5,26,'K','P')
# 2. pupil rechteroog 1 px naar links
zet(40,5,'Y','K'); zet(39,5,'K','Y')
# 3a. mond rechterkop: modellijn (50-52,16) (53-54,17) (55-56,18) (57-60,17) (61-66,18) (67,19)
#     -> sprite (31-32,8) (33-34,9) (35,10) (36-38,9) (39-42,10) (43,10). Gat op (33,9) dicht,
#     de knik op (55-56,18) zwart ligt een rij lager: (35,9) -> vlak b (model 129-131), (35,10) -> n
zet(33,9,'n','h'); zet(35,9,'b','n'); zet(35,10,'n','s')
# 3b. streep over de kop: model van de wenkbrauw (63-65,10, zwart) over rij 10 (53-57, lum 97-111)
#     naar de bovenrand (52,10); erboven (rij 9) en eronder (rij 11, 180) licht.
#     sprite: wenkbrauw (40-41,4) K, ooglid (38,5) K, dan (37,5) (36,4) (35,4) (34,4) tot de rand (33,4).
#     Lichtere lijntint s (model 97-111); onder de streep (35-36,5) licht h zoals het model (180).
zet(37,5,'s','b'); zet(36,4,'s','h'); zet(35,4,'s','m'); zet(34,4,'s','m')
zet(35,5,'h','m'); zet(36,5,'h','m')
open('raster_af.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
