"""r4: kopie van icoon_r3/sunperor/frame2.py; enige wijziging: de staf zakt mee (zie hieronder), alleen de vleugel maakt het gebaar.
Frame 2 zoals bij de viscacha (PROMPT_ICOON.md): hele frame 1 1 px omlaag, de bovenste pootrij (DROP) vervalt, de voeten blijven
op dezelfde rij; twee kleine gebaren zonder pixelverlies: de staf (x 9-11, rij 16-22) en de geheven vleugel (handpennen + onderarm, x 18-25,
rij 13-20, alleen vleugelpixels) zakken niet mee: de staf gaat 1 px omhoog (steel onderaan 1 px langer), de vleugel zwaait 1 px omhoog.
python3 frame2.py -> icon.png (32x64, P, index 0 transparant) + icon_anim.gif"""
import os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))+'/'
DROP=27; ZY=(15,22); ZX=(9,11)
I=Image.open(H+'icon_f1.png'); f1=np.array(I); f2=np.zeros_like(f1)
f2[DROP+1:]=f1[DROP+1:]; f2[1:DROP+1]=f1[0:DROP]
# r4: de staf zakt mee (in r4 deelt de kop zijn linkeromlijning x11 met de stafkop; een stilstaande staf zou die omlijning in frame 2 wissen)
# vleugel: de pixels die poets.py in de zone 'vleugel' zette (zelfde rasters), op hun frame 1-plek
V=[(13,23,'ff'),(14,22,'f66f'),(15,22,'f61f'),(16,22,'f61f'),(17,18,'ffff61e'),(18,18,'66666e'),(19,18,'11111e'),(20,18,'eeeee')]
vm=np.zeros_like(f1,bool)
for y,x0,r in V:
    for i,ch in enumerate(r): vm[y,x0+i]=True
sh=np.zeros_like(vm); sh[1:DROP+1]=vm[0:DROP]
f2[sh&~vm]=0                                  # verschoven vleugelkopie weg
f2[vm]=f1[vm]                                 # vleugel op zijn plek
# onder de onderarm schuift het lijf 1 px omlaag: de rand van het lijf op rij 21 (x18-19) dicht met omlijning
for x in (18,19):
    if f2[21,x]==0 and (f2[22,x]>0 or f2[21,x-1]>0): f2[21,x]=14
out=np.vstack([f1,f2]); im=Image.fromarray(out,'P'); im.putpalette(I.getpalette()); im.save(H+'icon.png',transparency=0)
P=I.getpalette(); fr=[]
for f in (f1,f2):
    a=Image.fromarray(f,'P'); a.putpalette(P); fr.append(Image.alpha_composite(Image.new('RGBA',(128,128),(98,156,131,255)),a.convert('RGBA').resize((128,128),Image.NEAREST)).convert('RGB'))
fr[0].save(H+'icon_anim.gif',save_all=True,append_images=[fr[1]],duration=300,loop=0)
from scipy import ndimage as nd
m2=f2>0; pad=np.pad(m2,1); edge=m2&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
print('frame 2: onderkant',np.nonzero(f1)[0].max(),'->',np.nonzero(f2)[0].max(),'| open randen',int((edge&(f2<14)).sum()),
      '| gaten',nd.label(nd.binary_fill_holes(m2)&~m2)[1],'| pixels f1',int((f1>0).sum()),'f2',int(m2.sum()),'(rij',DROP,'vervalt:',int((f1[DROP]>0).sum()),')')
