# Ogen: natief modelblok (x43..63, y31..42) ingedikt door hele kolommen/rijen te schrappen (geen pixel getekend).
import sys; from gemeen import *
N=np.load('natief_k.npy')
X0,X1,Y0,Y1=43,63,31,42
VAR={'A':({46,52,59},{33,40}),'B':({46,52,58},{37}),'C':({50,52,59},{33}),'D':({46,52,59},{33}),'E':({46,52,59},set()),'F':({46,51,58},{34}),'G':({46,52,58,59},{37}),'H':({46,52,59,60},{37}),'J':({50,52,58},set()),'K':({49,52,58},set()),'L':({50,52,58},{37})}
def blok(v):
    dc,dr=VAR[v]
    cols=[x for x in range(X0,X1+1) if x not in dc]; rows=[y for y in range(Y0,Y1+1) if y not in dr]
    return N[np.ix_(rows,cols)],cols,rows
if __name__=='__main__':
    from PIL import ImageDraw
    Z=12; ims=[]
    nat=N[Y0:Y1+1,X0:X1+1]; ims.append(('natief',nat))
    for v in VAR: ims.append((v,blok(v)[0]))
    W=sum(b.shape[1]*Z+20 for _,b in ims); im=Image.new('RGB',(W,13*Z+30),'white'); d=ImageDraw.Draw(im); x=0
    for nm,b in ims:
        r=rgba(b,(255,255,255,255)).resize((b.shape[1]*Z,b.shape[0]*Z),0); im.paste(r,(x,24)); d.text((x,4),nm,fill='black'); x+=b.shape[1]*Z+20
    im.save('ogen_kandidaten.png')
