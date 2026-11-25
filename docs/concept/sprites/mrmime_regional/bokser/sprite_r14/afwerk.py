# afwerk.py: bokser.png/.npy, bokser_8x.png, vel.png (r14 | r13 | r9 | Mr. Mime | Galar, 8x), grootte_vergelijk.png (4x)
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
sys.path.insert(0,'../sprite_r7'); from build import save
a=np.load('ruw.npy'); save(a,'bokser')
BG=(232,240,232); G='../../../../../../graphics/pokemon/'
def img(x,bg=BG): return Image.fromarray(np.array([bg]+PAL[1:],'uint8')[x])
img(a,(255,255,255)).resize((512,512),Image.NEAREST).save('bokser_8x.png')
r13=np.load('../sprite_r13/bokser.npy'); r11=np.load('../sprite_r11/bokser.npy'); r9=np.load('../sprite_r9/bokser.npy')
def gp(f):
    im=Image.open(G+f).crop((0,0,64,64)).convert('RGBA'); q=np.array(im); msk=q[...,3]>0
    if im.getpixel((0,0))[3]>0: c=q[0,0,:3]; msk=~np.all(q[...,:3]==c,axis=2)
    out=np.array(Image.new('RGB',(64,64),BG)); out[msk]=q[msk][:,:3]; return Image.fromarray(out),msk
mm,mmm=gp('mr_mime/anim_front_gba.png'); ga,gam=gp('mr_mime/galar/front.png')
ims=[('r14',img(a)),('r13',img(r13)),('r9',img(r9)),('Mr. Mime',mm),('Galar-Mr. Mime',ga)]
o=Image.new('RGB',(5*522,512+24+70),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im) in enumerate(ims):
    o.paste(im.resize((512,512),Image.NEAREST),(i*522,22)); d.text((i*522,5),t,fill=(0,0,0)); o.paste(im,(i*522,540))
o.save('vel.png')
L=[('Bokser r14',img(a),a>0,'kop 21 br.'),('Bokser r13',img(r13),r13>0,'kop 21 br.'),('Bokser r11',img(r11),r11>0,'kop 21 br.'),('Bokser r9',img(r9),r9>0,'kop 16 br.'),('Mr. Mime',mm,mmm,'kop 20 br.'),('Galar-Mr. Mime',ga,gam,'')]
for t,f in [('Machoke','machoke/anim_front_gba.png'),('Hitmonchan','hitmonchan/anim_front_gba.png')]:
    im,msk=gp(f); L.append((t,im,msk,''))
o=Image.new('RGB',(len(L)*272,300),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im,msk,k) in enumerate(L):
    ys,xs=np.where(msk); o.paste(im.resize((256,256),Image.NEAREST),(i*272,38))
    d.text((i*272,4),f'{t}  {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}',fill=(0,0,0)); d.text((i*272,20),k,fill=(0,0,0))
o.save('grootte_vergelijk.png')
