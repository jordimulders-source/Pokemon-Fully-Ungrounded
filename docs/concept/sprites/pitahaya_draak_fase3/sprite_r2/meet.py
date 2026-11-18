# Meting per spritepixel in een zone: achtergrond-, zwart-, groenfractie en gem. helderheid van de groene modelpixels
import sys,numpy as np; from groepen import laad
x0,y0,x1,y1=map(int,sys.argv[1:5]); NAT=sys.argv[5] if len(sys.argv)>5 else 'natief.png'
a,lum,g=laad(NAT); i=np.load('kaal_info.npz'); geo=i['geo']
S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
gu=np.repeat(np.repeat(g,4,0),4,1); lu=np.repeat(np.repeat(lum,4,0),4,1)
def win(X,Y):
    ny=by0-S+OY+S*(Y-Y0+ymin); nx=bx0-S+OX+S*(X-X0+xmin)
    return slice(int(round(4*ny)),int(round(4*(ny+S)))),slice(int(round(4*nx)),int(round(4*(nx+S))))
print('x/y: bg zwart groen lumgroen')
for Y in range(y0,y1):
    r=[]
    for X in range(x0,x1):
        sl=win(X,Y); gb=gu[sl]; n=gb.size; m=gb==4
        r.append('%2d/%2d/%2d/%3d'%(min(99,100*(gb==0).sum()//n),min(99,100*(gb==1).sum()//n),min(99,100*m.sum()//n),lu[sl][m].mean() if m.any() else 0))
    print('%2d '%Y+' '.join(r))
print('   '+' '.join('    %2d     '%X for X in range(x0,x1)))
