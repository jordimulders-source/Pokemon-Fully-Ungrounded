# c10: basis c9_2, cirkelzone (x23-29, y23-33) terug naar c7 A; dan een halve cirkel (U, open naar boven, zoals de boog
# op de foto-kop) rechts naast het nabije oog. Kerfstijl: groef 2, lip 5/14 direct onder/rechts, geen lip tussen groeven op 1 px.
import numpy as np
from PIL import Image
from basis import bevroren_kop
F=bevroren_kop()
VAR={
 '1': [(24,27),(24,28),(25,29),(26,29),(27,28),(27,27)],   # 4x3, kom op ooghoogte, naast de onderste helft van het oog
 '2': [(24,28),(24,29),(25,30),(26,30),(27,29),(27,28)],   # zelfde kom 1 px lager (wang)
}
def maak(t,v):
    a=np.array(Image.open(f'../c9/welp_c9_2{t}.png')); c7=np.array(Image.open(f'../c7/welp_c7_a{t}.png'))
    Z=np.zeros(a.shape,bool); Z[23:34,23:30]=True; a[Z]=c7[Z]; B=a.copy(); G=np.zeros(a.shape,bool)
    for x,y in VAR[v]:
        assert not F[y,x] and B[y,x] in (3,4,5),(x,y); G[y,x]=True; a[y,x]=2
    for x,y in VAR[v]:
        for ex,ey in ((0,1),(1,0)):
            X,Y=x+ex,y+ey
            if G[Y,X] or F[Y,X] or B[Y,X] not in (3,4,5) or G[min(Y+ey,63),min(X+ex,63)]: continue
            a[Y,X]=14 if B[Y,X]==5 else 5
    return a, Image.open(f'../c9/welp_c9_2{t}.png').getpalette()[:48]
if __name__=='__main__':
    for v in VAR:
        for t in ('','_grijs'):
            a,pal=maak(t,v); n=f'welp_c10_{v}{t}'
            im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal+[0]*(768-48)); im.save(n+'.png',transparency=0)
            r=Image.open(n+'.png').convert('RGBA'); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r)
            bg.resize((512,512),Image.NEAREST).save(n+'_8x.png')
