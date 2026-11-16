import numpy as np; from PIL import Image
o=np.load('r15w/o2.npy'); naad=np.load('r15w/naad.npy')
pal=Image.open('r14.png').getpalette(); pal[13*3:13*3+3]=[70,88,138]   # vrije slot (oude oogkern) -> binnennaad
fg=o>0
outer=np.array([[fg[j,i] and any(not fg[j+dy,i+dx] for dy in(-1,0,1) for dx in(-1,0,1)) for i in range(64)] for j in range(64)])
inner=naad&~outer
o[inner]=13
np.save('r15w/o3.npy',o)
im=Image.fromarray(o.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r15w/o3.png',transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save('r15w/o3_8x.png')
print(inner.sum())
