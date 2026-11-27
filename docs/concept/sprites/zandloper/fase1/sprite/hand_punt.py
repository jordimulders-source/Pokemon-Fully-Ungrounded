# Handen per cel uit het model: kleur in het celmidden (puntmonster, 5x5 mediaan) i.p.v. stemmen.
import sys; from gemeen import *
k,bg=klassen_model(model())
def punt(i0,j0,i1,j1,fx=0.5,fy=0.5,r=2):
    out=np.zeros((j1-j0,i1-i0),int)
    for j in range(j0,j1):
        for i in range(i0,i1):
            x,y=s2m(i+fx,j+fy); x,y=int(x),int(y)
            b=k[y-r:y+r+1,x-r:x+r+1].ravel(); out[j-j0,i-i0]=np.bincount(b,minlength=16).argmax()
    return out
if __name__=='__main__':
    for box in [(8,28,21,40),(43,36,56,47)]:
        for f in [(0.5,0.5),(0.3,0.3),(0.7,0.7)]:
            o=punt(*box,*f); print(box,f)
            for r in o: print(''.join(CH[v] for v in r))
