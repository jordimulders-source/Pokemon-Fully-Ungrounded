# Eindkeuring r2: reparaties op een KOPIE van sprite_r2 -> voorstel.png. Draaien vanuit fase1/: python3 eindkeuring_r2/voorstel.py
# Indices: 0 transp, 1 zwart(K), 2 D donkerpaars (outline base paars), 3 P, 4 p, 5 W, 6 w, 7 l, 8 m, 9 t, 10 T
import numpy as np
from PIL import Image
src=Image.open('sprite_r2/sprite.png'); a=np.array(src).copy(); orig=a.copy()
K,D,P,w,l,m=1,2,3,6,7,8
FIX=[
 # P1 zwart en paars om en om / zwart aan de lichtkant
 ('Z1',(15,23),D,K),('Z1',(15,22),K,P),    # K D K op de onderlijn van antenne 1: D->K, hoekpixel ernaast ->P (onderrand voetje is al P)
 ('Z2',(17,34),K,D),('Z2',(18,35),K,D),    # bovenkant rechtsboven-voetje (lichtkant)
 ('Z3',(34,39),K,D),                       # bovenrand antenne 3 bij de aanzet
 ('Z4',(48,37),K,D),                       # bovenrand antenne 4 bij de aanzet
 ('Z5',(44,31),K,D),('Z5',(44,32),K,D),('Z5',(44,33),K,D),('Z5',(45,30),K,D),('Z5',(46,29),K,D),  # onderste voetje boven/linksboven (lichtkant, binnenlijn)
 # P2 verdikte zwarte lijnen (2x2 / L-hoeken), silhouet gelijk
 ('V1',(37,37),K,m),('V1',(37,40),K,P),    # 2x2-blok en dubbele onderlijn bij de aanzet van antenne 3
 ('V2',(12,55),K,P),                       # onderlijn antenne 2: 2 zwart in kolom 55
 ('V3',(14,26),K,P),                       # onderlijn antenne 1: 2 zwart in kolom 26
 ('V4',(42,5),K,P),                        # rand linksonder bij het einde van de naad
 ('V5',(44,7),K,w),('V6',(46,8),K,l),('V7',(48,11),K,m),  # trap linksonder
 ('V8',(50,30),K,P),                       # onderkant onderste voetje
 ('V9',(56,55),K,P),                       # onderlijn antenne 4 bij de punt
 # P3 oogrand: L-hoeken in de zwarte boog (vorm van het oog blijft)
 ('O1',(39,7),K,w),('O1',(37,15),K,w),
]
for code,(y,x),old,new in FIX:
    assert a[y,x]==old,(code,y,x,a[y,x])
    a[y,x]=new
diff=np.argwhere(a!=orig); assert len(diff)==len(FIX)
assert ((a>0)==(orig>0)).all(), 'silhouet veranderd'
out=Image.fromarray(a.astype(np.uint8),'P'); out.putpalette(src.getpalette())
out.save('eindkeuring_r2/voorstel.png',transparency=0)
np.save('eindkeuring_r2/voorstel.npy',a)
print('gewijzigd',len(diff),'zwart',int((orig==1).sum()),'->',int((a==1).sum()))
