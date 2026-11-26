# Controle e2: silhouet, diff, 2x2-lijnclusters (index 1/2) in het gezichtsvak, snavelrand per kant.
import os, numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
a=np.array(Image.open(os.path.join(H,'..','af','ludicolo_gaucho.png'))); b=np.array(Image.open(os.path.join(H,'ludicolo_gaucho_e2.png')))
print('alpha-diff',int(((a>0)!=(b>0)).sum()),'| gewijzigd',int((a!=b).sum()),'| ogen (x19-31,y24-29) diff',int((a[24:30,19:32]!=b[24:30,19:32]).sum()))
L=lambda m:np.isin(m,[1,2])
for n,m in (('voor',a),('na',b)):
    c=[(x,y) for y in range(22,38) for x in range(13,38) if L(m[y:y+2,x:x+2]).all()]
    print(n,'2x2-lijnclusters in gezichtsvak:',c)
Y={12,13}
for n,m in (('voor',a),('na',b)):
    onder=[int(m[y,x]) for y in range(26,38) for x in range(14,37) if m[y,x] in (1,2) and m[y-1,x] in Y]
    zij=[int(m[y,x]) for y in range(26,38) for x in range(14,37) if m[y,x] in (1,2) and m[y-1,x] not in Y and (m[y,x-1] in Y or m[y,x+1] in Y)]
    print(n,'onder geel: zwart %d rood %d | zijkant: zwart %d rood %d'%(onder.count(1),onder.count(2),zij.count(1),zij.count(2)))
print('zwart-aandeel %.1f%% -> %.1f%%'%(100*(a==1).sum()/(a>0).sum(),100*(b==1).sum()/(b>0).sum()))
print('gebruikte indexen',sorted(np.unique(b).tolist()))
