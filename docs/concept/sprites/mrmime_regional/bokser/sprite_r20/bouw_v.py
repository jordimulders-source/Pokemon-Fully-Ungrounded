# r20 bouw_v.py: V-patroon = de V van r18 ('V groot', zelfde pixels/plek als r7 v_groot), punt blijft op (30,33)
# zoals in r18 (Jordi: "de positie verandert niet vanuit het midden" / "alleen de vorm is anders in perspectief").
# Perspectief alleen door kolommen van de r18-V te schrappen (links: smaller) en te herhalen (rechts: breder);
# kolom 30 (de punt) blijft staan. Alleen op romppixels (7/8): kop, ballen en borstvuist blijven ervoor.
import numpy as np, sys
sys.path.insert(0,'../sprite_r7'); from build import save
r18=np.load('../sprite_r18/bokser.npy'); r19ruw=np.load('../sprite_r19/ruw.npy')
V18={(int(x),int(y)) for y,x in zip(*np.where((r18==3)&np.isin(r19ruw,(7,8)))) if x>=26}   # de r18-V (alleen zichtbare pixels)
PUNT=30
def perspectief(schrap,herhaal):
    # links van de punt: geschrapte kolommen vallen weg, alles links ervan schuift 1 naar rechts (naar de punt)
    # rechts van de punt: herhaalde kolommen komen dubbel, alles rechts ervan schuift 1 naar rechts
    uit=set()
    for x,y in V18:
        if x<PUNT:
            if x in schrap: continue
            uit.add((x+sum(1 for s in schrap if s>x),y))
        elif x==PUNT: uit.add((x,y))
        else:
            nx=x+sum(1 for h in herhaal if h<x); uit.add((nx,y))
            if x in herhaal: uit.add((nx+1,y))
    return uit
VAR={'bokser':((27,),(31,)),'var_sterk':((27,28),(31,32))}
if __name__=='__main__':
    for naam,(s,h) in VAR.items():
        a=np.load('ruw.npy')
        assert a[22,25]==1; a[22,25]=4      # randpixel: bal loopt onder de wang door (enkele lijn = rompomlijning x26), tint 4 = baltint ernaast
        for x,y in perspectief(s,h):
            if a[y,x] in(7,8): a[y,x]=3
        save(a,naam if naam=='bokser' else 'var/'+naam)
        print(naam)
        for j in range(23,36): print('%2d '%j+''.join(str(v) if v else '.' for v in a[j,20:44]))
