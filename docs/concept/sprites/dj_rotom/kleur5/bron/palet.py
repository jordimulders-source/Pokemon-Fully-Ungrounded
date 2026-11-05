# Palet DJ Rotom kleur5: oranje, wit, grijs en index 0 op de exacte game-Rotom-waarden; gloed, navy, iris, equalizer = kleur4.
def g(h):
    v=[int(h[i:i+2],16) for i in (0,2,4)]
    return tuple(int(round(c/255*31))*255//31 for c in v)
PAL=[('transparant',(152,208,160)),
 ('gloed donker','40a878'),('gloed midden','80d8a8'),('gloed licht / plasma','c8f4d8'),
 ('oranje hooglicht',(248,168,128)),('oranje basis',(232,112,40)),('oranje schaduw',(192,72,24)),('oranje donker',(120,56,32)),
 ('zwart','101010'),('speakerfront navy','1c2234'),('conus ring','3c4458'),('grijs (glans/tanden)',(184,184,184)),
 ('iris donker','3890a8'),('iris licht','70d0d8'),('equalizer groen','30d898'),('wit',(248,248,248))]
COLS=[c if isinstance(c,tuple) else g(c) for _,c in PAL]
if __name__=='__main__':
    import sys
    with open(sys.argv[1],'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in COLS: f.write('%d %d %d\n'%c)
