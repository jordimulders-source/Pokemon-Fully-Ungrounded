# Stap 1: kop van de Hitmontop-evolutie.
# Basis = Hitmontop frame 1, kop (x12-53, y32-57) verticaal gespiegeld (rechtop, hoorn boven).
# Gezicht (dome, ogen, wenkbrauwen, plooi, schaduw onder de rand) pixel voor pixel uit Hitmontop;
# oogrijen teruggezet zodat de glans weer linksboven zit; glans van de dome naar linksboven.
# De rand (brim) blijft als silhouet en wordt bruine dreads (met de hand, per pixel geplaatst):
# drie strengen naar voren/omhoog naar de knot onder de hoorn, twee links omlaag, twee rechts; hoorn klein.
# Handen en lijf weg. Kolom = Hitmontop-kolom - 12, rij = 57 - Hitmontop-rij.
from PIL import Image
from pal import PAL, ch2i
SEG = {
 4: [(19,"ff")],
 5: [(18,"f23f")],
 6: [(15,"fff2334ffff")],
 7: [(13,"ff"),(15,"455e455e45e"),(26,"ffff")],
 8: [(12,"f"),(13,"4e455e455e4554444"),(30,"fff")],
 9: [(11,"f"),(12,"45e455e455e455554444"),(32,"ff")],
10: [(9,"ff"),(11,"455e455e4eeeeee5555554"),(33,"ff")],
11: [(7,"ff"),(9,"455e455"),(16,"eeee"),(20,"f44445ff"),(28,"eeee5e"),(34,"f")],
12: [(7,"f"),(8,"455e4"),(13,"f55223333ff4444ff"),(30,"ffff")],
13: [(7,"f"),(8,"455e"),(12,"f22333333f1ff44444f")],
14: [(6,"f"),(7,"455e"),(11,"f3ff333333ffff44444f")],
15: [(6,"f"),(7,"455e"),(11,"ff1ff333333ff334444f")],
16: [(5,"f"),(6,"455e"),(10,"f3ffff33333333333444f")],
17: [(4,"f"),(5,"4555e"),(10,"f33ff333555333333344f")],
18: [(4,"f"),(5,"4555e"),(10,"f333333533355333334 4f")],
19: [(4,"f"),(5,"4555e"),(10,"f3333333333335333444f")],
20: [(5,"f"),(6,"4555e"),(11,"f33333333333334444f")],
21: [(5,"f"),(6,"55e45"),(11,"f4333333333444444f")],
22: [(6,"fff45e"),(12,"f4333334444444f")],
23: [(8,"f5ef"),(12,"ff44444444444f")],
24: [(9,"ff"),(14,"fffffffffff")],
}
def kop():
    g=[[0]*42 for _ in range(26)]
    for y,segs in SEG.items():
        for x0,s in segs:
            s=s.replace(' ','')
            for i,c in enumerate(s):
                if c!='.': g[y][x0+i]=ch2i(c)
    return g
def save(g,fn):
    im=Image.new('P',(len(g[0]),len(g))); im.putpalette([v for c in PAL for v in c]+[0]*(768-48))
    im.putdata([v for r in g for v in r]); im.save(fn)
def dump(g):
    return ['%2d '%y+''.join('.' if v==0 else '%x'%v for v in r) for y,r in enumerate(g)]
if __name__=='__main__':
    g=kop(); save(g,'kop_raw.png'); print('\n'.join(dump(g)))
