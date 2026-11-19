# Palpaca r5: vanaf r4 (goedgekeurd als basis). Alleen uitvoering: palet-contrast, torso-perspectief, belijning, losse pixels.
# Indices: 1 donkere lijn, 2-5 wol (licht->schaduw), 6 zachte lijn, 7-10 rood, 11/15 verre poot, 12 geel, 13 turkoois, 14 roze.
import numpy as np; from PIL import Image
R4=np.array(Image.open('../../r4/palpaca.png'))
# palet: wol-tinten verder uit elkaar (DFC: geen te dicht bij elkaar liggende tinten), warm hue-shift behouden
PAL=[(152,208,160),(52,44,36),(255,253,245),(238,231,210),(210,200,174),(176,163,138),(124,112,92),
     (244,108,98),(218,64,68),(158,36,56),(84,24,34),(154,137,113),(236,206,100),(62,176,156),(222,160,164),(112,97,78)]
a=R4.copy()
CH='.123456789ABCDEF'
# torso x17..45, rijen 39-49 (met de hand, per rij uit segmenten opgebouwd)
T={
39:"....6"+"2222"+"333333"+"2222222"+"3334451",
40:"....6"+"222"+"33333333"+"222222"+"34"+"65551",
41:"....6"+"222"+"3"*14+"345651.",
42:"....6"+"22"+"3"*16+"445"+"1..",
43:"....6"+"3"*18+"445"+"1..",
44:"....6"+"3"*17+"4445"+"1..",
45:"...6"+"4"+"3"+"3"*16+"44"+"5"+"5"+"F1.",
46:".66"+"2"+"3"+"5"+"3"*13+"22"+"445"+"6"+"BF1.",
47:"6"+"22"+"33"+"5"+"44"+"3333333"+"4"+"5"+"4"+"22"+"3"+"4"+"5"+"6"+"BFF1.",
48:"6"+"22"+"3"+"3"+"4"+"6"+"5"+"44"+"2"+"33"+"3"+"44"+"5"+"4"+"333"+"4"+"1"+"BFFF1.",
49:"6"+"33"+"44"+"55"+"1"+"55"+"22"+"33"+"4"+"5"+"6"+"5"+"4"+"33"+"4"+"6"+"1"+"FFF1.",
}
for y,row in T.items():
    assert len(row)==29,(y,len(row),row)
    for i,c in enumerate(row):
        x=17+i; v=CH.index(c)
        assert (v>0)==(R4[y,x]>0),('alfa',x,y)
        a[y,x]=v
# fijnstelling: borsthooglicht als ovaal, schaduwsikkel verre flank smal boven -> breed onder, jagged buikschaduw (wol)
P={(26,40):2,(22,42):3,(25,41):3,(24,42):2,(23,43):2,
   (40,42):3,(40,43):3,(39,44):3,(38,45):4,
   (32,46):4,(23,46):4,(30,47):4,(31,47):4,
   (31,45):4,(26,38):4,(30,38):3,  # losse pixels in de halsbandschaduw
   
   (33,40):3,(38,40):3,(35,41):2,(36,41):2,  # rughooglicht als bol i.p.v. band langs de rand (geen banding)
  (33,45):4,(30,46):4,(31,46):4,(33,46):4,(30,48):4,(32,48):5}
for (x,y),v in P.items():
    assert a[y,x]>0; a[y,x]=v
# belijning (DFC: nooit zwart en zachte lijn om en om op een rand; selout lichtkant, zwart schaduwkant)
L={(24,17):6,   # kruin tussen de oren: 6-1-6 -> 6
   (36,37):6,   # rugbultje: 6-1-6 -> 6
   (22,37):6,   # linkerkant halsband op de lichtkant: 6-1-6 -> 6
   (17,52):10,  # handschoen links: A-1-A -> A (donkerrood)
   (44,54):1,(45,56):6}  # verre achterpoot linkerrand: boven in de lijfschaduw zwart, onder selout 6
for (x,y),v in L.items():
    assert a[y,x]>0; a[y,x]=v
# losse zwarte pixel bovenin de verre achterpoot (Jordi): (42,47) 1 -> F (zit in rij 47 hierboven)
assert R4[47,42]==1 and a[47,42]==15
assert ((a>0)!=(R4>0)).sum()==0
pal=[c for t in PAL for c in t]
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(pal); im.save('../palpaca.png',transparency=0)
open('../normal.pal','w').write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%t for t in PAL))
print('kleuren',len(np.unique(a)),'anders dan r4',(a!=R4).sum(),'alfa-diff',((a>0)!=(R4>0)).sum())
