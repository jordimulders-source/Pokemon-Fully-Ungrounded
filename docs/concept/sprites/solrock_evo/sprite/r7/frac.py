# Per spritepixel: klasse-aandelen uit het originele 1024-model (11,87 x 11,87 px per spritepixel).
import sys,numpy as np; from PIL import Image
sys.path.insert(0,'../r6'); from klas import klas, S, X0, Y0
M=np.asarray(Image.open('../../referenties/model.png').convert('RGB')).astype(int)
def frac(x,y):
    a=M[int(round(Y0+y*S)):int(round(Y0+(y+1)*S)), int(round(X0+x*S)):int(round(X0+(x+1)*S))].reshape(-1,3)
    ks=[klas(p) for p in a]; n=len(ks)
    return {k:ks.count(k)/n for k in set(ks)}
if __name__=='__main__':
    x0,x1,y0,y1=[int(v) for v in sys.argv[1:5]]
    for y in range(y0,y1):
        row=[]
        for x in range(x0,x1):
            f=frac(x,y); s=sorted(f.items(),key=lambda t:-t[1])
            row.append(''.join(f'{k}{int(v*9.99)}' for k,v in s[:2]).ljust(4))
        print(y,' '.join(row))
    print('   ',' '.join(str(x).ljust(4) for x in range(x0,x1)))
