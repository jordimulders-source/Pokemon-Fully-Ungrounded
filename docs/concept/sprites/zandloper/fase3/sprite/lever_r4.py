import numpy as np; from PIL import Image, ImageDraw; import maak_r4 as m, maak_r2 as m2, kijk, hoofd, bewerk
z=np.zeros((201,201),bool)
for y,(l,r) in bewerk.HOOFD.items(): z[y,l:r+1]=True
hoofd.BREIN=z
R='r4/'; V=[('H1',1.15),('H2',1.25),('H3',1.35)]
for n,s in V:
    lab=m.bouw_sprite(s); m2.label_png(lab,R+n+'.png'); im=Image.open(R+n+'.png'); assert im.size==(64,64)
    print(n,len(np.unique(np.asarray(im))),'kleuren',{k:len(v) for k,v in m.LOG.items()})
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
ims=[(Image.open(R+n+'.png'),'%s (hoofd %.2fx)'%(n,s)) for n,s in V]+[(Image.open('r3/zandloper_fase3_B.png'),'r3')]
c=Image.new('RGB',(5*520,20+512+130+330),'white')
for i,(im,t) in enumerate(ims): c.paste(kijk.op_wit(im,8),(i*520,20)); tekst(c,(i*520+4,4),t)
c.paste(kijk.model64().resize((512,512),Image.NEAREST),(4*520,20)); tekst(c,(4*520+4,4),'model r5 verkleind')
y=545
for i,(im,t) in enumerate(ims):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
    tekst(c,(i*300,y),t+' 1x')
y=665
for i,(im,t) in enumerate(ims):
    c.paste(kijk.op_wit(im,12).crop((14*12,0,46*12,26*12)),(i*400,y+14)); tekst(c,(i*400,y),t+' hoofd 12x')
c.save(R+'vel.png')
