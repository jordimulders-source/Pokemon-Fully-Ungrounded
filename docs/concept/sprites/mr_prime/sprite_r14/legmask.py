import numpy as np; from PIL import Image
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mr_prime/sprite_r1')
from bgmask import bgmask
N=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mr_prime/sprite_r1/natief.png').convert('RGB'))
BG=bgmask(N); Lum=N.astype(int).mean(axis=2)
H,W=BG.shape; yy,xx=np.mgrid[0:H,0:W]
def Lline(x): return 130+(x-120)*(9/27)
def Bline(x): return 144+(x-117)*0.36
leg=(~BG)&(xx>=113)&(yy>=Lline(xx)-0.5)&(yy>=126)&((yy<=Bline(xx)+1.2)|(xx>=150))
# alles rechts van de jaskant onder L is been
if __name__=='__main__':
    x0,x1,y0,y1=100,186,120,178
    for y in range(y0,y1):
        s=''
        for x in range(x0,x1):
            if BG[y,x]: s+=' '
            else:
                c='@#%*+=-:.'[min(8,int(Lum[y,x])//28)]
                s+= c if not leg[y,x] else {'@':'0','#':'1','%':'2','*':'3','+':'4','=':'5','-':'6',':':'7','.':'8'}[c]
        print('%3d '%y+s)
    print('    '+''.join(str((x//10)%10) for x in range(x0,x1)))
    print('    '+''.join(str(x%10) for x in range(x0,x1)))
