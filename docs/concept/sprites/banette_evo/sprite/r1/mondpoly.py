# Mondvorm als polygoon uit de modelranden (boven-/onderrand per kolom), gerasterd op pixelmiddens
import numpy as np; from matplotlib.path import Path
m=np.load('mond_vol.npy'); S=968/62
top=[];bot=[]
for x in range(242,669,2):
    ys=np.where(m[:,x])[0]
    if len(ys): top.append(((x-24)/S+1,(ys.min()-1)/S+4)); bot.append(((x-24)/S+1,(ys.max()+1-1)/S+4))
poly=Path(top+bot[::-1])
M=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64): M[j,i]=poly.contains_point((i+0.5,j+0.5))
np.save('mond_sprite.npy',M)
for j in range(22,45): print('%2d'%j,''.join('#' if M[j,i] else '.' for i in range(12,47)))
