"""Snelle controle: 1x en 3x naast Galar-Linoone en ronde 23, plus 8x."""
import sys
sys.path.insert(0,'/home/user/projectgrounded/docs/concept/sprites/olinguito/herbouw_linoone/bron')
from render import load,to_img,zoom
from PIL import Image
D='/home/user/projectgrounded/docs/concept/sprites/olinguito/'
im=to_img(load(sys.argv[1]))
lin=Image.open(D+'referenties/galar_linoone_front.png')
r23=Image.open(D+'ronde23/anim_front.png').crop((0,0,64,64))
W=Image.new('RGBA',(64*3+64*3*3+40, 64*3+10),(255,255,255,255))
x=0
for i in (lin,r23,im):
    W.paste(zoom(i,1),(x,0)); x+=66
x=210
for i in (lin,r23,im):
    W.paste(zoom(i,3),(x,0)); x+=196
W.save(sys.argv[2])
