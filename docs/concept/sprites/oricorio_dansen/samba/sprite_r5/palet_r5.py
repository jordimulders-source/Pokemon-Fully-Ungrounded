# palet_r5.py: schrijft palet.py voor r5 (alleen tinten; indexen gelijk aan r4). Oog/snavel (11-14) ongewijzigd.
# groen: licht geler, schaduw blauwer (hue 99/125/138/146 graden), stappen ~40 in helderheid;
# donkergeel 8 lichter (stap 60 -> ~42) en oranjer; blauw ongewijzigd.
PAL=[(152,208,160),(16,24,16),
     (144,216,104),(80,176,88),(48,128,72),(24,80,48),
     (248,232,96),(232,184,48),(192,136,32),
     (80,120,216),(40,64,152),
     (255,166,181),(191,105,120),(115,63,72),(252,252,252),(0,0,0)]
L=lambda c:0.299*c[0]+0.587*c[1]+0.114*c[2]
if __name__=='__main__':
    open('palet.py','w').write('# palet r5 (index 0 = transparant); gemaakt door palet_r5.py\nPAL=[\n'+''.join('    (%d,%d,%d),  # %d\n'%(c+(i,)) for i,c in enumerate(PAL))+']\n')
    for g in [(2,3,4,5),(6,7,8),(9,10),(11,12,13)]: print(g,[round(L(PAL[i])) for i in g])
