import numpy as np; from PIL import Image, ImageDraw; import maak_r6 as m, kijk
R='r6/'; OOG='hitmonchan'
ZONES=[(0,18,22,41),(15,10,31,22),(21,10,34,37)]          # hoofd, linkerarm/schouder, handen (y0,x0,y1,x1)
def bouw(keuze,oog=OOG):
    m.LOG.clear(); A=m.R5.copy()
    A=m.brein(A,keuze); A=m.gezicht(A); A=m.ogen(A,oog); A=m.linkerarm(A); A=m.selout_links(A)
    A=m.vlekjes(A,(21,10,34,37))
    Z=np.zeros((64,64),bool)
    for y0,x0,y1,x1 in ZONES: Z[y0:y1+1,x0:x1+1]=True
    assert ((A!=m.R5)&~Z).sum()==0, 'diff buiten de zones'
    return A,dict(m.LOG)
def png(A,pad=None):
    im=Image.fromarray(A.astype('uint8'),'P'); im.putpalette(m.PAL); im.info['transparency']=0
    if pad: im.save(pad,transparency=0)
    return im
def tekst(c,xy,t): ImageDraw.Draw(c).text(xy,t,fill=(0,0,0))
def r8_hoofd(w,h):
    return Image.open('../gemini/r8.png').convert('RGB').crop((395,130,610,330)).resize((w,h),Image.LANCZOS)
if __name__=='__main__':
    W={}
    for naam,k in (('W1','BCD'),('W2','ABCD')):
        A,log=bouw(k); W[naam]=png(A,R+'zandloper_fase3_%s.png'%naam)
        print(naam,len(np.unique(A)),'kleuren; diff met r5:',int((A!=m.R5).sum()),'px')
        for kk,v in log.items(): print('  ',kk,len(v),[(p,o,n) for p,o,n in v])
    r5=png(m.R5)
    c=Image.new('RGB',(4*520,20+512+150+290+300),'white')
    for i,(x,t) in enumerate([(kijk.op_wit(W['W1'],8),'W1 (3 windingen)'),(kijk.op_wit(W['W2'],8),'W2 (4 windingen)'),(kijk.op_wit(r5,8),'r5'),(kijk.model64().resize((512,512),Image.NEAREST),'model r5')]):
        c.paste(x,(i*520,20)); tekst(c,(i*520+4,4),t)
    y=545
    for i,(x,t) in enumerate([(W['W1'],'W1'),(W['W2'],'W2'),(r5,'r5')]):
        for j,bg in enumerate([(255,255,255),(232,224,208),(40,44,52),(16,16,16)]):
            b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(x.convert('RGBA')); c.paste(b.convert('RGB'),(i*300+j*70,y+14))
        tekst(c,(i*300,y),t+' 1x licht/donker')
    y=680
    for i,(x,t) in enumerate([(W['W1'],'W1 hoofd 12x'),(W['W2'],'W2 hoofd 12x'),(r5,'r5 hoofd 12x')]):
        c.paste(kijk.op_wit(x,12).crop((17*12,0,43*12,23*12)),(i*330,y+14)); tekst(c,(i*330,y),t)
    c.paste(r8_hoofd(312,276),(990,y+14)); tekst(c,(990,y),'r8-hoofd (model)')
    y=980
    for i,(x,t) in enumerate([(W['W1'],'W1 handen 12x'),(r5,'r5 handen 12x')]):
        c.paste(kijk.op_wit(x,12).crop((10*12,20*12,38*12,35*12)),(i*345,y+14)); tekst(c,(i*345,y),t)
    a=Image.open('../gemini/r5.webp').convert('RGB'); x0=(0*3+2)*5.12-0.12; y0=(2*3+2)*5.12-0.12; p=15.36
    c.paste(a.crop((int(x0+10*p),int(y0+20*p),int(x0+38*p),int(y0+35*p))).resize((336,180),Image.LANCZOS),(690,y+14)); tekst(c,(690,y),'model handen')
    c.save(R+'vel.png')
    # ogenvel: 4 Gen 3-ogen op het hoofd van W1
    namen=list(m.OGEN); v=Image.new('RGB',(4*330,20+276+90),'white')
    for i,n in enumerate(namen):
        A,_=bouw('BCD',n); im=png(A); png(A,R+'ogen_%s.png'%n)
        v.paste(kijk.op_wit(im,12).crop((17*12,0,43*12,23*12)),(i*330,20)); tekst(v,(i*330,4),'%s (anim_front_gba)'%n)
        v.paste(kijk.op_wit(im,1),(i*330,310)); v.paste(kijk.op_wit(im,2).crop((28,0,100,60)),(i*330+80,310))
    v.save(R+'vel_ogen.png')
