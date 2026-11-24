# r4: mr_prime.png (64x64, geindexeerd, index 0 transparant), ogen_vel.png (V1-V5, ringen R1/R2) en vel.png.
import sys, numpy as np, bouw, ogen; from PIL import Image, ImageDraw; from toon import rgb, PAL
KEUZE=('V4','R1')   # wat volgens de maker het best leest; Jordi kiest het oog
BG=(152,208,160)
def png(C,path):
    im=Image.fromarray((C+1).astype('uint8'),'P')
    pal=list(BG)+sum([[t,t,t] for t in PAL],[]); pal+= [0,0,0]*(256-len(pal)//3)
    im.putpalette(pal); im.save(path,transparency=0)
def groot(C,z,bg=BG,pal=PAL):
    img=np.zeros(C.shape+(3,),'uint8'); img[:]=bg
    for i,t in enumerate(pal): img[C==i]=t
    return Image.fromarray(img).resize((C.shape[1]*z,C.shape[0]*z),0)
def model(z,box=(0,0,64,64),bron='natief.png'):
    n=Image.open(bron).convert('RGB'); s=z/2.5
    big=n.resize((int(199*s),int(199*s)),Image.LANCZOS)
    W=Image.new('RGB',(64*z,64*z),(255,255,255)); W.paste(big,(int(-7*s),int((-25+3*2.5)*s)))
    return W.crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))
def blad(rows,titels,path):
    pad=12; Wd=max(sum(i.width+pad for i in r) for r in rows); Ht=sum(max(i.height for i in r)+26 for r in rows)
    V=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(V); y=0
    for t,r in zip(titels,rows):
        d.text((4,y+7),t,fill=(0,0,0)); y+=26; x=0
        for i in r: V.paste(i,(x,y)); x+=i.width+pad
        y+=max(i.height for i in r)
    V.save(path)
log0={}; B=bouw.bouw('B','E2r3',log=log0)
S={}; logs={}
for v in ('V1','V2','V3','V4','V5'):
    for r in ('R1','R2'):
        logs[(v,r)]={}; S[(v,r)]=ogen.maak(B,v,r,logs[(v,r)])
C=S[KEUZE]; png(C,'mr_prime.png')
for k,c in S.items(): png(c,'variant_%s_%s.png'%k)
kb=(22,3,50,27); kz=12
namen={'V1':'V1 Mr. Mime-oog','V2':'V1 + Hitmonchan-lid','V3':'V3 Hitmonchan-oog compleet','V4':'V4 Mewtwo-oog','V5':'V5 Rime-oog + lid'}
rows=[]; tit=[]
for v in ('V1','V2','V3','V4','V5'):
    c=S[(v,'R1')]
    rows.append([groot(c[kb[1]:kb[3],kb[0]:kb[2]],kz), groot(c,2,(232,236,240)), groot(c,1,(232,236,240)), groot(c,1,(40,44,52))])
    tit.append(namen[v]+' (ring R1): kop 12x | 2x | 1x licht | 1x donker')
for r,n in (('R1','R1 Magnemite-oogomtrek'),('R2','R2 modelring factor 2.3')):
    c=S[(KEUZE[0],r)]
    rows.append([groot(c[kb[1]:kb[3],kb[0]:kb[2]],kz), groot(c,2,(232,236,240)), groot(c,1,(232,236,240)), groot(c,1,(40,44,52))])
    tit.append('ring %s op %s: kop 12x | 2x | 1x licht | 1x donker'%(n,KEUZE[0]))
blad(rows,tit,'ogen_vel.png')
r3=np.asarray(Image.open('../sprite_r3/mr_prime.png')).astype(int)-1
P3=[16,48,80,112,112,144,208,248]
rij1=[groot(C,8),groot(r3,8,pal=P3),model(8)]
kop=[groot(C[2:30,18:64],12),groot(r3[2:30,18:64],12,pal=P3),model(12,(18,2,64,30))]
een=[groot(C,1,(232,236,240)),groot(C,1,(40,44,52)),groot(C,2,(232,236,240)),groot(C,2,(40,44,52))]
blad([rij1,kop,een],['r4 (%s, %s) 8x | r3 8x | model r9'%KEUZE,'kop 12x: r4 | r3 | model r9','1x en 2x op licht en donker'],'vel.png')
P=np.asarray(Image.open('mr_prime.png'))
print('kleuren (incl. transparant)',len(np.unique(P)))
for k,v in logs.items(): print(k,v)
