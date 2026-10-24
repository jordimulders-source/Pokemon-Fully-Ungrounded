# Frame 2: romp en kop zakken 2 px (ademhaling/neerduiken zoals Poochyena-frame 2); poten en staartpunt blijven staan.
import sys
r=[l.rstrip('\n').ljust(64,'.') for l in open(sys.argv[1])]
n=list(r)
for y in range(2,42): n[y]=r[y-2]
n[0]=n[1]='.'*64
# naad rij 41/42: romprand sluiten
row=list(n[41]); row[50]='1'; row[51]='1'; n[41]=''.join(row)
open(sys.argv[2],'w').write('\n'.join(n)+'\n')
