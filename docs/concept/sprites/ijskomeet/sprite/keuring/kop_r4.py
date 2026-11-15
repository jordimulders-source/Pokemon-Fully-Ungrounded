# kop/gezicht r4 naast model (3x-verkleind, uitgelijnd) op 12x, plus 1x/2x/3x van r4
from PIL import Image
s=Image.open('../r4.png').convert('RGBA'); b=Image.new('RGBA',s.size,(255,255,255,255)); b.alpha_composite(s); s=b.convert('RGB')
m=Image.open('model3x_r2.png').convert('RGB')
box=(0,22,36,60)
W=Image.new('RGB',(36*12*2+20,38*12+140),'white')
W.paste(m.crop(box).resize((432,456),0),(0,0)); W.paste(s.crop(box).resize((432,456),0),(452,0))
for i,k in enumerate((1,2,3)): W.paste(s.resize((64*k,64*k),0),(10+i*110 if k<3 else 240,466))
W.save('kop_r4_12x.png')
