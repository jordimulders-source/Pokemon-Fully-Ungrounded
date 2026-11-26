import numpy as np; from PIL import Image, ImageDraw; import maak_r5 as m, maak_r2 as m2, kijk
R='r5/'
lab=m.bouw_sprite(); m2.label_png(lab,R+'zandloper_fase3.png'); im=Image.open(R+'zandloper_fase3.png')
assert im.size==(64,64) and im.mode=='P'; print(len(np.unique(np.asarray(im))),'kleuren',{k:len(v) for k,v in m.LOG.items()})
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
A=im; B=Image.open('r4/H2.png')
c=Image.new('RGB',(3*520,20+512+130+360),'white')
for i,(x,t) in enumerate([(kijk.op_wit(A,8),'r5'),(kijk.op_wit(B,8),'r4 H2'),(kijk.model64().resize((512,512),Image.NEAREST),'model r5 verkleind')]):
    c.paste(x,(i*520,20)); tekst(c,(i*520+4,4),t)
y=545
for i,(x,t) in enumerate([(A,'r5'),(B,'r4 H2')]):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
    tekst(c,(i*300,y),t+' 1x')
c.paste(kijk.model64(),(620,y+14)); tekst(c,(620,y),'model 1x')
y=665
c.paste(kijk.op_wit(A,12).crop((14*12,0,46*12,26*12)),(0,y+14)); tekst(c,(0,y),'r5 hoofd 12x')
c.paste(kijk.op_wit(B,12).crop((14*12,0,46*12,26*12)),(400,y+14)); tekst(c,(400,y),'r4 H2 hoofd 12x')
c.paste(kijk.op_wit(A,12).crop((6*12,14*12,50*12,36*12)).resize((396,198),Image.NEAREST),(800,y+14)); tekst(c,(800,y),'r5 armen/schouders (6x)')
c.paste(kijk.model64().crop((6,14,50,36)).resize((396,198),Image.NEAREST),(1200,y+14)); tekst(c,(1200,y),'model armen (6x)')
c.save(R+'vel.png')
