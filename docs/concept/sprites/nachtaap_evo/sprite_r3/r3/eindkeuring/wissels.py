# Eindkeuring Moonkey r3 (19 nov): wissels ((x, y), van, naar) op frame 1 (y 0-63); frame 2 = zelfde (kopie).
# Indexen van r3/normal.pal (1 zwart, 2 selout, 3/4/5 paars schaduw/basis/licht, 6 lavendel, F blauw).
# Alleen tintwissels binnen bestaande vlakken; silhouet, maan, ogen en kop blijven gelijk.
WISSELS = [
    # 1 hoog: open buitenrand bovenop de staartkrul (3 zonder lijn tegen de lucht, lichtkant); oude sprite had hier 2
    ((51,10),3,2),((52,10),3,2),((49,11),3,2),((50,11),3,2),
    # 2 midden: open buitenranden (3 zonder lijn): linkerbovenhoek rug en linkerrand nabije voorpoot
    ((20,29),3,2),((22,55),3,2),
    # 3 midden: zwart in de gekleurde selout bovenop de rug (2-2-1-1-2-2 = om en om, op de lichtkant)
    ((37,29),1,2),((38,29),1,2),
    # 4 laag: naad kop/rug 2-2-1-1-2-2-1: zwart midden in de lijn; lijn taps maken (2 boven, 1 pas vanaf (25,38))
    ((21,36),1,2),((22,37),1,2),
    # 5 laag: losse 2-px 4-strook tussen lijn x39 en de blauwe streep/lavendel vlek bij de staartvoet
    ((40,33),4,0xF),((40,34),4,6),
    # 6 laag: 5-strook op de achterpoot direct onder de buiklijn y54 (slagschaduw van de buik; 5 naast 3 slaat 4 over); oud = 4
    ((42,55),5,4),((43,55),5,4),((44,55),5,4),
    # 7 laag: 2-px 4-vlekje op de verre voorpoot boven de voet (verre poot hoort egaal in 3)
    ((11,58),4,3),((12,58),4,3),
    # 8 optioneel: hooglicht op de heup (nu één vlak 4 van ±10x10); kleine sikkel langs de dijlijn x36
    ((38,44),4,5),((39,44),4,5),((38,45),4,5),((37,46),4,5),((38,46),4,5),((37,47),4,5),
]

if __name__ == "__main__":
    import sys
    from PIL import Image
    import numpy as np
    src = sys.argv[1] if len(sys.argv) > 1 else "../anim_front.png"
    dst = sys.argv[2] if len(sys.argv) > 2 else "voorstel_anim_front.png"
    zonder8 = "--zonder8" in sys.argv
    im = Image.open(src); a = np.array(im)
    n = 0
    for i, ((x, y), v, w) in enumerate(WISSELS):
        if zonder8 and i >= len(WISSELS) - 6:
            break
        for oy in (0, 64):
            assert a[y+oy, x] == v, ((x, y+oy), a[y+oy, x], v)
            a[y+oy, x] = w
        n += 1
    out = Image.fromarray(a, "P"); out.putpalette(im.getpalette())
    out.save(dst, transparency=0)
    print(n, "wissels ->", dst)
