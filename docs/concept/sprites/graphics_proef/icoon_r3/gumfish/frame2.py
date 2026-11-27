"""Frame 2 zoals bij de viscacha (PROMPT_ICOON.md): hele frame 1 (ook de staart) 1 px omlaag, één rij vervalt (vis zonder poten:
de effen lijfrij DROP), de onderkant blijft op dezelfde rij; één klein gebaar zonder pixelverlies: de bovenste 2 rijen van de
staartvin (y < STOP, x >= XS) 1 px naar links (zwiep, zoals de pluim van de viscacha).
python3 frame2.py -> icon.png (32x64, P, index 0 transparant) + icon_anim.gif"""
import os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
DROP,STOP,XS=23,17,25
I=Image.open(H+'icon_f1.png'); f1=np.array(I); f2=np.zeros_like(f1)
f2[DROP+1:]=f1[DROP+1:]; f2[1:DROP+1]=f1[0:DROP]
for y in range(0,STOP):                    # rijen van frame 1, in frame 2 op y+1
    seg=f2[y+1,XS:].copy()
    assert f2[y+1,XS-1]==0 or not seg.any(), 'zwiep zou een pixel overschrijven'
    f2[y+1,XS:]=0; f2[y+1,XS-1:31]=seg[:32-XS]
out=np.vstack([f1,f2]); im=Image.fromarray(out,'P'); im.putpalette(I.getpalette()); im.save(H+'icon.png',transparency=0)
P=I.getpalette(); fr=[]
for f in (f1,f2):
    a=Image.fromarray(f,'P'); a.putpalette(P); fr.append(Image.alpha_composite(Image.new('RGBA',(128,128),(98,156,131,255)),a.convert('RGBA').resize((128,128),Image.NEAREST)).convert('RGB'))
fr[0].save(H+'icon_anim.gif',save_all=True,append_images=[fr[1]],duration=300,loop=0)
from scipy import ndimage as nd
m2=f2>0; pad=np.pad(m2,1); edge=m2&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
print('frame 2: onderkant',np.nonzero(f1)[0].max(),'->',np.nonzero(f2)[0].max(),'| open randen',int((edge&(f2<14)).sum()),
      '| gaten',nd.label(nd.binary_fill_holes(m2)&~m2)[1],'| pixels f1',int((f1>0).sum()),'f2',int(m2.sum()),'(rij',DROP,'vervalt:',int((f1[DROP]>0).sum()),')')
