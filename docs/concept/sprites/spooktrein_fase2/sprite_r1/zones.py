# telt per zone de pixels die afwijken van de kale reductie (basis -> post)
import sys,numpy as np
for V in 'AB':
    b=np.load(f'basis_{V}.npy'); o=np.load(f'post_{V}.npy'); d=b!=o
    s,X0,Y0,oy,XC,k=[float(v) for v in open(f'basis_{V}.meta').read().split()]
    top=(98-Y0)*s+oy; bot=(140-Y0)*s+oy     # model: wagonrand y~98, onderkant wagon y~140 (natief)
    z={'geest (kop/armen/vuist)':0,'wagon (hout/staal/barsten)':0,'wielen':0,'staart':0}
    for y,x in zip(*np.where(d)):
        g=o[y,x] in (2,3,4,5) or b[y,x] in (2,3,4,5,6)
        if o[y,x] in (12,13) or (b[y,x] in (12,13)) or (y>=top+8 and y<=top+14 and x<20 and o[y,x] in (1,14)): z['wielen']+=1
        elif g and y<top+2: z['geest (kop/armen/vuist)']+=1
        elif g and y>bot-4: z['staart']+=1
        else: z['wagon (hout/staal/barsten)']+=1
    print(V,'totaal',d.sum(),z)
