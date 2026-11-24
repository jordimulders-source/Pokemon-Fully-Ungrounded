# Proef: schrap opgegeven rijen/kolommen en toon op 8x naast elkaar. proef.py "r1,r2,.." "k1,k2,.." uit.png
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse, PAL
k,a=klasse()
rows=[int(v) for v in sys.argv[1].split(',')]; cols=[int(v) for v in sys.argv[2].split(',')]
kk=np.delete(np.delete(k,rows,0),cols,1); ys,xs=np.where(kk>0); kk=kk[ys.min():ys.max()+1,xs.min():xs.max()+1]
print(kk.shape)
P=np.array(PAL,'uint8'); im=Image.fromarray(P[kk]); im.resize((kk.shape[1]*8,kk.shape[0]*8),Image.NEAREST).save(sys.argv[3])
