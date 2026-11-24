# r6: mr_prime.png (64x64, geindexeerd, index 0 transparant) + vel.png
import numpy as np, r6 as r5, palet; from PIL import Image, ImageDraw
BG=(152,208,160); KEUZE='B'
def png(C,path):
    im=Image.fromarray((C+1).astype('uint8'),'P')
    pal=list(BG)+sum([list(t) for t in palet.PAL5],[]); pal+=[0,0,0]*(256-len(pal)//3)
    im.putpalette(pal); im.save(path,transparency=0)
def groot(C,z,bg=BG):
    return Image.fromarray(palet.rgb(C,bg)).resize((C.shape[1]*z,C.shape[0]*z),0)
def rgbgroot(path,z,box=None,bg=BG):
    im=Image.open(path).convert('RGBA'); W=Image.new('RGBA',im.size,bg+(255,)); W.alpha_composite(im); im=W.convert('RGB')
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),0)
def r4(z,box=None,bg=BG):   # r6: toont r5
    P=np.asarray(Image.open('../sprite_r5/mr_prime.png').convert('RGB'))
    T=np.asarray(Image.open('../sprite_r5/mr_prime.png')); img=P.copy(); img[T==0]=bg
    im=Image.fromarray(img)
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),0)
def model(z,box=(0,0,64,64)):
    n=Image.open('natief.png').convert('RGB'); s=z/2.5
    big=n.resize((int(199*s),int(199*s)),Image.LANCZOS)
    W=Image.new('RGB',(64*z,64*z),(255,255,255)); W.paste(big,(int(-7*s),int(-17.5*s)))
    return W.crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))
def blad(rows,titels,path):
    pad=12; Wd=max(sum(i.width+pad for i in r) for r in rows); Ht=sum(max(i.height for i in r)+26 for r in rows)
    V=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(V); y=0
    for t,r in zip(titels,rows):
        d.text((4,y+7),t,fill=(0,0,0)); y+=26; x=0
        for i in r: V.paste(i,(x,y)); x+=i.width+pad
        y+=max(i.height for i in r)
    V.save(path)
log={}; C=r5.maak(KEUZE,log); png(C,'mr_prime.png')
L,D=(232,236,240),(40,44,52)
kb=(18,0,58,28)
rime=rgbgroot('../../../../../graphics/pokemon/mr_rime/front.png',12,(12,0,52,28))
rows=[[groot(C,8),r4(8),model(8)],
      [groot(C[kb[1]:kb[3],kb[0]:kb[2]],12),r4(12,kb),model(12,kb),rime],
      [groot(C[8:44,0:26],12),r4(12,(0,8,26,44)),model(12,(0,8,26,44))],
      [groot(C[2:24,12:36],12),r4(12,(12,2,36,24)),rgbgroot('../../../../../graphics/pokemon/mr_rime/front.png',12,(1,5,25,27))],
      [groot(C,1,L),groot(C,1,D),groot(C,2,L),groot(C,2,D),r4(1,bg=L),r4(1,bg=D),
       rgbgroot('../../mightyena_evo/af/alphyena.png',1,bg=L),rgbgroot('../../mightyena_evo/af/alphyena.png',1,bg=D),
       rgbgroot('../../mightyena_evo/af/alphyena.png',2,bg=L),rgbgroot('../../mightyena_evo/af/alphyena.png',2,bg=D)]]
tit=['r6 8x | r5 8x | model r9',
     'kop 12x: r6 | r5 | model r9 | Mr. Rime (front.png)',
     'stok 12x: r6 | r5 | model r9',
     'aansluiting linkerhaar 12x: r6 | r5 | Mr. Rime',
     '1x en 2x op licht en donker: r6 | r5 1x | Alphyena 1x en 2x']
blad(rows,tit,'vel.png')
P=np.asarray(Image.open('mr_prime.png')); ys,xs=np.where(P>0)
print('kleuren (incl. transparant)',len(np.unique(P)),'bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
for k,v in sorted(log.items()): print(v,k)
