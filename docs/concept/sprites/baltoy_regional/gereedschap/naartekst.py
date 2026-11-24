# Kale reductie 48 -> tekstraster in het spritepalet (kaal48.txt). Klassen -> letters:
# K zwart, D donkere lijn, d relief/donker, m schaduw/zijvlak (model m en M samen), l licht, h hooglicht, R rood licht, r rood donker. '.' = transparant.
import sys, numpy as np; sys.path.insert(0,'gereedschap'); import schrap as S
kk,rr,rows,cols,*_=S.schrap_zones(48); np.save('gereedschap/kaal48_k.npy',kk); np.save('gereedschap/kaal48_rgb.npy',rr)
L='.KDdmmlhRr'
open('gereedschap/kaal48.txt','w').write('\n'.join(''.join(L[v] for v in r) for r in kk)+'\n')
open('gereedschap/kaal48_bron.txt','w').write('rijen geschrapt: %s\nkolommen geschrapt: %s\n'%(list(map(int,rows)),list(map(int,cols))))
