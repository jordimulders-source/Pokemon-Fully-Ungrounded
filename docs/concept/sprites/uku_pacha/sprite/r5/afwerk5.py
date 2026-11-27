# Uku Pacha r5 laatste stap: strook van 2 px s tussen m en d bij (46-47,44-45), model 71-73 -> d
R=[list(l.rstrip('\n')) for l in open('raster_s.txt')][:64]
for x,y in ((46,44),(47,44),(47,45)): R[y][x]='d'
open('raster_af.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
