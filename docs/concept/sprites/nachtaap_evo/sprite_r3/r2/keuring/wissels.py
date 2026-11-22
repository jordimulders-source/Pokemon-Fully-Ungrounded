# Keuring Moonkey r2 (19 nov): wissels ((x, y), van, naar) op frame 1 (y 0-63); frame 2 = zelfde (kopie).
# Indexen van r2/normal.pal. Alleen tintwissels binnen bestaande vlakken; silhouet blijft gelijk.
WISSELS = [
    # 1 midden: tweede lavendel 6-vlek (x36-38) links van de binnenlijn; de vlek bij de staartvoet (x41-43) is
    #   model + oude sprite en blijft. Twee 6-vlekken met een 2-lijn ertussen = rommelig, en 3 links van een licht vlak = omgekeerd.
    ((37,31),6,5),((37,32),6,5),((37,33),6,5),((38,33),6,5),((36,34),6,5),((37,34),6,5),((38,34),6,5),
    ((36,35),6,5),((37,35),6,5),((38,35),6,5),
    ((35,34),3,4),((34,35),3,4),((35,35),3,4),   # schaduw links van de (nu) lichte vlek: 3 naast 5 = omgekeerd
    # 2 midden: banding in het verre oor (5/4, dan rij 3, dan weer 4)
    ((23,39),3,4),((24,39),3,4),
    # 3 midden: achterpoot dichtbij volledig 3 onder een rechte 4/3-rand (y48/49): lichtkant van de poot in basis
    ((36,49),3,4),((37,49),3,4),((38,49),3,4),((39,49),3,4),((36,50),3,4),((37,50),3,4),((38,50),3,4),((37,51),3,4),
    # 4 laag: zwarte binnenlijn kop/rug aan de lichtkant + L-klontje
    ((19,35),1,2),((20,35),1,2),((21,37),1,5),
    # 5 laag: donkere 3 in de bovenste rugrand tussen de wiggen (licht moet daar het hoogst zijn)
    ((28,28),3,5),((29,28),3,5),
    # 6 laag: losse 2 in de staart (4-2-3 om en om)
    ((49,30),2,3),
    # 7 laag: kaakrij 5-5-3-4-3 (oude sprite had 5-5-4-4)
    ((13,54),3,4),
]

if __name__ == "__main__":
    import sys
    from PIL import Image
    import numpy as np
    src = sys.argv[1] if len(sys.argv) > 1 else "../anim_front.png"
    dst = sys.argv[2] if len(sys.argv) > 2 else "voorstel_anim_front.png"
    im = Image.open(src); a = np.array(im)
    for (x, y), v, n in WISSELS:
        for oy in (0, 64):
            assert a[y+oy, x] == v, ((x, y+oy), a[y+oy, x], v)
            a[y+oy, x] = n
    out = Image.fromarray(a, "P"); out.putpalette(im.getpalette()); out.info["transparency"] = 0
    out.save(dst, transparency=0)
    print(len(WISSELS), "wissels ->", dst)
