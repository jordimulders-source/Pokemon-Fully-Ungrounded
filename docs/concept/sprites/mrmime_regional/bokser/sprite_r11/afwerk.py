# afwerk.py: bokser.png/.npy (64x64), bokser_8x.png, vel.png (r11 | r9 | model, 8x), grootte_vergelijk.png (4x)
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
sys.path.insert(0,'../sprite_r7'); from build import save
a=np.load('ruw.npy'); save(a,'bokser')
BG=(232,240,232)
def img(a,bg=BG): return Image.fromarray(np.array([bg]+PAL[1:],'uint8')[a])
img(a,(255,255,255)).resize((512,512),Image.NEAREST).save('bokser_8x.png')
r9=np.load('../sprite_r9/bokser.npy')
m=Image.open('../r12.png').convert('RGB').resize((512,512),Image.LANCZOS)
ims=[('r11 (kop natief, lijf r10 korter)',img(a).resize((512,512),Image.NEAREST),img(a)),('r9',img(r9).resize((512,512),Image.NEAREST),img(r9)),('model r12',m,None)]
o=Image.new('RGB',(3*522,512+24+70),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im,one) in enumerate(ims):
    o.paste(im,(i*522,22)); d.text((i*522,5),t,fill=(0,0,0))
    if one: o.paste(one,(i*522,540))
o.save('vel.png')
# grootte
G='../../../../../../graphics/pokemon/'
def bok(x): return Image.fromarray(np.array([(0,0,0)]+PAL[1:],'uint8')[x]).convert('RGBA'), x>0
def gp(f):
    im=Image.open(G+f).crop((0,0,64,64)).convert('RGBA'); q=np.array(im); msk=q[...,3]>0
    if im.getpixel((0,0))[3]>0: c=q[0,0,:3]; msk=~np.all(q[...,:3]==c,axis=2)
    return im,msk
KOP={'Bokser r11':'kop 21 br.','Bokser r9':'kop 16 br.','Mr. Mime':'kop 20 br.'}
L=[('Bokser r11',)+bok(a),('Bokser r9',)+bok(r9)]
for t,f in [('Mr. Mime','mr_mime/anim_front_gba.png'),('Galar-Mr. Mime','mr_mime/galar/front.png'),('Machoke','machoke/anim_front_gba.png'),('Hitmonchan','hitmonchan/anim_front_gba.png')]:
    L.append((t,)+gp(f))
o=Image.new('RGB',(len(L)*272,300),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im,msk) in enumerate(L):
    ys,xs=np.where(msk); out=np.array(Image.new('RGB',(64,64),BG)); q=np.array(im); out[msk]=q[msk][:,:3]
    o.paste(Image.fromarray(out).resize((256,256),Image.NEAREST),(i*272,38))
    d.text((i*272,4),f'{t}  {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}',fill=(0,0,0)); d.text((i*272,20),KOP.get(t,''),fill=(0,0,0))
o.save('grootte_vergelijk.png')
