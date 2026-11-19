import numpy as np; from PIL import Image, ImageDraw
exec(open('bouw.py').read().split("o=np.load")[0])
src=open('bouw.py').read()
PAL=eval(src.split('PAL=')[1].split('\nMAP')[0]); MAP={16:15,17:13}
def png(a,uit):
    idx=np.vectorize(lambda v:MAP.get(v,v))(a)
    full=np.zeros((64,64),'uint8'); full[10:10+54,0:59]=idx[:54,5:64] if False else 0
    o=np.load('r5.npy'); ys,xs=np.where(o>0); h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1; x0=(64-w)//2; y0=63-h
    full[y0:y0+h,x0:x0+w]=idx[ys.min():ys.max()+1,xs.min():xs.max()+1]
    p=Image.fromarray(full,'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save(uit,transparency=0)
    return Image.open(uit).convert('RGBA')
def on(im,s,bg=(255,255,255,255)):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
from toon import img
tiles=[]
for k in 'ABCD':
    a=np.load('var_%s.npy'%k); sp=png(a,'picapau_oog_%s.png'%k)
    kop=img(a[12:26,16:32],12)
    t=Image.new('RGB',(kop.width+140,kop.height+30),(210,210,210)); d=ImageDraw.Draw(t)
    t.paste(kop,(0,24)); t.paste(on(sp,1),(kop.width+8,24)); t.paste(on(sp,2),(kop.width+8,24+70)); d.text((4,4),k,fill=(0,0,0))
    tiles.append(t)
V=Image.new('RGB',(sum(t.width+10 for t in tiles),tiles[0].height),(160,160,160)); x=0
for t in tiles: V.paste(t,(x,0)); x+=t.width+10
V.save('varianten_oog.png'); print(V.size)
