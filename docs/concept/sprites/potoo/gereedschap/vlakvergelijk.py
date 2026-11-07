# vlakvergelijk.py ronde: gemiddelde helderheid per 4x4-blok, model (box-verkleind, alleen silhouet) vs sprite; verschil sprite-model.
import sys,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
m=np.asarray(Image.open(P+'silhouet/gids_gemiddeld.png').convert('RGBA')).astype(float)
s=np.asarray(Image.open(P+sys.argv[1]+'/potoo.png').convert('RGBA')).astype(float)
a=s[...,3]>0
print('blok (x,y = linksboven) : verschil L (sprite - model), alleen blokken met >= 8 px')
for by in range(0,64,4):
  r=f'{by:2d} '
  for bx in range(16,48,4):
    f=a[by:by+4,bx:bx+4]
    if f.sum()<8: r+='     .'; continue
    d=s[by:by+4,bx:bx+4,:3][f].mean()-m[by:by+4,bx:bx+4,:3][f].mean(); r+=f'{d:+6.0f}'
  print(r)
print('   '+''.join(f'{x:6d}' for x in range(16,48,4)))
