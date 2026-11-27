import numpy as np; from PIL import Image, ImageDraw; import maak_r7 as m7, maak_r6 as m, kijk
from lever_r6 import png, tekst
R='r7/'
A,log=m7.bouw(); im=png(A,R+'zandloper_fase3.png'); W1=Image.open('r6/zandloper_fase3_W1.png')
Z=np.zeros((64,64),bool); Z[0:23,18:42]=True; Z[15:34,10:24]=True
print(len(np.unique(A)),'kleuren; diff met r5:',int((A!=m.R5).sum()),'px; buiten zones:',int(((A!=m.R5)&~Z).sum()))
with open(R+'log.txt','w') as f:
    for k,v in log.items(): f.write('%s %d %s\n'%(k,len(v),v))
def model_crop(x0s,y0s,x1s,y1s,s):
    a=Image.open('../gemini/r5.webp').convert('RGB'); x0=(0*3+2)*5.12-0.12; y0=(2*3+2)*5.12-0.12; p=15.36
    return a.crop((int(x0+x0s*p),int(y0+y0s*p),int(x0+x1s*p),int(y0+y1s*p))).resize(((x1s-x0s)*s,(y1s-y0s)*s),Image.LANCZOS)
c=Image.new('RGB',(3*520,20+512+110+300+290),'white')
for i,(x,t) in enumerate([(kijk.op_wit(im,8),'r7'),(kijk.op_wit(W1,8),'r6 W1'),(kijk.model64().resize((512,512),Image.NEAREST),'model r5')]):
    c.paste(x,(i*520,20)); tekst(c,(i*520+4,4),t)
y=545
for i,(x,t) in enumerate([(im,'r7'),(W1,'r6 W1')]):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
    tekst(c,(i*300,y),t+' 1x licht/donker')
y=650
for i,(x,t) in enumerate([(im,'r7 hoofd 12x'),(W1,'r6 W1 hoofd 12x')]):
    c.paste(kijk.op_wit(x,12).crop((17*12,0,43*12,23*12)),(i*330,y+14)); tekst(c,(i*330,y),t)
c.paste(Image.open('../gemini/r8.png').convert('RGB').crop((395,130,610,330)).resize((312,276),Image.LANCZOS),(660,y+14)); tekst(c,(660,y),'r8-hoofd (model)')
c.paste(model_crop(19,0,45,23,12),(990,y+14)); tekst(c,(990,y),'r5-model (lijfschaal, hoofd is 1,25x)')
y=950
c.paste(kijk.op_wit(im,12).crop((9*12,14*12,26*12,35*12)),(0,y+14)); tekst(c,(0,y),'r7 linkerarm 12x')
c.paste(kijk.op_wit(W1,12).crop((9*12,14*12,26*12,35*12)),(220,y+14)); tekst(c,(220,y),'r6 W1')
c.paste(model_crop(9,14,26,35,12),(440,y+14)); tekst(c,(440,y),'model')
c=c.crop((0,0,c.width,y+14+252+10)); c.save(R+'vel.png')
# overlay: ogen (sprite 12x naast r8-oogdeel op dezelfde schaal) en arm (spritelijnen over het model)
o=Image.new('RGB',(1100,640),'white')
o.paste(kijk.op_wit(im,12).crop((20*12,13*12,35*12,21*12)),(0,20)); tekst(o,(0,4),'r7 ogen 12x')
b8=Image.open('../gemini/r8.png').convert('RGB').crop((412,264,532,328)); o.paste(b8.resize((180,96),Image.NEAREST),(200,20)) if False else None
o.paste(b8.resize((int(120*12/8),int(64*12/8)),Image.LANCZOS),(200,20)); tekst(o,(200,4),'r8-oogdeel, zelfde schaal (8 modelpx = 1 spritepx)')
mm=model_crop(9,14,26,35,24); d=ImageDraw.Draw(mm)
for yy in range(14,35):
    for xx in range(9,26):
        v=A[yy,xx]; px=(xx-9)*24; py=(yy-14)*24
        if v in (1,2): d.rectangle([px+5,py+5,px+18,py+18],outline=(255,0,0) if v==1 else (0,0,255),width=2)
        if v==7: d.rectangle([px+8,py+8,px+15,py+15],outline=(0,200,0),width=2)
o2=Image.new('RGB',(max(o.width,mm.width+10),140+mm.height+20),'white'); o2.paste(o.crop((0,0,o.width,130)),(0,0))
o2.paste(mm,(0,150)); tekst(o2,(0,134),'linkerarm: r7-lijnen (blauw = selout/binnenlijn, rood = zwart, groen = glasomlijning) over het r5-model, 24x')
o2.save(R+'overlay_arm_ogen.png')
