# Bewaakt r4: silhouet gelijk aan r3 (A, oog 1 links) behalve de rugzone (rijen 12-34, x >= 24); patronen en kenmerken ongewijzigd van plek.
import sys, numpy as np
r3=np.load('welp_r3_A_oog1.npy'); a=np.load(sys.argv[1] if len(sys.argv)>1 else 'welp_r4.npy')
diff=(r3>0)!=(a>0); rug=np.zeros_like(diff); rug[12:35,24:]=True
buiten=int((diff&~rug).sum()); print('silhouet-diff rug:',int((diff&rug).sum()),'| buiten de rug:',buiten)
pat3=np.isin(r3,[6,7,8,11,10,12,13,9]); pat4=np.isin(a,[6,7,8,11,10,12,13,9])
moved=int((pat3!=pat4)[~rug].sum()); print('patroon/kenmerkpixels (lila, creme, oog, tand, tong) verplaatst buiten de rug:',moved)
fig=(a>0).sum(); print('zwart %.1f%% (r3 %.1f%%), lijnbruin %.1f%%'%(100*(a==1).sum()/fig,100*(r3==1).sum()/(r3>0).sum(),100*(a==2).sum()/fig))
print('bruintinten:',sorted({int(v) for v in a.ravel() if v in (3,4,5)}),'kleuren:',len(set(a.ravel()))-1)
ok=buiten==0 and moved==0; print('OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
