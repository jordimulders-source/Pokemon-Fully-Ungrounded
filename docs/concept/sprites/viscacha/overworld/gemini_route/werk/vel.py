import numpy as np; from PIL import Image, ImageDraw
BG=(152,208,160)
a=Image.open('../af/overworld.png').convert('RGBA')
def frame(i):
    f=a.crop((i*32,0,i*32+32,32)); bg=Image.new('RGBA',(32,32),BG+(255,)); bg.alpha_composite(f); return bg.convert('RGB')
nat={n:Image.open(f'nat_{n}.png').convert('RGB') for n in ['front','back','side']}
S=8
W=(52*4+32*S+40)*1; H=(52*4+20)*3
vel=Image.new("RGB",(52*4+32*S+60, 3*(32*S+20)),(255,255,255))
for k,(n,i) in enumerate([('front',0),('back',2),('side',4)]):
    m=nat[n].resize((nat[n].width*4,nat[n].height*4),Image.NEAREST)
    y=k*(32*S+20)
    vel.paste(m,(10,y+10)); vel.paste(frame(i).resize((32*S,32*S),Image.NEAREST),(52*4+40,y+10))
vel.save('../af/vel_vergelijk.png')
# naast echte overworldsprites
import os
R='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
row=[]
for n in ['eevee','pachirisu','rattata']:
    im=Image.open(R+n+'/overworld.png'); pal=open(R+n+'/overworld_normal.pal').read().split('\n')[3:19]
    im.putpalette([int(v) for l in pal for v in l.split()]); im=im.convert('RGB')
    arr=np.array(im); arr[np.array(Image.open(R+n+'/overworld.png'))==0]=BG; row.append(Image.fromarray(arr))
mine=Image.new('RGB',(192,32),BG)
for i in range(6): mine.paste(frame(i),(i*32,0))
sheet=Image.new('RGB',(192*6,32*6*4),BG)
for j,im in enumerate([mine]+row): sheet.paste(im.resize((192*6,192),Image.NEAREST),(0,j*192))
sheet.save('naast_echt.png')
