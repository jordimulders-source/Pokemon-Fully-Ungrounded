# grootte_vergelijk.png: r10 | r9 | Mr. Mime | Galar-Mr. Mime | Machoke | Hitmonchan op 4x (eerste frame 64x64)
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'../sprite_r6'); from palet import PAL
G='../../../../../../graphics/pokemon/'; BG=(232,240,232); Z=4
def bok(a): return Image.fromarray(np.array([(0,0,0)]+PAL[1:],'uint8')[a]).convert('RGBA'), a>0
def gp(f):
    im=Image.open(G+f); im=im.crop((0,0,64,64)).convert('RGBA'); a=np.array(im); m=a[...,3]>0
    if im.getpixel((0,0))[3]>0:  # achtergrondkleur = index 0 -> transparant
        c=a[0,0,:3]; m=~np.all(a[...,:3]==c,axis=2)
    return im,m
L=[('Bokser r10',)+bok(np.load('bokser64.npy')),('Bokser r9',)+bok(np.load('../sprite_r9/bokser.npy'))]
for t,f in [('Mr. Mime','mr_mime/anim_front_gba.png'),('Galar-Mr. Mime','mr_mime/galar/front.png'),('Machoke','machoke/anim_front_gba.png'),('Hitmonchan','hitmonchan/anim_front_gba.png')]:
    L.append((t,)+gp(f))
o=Image.new('RGB',(len(L)*272,286),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im,m) in enumerate(L):
    ys,xs=np.where(m); bg=Image.new('RGB',(64,64),BG); a=np.array(im); out=np.array(bg); out[m]=a[m][:,:3]
    o.paste(Image.fromarray(out).resize((256,256),Image.NEAREST),(i*272,24)); d.text((i*272,6),f'{t}  {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}',fill=(0,0,0))
o.save('grootte_vergelijk.png')
