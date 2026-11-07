import sys; sys.path.insert(0,'.')
import numpy as np
from PIL import Image, ImageDraw
from pose import masker
R='/home/user/Pokemon-Fully-Ungrounded/'
m=masker()
foto=Image.open(R+'docs/concept/sprites/hitmontop_evo/referenties/pose_eenhandsstand.webp').convert('RGB').crop((0,0,1580,1600)).transpose(Image.FLIP_LEFT_RIGHT).crop((82,82,1325,1500)).resize((53*8,61*8))
fc=Image.new('RGB',(512,512),'white'); fc.paste(foto,(5*8,1*8))
sil=Image.new('RGB',(512,512),(235,235,235)); d=ImageDraw.Draw(sil)
for y in range(64):
  for x in range(64):
    if m[y,x]: d.rectangle([x*8,y*8,x*8+7,y*8+7],fill=(40,40,40))
# overlay outline on foto
ov=fc.copy(); d2=ImageDraw.Draw(ov)
for y in range(64):
  for x in range(64):
    if m[y,x] and (x==0 or not m[y,x-1] or not m[y,x+1] or not m[y-1,x] or not m[y+1,x]):
      d2.rectangle([x*8+2,y*8+2,x*8+5,y*8+5],fill=(220,0,0))
lee=Image.open(R+'graphics/pokemon/hitmonlee/anim_front.png').crop((0,0,64,64)).convert('RGB')
top=Image.open(R+'graphics/pokemon/hitmontop/anim_front.png').crop((0,0,64,64)).convert('RGB')
W=Image.new('RGB',(4*520,512+80),'white')
for i,im in enumerate([ov,sil,lee.resize((512,512),Image.NEAREST),top.resize((512,512),Image.NEAREST)]): W.paste(im,(i*520,0))
s1=Image.fromarray(np.where(m[...,None]>0,[40,40,40],[235,235,235]).astype('uint8'))
for i,im in enumerate([s1,lee,top]): W.paste(im,(i*70+10,520))
W.save(sys.argv[1])
