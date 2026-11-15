# Palet r7: bruin terug naar de modelkleur (keuring: gemeten op dezelfde pixels), lila/creme op modelwaarden,
# iris grijsbeige (g/G alleen in het oog), tweede roze U voor de tong. 16 kleuren incl. transparant.
import numpy as np
F=np.load('FIN6.npy').astype(int).tolist()
F[3]=[98,64,60]; F[4]=[136,96,88]; F[5]=[170,128,114]; F[14]=[204,166,148]
F[6]=[113,86,97]; F[7]=[148,121,142]; F[8]=[174,152,181]   # lila zoals model/r5
F[9]=[188,178,164]; F[13]=[138,126,118]                     # iris licht / schaduw (grijsbeige)
F.append([186,96,98])                                       # 15 U donkerroze tong
np.save('FIN7.npy',np.array(F,dtype=np.uint8))
for i,c in enumerate(F): print(i,c,int(0.299*c[0]+0.587*c[1]+0.114*c[2]))
