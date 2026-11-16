# sim_moet.png: boven r7 | sim | model op 16x (arm + voet), onder r7 | sim op 2x en 1x
import numpy as np; from PIL import Image
def rgb(f,bg=(205,212,222)):
    a=Image.open(f); i=np.array(a); r=np.array(a.convert('RGB')); r[i==0]=bg; return Image.fromarray(r)
nat=Image.open('../sprite_r7/natief.png').convert('RGB')
x0,y0,x1,y1=30,34,48,57; Z=16; w=(x1-x0)*Z
W=Image.new('RGB',(3*w+40,(y1-y0)*Z+150),(255,255,255))
for k,f in enumerate(['../sprite_r7/pitahaya_r7.png','sim_moet_sprite.png']):
    W.paste(rgb(f).crop((x0,y0,x1,y1)).resize((w,(y1-y0)*Z),Image.NEAREST),(k*(w+20),0))
    W.paste(rgb(f).resize((128,128),Image.NEAREST),(k*(w+20),(y1-y0)*Z+10)); W.paste(rgb(f),(k*(w+20)+140,(y1-y0)*Z+10))
W.paste(nat.crop((3*x0+4,3*y0+6,3*x1+4,3*y1+6)).resize((w,(y1-y0)*Z),Image.NEAREST),(2*(w+20),0))
W.save('sim_moet.png')
