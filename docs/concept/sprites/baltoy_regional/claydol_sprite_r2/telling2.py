# Telt per zone de pixels die afwijken van de kale reductie (kaal.npy = r2-model geschrapt + paletindex) en per stap (bouw2-log).
import numpy as np
K=np.load('claydol_sprite_r2/kaal.npy'); S=np.load('claydol_sprite_r2/sprite.npy'); V=np.load('claydol_sprite_r2/vlakken.npy')
Z=np.where(np.char.startswith(V,'krans'),'krans',V); Z=np.where(np.isin(Z,['oog','ring','neus']),'gezicht',Z)
Z=np.where(Z=='punt','kop',Z); Z=np.where((Z=='')&(S>0),'krans',Z)   # nieuwe pixels buiten het oude silhouet = bolletjes/gaatjes
d=K!=S
for z in ['gezicht','krans','kop','lijf','staf']: print(z,int((d&(Z==z)).sum()),'van',int(((Z==z)&((S>0)|(K>0))).sum()))
print('totaal',int(d.sum()))
