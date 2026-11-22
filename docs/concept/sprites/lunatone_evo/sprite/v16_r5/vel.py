import numpy as np, tool; from PIL import Image, ImageDraw
a=np.load('../v16_r2/idx.npy'); b=np.load('idx.npy')
M=Image.open('../../referenties/model_v16.png').convert('RGB').resize((512,512),Image.LANCZOS)
V=Image.new('RGB',(16+3*528,660),(230,230,230)); d=ImageDraw.Draw(V)
for k,(im,t) in enumerate([(tool.rgba(a,sc=8),'v16 r2A'),(tool.rgba(b,sc=8),'v16 r5'),(M,'model v16')]):
    V.paste(im,(16+k*528,30)); d.text((16+k*528,10),t,fill=(0,0,0))
for k,o in enumerate([a,b]):
    for j,bg in enumerate([(240,240,240),(48,48,56)]): V.paste(tool.rgba(o,bgc=bg),(16+k*528+j*80,570))
V.paste(M.resize((64,64),Image.LANCZOS),(16+2*528,570)); V.save('vel.png')
