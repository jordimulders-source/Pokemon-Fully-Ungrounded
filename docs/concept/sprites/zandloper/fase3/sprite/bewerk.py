# Bewerkt natief raster van r5: glaswerk achter de rug weg (alleen weghalen),
# fles + trechter uit r8 (zelfde schaal, gemeten aan torsobreedte 111 vs 108 natieve px) verschoven op de schouders.
import numpy as np; from PIL import Image; import materiaal as mt
R5=np.asarray(Image.open('natief_r5.png')).astype(int).copy()
R8=np.asarray(Image.open('natief_r8_5.png')).astype(int)
WIT=np.array([255,255,255])
def zonder_rugglas(a):
    a=a.copy()
    M,_=mt.kaart(a)
    # linker fles achter de schouder: niet-zand in x50-71, y33-57 weg
    for y in range(33,58):
        for x in range(48,72):
            if M[y,x] in (1,3): a[y,x]=WIT
    # rechts: alles rechts van de lijflijn (deltoïde-omlijning) weg
    rand={}
    for y in range(20,44): rand[y]=117
    for y in range(44,48): rand[y]=121
    for y in range(48,53): rand[y]=131
    for y in range(53,58): rand[y]=134
    for y in range(58,61): rand[y]=144
    for y in range(61,82): rand[y]=146
    for y in range(82,86): rand[y]=142
    for y in range(86,90): rand[y]=137
    for y in range(90,94): rand[y]=133
    for y in range(94,100): rand[y]=131
    for y in range(100,113): rand[y]=130
    for y,xm in rand.items(): a[y,xm+1:]=WIT
    # restjes glas/veer boven de schouder rechts (x>117, y<58) die niet op het lijf liggen
    for y in range(20,58):
        for x in range(119,150):
            if M[y,x] in (1,3) and y<48: a[y,x]=WIT
    for y in range(56,113):
        for x in range(139,160):
            if M[y,x]==3: a[y,x]=WIT
    return a
def asset_fles():
    m=np.zeros(R8.shape[:2],bool)
    for y in range(37,74):
        for x in range(49,78): m[y,x]=True
    return m
def asset_trechter():
    m=np.zeros(R8.shape[:2],bool)
    for y in range(31,50):
        for x in range(127,164): m[y,x]=True
    for y in range(50,58):
        for x in range(131,164): m[y,x]=True
    for y in range(58,74):
        for x in range(131,144): m[y,x]=True
    return m
M8,_=mt.kaart(R8)
def plak(a,mask,dx,dy):
    a=a.copy(); ys,xs=np.where(mask&(M8!=0))
    for y,x in zip(ys,xs):
        Y,X=y+dy,x+dx
        if 0<=Y<a.shape[0] and 0<=X<a.shape[1]: a[Y,X]=R8[y,x]
    return a
def maak(fles=(0,-14),trechter=(0,-8)):
    a=zonder_rugglas(R5)
    a=plak(a,asset_fles(),*fles); a=plak(a,asset_trechter(),*trechter)
    return a.astype('uint8')
if __name__=='__main__':
    Image.fromarray(zonder_rugglas(R5).astype('uint8')).save('/tmp/claude-0/kaal_r5.png')
    Image.fromarray(maak()).save('/tmp/claude-0/bew.png')

# --- variant A: hersenwindingen van r8 binnen de hoofdvorm van r5 (schaal 47/38 = 1,24, dichtstbijzijnde pixel) ---
HOOFD={}
for y in range(29,31): HOOFD[y]=(79,106)
for y in range(31,34): HOOFD[y]=(76,109)
for y in range(34,37): HOOFD[y]=(74,111)
for y in range(37,41): HOOFD[y]=(72,113)
for y in range(41,47): HOOFD[y]=(71,114)
def brein_r8(a,lijn=150):
    a=a.copy(); M8,L8=mt.kaart(R8); s=38/47
    for y,(l,r) in HOOFD.items():
        for x in range(l,r+1):
            X=int(round(80+(x-70)*s)); Y=int(round(37+(y-27)*s))
            if M8[Y,X]==0 or L8[Y,X]<55: continue   # r8-buitenlijn/achtergrond niet overnemen
            a[y,x]=R8[Y,X] if L8[Y,X]>=lijn else (110,81,29)   # r8-winding (bruine lijn) krijgt de lijntint S0
    return a.astype('uint8')
