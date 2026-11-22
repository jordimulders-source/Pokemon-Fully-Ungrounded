# maak.py: hele keten r5 vanaf r4 (r4_ref.png) -> work.txt -> samba.png, samba_8x.png, samba_r5.npy, log_r5.json, vel.png
# volgorde: tooi (bovenste veren) -> geel2 (gele bladen) -> lijf (banden) -> lvleugel -> poten -> rvleugel -> romp -> onderveren -> rand
import numpy as np, subprocess; from PIL import Image
import tooi, geel2, lijf, lvleugel, poten, rvleugel, romp, onderveren, rand
a=np.array(Image.open('r4_ref.png')).astype(np.uint8)
a[2:13,15:52]=0; a=tooi.teken(a)
for m in (geel2,lijf,lvleugel,poten,rvleugel,romp,onderveren,rand): a=m.pas(a)
np.save('samba_r5.npy',a)
H='.123456789abcdef'
open('work.txt','w').write(''.join('%02d '%y+''.join(H[v] for v in a[y])+'\n' for y in range(64)))
for c in (['python3','palet_r5.py'],['python3','render.py'],['python3','check.py'],['python3','vel.py']): subprocess.run(c,check=True,stdout=subprocess.DEVNULL)
print('klaar')
