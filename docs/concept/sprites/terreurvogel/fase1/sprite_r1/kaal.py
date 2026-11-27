# Kale reductie (vlakgemiddelde per groep + dichtstbijzijnde paletkleur) -> kaal.png/kaal.npy
import numpy as np; from lib import *
Sx,G2,ML=kaal(); np.save('kaal.npy',Sx); np.save('ml.npy',ML); np.save('groep.npy',G2); opslaan(Sx,'kaal.png')
yy_,xx_=np.where(Sx>0); print('bbox',xx_.min(),xx_.max(),yy_.min(),yy_.max(),'px',(Sx>0).sum())
rgba(Sx,k=10).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df86894d-b124-532a-bd91-e1c7851558e7/scratchpad/kaal10.png')
