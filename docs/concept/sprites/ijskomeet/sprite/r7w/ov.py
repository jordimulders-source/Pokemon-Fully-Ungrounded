import sys; sys.path.insert(0,'r7w'); sys.path.insert(0,'.')
from proj import *
from PIL import ImageDraw
from gio import from_txt,CH
o=from_txt(sys.argv[1] if len(sys.argv)>1 else 'r5.txt')
s=12; im=model_s(s).convert('RGB'); d=ImageDraw.Draw(im)
m=np.load('mask_r1.npy')
for j in range(64):
  for i in range(64):
    v=o[j,i]
    if v>=0 and CH[v] in 'KS': d.rectangle([i*s+4,j*s+4,i*s+7,j*s+7],fill=(255,0,0))
    # maskerrand
    if m[j,i] and (j==0 or not m[j-1,i]): d.line([i*s,j*s,i*s+s,j*s],fill=(0,200,0))
    if m[j,i] and (i==0 or not m[j,i-1]): d.line([i*s,j*s,i*s,j*s+s],fill=(0,200,0))
im.save(sys.argv[2] if len(sys.argv)>2 else '/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/dc7c53d6-43c5-5b88-a920-99d5791f3af7/scratchpad/ov.png')
