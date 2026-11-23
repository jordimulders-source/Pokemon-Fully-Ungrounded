# Ronde 5 (2 ogen): ogen + neus naar de posities uit Gemini r7 (gemeten t.o.v. de kop), rode lijn uit r7 die doorgolft,
# losse/vage rode resten weg, vrijgekomen plekken = kopsteen/cracks uit de sprite zelf (blokken verschoven, niets gemiddeld).
import os, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
U=np.array(Image.open(os.path.join(H,'../r4/claydol_2ogen_U5.png'))).astype(int)
PAL=Image.open(os.path.join(H,'../r4/claydol_2ogen_U5.png')).getpalette()
RED=(8,9)

# ---- zone die mag veranderen (kopvlak); alles erbuiten diff 0 ----
Z=np.zeros((64,64),bool)
Z[12:31,11:51]=True; Z[31,13:48]=True
Z[9:12,19:43]=True                                  # voorhoofd tussen de bovenste kransbolletjes
for p in [(10,43),(10,44),(11,44),(11,18),(12,17)]: Z[p]=True   # losse rode restjes aan de bolletjes
Z[16:20,50]=False                                   # donkere koprand rechts
Z&=(U!=7)                                           # buitenlijnen blijven

# ---- de assets (oude kolommen) ----
OOG_L=list(range(15,27)); NEUS=list(range(27,32)); OOG_R=list(range(32,44))
RIJ0,RIJ1=18,31          # assets: 2 rijen steen boven de oogring t/m onderkant

def kolommap(I):
    """nieuwe kolom -> oude kolom voor de band met ogen+neus"""
    if I=='I1':   # middelpunten exact r7: oog L -4, oog R -6; de twee gelijke middenkolommen van de neus (29, 30: toon 4) vervallen
        src=list(range(15,27))+[27,28,31]+list(range(32,44)); x0=11
    else:         # I2: hele blok -4 (afstand ogen ongewijzigd, rechteroog 2 px rechts van r7)
        src=list(range(15,44)); x0=11
    return {x0+i:s for i,s in enumerate(src)}

# ---- rode lijn uit r7 (cellen met >50% rood op het 16px-raster), in onze dikte/tinten ----
R7=[(16,x) for x in range(15,19)]+[(17,x) for x in range(14,20)]+[(18,13),(18,14),(18,18),(18,19),(18,20),(19,13),(19,19),(19,20),
    (20,20),(20,21),(21,21),(21,22),(22,22),(22,23),(22,24),(23,22),(23,23),
    (21,24),(21,25),(20,25),(20,26),(19,26),(19,27),(18,27),(18,28)]+[(17,x) for x in range(28,35)]+[(16,x) for x in range(29,34)]+[
    (18,34),(18,35),(19,35),(19,36),(20,36),(20,37),(21,37)]
def golf(v):
    """doorgolven na boog 2: V2 + boog 3. A = boog 3 = boog 2 verschoven (+15 kol), door de koprand afgesneden;
       B = boog 3 verkort (perspectief: smaller, 1 rij lager) met de daling tot aan de rand"""
    V2=[(22,37),(22,38),(22,39),(23,37),(23,38),(21,39),(21,40),(20,40),(20,41),(19,41),(19,42),(18,42),(18,43)]
    if v=='A':
        top=[(17,x) for x in range(43,50)]+[(16,x) for x in range(44,49)]+[(18,49),(18,50),(19,50)]
    else:
        top=[(17,x) for x in range(43,47)]+[(16,x) for x in range(44,46)]+[(18,47),(18,48),(19,48),(19,49),(20,49),(20,50),(21,50)]
    return V2+top

def lijnpix(v):
    L=[p for p in R7+golf(v) if Z[p] or U[p] in RED]
    L=sorted(set(L)); S=set(L)
    # tinten: bovenste rij van een boog donkerrood 9, rij eronder (met rood erboven) lichtrood 8 zoals de bestaande lijn
    return {p:(8 if ((p[0]-1,p[1]) in S and (p[0]-2,p[1]) not in S and p[0] in (17,) and (p[0],p[1]-1) in S and (p[0],p[1]+1) in S) else 9) for p in L}

def bouw(I='I1', v='A', roff=-2):
    S=U.copy(); bron={}
    km=kolommap(I)
    # 1. band rij 18-31: ogen+neus als assets op de nieuwe kolommen
    for y in range(RIJ0,RIJ1+1):
        for x,s in km.items():
            if Z[y,x] and U[y,s]!=7: S[y,x]=U[y,s]; bron[(y,x)]='asset'
    # 2. vrijgekomen strook rechts van het rechteroog: rechterkopsteen ernaast (kol +dx), 2 rijen hoger (cracks niet op dezelfde hoogte)
    xe=max(km)+1
    dx=44-xe
    for y in range(RIJ0,RIJ1+1):
        for x in range(xe,44):
            if Z[y,x]:
                sy=y+roff if y>=20 else y
                S[y,x]=U[sy,x+dx]; bron[(y,x)]='rechterkop'
    # 3. rood dat niet op de nieuwe lijn ligt -> steen; eerst steen in de nabije rij erboven (blokverschuiving -3 rijen), anders buur
    lp=lijnpix(v)
    T=S.copy()
    for (y,x) in sorted(zip(*np.where(Z & np.isin(S,RED)))):
        if (y,x) in lp: continue
        for dy,dx2 in [(-3,0),(-2,0),(-4,0),(0,-1),(0,1),(-1,0),(1,0),(0,-2),(0,2)]:
            sy,sx=y+dy,x+dx2
            if 0<=sy<64 and T[sy,sx] not in RED and T[sy,sx] not in (0,1,2,7):
                T[y,x]=T[sy,sx]; bron[(y,x)]='rood weg (%+d,%+d)'%(dy,dx2); break
    S=T
    # 4. binnenkant van de V boven de punt: neusrug (rij 20-21) -> steen van rij 18-19 erboven
    for (y,x) in [(20,22),(20,23),(20,24),(21,23)]:
        S[y,x]=S[y-2,x]; bron[(y,x)]='V-binnen'
    # 5. nieuwe lijn
    for p,c in lp.items(): S[p]=c; bron[p]='lijn'
    return S,bron

def check(S):
    assert ((S>0)==(U>0)).all(), 'silhouet'
    assert not ((S!=U)&~Z).any(), 'buiten zone'
    assert set(np.unique(S))<=set(range(10))

def save(S,pad,schaal=8):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((64*schaal,64*schaal),Image.NEAREST).save(pad+'_8x.png',transparency=0)
def rgba(S):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.info['transparency']=0; return im.convert('RGBA')

VAR={'I1A':('I1','A'),'I1B':('I1','B'),'I2A':('I2','A'),'I2B':('I2','B')}

# ---- levering: hoofdversie I1A + varianten, vel ----
MARK={'oog L':(16.5,25.5),'oog R':(31.5,25.5),'neus':(23.5,27.5)}   # r7-middelpunten op het 64-raster (r7 valt 1-op-1 op ons raster)
def vel():
    from PIL import ImageDraw
    hoofd,_=bouw('I1','A'); check(hoofd); save(hoofd,os.path.join(H,'claydol_2ogen_r5'))
    var={n:bouw(I,v)[0] for n,(I,v) in VAR.items()}
    for n,Sx in var.items(): check(Sx); save(Sx,os.path.join(H,'claydol_2ogen_r5_'+n))
    r7=Image.open(os.path.join(H,'../../gemini/claydol_r7_2ogen.png')).convert('RGBA').resize((512,512),Image.NEAREST)
    W=3*522+10; v=Image.new('RGBA',(W,16+512+12+16+27*12+12+90+16+4*0+300),(255,255,255,255)); d=ImageDraw.Draw(v)
    items=[('r5 (I1A, hoofdversie)',rgba(hoofd)),('U5 (r4)',rgba(U)),('Gemini r7 + gemeten oog/neus-middelpunten',r7)]
    for i,(t,im) in enumerate(items):
        x=10+i*522; d.text((x,3),t,fill='black')
        v.alpha_composite(im if im.size==(512,512) else im.resize((512,512),Image.NEAREST),(x,16))
        if i in (0,2):
            for k,(cx,cy) in MARK.items():
                X,Y=x+cx*8+4,16+cy*8+4; d.ellipse((X-6,Y-6,X+6,Y+6),outline=(0,120,255),width=2); d.text((X+8,Y-6),k,fill=(0,120,255))
    y=16+512+12; d.text((10,y),'kop 12x: r5 | U5',fill='black'); y+=16
    for i,S_ in enumerate([hoofd,U]):
        v.alpha_composite(rgba(S_).crop((8,7,56,34)).resize((48*12,27*12),Image.NEAREST),(10+i*(48*12+10),y))
    y+=27*12+12
    for i,S_ in enumerate([hoofd,U]):
        for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
            t=Image.new('RGBA',(80,80),bg); t.alpha_composite(rgba(S_),(8,8)); v.alpha_composite(t,(10+i*200+j*90,y))
    y+=96; d.text((10,y),'varianten 4x: I1A (= r5) | I1B (boog 3 verkort) | I2A (blok -4, afstand ogen gelijk) | I2B',fill='black'); y+=14
    for i,n in enumerate(VAR):
        v.alpha_composite(rgba(var[n]).resize((256,256),Image.NEAREST),(10+i*266,y)); d.text((10+i*266,y),n,fill='black')
    v=v.crop((0,0,W,y+260)); v.save(os.path.join(H,'vel.png'))
    return hoofd

if __name__=='__main__':
    for n,(I,v) in VAR.items():
        S,b=bouw(I,v); check(S); pass
        from collections import Counter
        print(n,'diff t.o.v. U5:',(S!=U).sum(), Counter(b[k].split(' (')[0] for k in b if S[k]!=U[k]))
    vel()
