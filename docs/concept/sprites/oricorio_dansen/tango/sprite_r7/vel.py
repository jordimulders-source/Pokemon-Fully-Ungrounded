# vel.png r7: r7 | r6 | model (8x); r7_donker 8x klein; 1x en 2x op wit/donker/gevechtsgroen naast Murkrow en Umbreon; paletstrip met helderheden
import numpy as np; from PIL import Image, ImageDraw; from palet import pal, NAMEN
G=(152,208,160); GR='../../../../../../graphics/pokemon/'
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
def gen3(n):
    im=Image.open(GR+n+'/anim_front.png'); p=im.getpalette()[:48]
    pal_=Image.open(GR+n+'/normal.pal').read() if False else None
    a=np.array(im)[:64]; t=Image.fromarray(a,'P'); 
    lines=open(GR+n+'/normal.pal').read().split('\n')[3:19]; fl=[int(v) for l in lines for v in l.split()]
    t.putpalette(fl); t.info['transparency']=0; t.save('/tmp/_g.png',transparency=0); return rgba('/tmp/_g.png')
A=rgba('tango.png'); Dk=rgba('tango_r7_donker.png'); R6=rgba('r6_ref.png'); MU=gen3('murkrow'); UM=gen3('umbreon')
m=Image.open('../model/gemini_r7.png').convert('RGB'); ma=np.asarray(m); ys,xs=np.where(ma.min(2)<200)
al=np.asarray(A)[:,:,3]>0; sy,sx=np.where(al)
mc=m.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.LANCZOS)
M=Image.new('RGB',(512,512),'white'); M.paste(mc,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(4*522,30+512+40+150+40+120),(230,230,230)); d=ImageDraw.Draw(W)
for k,(im,t) in enumerate([(op(A,'white',8),'r7 tango.png (reeks r7)'),(op(Dk,'white',8),'r7_donker (zelfde reeks, donkerder)'),(op(R6,'white',8),'r6'),(M,'model gemini_r7')]):
    W.paste(im,(k*522,30)); d.text((k*522+4,10),t,fill='black')
y=582; d.text((4,y),'1x en 2x: r7 | r7_donker | Murkrow | Umbreon  op wit / donker / gevechtsgroen',fill='black')
x=0
for bg in ('white',(40,40,48),G):
    for im in (A,Dk,MU,UM):
        W.paste(op(im,bg,1),(x,y+20)); W.paste(op(im,bg,2),(x,y+90)) if False else None; x+=68
    x+=20
x2=900
for i,(bg) in enumerate(('white',(40,40,48),G)):
    for j,im in enumerate((A,Dk,MU,UM)): W.paste(op(im,bg,2),(x2+j*132,y+20+0)) if i==2 else None
y=y+170; d.text((4,y),'paletstrip (helderheid 0,299R+0,587G+0,114B): r7 boven, r7_donker onder; idx 4 (D2) samengevoegd met D3',fill='black')
for row,v in enumerate(('r7','r7_donker')):
    for i,(n,c) in enumerate(zip(NAMEN,pal(v))):
        if n in ('_','D2'): continue
        X=i*96; Y=y+18+row*50; d.rectangle([X,Y,X+40,Y+40],fill=c); d.text((X+44,Y+4),n,fill='black'); d.text((X+44,Y+20),str(round(.299*c[0]+.587*c[1]+.114*c[2])),fill='black')
W.save('vel.png'); print(W.size)
