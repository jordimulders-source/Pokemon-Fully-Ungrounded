# Bouwt de olinguito (ronde 8) uit de handgetekende tekstrasters in deze map.
# Geen vormfuncties, geen automatische schaduw of omlijning: elke pixel staat in de .txt-bestanden.
# Gebruik: python3 build.py <uit.png> deel.txt,x,y [deel.txt,x,y ...]   (achterste deel eerst)
import re, sys, os
from PIL import Image
B = os.path.dirname(os.path.abspath(__file__))
PAL = [(152,208,160),(16,12,18),(44,28,28),(68,44,38),(98,64,50),(136,94,70),
       (172,140,104),(220,192,146),(246,232,198),(118,110,114),(190,182,178),(238,234,226),
       (252,252,252),(236,180,56),(170,98,34),(150,46,52)]
# tekens: . transparant | 0 zwart | 1 omlijning-bruin | 2 schaduw | 3 basis | 4 hooglicht
# 5 6 7 room (schaduw/basis/hooglicht) | 8 9 a klauw (schaduw/basis/hooglicht) | b wit
# c goud | d donkergoud | e rood
CH = {'.':0,'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':7,'7':8,'8':9,'9':10,'a':11,'b':12,'c':13,'d':14,'e':15}

def part(name):
    rows = {}
    for ln in open(os.path.join(B, name)):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'):
            continue
        y, rest = ln.split(':', 1)
        px = {}
        for x, s in re.findall(r'(\d+)"([^"]*)"', rest):
            s = s.replace(' ', '')
            # schrijfgemak: 2{5} = 22222 (een handgekozen reeks van dezelfde pixel)
            s = re.sub(r'(.)\{(\d+)\}', lambda m: m.group(1) * int(m.group(2)), s)
            for i, c in enumerate(s):
                if c != '.':
                    px[int(x) + i] = CH[c]
        rows.setdefault(int(y), {}).update(px)  # latere regels liggen er bovenop
    return rows

def compose(layers, W=64, H=64):
    g = [[0] * W for _ in range(H)]
    for name, ox, oy in layers:
        for y, px in part(name).items():
            for x, v in px.items():
                X, Y = x + ox, y + oy
                if 0 <= X < W and 0 <= Y < H:
                    g[Y][X] = v
    return g

def img(g):
    im = Image.new('P', (len(g[0]), len(g)))
    flat = []
    for c in PAL:
        flat += c
    im.putpalette(flat + [0] * (768 - len(flat)))
    im.putdata([v for r in g for v in r])
    return im

if __name__ == '__main__':
    layers = []
    for a in sys.argv[2:]:
        n, x, y = a.split(',')
        layers.append((n, int(x), int(y)))
    g = compose(layers)
    img(g).convert('RGB').resize((64 * 8, 64 * 8), Image.NEAREST).save(sys.argv[1])
