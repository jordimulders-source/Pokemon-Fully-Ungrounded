# Palet DJ Rotom kleur1 (index: naam, kleur). Oranje = game-Rotom-oranje (bron #e2673c ~ game #e87028).
def g(h):
    v=[int(h[i:i+2],16) for i in (0,2,4)]
    return tuple(int(round(c/255*31))*255//31 for c in v)
PAL=[('transparant','98d0a0'),
 ('gloed donker (buitenrand)','40a878'),('gloed midden','80d8a8'),('gloed licht / plasma','c8f4d8'),
 ('oranje hooglicht','f8a880'),('oranje basis','e87028'),('oranje schaduw','c04818'),('oranje donker','783820'),
 ('zwart','101010'),
 ('speakerfront navy','1c2234'),('conus ring','3c4458'),('conus glans grijs','a8b0c0'),
 ('iris donker','3890a8'),('iris licht','70d0d8'),
 ('equalizer groen','30d898'),('wit','f8f8f8')]
COLS=[g(h) for _,h in PAL]
if __name__=='__main__':
    import sys
    with open(sys.argv[1],'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in COLS: f.write('%d %d %d\n'%c)
