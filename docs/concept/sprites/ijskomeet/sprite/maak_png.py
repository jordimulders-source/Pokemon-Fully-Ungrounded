# r1.txt -> r1.png (geindexeerd, index 0 transparant), r1_8x.png, vel_r1.png; plus alpha-diff met het bevroren silhouet.
import sys, numpy as np; from PIL import Image
from gio import from_txt
from pal import PAL
naam=sys.argv[1] if len(sys.argv)>1 else 'r1'
o=from_txt(naam+'.txt'); m=np.load('mask_r1.npy')
print('alpha-diff met mask_r1:',int(((o>=0)!=m).sum()))
idx=(o+1).astype('uint8')  # -1 -> 0
im=Image.fromarray(idx,'P'); pal=[255,255,255]+[v for c in PAL for v in c]; pal+= [0]*(768-len(pal)); im.putpalette(pal)
im.save(naam+'.png',transparency=0)
im2=Image.open(naam+'.png'); print(im2.mode,im2.size,'kleuren',len(set(np.asarray(im2).ravel())))
r=Image.open(naam+'.png').convert('RGBA').resize((512,512),Image.NEAREST)
bg=Image.new('RGBA',(512,512),(255,255,255,255)); bg.alpha_composite(r); bg.convert('RGB').save(naam+'_8x.png')
