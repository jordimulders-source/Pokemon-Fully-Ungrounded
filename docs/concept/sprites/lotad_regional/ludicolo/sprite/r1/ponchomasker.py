# Ponchogebied (alleen hierbinnen mogen de varianten A/B/C afwijken). Rode/zwarte pixels van het lijf onder hoed en gezicht,
# zonder gezicht, armen (olijf), linkervoet, rechterbeen en staart. Grenzen gemeten op basis0 (zie NOTITIE).
import numpy as np
def masker(o):
    P=np.zeros((64,64),bool)
    for y in range(24,56):
        for x in range(8,52):
            k=o[y,x]
            if k==0 or k in (8,9,10,11,12,13): continue
            if y<=34 and 15<=x<=35: continue                 # gezicht (snavel, ogen, oogmasker)
            if y<=27: continue                                # onder de hoedrand: alleen vanaf rij 28
            if y>=50 and x<=17+(y-50): continue               # linkervoet (onder de diagonale ponchorand (17,50)-(22,55))
            if y>=47 and x>=32-(y-47): continue               # rechterbeen (rechts van de ponchorand (32,47)-(24,55))
            if x>=44 and y>=44: continue                      # staart
            if k==1 and any(o[y+dy,x+dx] in (0,8,9,10,11) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): continue  # buitenlijn / lijn tegen de arm
            if x<=12 and y>=37: continue                      # linkerarm
            P[y,x]=True
    return P
