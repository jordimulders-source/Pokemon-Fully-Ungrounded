# Kricketune-evolutie r2: alleen het verre (linker) oog verplaatst (Jordi op r1: "let op de positie van het linker oog" / "die is niet
# natuurlijk" / "naar de plek waar het oog in het model staat"). Plek en grootte uit het ORIGINELE model gemini/v3_r1.png: kleine witte
# plek net binnen de linkerkopomlijning, 1024-px x410-420, y266-276 = natief (39,25) -> sprite (25,14), op de hoogte van de glans van het
# nabije oog (33,14). Vorm en kleuren: Kricketune-oog (anim_front frame 1, veraf, rijen 21-23 = lid | glans+pupil | onderkant), glans op
# (25,14). Plek van het r1-oog terug naar de kop: omlijning x24 zwart, selout x25 donkerrood, binnenin rood licht (10) zoals de buren.
# Verder pixeldiff 0 met r1 (assert). Bouwen: cd kricketune_evo && python3 sprite_r2/bouw.py
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image
r1=laden('sprite_r1/kricketune_evo_r1.png'); o=r1.copy()
KT=np.asarray(Image.open('../../../../graphics/pokemon/kricketune/anim_front.png')).astype(int); KTM={4:1,5:2,6:12,7:6}
for y in range(13,18):                      # r1-oog (x25-28, y14-17) weg: kop zoals het model
    o[y,24]=1; o[y,25]=7
    for x in range(26,30):
        if o[y,x] in (1,2,6,12): o[y,x]=10
for y in range(21,24):                      # Kricketune verre oog, rijen 21-23, x24-27 -> +1,-8 (glans kt (24,22) -> (25,14))
    for x in range(24,28):
        if KT[y,x] in KTM: o[y-8,x+1]=KTM[KT[y,x]]
d=o!=r1; zone=np.zeros_like(d); zone[12:19,24:31]=True
assert not (d&~zone).any()
opslaan(o,'sprite_r2/kricketune_evo_r2.png'); print('anders dan r1:',int(d.sum()),'px, alle in x24-30 y12-18'); toon(o,y0=11,y1=19,x0=22,x1=38)
# vel: kop 12x (r1 | r2 | origineel model op dezelfde schaal, precies dezelfde modelpixels) en hele sprite 4x (r1 | r2)
import schrap as S
a,c,L=klassen(); S.PRIO={11:4,5:4,4:4}; _,rows,cols=S.schrap_merge(c)
KR=[i for i in range(85) if i not in rows]; KK=[i for i in range(75) if i not in cols]
x0,y0,x1,y1=18,4,46,24; z=12; bw,bh=(x1-x0)*z,(y1-y0)*z
M=Image.open('gemini/v3_r1.png').convert('RGB'); px=lambda u:int(9.75+10.24*u)
m=M.crop((px(U0+KK[x0-X0]),px(V0+KR[y0-Y0]),px(U0+KK[x1-1-X0]+1),px(V0+KR[y1-1-Y0]+1))).resize((bw,bh),Image.LANCZOS)
from PIL import ImageDraw
W=Image.new('RGB',(3*(bw+12),20+bh+20+256+16+70),'white'); dr=ImageDraw.Draw(W)
for i,(n,im) in enumerate([('r1',rgb(r1,(255,255,255))),('r2',rgb(o,(255,255,255))),('origineel model (gemini/v3_r1.png)',m)]):
    X=i*(bw+12); dr.text((X+2,4),n+' kop 12x',fill=(0,0,0))
    W.paste(im.crop((x0,y0,x1,y1)).resize((bw,bh),Image.NEAREST) if i<2 else im,(X,20))
for i,s in enumerate((r1,o)):
    X=i*(bw+12); W.paste(rgb(s,(255,255,255)).resize((256,256),Image.NEAREST),(X,40+bh)); dr.text((X+262,40+bh),('r1' if i==0 else 'r2')+' 4x',fill=(0,0,0))
    for j,bg in enumerate([(232,232,216),(40,48,56)]): W.paste(rgb(s,bg),(X+j*70,56+bh+256))
W.save('sprite_r2/vel.png')
