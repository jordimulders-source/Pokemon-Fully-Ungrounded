# naden: automatisch (modelrand lum<60, uitgedund) + benoemde correcties, elk op een modelrand
import numpy as np
s=np.load('r7w/seam_auto.npy').copy()
weg=[(28,9),(38,3),(39,4),(40,4),          # dubbel met de buitenlijn (modelomlijning ligt 1 px binnen het masker)
     (55,8),(56,9),(57,10),                 # idem linksonder
     (52,7),(53,7),(52,8),(42,2)]
bij=[(41,2),(42,3),(42,4),                  # bovenrand linkerschots (model (1,41)->(5,43))
     (46,18),                               # gat in de rand onder de kern-schots
     (47,24),(48,24),                       # onderbroken rand rechterschots doorgetrokken (model x24 r46-50)
     (52,9),(53,10),                        # linkerschots -> voetnaad op de modelrand
     (54,30),(54,31)]                       # bovenrand voetschots rechts doorgetrokken tot de buitenlijn
for p in weg: s[p]=False
for p in bij: s[p]=True
np.save('r7w/seam_hand.npy',s)
