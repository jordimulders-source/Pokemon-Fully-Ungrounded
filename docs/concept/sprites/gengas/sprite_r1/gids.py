# gids.py: meetkaart om met de hand te tekenen: bolcirkel (middelpunt 30,35.5, r 22.5) als ring 'O',
# modelklasse binnen/buiten (meet.py), Gengar-gezicht op plek A als hoofdletters G(rood) W(wit/grijs) e/d/f.
import sys,numpy as np; sys.path.insert(0,'.')
from meet import klas; from gezicht_px import face
CX,CY,R=30,35.5,22.5
def inb(x,y): return (x-CX)**2+(y-CY)**2<=R*R
f=face()
print('    '+''.join(str(x%10) for x in range(64)))
for y in range(64):
    r=''
    for x in range(64):
        if (x,y) in f:
            v=f[(x,y)]; r+={5:'G',6:'H',1:'W',2:'V',7:'U',3:'T',14:'e',13:'d',15:'f'}[v]
        elif inb(x,y) and not all(inb(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): r+='O'
        else:
            k=klas(x,y); r+= k if inb(x,y) else (k if k in '.' else k.lower() if k.isalpha() else {'1':'#','2':':','3':';','4':'-','5':'+','6':'*'}.get(k,k))
    print('%3d '%y+r)
