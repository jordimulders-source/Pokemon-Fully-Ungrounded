# r12: oogvarianten op r11 (haar + snor van r11 blijven). Jordi bij r11: "haha die ogen kunnen niet" en "wat niet kan is dat
# het linkeroog niet in perspectief is, waardoor die heel clownesk eruit ziet". Alle varianten zonder monocle, beide ogen
# in dezelfde stijl; verre oog ±0,6 van de breedte van het nabije oog (gemeten: Rime 4:6, Hitmonchan 3:5, Mr. Mime 2:2),
# buitenkolommen weggeknipt, tegen de kopomtrek (x28) zoals Rime's verre oog. Alleen pixels uit bestaande sprites:
# O1/O2 = het Rime-oog uit r10 (767/636/616/636/767), O3/O4 = het Gen 3 Mr. Mime-oog (anim_front_gba x30-31 rij 20-23),
# O4 + het Hitmonchan-lid (zwarte lijn boven het oog, anim_front_gba rij 19 x35-37). PNG-index: 1=16 3=66 5=128 6=164
# 7=200 8=248 (gezichtswit).
import numpy as np; from PIL import Image, ImageDraw
R11=np.asarray(Image.open('r11.png')).astype(int); PALI=Image.open('r11.png').getpalette()
# KOP ROND (Jordi: "hoofd is weer niet rond bedoel ik"). Rechts staat de Gen 3 Mr. Mime-boog van r8 nog (14:x46, 15-16:x47,
# 17-21:x48, 22:x47, 23:x46, 24:x44-45); het rechte stuk van 5 px op x48 wordt 3 px (rij 17 en 21 1 naar binnen, zoals de
# boog zelf al op rij 16/22 doet). Links dezelfde boog gespiegeld onder het zijhaar: rij 16 x28, rij 17-19 x27 (gezichtsselout
# 5 1 kolom naar buiten, x28 -> gezichtswit), rij 20 x27 = snorlijn 2 (krultop, zoals r10).
def kop_rond(C):
    for y in (17,21): C[y,48]=0; C[y,47]=1
    for y in (17,18,19): C[y,27]=5; C[y,28]=8
    C[20,27]=2
    return C
def leeg():
    C=kop_rond(R11.copy())
    for y in range(14,21):
        for x in range(29,43):
            if (y,x) in ((14,29),(14,30)) or (y==20 and x==41): continue
            if C[y,x] in (1,3,5,6,7) and not (x<=29 and C[y,x]==5): C[y,x]=8
    return C
def stempel(C,x0,y0,rows):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r):
            if ch!='.': C[y0+j,x0+i]=int(ch)
# verre oog = nabije oog met de buitenste (linker) kolommen weggeknipt
def knip(rows,n): return [r[n:] for r in rows]
V={}
# O1: Rime-oog + strakke 1-px-omlijning (3) direct om het oog, hoeken weg (diagonaal zoals Rime's eigen oogcontour)
O1=['.333.',
    '.767.',
    '36363',
    '36163',
    '36363',
    '.767.',
    '.333.']
V['O1']=(O1,knip(O1,2))      # 5 -> 3 breed (0,6)
# O2: Rime-oog zonder omlijning; bovenste rij en buitenkolom (rechts, schaduwkant) 1 tint donkerder
O2=['656',
    '635',
    '615',
    '635',
    '766']
V['O2']=(O2,knip(O2,1))      # 3 -> 2 breed (0,67)
# O3: Mr. Mime-oog (W w / g W / # W / W w -> 7 6 / 3 7 / 1 7 / 7 6), omlijning = Mime's omringende huidpixels -> 3,
# hoeken linksboven/rechtsonder weg (zijkanten max 3 px)
O3=['.33.',
    '.763',
    '3373',
    '3173',
    '376.',
    '.33.']
V['O3']=(O3,knip(O3,1))      # 4 -> 3 breed (0,75; smaller kan niet zonder de pupil te verliezen)
# O4: O3 + Hitmonchan-lid: zwarte lijn over de bovenkant, bovenste oogrij in de lidschaduw 3 (serieuze blik)
O4=['111.',
    '.333',
    '3373',
    '3173',
    '376.',
    '.33.']
V['O4']=(O4,knip(O4,1))
POS={'O1':((37,14),(29,14)),'O2':((38,15),(29,15)),'O3':((37,15),(29,15)),'O4':((37,15),(29,15))}
def png(C,p):
    im=Image.fromarray(C.astype('uint8'),'P'); im.putpalette(PALI); im.save(p,transparency=0)
UIT={}
for k,(nab,ver) in V.items():
    C=leeg(); (nx,ny),(vx,vy)=POS[k]; stempel(C,nx,ny,nab); stempel(C,vx,vy,ver); UIT[k]=C; png(C,'oog_%s.png'%k)
    print(k,'pixels anders dan r11:',int((C!=R11).sum()))
BEST='O4'   # serieuze blik (Jordi eerder: "minder geschokt maar iets meer serieus dan mr rime")
png(UIT[BEST],'mr_prime.png')
# vel
BG=(152,208,160); L,D=(232,236,240),(40,44,52)
def groot(p,z,box=None,bg=BG):
    im=Image.open(p).convert('RGBA'); W=Image.new('RGBA',im.size,bg+(255,)); W.alpha_composite(im); im=W.convert('RGB')
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),0)
KOP=(22,4,50,28)
rows=[]; tit=[]
for k in ['r11']+list(V):
    p='r11.png' if k=='r11' else 'oog_%s.png'%k
    rows.append([groot(p,12,KOP),groot(p,2,bg=L),groot(p,1,bg=L),groot(p,1,bg=D)]); tit.append(k+(' (huidig, afgekeurd)' if k=='r11' else '')+': kop 12x | 2x | 1x licht | 1x donker')
pad=12; Wd=max(sum(i.width+pad for i in r) for r in rows); Ht=sum(max(i.height for i in r)+26 for r in rows)
Vb=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(Vb); y=0
for t,r in zip(tit,rows):
    d.text((4,y+7),t,fill=(0,0,0)); y+=26; x=0
    for i in r: Vb.paste(i,(x,y)); x+=i.width+pad
    y+=max(i.height for i in r)
Vb.save('ogen_vel.png')
groot('mr_prime.png',8,bg=(224,224,224)).save('mr_prime_8x.png')
