# vel.png: ek 8x | r2-c 8x | maatstaf + Gen 3 (4x) ; onderaan 1x en 2x op licht en donker.
# vel_binnenlijn_test.png: de teruggedraaide binnenlijn-test (16x uitsnede).  Draaien vanuit deze map.
import numpy as np
from PIL import Image, ImageDraw
R='../../../../../'
def gba(n):
    src=Image.open(R+f'graphics/pokemon/{n}/anim_front_gba.png').crop((0,0,64,64))
    L=open(R+f'graphics/pokemon/{n}/normal_gba.pal').read().split('\n')[3:19]
    pal=[int(v) for l in L for v in l.split()]
    p=src.convert('P') if src.mode!='P' else src
    q=p.copy(); q.putpalette(pal+[0]*(768-len(pal))); rgba=q.convert('RGBA'); A=np.array(rgba); A[np.array(p)==0,3]=0
    return Image.fromarray(A)
ek=Image.open('ledian_evo_ek.png').convert('RGBA'); r2=Image.open('../sprite_r2/rood_c.png').convert('RGBA')
refs=[('Ledian G3',gba('ledian')),('Scizor G3',gba('scizor'))]+[(n,Image.open(f'../../{p}').convert('RGBA')) for n,p in
      [('Dundragoon','dundragoon/af/dundragoon.png'),('Skinguin','skinguin/af/skinguin.png'),('Princadee','awki/af/awki.png'),('Zapacha','viscacha/af/viscacha.png')]]
BG=(200,200,200,255)
def on(im,S,bg=BG):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.resize((im.width*S,im.height*S),Image.NEAREST)
W=512*2+256*2+60; H=512+40+200
V=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(V)
V.paste(on(ek,8),(0,20)); d.text((4,4),'eindkeuring (ek) 8x',fill=(0,0,0))
V.paste(on(r2,8),(532,20)); d.text((536,4),'r2 rood c 8x',fill=(0,0,0))
for i,(n,im) in enumerate(refs):
    x=1064+(i%2)*260; y=20+(i//2)*170
    V.paste(on(im,4).crop((0,0,256,256)).resize((160,160),Image.NEAREST),(x,y)); d.text((x,y+160),n,fill=(0,0,0))
y0=512+40
for j,bg in enumerate([(248,248,248,255),(24,24,40,255),(80,120,80,255)]):
    x=j*360
    V.paste(on(ek,1,bg),(x+10,y0)); V.paste(on(r2,1,bg),(x+80,y0))
    V.paste(on(ek,2,bg),(x+150,y0)); 
d.text((10,y0+140),'1x: ek | r2-c ; 2x: ek  (licht / donker / groen)',fill=(0,0,0))
V.save('vel.png')
# binnenlijn-test
import ek as E
t=E.s.copy()
for x,y in E.TEST_BINNEN: t[y,x]=7
o=Image.fromarray(t.astype('uint8'),'P'); o.putpalette(E.pal+[0]*(768-len(E.pal))); o=o.convert('RGBA'); A=np.array(o); A[t==0,3]=0; o=Image.fromarray(A)
box=(26,22,50,38); w,h=24,16; S=16
T=Image.new('RGBA',(w*S*2+16,h*S+16),(255,255,255,255))
T.paste(on(ek.crop(box),S),(0,16)); T.paste(on(o.crop(box),S),(w*S+16,16))
ImageDraw.Draw(T).text((4,2),'ek (binnenlijnen zwart)  |  test: binnenlijnen selout -> hoofd/arm/vleugel smelten',fill=(0,0,0))
T.save('vel_binnenlijn_test.png')
