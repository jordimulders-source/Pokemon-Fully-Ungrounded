import sys; sys.path.insert(0,'.')
import numpy as np; from PIL import Image, ImageDraw
exec(open('r7.py').read())
exec(open('r8.py').read())
exec(open('r9.py').read())
exec(open('r10.py').read())
exec(open('r11.py').read())
BG=(152,208,160)
def png(C,path):
    im=Image.fromarray(C.astype('uint8'),'P'); pal=sum([list(p) for p in PAL],[]); pal+=[0]*(768-len(pal))
    im.putpalette(pal); im.save(path,transparency=0)
png(C,'mr_prime.png'); png(R10,'r10_uit.png')
print('pixels gewijzigd t.o.v. r10:',int((C!=R10).sum()))
for k,v in LOG.items(): print(v,k)
# variant_monocle: r11 (haar, snor) met de ogen van r10 terug (monoclering met glasgat om het nabije oog)
V=C.copy(); V[14:21,29:43]=R10[14:21,29:43]; V[20,41]=C[20,41]; png(V,'variant_monocle.png')   # ogen van r10 (monocle, verre oog zonder ring)
print('variant_monocle: pixels anders dan r11:',int((V!=C).sum()))
def rgbgroot(path,z,box=None,bg=BG):
    im=Image.open(path).convert('RGBA'); W=Image.new('RGBA',im.size,bg+(255,)); W.alpha_composite(im); im=W.convert('RGB')
    if box: im=im.crop(box)
    return im.resize((im.width*z,im.height*z),0)
def model(z,box=(0,0,64,64)):
    n=Image.open('natief.png').convert('RGB'); s=z/2.5
    big=n.resize((int(199*s),int(199*s)),Image.LANCZOS)
    W=Image.new('RGB',(64*z,64*z),(255,255,255)); W.paste(big,(int(-7*s),int(-17.5*s)))
    return W.crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z))
RIMEV=Image.open(G%'mr_rime/front').convert('RGBA'); RS=Image.new('RGBA',(64,64),(0,0,0,0)); RS.alpha_composite(RIMEV,(7,-3))
def rime12(box):
    W=Image.new('RGBA',(64,64),BG+(255,)); W.alpha_composite(RS); im=W.convert('RGB').crop(box); return im.resize((im.width*12,im.height*12),0)
def blad(rows,titels,path):
    pad=12; Wd=max(sum(i.width+pad for i in r) for r in rows); Ht=sum(max(i.height for i in r)+26 for r in rows)
    Vb=Image.new('RGB',(Wd,Ht),(255,255,255)); d=ImageDraw.Draw(Vb); y=0
    for t,r in zip(titels,rows):
        d.text((4,y+7),t,fill=(0,0,0)); y+=26; x=0
        for i in r: Vb.paste(i,(x,y)); x+=i.width+pad
        y+=max(i.height for i in r)
    Vb.save(path)
A,AV,A10,A9='mr_prime.png','variant_monocle.png','r10_uit.png','../sprite_r9/mr_prime.png'
MIME=G%'mr_mime/anim_front_gba'
L,D=(232,236,240),(40,44,52)
KOP=(18,0,52,28); HAAR=(11,3,36,17); SNOR=(22,18,46,28)
rows=[[rgbgroot(A,8),rgbgroot(A10,8),model(8)],
      [rgbgroot(A,12,KOP),rgbgroot(AV,12,KOP),rgbgroot(A10,12,KOP),model(12,(18,3,52,31))],
      [rgbgroot(A,12,HAAR),rime12(HAAR),rgbgroot(A10,12,HAAR)],
      [rgbgroot(A,12,SNOR),rgbgroot(A9,12,SNOR),rgbgroot(A10,12,SNOR),model(12,SNOR)],
      [rgbgroot(A,1,bg=L),rgbgroot(A,1,bg=D),rgbgroot(A,2,bg=L),rgbgroot(A,2,bg=D),
       rgbgroot(AV,1,bg=L),rgbgroot(AV,2,bg=L),rgbgroot(A10,1,bg=L),rgbgroot(A10,2,bg=L),
       rgbgroot(MIME,1,(0,0,64,64),bg=L),rgbgroot(MIME,2,(0,0,64,64),bg=L)]]
tit=['r11 8x | r10 8x | model r9',
     'kop 12x: r11 | variant_monocle | r10 | model (modeluitsnede 3 rijen lager: voorhoofd +2 in de sprite)',
     'linkerhaar 12x: r11 | Mr. Rime op de hoedverschuiving (+7,-3) | r10',
     'snor 12x: r11 | r9 | r10 | model (zelfde uitsnede)',
     '1x en 2x: r11 licht/donker | variant_monocle | r10 | Gen 3 Mr. Mime']
blad(rows,tit,'vel.png')
rgbgroot(A,8,bg=(224,224,224)).save('mr_prime_8x.png')
