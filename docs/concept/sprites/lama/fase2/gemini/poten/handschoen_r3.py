# plakwerk v2 (r4 + poten r12) + handschoenen van r3 op de voorvoeten (Jordi: "ja van r3")
from PIL import Image; import numpy as np
P=np.array(Image.open('poten/r4_poten_r12.png').convert('RGB')).astype(int)
R=np.array(Image.open('r3/r3_prompt_v3.png').convert('RGB')).astype(int)
O=P.copy(); white=lambda p: p.sum()>=700
def tan(p): r,g,b=p; return r>150 and g>100 and r-b>50 and g-b>25
# (r3-box x0,x1,y0,y1), verschuiving, wisgebied in het plakwerk
for (x0,x1,y0,y1),(dx,dy),(wx0,wx1,wy0) in [((380,505,838,990),(-5,-5),(385,512,836)),((218,380,858,1010),(4,-6),(195,386,856))]:
    O[wy0:,wx0:wx1]=255
    for y in range(y0,y1):
        for x in range(x0,x1):
            p=R[y,x]
            if white(p): continue
            if y<y0+12 and tan(p): continue   # r3-been boven de polsband niet meenemen
            O[y+dy,x+dx]=p
Image.fromarray(O.astype('uint8')).save('poten/model_handschoenen_r3.png')
Image.fromarray(O.astype('uint8')).crop((180,700,900,1024)).save('poten/zoom.png')
