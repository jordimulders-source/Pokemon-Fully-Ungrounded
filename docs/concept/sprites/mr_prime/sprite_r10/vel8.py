import sys; sys.path.insert(0,'.')
import numpy as np; from PIL import Image, ImageDraw
exec(open('r7.py').read())
exec(open('r8.py').read())
BG=(152,208,160)
def png(C,path):
    im=Image.fromarray(C.astype('uint8'),'P'); pal=sum([list(p) for p in PAL],[]); pal+=[0]*(768-len(pal))
    im.putpalette(pal); im.save(path,transparency=0)
png(C,'mr_prime.png'); png(R7,'r7_uit.png')
print('pixels gewijzigd t.o.v. r7:',int((C!=R7).sum()))
for k,v in LOG.items(): print(v,k)
def rgbgroot(path,z,box=None,bg=BG,rows=64):
    im=Image.open(path).convert('RGBA'); im=im.crop((0,0,im.width,min(im.height,rows)))
    W=Image.new('RGBA',im.size,bg+(255,)); W.alpha_composite(im); im=W.convert('RGB')
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
R8,R7P,RIMEP,MIME='mr_prime.png','r7_uit.png',G%'mr_rime/front',G%'mr_mime/anim_front_gba'
ALPH='../../mightyena_evo/af/alphyena.png'
L,D=(232,236,240),(40,44,52)
rows=[[rgbgroot(R8,8),rgbgroot(R7P,8),model(8)],
      [rgbgroot(R8,12,(18,0,52,28)),rgbgroot(R7P,12,(18,0,52,28))],
      [rgbgroot(R8,12,(0,13,26,42)),rgbgroot(R7P,12,(0,13,26,42)),model(12,(0,13,26,42))],
      [rgbgroot(R8,12,(10,3,34,21)),rgbgroot(R7P,12,(10,3,34,21)),rgbgroot(RIMEP,12,(3,6,27,24))],
      [rgbgroot(R8,1,bg=L),rgbgroot(R8,1,bg=D),rgbgroot(R8,2,bg=L),rgbgroot(R8,2,bg=D),
       rgbgroot(ALPH,1,bg=L),rgbgroot(ALPH,1,bg=D),rgbgroot(ALPH,2,bg=L),rgbgroot(ALPH,2,bg=D),
       rgbgroot(MIME,1,bg=L),rgbgroot(MIME,1,bg=D),rgbgroot(MIME,2,bg=L),rgbgroot(MIME,2,bg=D)]]
tit=['r8 8x | r7 8x | model r9',
     'kop 12x: r8 | r7',
     'stok + hand 12x: r8 | r7 | model',
     'linkerhaar 12x: r8 | r7 | Mr. Rime (zelfde uitsnede, verschuiving (+7,-3))',
     '1x en 2x op licht en donker: r8 | Alphyena | Gen 3 Mr. Mime']
blad(rows,tit,'vel.png')
