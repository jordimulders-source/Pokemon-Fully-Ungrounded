# python3 sprite/meet/px.py x,y [x,y ...]  (vanuit sneeuwbolslak_fase2/)
# Modelkleur per spritepixel: gemiddelde RGB, helderheid gem / p15 / max van het modelblok.
import sys,numpy as np; from PIL import Image
c=np.asarray(Image.open('sprite/r8_bol_r7.png').convert('RGB')).astype(float); L=c.mean(2)
X0,Y0,S,OX,OY=144,215,(973-144)/56,4,19
def blok(x,y):
    ya,yb=int(Y0+(y-OY)*S),int(Y0+(y-OY+1)*S); xa,xb=int(X0+(x-OX)*S),int(X0+(x-OX+1)*S)
    return c[ya:yb,xa:xb],L[ya:yb,xa:xb]
if __name__=='__main__':
    for a in sys.argv[1:]:
        x,y=map(int,a.split(',')); b,l=blok(x,y)
        if l.size==0: print(f'({x},{y}) buiten model'); continue
        print(f'({x},{y}) rgb {b.reshape(-1,3).mean(0).astype(int)}  L gem {l.mean():.0f} p15 {np.percentile(l,15):.0f} max {l.max():.0f}')
