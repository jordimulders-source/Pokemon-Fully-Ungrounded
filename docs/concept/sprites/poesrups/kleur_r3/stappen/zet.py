# zet.py bron.txt doel.txt "y,x,c" ... : losse handmatige pixelwijzigingen in een tekstraster (handwerk, geen generatie)
import sys
L=open(sys.argv[1]).read().split('\n')
def setpx(rows,y,x,c):
    for i,l in enumerate(rows):
        if l.startswith(f'{y}:'):
            head,rest=l.split(':',1); toks=rest.split(); stuk=[]
            for t in toks:
                if '=' in t: stuk.append([int(t.split('=')[0]),t.split('=')[1]])
                else: stuk[-1][1]+=t
            for s in stuk:
                if s[0]<=x<s[0]+len(s[1]):
                    s[1]=s[1][:x-s[0]]+c+s[1][x-s[0]+1:]
                    rows[i]=f'{y}: '+' '.join(f'{a}={b}' for a,b in stuk); return
    raise SystemExit(f'pixel {x},{y} niet in het raster')
for a in sys.argv[3:]:
    y,x,c=a.split(','); setpx(L,int(y),int(x),c)
open(sys.argv[2],'w').write('\n'.join(L))
