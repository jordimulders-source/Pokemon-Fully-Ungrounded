# anim_front.png (64x128), normal.pal (JASC), anim.gif en vel.png
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
R='/home/user/Pokemon-Fully-Ungrounded/'
f1=np.array(Image.open('frame1.png')); f2=np.array(Image.open('frame2.png'))
assert f1.shape==f2.shape==(64,64)
an=np.vstack([f1,f2]).astype('uint8'); im=Image.fromarray(an,'P'); im.putpalette(sum(PAL,())); im.save('anim_front.png',transparency=0)
with open('normal.pal','w',newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%p for p in PAL))
def rgba(path,crop=None):
    im=Image.open(path); im=im.convert('RGBA') if im.mode!='P' else Image.open(path).convert('RGBA')
    if im.mode=='RGBA' and Image.open(path).mode=='P' and 'transparency' not in Image.open(path).info:
        pass
    return im.crop(crop) if crop else im
def p2rgba(path,crop=None):
    src=Image.open(path); a=np.array(src); pal=np.array(src.getpalette()[:48]).reshape(16,3)
    if crop: a=a[crop[1]:crop[3],crop[0]:crop[2]]
    rgb=pal[a]; al=np.where(a==0,0,255)
    return Image.fromarray(np.dstack([rgb,al]).astype('uint8'),'RGBA')
# gif: frame 1 / frame 2 afwisselend op licht en donker
fr=[]
for bg in [(248,248,248)]:
    for f in ['frame1.png','frame2.png']:
        c=Image.new('RGB',(64*4,64*4),bg); s=p2rgba(f).resize((256,256),0); c.paste(s,(0,0),s); fr.append(c)
fr[0].save('anim.gif',save_all=True,append_images=fr[1:],duration=[500,350],loop=0)
# vel
S=8; W=64*S; G=12
M1=Image.open('../../referenties/gemini_gekozen_r4.png').convert('RGB'); M2=Image.open('../../gemini/r3_frame2_kandidaat.png').convert('RGB')
import json; P=json.load(open('plaats.json'))
def model_op_schaal(M,pitch,fase,bbox_nat,off,schaal=1.0):
    # model zo uitsnijden/schalen dat 1 natieve cel = schaal spritepixels, geplaatst als in de sprite
    (x0n,y0n)=bbox_nat; ox,oy=off; ppx=S*schaal/pitch*1.0
    # linkerboven van het 64-kader in modelpixels:
    X0=fase[0]+(x0n - ox/schaal)*pitch; Y0=fase[1]+(y0n - oy/schaal)*pitch; side=64/schaal*pitch
    Mp=Image.new('RGB',(M.width+800,M.height+800),(255,255,255)); Mp.paste(M,(400,400)); X0+=400; Y0+=400
    c=Mp.crop((int(round(X0)),int(round(Y0)),int(round(X0+side)),int(round(Y0+side)))).resize((W,W),Image.LANCZOS)
    return c
from bron import laad
import bron as B
def natbbox(n):
    a=np.asarray(Image.open(B.NAT[n]).convert('RGB')).astype(float); _,_,m,_=laad(n)
    bg=a.min(axis=2)>=242
    for _ in range(2):
        p=np.pad(bg,1,constant_values=True); nb=p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]
        bg|= nb&(a.min(axis=2)>=170)&((a[...,2]-a[...,1])<=15)
    ys,xs=np.where(~bg); return xs.min(),ys.min()
m1=model_op_schaal(M1,15.5,(14.5,14.0),natbbox('f1'),P['f1'])
m2=model_op_schaal(M2,10.24,(5.25,5.5),natbbox('f2'),P['f2'],B.S2)
tiles=[('frame 1 (8x)',p2rgba('frame1.png').resize((W,W),0),'g'),('model frame 1 (zelfde schaal)',m1,'w'),
       ('frame 2 (8x)',p2rgba('frame2.png').resize((W,W),0),'g'),('model frame 2 (x%.2f)'%B.S2,m2,'w'),
       ('oude Soulibri (af/)',p2rgba('../../af/kolibrie.png').resize((W,W),0),'g')]
for s in ['crobat','ninjask','beautifly']:
    tiles.append((s+' (Gen 3)',p2rgba(R+'graphics/pokemon/%s/anim_front.png'%s,(0,0,64,64)).resize((W,W),0),'g'))
cols=4; rows=(len(tiles)+cols-1)//cols
V=Image.new('RGB',(cols*(W+G)+G, rows*(W+G+16)+G+250),(60,60,68)); d=ImageDraw.Draw(V)
for k,(t,im,bgk) in enumerate(tiles):
    x=G+(k%cols)*(W+G); y=G+(k//cols)*(W+G+16)
    V.paste(Image.new('RGB',(W,W),(200,200,208) if bgk=='g' else (255,255,255)),(x,y+16))
    V.paste(im,(x,y+16),im if im.mode=='RGBA' else None); d.text((x,y+2),t,fill=(255,255,255))
# 1x op licht en donker
y=G+rows*(W+G+16); x=G; d.text((x,y),'1x licht / donker: frame 1, frame 2, Crobat',fill=(255,255,255)); y+=14
for bg in [(248,248,248),(32,32,40)]:
    for f in [p2rgba('frame1.png'),p2rgba('frame2.png'),p2rgba(R+'graphics/pokemon/crobat/anim_front.png',(0,0,64,64))]:
        V.paste(Image.new('RGB',(68,68),bg),(x,y)); V.paste(f,(x+2,y+2),f); x+=72
    x+=16
# 2x ook
x=G; y+=76
for bg in [(248,248,248),(32,32,40)]:
    for f in ['frame1.png','frame2.png']:
        s=p2rgba(f).resize((128,128),0); V.paste(Image.new('RGB',(128,128),bg),(x,y-2)); V.paste(s,(x,y-2),s); x+=134
V.save('vel.png'); print(V.size)
