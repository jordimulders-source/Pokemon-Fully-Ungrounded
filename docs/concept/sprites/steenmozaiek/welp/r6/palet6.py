# Palet r6: bruin opgehelderd met Gen 3-stappen (~38 helderheid) + 4e bruintint H (hooglicht) voor de lichtste modelvlakken.
import numpy as np
F=np.load('FIN2.npy').astype(int).tolist()
F[3]=[118,74,64]    # S  (was 99,62,57)
F[4]=[166,110,93]   # M  (was 148,99,86)
F[5]=[206,152,129]  # L  (was 186,141,126)
F.append([236,194,166]) # 14 H  hooglicht
F[8]=[192,170,204]  # R lila licht (was 172,152,177): meegeschoven met het bruin, verhouding model (lila ~1,6x mid)
F[7]=[158,132,160]  # Q lila schaduw (was 148,121,142)
np.save('FIN6.npy',np.array(F,dtype=np.uint8))
for i,c in enumerate(F): print(i,c,int(0.299*c[0]+0.587*c[1]+0.114*c[2]))
