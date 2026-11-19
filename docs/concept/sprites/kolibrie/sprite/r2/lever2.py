# r2: anim_front, normal.pal, anim.gif, vel.png (frame 2 r1 | r2 op 8x, close-up 12x van de zone), diffbewijs
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
f1=np.array(Image.open('frame1.png')); f2=np.array(Image.open('frame2.png'))
r1a=np.array(Image.open('../r1/frame1.png')); r1b=np.array(Image.open('../r1/frame2.png'))
assert (f1==r1a).all(); d=f2!=r1b; Y,X=np.mgrid[0:64,0:64]; zone=(Y>=10)&(Y<=22)&(X>=45)&(X<=52)
assert not (d&~zone).any(); print('frame1 diff',int((f1!=r1a).sum()),'frame2 diff',int(d.sum()),'buiten zone',int((d&~zone).sum()))
an=Image.fromarray(np.vstack([f1,f2]).astype('uint8'),'P'); an.putpalette(sum(PAL,())); an.save('anim_front.png',transparency=0)
with open('normal.pal','w',newline='\r\n') as f: f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%p for p in PAL))
def rgba(a):
    pal=np.array(sum(PAL,())).reshape(16,3); return Image.fromarray(np.dstack([pal[a],np.where(a==0,0,255)]).astype('uint8'),'RGBA')
fr=[]
for a in (f1,f2):
    c=Image.new('RGB',(256,256),(248,248,248)); s=rgba(a).resize((256,256),0); c.paste(s,(0,0),s); fr.append(c)
fr[0].save('anim.gif',save_all=True,append_images=fr[1:],duration=[500,350],loop=0)
G=12; W=512; V=Image.new('RGB',(G+2*(W+G)+ (16*12*2+G*3) ,W+G*2+40),(60,60,68)); dr=ImageDraw.Draw(V)
for k,(t,a) in enumerate([('frame 2 r1',r1b),('frame 2 r2',f2)]):
    x=G+k*(W+G); V.paste(Image.new('RGB',(W,W),(200,200,208)),(x,G+16)); s=rgba(a).resize((W,W),0); V.paste(s,(x,G+16),s); dr.text((x,G),t,fill=(255,255,255))
    dr.rectangle([x+45*8,G+16+10*8,x+53*8,G+16+23*8],outline=(255,80,80))
x0=G+2*(W+G)
for k,(t,a) in enumerate([('r1 12x',r1b),('r2 12x',f2)]):
    c=rgba(a[6:30,42:58]).resize((16*12,24*12),0); x=x0+k*(16*12+G)
    V.paste(Image.new('RGB',c.size,(200,200,208)),(x,G+16)); V.paste(c,(x,G+16),c); dr.text((x,G),t,fill=(255,255,255))
V.save('vel.png'); print(V.size)
