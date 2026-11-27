import numpy as np; from PIL import Image, ImageDraw; import maak_r3 as m, maak_r2 as m2, kijk
R='r3/'
V=[('zandloper_fase3_B','i'),('ogen_ii_graveler','ii'),('ogen_iii_geodude','iii')]
logs={}
for n,o in V:
    lab=m.bouw_sprite(o); logs[n]={k:len(v) for k,v in m.LOG.items()}
    m2.label_png(lab,R+n+'.png'); im=Image.open(R+n+'.png'); assert im.size==(64,64) and im.mode=='P'
    print(n,len(np.unique(np.asarray(im))),'kleuren', logs[n])
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
B3=Image.open(R+'zandloper_fase3_B.png'); B2=Image.open('r2/zandloper_fase3_B.png')
c=Image.new('RGB',(3*520,20+512+130+300),'white')
for i,(im,t) in enumerate([(kijk.op_wit(B3,8),'r3 (B, ogen i)'),(kijk.op_wit(B2,8),'r2 (B, gezicht b)'),(kijk.model64().resize((512,512),Image.NEAREST),'model r5 verkleind')]):
    c.paste(im,(i*520,20)); tekst(c,(i*520+4,4),t)
y=545
for i,(im,t) in enumerate([(B3,'r3'),(B2,'r2')]):
    for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
    tekst(c,(i*300,y),t+' op 1x')
c.paste(kijk.model64(),(620,y+14)); tekst(c,(620,y),'model 1x')
y=665
for i,(im,t) in enumerate([(B3,'r3 hoofd 12x'),(B2,'r2 hoofd 12x')]):
    c.paste(kijk.op_wit(im,12).crop((18*12,0,42*12,22*12)),(i*300,y+14)); tekst(c,(i*300,y),t)
c.save(R+'vel.png')
lbl=['(i) r8-ogen op /3 (echte schaal)','(ii) Graveler-ogen 1-op-1','(iii) Geodude-oog 1-op-1 (2e oog gespiegeld)']
c=Image.new('RGB',(3*310,20+290+100),'white')
for i,(n,o) in enumerate(V):
    im=Image.open(R+n+'.png'); c.paste(kijk.op_wit(im,12).crop((18*12,0,42*12,22*12)),(i*310,20)); tekst(c,(i*310,4),lbl[i])
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im.convert('RGBA')); c.paste(b.convert('RGB'),(i*310+j*70,330))
c.save(R+'vel_ogen.png')
