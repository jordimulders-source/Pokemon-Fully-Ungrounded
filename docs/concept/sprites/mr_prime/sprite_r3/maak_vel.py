# r3: levert mr_prime.png (64x64, geindexeerd, index 0 transparant) en vel.png.
import numpy as np, bouw; from PIL import Image, ImageDraw; from toon import rgb, PAL
KEUZE=('B','E2r3')
BG=(152,208,160)
def png(C,path):
    C=C.copy(); C[C==4]=3          # selout 112 en pak 112 zijn dezelfde kleur: 1 paletplek
    im=Image.fromarray((C+1).astype('uint8'),'P')
    pal=list(BG)+sum([[t,t,t] for t in PAL],[]); pal+= [0,0,0]*(256-len(pal)//3)
    im.putpalette(pal); im.save(path,transparency=0)
def groot(C,z,bg=BG,pal=None):
    img=rgb(C,bg) if pal is None else pal(C,bg)
    return Image.fromarray(img).resize((C.shape[1]*z,C.shape[0]*z),0)
def rgb_r2(C,bg):
    P=[16,48,64,80,112,144,208,248]; img=np.zeros(C.shape+(3,),'uint8'); img[:]=bg
    for i,t in enumerate(P): img[C==i]=t
    return img
def model(z,box=(0,0,64,64),bron='natief.png'):
    n=Image.open(bron).convert('RGB'); s=z/2.5
    big=n.resize((int(199*s),int(199*s)),Image.LANCZOS)
    ox=-7*s+0; oy=(-25+3*2.5)*s
    W=Image.new('RGB',(64*z,64*z),(255,255,255)); W.paste(big,(int(ox),int(oy)))
    return W.crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))
log={}; C=bouw.bouw(*KEUZE,log=log); png(C,'mr_prime.png')
r2=np.asarray(Image.open('../sprite_r2/variant_hoedB_E2.png')).astype(int)-1
z=8; pad=12
rij1=[groot(C,z),groot(r2,z,pal=rgb_r2),model(z)]
kz=12; kb=(18,0,64,30)
kop=[groot(C[kb[1]:kb[3],kb[0]:kb[2]],kz),groot(r2[kb[1]:kb[3],kb[0]:kb[2]],kz,pal=rgb_r2),model(kz,kb)]
een=[groot(C,1,(232,236,240)),groot(C,1,(40,44,52)),groot(C,2,(232,236,240)),groot(C,2,(40,44,52))]
Wd=max(sum(i.width for i in r)+pad*len(r) for r in (rij1,kop,een))
rows=[rij1,kop,een]
Ht=sum(max(i.height for i in r)+30 for r in rows)
V=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(V); y=0
titels=['r3 (hoed B, oog E2) 8x | r2 (B, E2) 8x | model r9 verkleind',
        'kop 12x: r3 | r2 | model r9',
        '1x en 2x op licht en donker']
for t,r in zip(titels,rows):
    d.text((4,y+8),t,fill=(0,0,0)); y+=30; x=0
    for i in r: V.paste(i,(x,y)); x+=i.width+pad
    y+=max(i.height for i in r)
V.save('vel.png')
P=np.asarray(Image.open('mr_prime.png'))
print('kleuren (incl. transparant)',len(np.unique(P)),'maat x',[int(v) for v in (np.where((C>=0).any(0))[0][[0,-1]])],'y',[int(v) for v in np.where((C>=0).any(1))[0][[0,-1]]])
for k,v in log.items(): print(' ',k,v)
