# Levert mr_prime.png (64x64, geindexeerd, index 0 transparant), varianten en vel.png.
import numpy as np, bouw; from PIL import Image, ImageDraw; from toon import rgb, PAL
KEUZE=('B','E1')
BG=(152,208,160)
def png(C,path):
    im=Image.fromarray((C+1).astype('uint8'),'P')
    pal=list(BG)+sum([[t,t,t] for t in PAL],[]); pal+= [0,0,0]*(256-len(pal)//3)
    im.putpalette(pal); im.save(path,transparency=0)
def groot(C,z,bg=BG): return Image.fromarray(rgb(C,bg)).resize((C.shape[1]*z,C.shape[0]*z),0)
def model(z,box=(0,0,64,64),bron='natief.png'):
    n=Image.open(bron).convert('RGB'); s=z/2.5
    big=n.resize((int(199*s),int(199*s)),Image.LANCZOS)
    ox=-7*s+0; oy=(-25+3*2.5)*s
    W=Image.new('RGB',(64*z,64*z),(255,255,255)); W.paste(big,(int(ox),int(oy)))
    return W.crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))
logs={}
S={}
for hv in 'AB':
    for ov in ('E1','E2','E3'):
        log={}; S[(hv,ov)]=bouw.bouw(hv,ov,log); logs[(hv,ov)]=log
C=S[KEUZE]; png(C,'mr_prime.png')
for (hv,ov),c in S.items(): png(c,'variant_hoed%s_%s.png'%(hv,ov))
kaal=np.full((64,64),-1); kaal[3:64]=np.load('kaal_idx.npy')[:61]
# vel
F=lambda t: None
z=8; pad=12
r1=np.asarray(Image.open('../sprite_r1/mr_prime.png')).astype(int)-1
rij1=[groot(C,z),groot(r1,z),groot(kaal,z),model(z)]
kz=12; kb=(18,2,62,30)
kop=[groot(C[kb[1]:kb[3],kb[0]:kb[2]],kz),groot(r1[kb[1]:kb[3],kb[0]:kb[2]],kz),model(kz,kb)]
var_h=[groot(S[('A',KEUZE[1])],z),groot(S[('B',KEUZE[1])],z)]
oz=12; ob=(22,10,50,28)
var_o=[groot(S[(KEUZE[0],o)][ob[1]:ob[3],ob[0]:ob[2]],oz) for o in ('E1','E2','E3')]
een=[groot(C,1,(232,236,240)),groot(C,1,(40,44,52)),groot(C,2,(232,236,240)),groot(C,2,(40,44,52))]
Wd=max(sum(i.width for i in rij1)+pad*2, sum(i.width for i in kop)+pad, sum(i.width for i in var_o)+pad*2)
rows=[rij1,kop,var_h+een,var_o]
Ht=sum(max(i.height for i in r)+30 for r in rows)
V=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(V); y=0
titels=['r2 (hoed B, oog E1) 8x | r1 8x | kale reductie r2 8x | model r9 verkleind',
        'kop 12x: r2 | r1 | model r9',
        'hoed A | hoed B (8x)   |   1x en 2x op licht en donker',
        'ogen 12x: E1 modeloog (kale reductie) | E2 E1 + Hitmonchan-lid | E3 Rime-oog + Hitmonchan-lid']
for t,r in zip(titels,rows):
    d.text((4,y+8),t,fill=(0,0,0)); y+=30; x=0
    for i in r: V.paste(i,(x,y)); x+=i.width+pad
    y+=max(i.height for i in r)
V.save('vel.png')
print('kleuren',len(np.unique(C)),'maat', [int(v) for v in (np.where((C>=0).any(0))[0][[0,-1]])], [int(v) for v in np.where((C>=0).any(1))[0][[0,-1]]])
for k,v in logs.items(): print(k,v)
