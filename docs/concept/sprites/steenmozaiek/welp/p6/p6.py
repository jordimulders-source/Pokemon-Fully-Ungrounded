# p6: alleen het voorhoofd. Elke voorhoofdpixel (y20-25, x12-24, geen r11-lijn) opnieuw ingekleurd naar het model
# (sample.py: lila haarspeld, U open naar rechts, bocht linksonder; groef ertussen): basisbruin (p1/basis.npy) + golf.
import numpy as np
from PIL import Image
P5=np.array(Image.open('../p5/welp_p5.png')); R=np.array(Image.open('../r11/welp_r11.png')); B=np.load('../p1/basis.npy')
PAL=Image.open('../r11/welp_r11.png').getpalette()
# U = bovenarm, W = onderarm/bocht, g = groef (rij 20 begint op x12)
GOLF='''
....UUUUUU...
..UUUUggg....
.UUgggWWW....
UUgWWW.......
UgWW.........
WWW..........
'''
def maak(groef):
    a=P5.copy()
    for y in range(20,26):
        for x in range(12,25):
            if R[y,x] not in (1,2) and a[y,x]!=0: a[y,x]=B[y,x]
    for j,row in enumerate(GOLF.strip('\n').split('\n')):
        for i,ch in enumerate(row):
            x,y=12+i,20+j
            if ch=='.' or R[y,x] in (1,2): continue
            licht=B[y,x] in (5,14)
            if ch=='U': a[y,x]=8
            elif ch=='W': a[y,x]=8 if licht else 7
            else: a[y,x]=groef
    # schaduwrand: lila pixel waarvan de buur eronder bruin is en die op donker bruin ligt -> 7 (onderkant golf)
    b=a.copy(); G={(12+i,20+j) for j,row in enumerate(GOLF.strip('\n').split('\n')) for i,ch in enumerate(row) if ch!='.'}
    for y in range(20,26):
        for x in range(12,25):
            if a[y,x]==8 and (x,y+1) not in G and B[y,x]==3: b[y,x]=7
    return b
def bewaar(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save(naam+'.png',transparency=0)
    q=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
if __name__=='__main__':
    bewaar(maak(3),'welp_p6_A')   # groef bruin 3 (zoals het model)
    bewaar(maak(6),'welp_p6_B')   # groef donkerlila 6
