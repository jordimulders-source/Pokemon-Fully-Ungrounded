# kraag.py: krulvachtrand van de echte Bibarel (graphics/pokemon/bibarel/anim_front.png frame 1) pixel voor pixel overnemen,
# omgezet naar ons bruinpalet (Bibarel 1 lijn->2, 2 midden->4, 4 donker->3, 3 zwart->1), als geheel verschoven naar de kraagplek
# van het model. Alleen bruin/lijn wordt geplakt, alleen op pixels die nu kraag (bruin) zijn: gezicht, stam/hand en silhouet blijven.
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image
B=np.array(Image.open('../../../../graphics/pokemon/bibarel/anim_front.png'))[:64].astype(int)
MAP={1:2,2:4,4:3,3:1}
BUITEN=np.zeros((64,64),bool)   # kraagzone-pixels waar de Bibarel-uitsnede achtergrond is (achter de bolletjes)
def plak(o,bx0,by0,bx1,by1,dx,dy,mag,log,naam,zwart_houden=False):
    r1=o.copy()
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            v=B[y,x]; X,Y=x+dx,y+dy
            if not (0<=X<64 and 0<=Y<64 and mag[Y,X]): continue
            if v==0: BUITEN[Y,X]=True
            if v not in MAP: continue
            w=MAP[v]
            # Bibarel-zwart is daar buitenrand; bij ons ligt de kraag binnen de figuur -> binnenlijn 2, behalve waar r1 al zwart had
            if w==1 and not zwart_houden and r1[Y,X]!=1 and all(o[Y+ddy,X+ddx]!=0 for ddy,ddx in ((-1,0),(1,0),(0,-1),(0,1))): w=2
            if o[Y,X]!=w: o[Y,X]=w; log.append((X,Y,naam))
ZONE=np.zeros((64,64),bool)
ZONE[15:28,35:42]=True      # rechterwang tot de lijn met de stam (x41)
ZONE[15:28,18:21]=True      # linkerwang tussen hand/stam en gezicht
ZONE[27:31,19:39]=True      # onder de kaak, boven het borststuk
ZONE[14:27,20:35]=False     # gezicht
def kraag(o,log):
    o=o.copy()
    mag=ZONE&np.isin(o,(1,2,3,4,5))
    mag[:,41]&=True
    voor=o.copy()
    plak(o,31,13,38,24,4,1,mag,log,'kraag rechts',zwart_houden=True)   # rechts = schaduwkant: Bibarel-zwart blijft zwart     # buitenrand Bibarel-wang (x37) -> modellijn kraag/stam (x41), ogen y14 -> y15
    plak(o,10,13,12,22,8,1,mag,log,'kraag links')      # binnenste kolommen van de linkerwang (links zit de hand)
    plak(o,21,25,30,27,8,2,mag,log,'kraag onder')      # onderlip/kinvacht onder de tanden (tandonderkant y25 -> y27)
    geplakt=np.zeros((64,64),bool)
    for X,Y,_ in log: geplakt[Y,X]=True
    # wat in de kraagzone niet door een Bibarel-pixel bedekt is en niet de buitenlijn is: basistint van de Bibarel-kraag (2 -> 4)
    P=np.pad(voor>0,1); rand=(voor>0)&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
    for Y,X in zip(*np.where(mag&~geplakt&~rand)):
        w=3 if BUITEN[Y,X] else 4      # achter de bolletjes donker, binnen de wang de basistint (Bibarel 2 -> 4)
        if o[Y,X]!=w and o[Y,X]!=1: o[Y,X]=w; log.append((X,Y,'kraag basistint'))
    return o
if __name__=='__main__':
    o=laad('sprite_r1/sprite.png'); log=[]; k=kraag(o,log); print(len(log))
    opslaan(k,'sprite_r2/_kraagtest.png',12)
