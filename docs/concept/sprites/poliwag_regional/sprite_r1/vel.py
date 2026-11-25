# vel.png: r1 8x | model op dezelfde schaal; close-up kop en buik 12x naast het model; 1x licht/donker; naast Poliwag, Ninjask, Dundragoon (gba)
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']; r=np.load('r1.npy'); H,W=r.shape
mod=Image.open('../referenties/gemini_gekozen_v2.png').convert('RGB')
def rgb(a,bg=(255,255,255)):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=bg
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def modcrop(c0,c1,r0,r1,w,h): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1+1]))).resize((w,h),Image.LANCZOS)
def gba(n):
    a=np.array(Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n))[:64]
    p=open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]
    cols=[tuple(map(int,p[i*3:i*3+3])) for i in range(16)]
    o=np.zeros((64,64,3),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=cols[k]
    return Image.fromarray(o)
rows=[]
A=rgb(r).resize((W*8,H*8),Image.NEAREST); B=modcrop(0,W-1,0,H-1,W*8,H*8)
row1=Image.new('RGB',(W*16+20,H*8),'white'); row1.paste(A,(0,0)); row1.paste(B,(W*8+20,0)); rows.append(('r1 8x | model (zelfde schaal)',row1))
def close(c0,c1,r0,r1,s=12):
    a=rgb(r[r0:r1+1,c0:c1+1]).resize(((c1-c0+1)*s,(r1-r0+1)*s),Image.NEAREST); b=modcrop(c0,c1,r0,r1,a.size[0],a.size[1])
    c=Image.new('RGB',(a.size[0]*2+20,a.size[1]),'white'); c.paste(a,(0,0)); c.paste(b,(a.size[0]+20,0)); return c
rows.append(('kop 12x | model',close(0,32,0,19)))
rows.append(('buik 12x | model',close(0,20,16,35)))
S=np.array(Image.open('poliwag_regional_r1.png'))
one=Image.new('RGB',(64*4*2+40,64*2+10),'white')
for i,bg in enumerate([(255,255,255),(232,232,216),(48,48,64),(20,20,28)]):
    t=rgb(S,bg); one.paste(t,(i*74,0))
refs=[('poliwag',gba('poliwag')),('ninjask',gba('ninjask'))]
dd=Image.open('../../dundragoon/af/dundragoon.png').convert('RGBA'); bgd=Image.new('RGBA',dd.size,(255,255,255,255)); bgd.alpha_composite(dd)
ref=Image.new('RGB',(64*4*4+60,64*4),'white')
for i,im in enumerate([rgb(S),refs[0][1],refs[1][1],bgd.convert('RGB')]): ref.paste(im.resize((256,256),Image.NEAREST),(i*276,0))
rows.append(('1x op licht en donker',one)); rows.append(('4x: r1 | Poliwag | Ninjask | Dundragoon (gba)',ref))
Wt=max(im.size[0] for _,im in rows); Ht=sum(im.size[1]+28 for _,im in rows)
vel=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(vel); y=0
for t,im in rows:
    d.text((4,y+6),t,fill=(0,0,0)); vel.paste(im,(0,y+24)); y+=im.size[1]+28
vel.save('vel.png'); print(vel.size)
