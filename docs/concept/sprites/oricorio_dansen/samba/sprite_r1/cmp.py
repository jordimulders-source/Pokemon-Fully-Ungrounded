# model (zelfde schaal) | sprite, 10x, uitsnede van de sprite-bbox
import sys, numpy as np; from PIL import Image
from render import zoom
Z=int(sys.argv[2]) if len(sys.argv)>2 else 10
s=Image.open(sys.argv[1]).convert('RGBA'); a=np.array(s); ys,xs=np.where(a[...,3]>0)
box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1); w,h=box[2]-box[0],box[3]-box[1]
m=Image.open('../model/gemini_r6.png').convert('RGB').crop((294,60,768,513)).resize((w*Z,h*Z),Image.LANCZOS)
sp=Image.new('RGB',(w*Z,h*Z),'white'); r=s.crop(box).resize((w*Z,h*Z),Image.NEAREST); sp.paste(r,(0,0),r)
W=Image.new('RGB',(2*w*Z+10,h*Z),(200,200,200)); W.paste(m,(0,0)); W.paste(sp,(w*Z+10,0)); W.save(sys.argv[3] if len(sys.argv)>3 else '/tmp/claude-0/cmp.png')
