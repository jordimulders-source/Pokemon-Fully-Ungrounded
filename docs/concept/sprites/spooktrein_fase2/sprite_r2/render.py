# raster (npy) -> geïndexeerde png (index 0 transparant) + 8x; ongebruikte kleuren eruit, palet compact
import sys; from PIL import Image; import numpy as np
SRC,OUT=sys.argv[1],sys.argv[2]
H=lambda c:[int(c[i:i+2],16) for i in (1,3,5)]
PAL=['#292018','#b5f3b6','#72d779','#67b370','#467e4b','#3f6036','#9cf08d','#a0846a','#725641','#3d3827','#8c6246','#aba09a','#7b7c7e','#4a443c']
o=np.load(SRC); used=[v for v in range(1,15) if (o==v).any()]
m=np.zeros(16,int)
for n,v in enumerate(used): m[v]=n+1
q=m[o]; pal=[0,0,0]
for v in used: pal+=H(PAL[v-1])
pal+=[0]*(768-len(pal))
im=Image.fromarray(q.astype(np.uint8),'P'); im.putpalette(pal); im.save(OUT,transparency=0)
im=Image.open(OUT).convert('RGBA'); bg=Image.new('RGBA',im.size,'white')
Image.alpha_composite(bg,im).convert('RGB').resize((512,512),Image.NEAREST).save(OUT.replace('.png','_8x.png'))
print(OUT,'kleuren (zonder transparant):',len(used))
