from PIL import Image
import numpy as np
m=Image.open('model/model.png').convert('RGB')
s=Image.open('sprite_r2/pitahaya2_r2.png').convert('RGB')
n=Image.open('sprite_r2/natief.png').convert('RGB')
# model op 64 via natief 201->67 box
nd=n.resize((67,67),Image.BOX)
W=8
sheet=Image.new('RGB',(64*W*2+67*W+40,max(67,64)*W+20),(128,128,128))
sheet.paste(s.resize((64*W,64*W),Image.NEAREST),(10,10))
sheet.paste(nd.resize((67*W,67*W),Image.NEAREST),(64*W+20,10))
sheet.paste(m.resize((64*W,64*W),Image.LANCZOS),(64*W+67*W+30,10))
sheet.save('keuring_r2/vel8x.png')
one=Image.new('RGB',(64*2+67+40,80),(255,255,255))
one.paste(s,(10,10)); one.paste(nd,(84,10)); one.paste(m.resize((64,64),Image.LANCZOS),(160,10))
one.resize((one.width*2,one.height*2),Image.NEAREST).save('keuring_r2/vel1x_2x.png')
