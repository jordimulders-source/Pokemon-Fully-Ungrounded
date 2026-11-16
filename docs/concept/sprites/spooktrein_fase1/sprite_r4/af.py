# Reparatie 5 + afronden: #b39b87 (index 6) opgeheven -> #9f7e65; selout opnieuw (wiel had nieuwe randlijn).
import numpy as np
o=np.load('bout.npy').copy(); n6=(o==6).sum(); o[o==6]=5
np.save('grens.npy',o); print('tint #b39b87 -> #9f7e65:',n6)
