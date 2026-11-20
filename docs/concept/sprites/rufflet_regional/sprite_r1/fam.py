# familie per natieve cel: K lijn (lum<70), Y geel, D donkergrijs (snavel/klauw/veerlijn, lum<105), G koel grijs, H warm wit/creme
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); bg=np.load('bg.npy')
R,G,B=a[...,0],a[...,1],a[...,2]; lum=(a@[0.299,0.587,0.114])
fam=np.full(bg.shape,'.'); f=~bg
fam[f&(lum<70)]='K'; fam[f&(lum>=70)&(R-B>40)]='Y'; rest=f&(fam=='.')
fam[rest&(lum<105)]='D'; cool=(B-R>=4); fam[rest&(lum>=105)&cool]='G'; fam[rest&(lum>=105)&~cool]='H'
np.save('fam.npy',fam)
