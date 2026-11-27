# Klasse per natieve pixel: 0 bg,1 zwart,2 groen,3 goud,4 creme,5 paars,6 wit(ingesloten)
import numpy as np; from PIL import Image
from collections import deque
def klassen():
    a=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kay_pacha/sprite/r1/natief.png')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]; L=a.mean(2)
    H,W=L.shape; K=np.zeros((H,W),int)
    light=a.min(2)>=228
    # achtergrond = licht en verbonden met rand
    bg=np.zeros((H,W),bool); q=deque([(0,0)]); bg[0,0]=1
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and light[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
    K[~bg]=4
    K[(g>r+12)&(g>=b)&~bg]=2
    K[(r-b>95)&(r>g+20)&~bg]=3
    K[(r>g+25)&(b>g+25)&~bg]=5
    K[(L<62)&~bg]=1
    K[light&~bg&(a.min(2)>=240)]=6
    return a,L,K
if __name__=='__main__':
    a,L,K=klassen()
    for k in range(1,7):
        v=L[K==k]; print(k,len(v),np.percentile(v,[5,25,50,75,95]).round() if len(v) else '')
    col=np.array([[255,255,255],[0,0,0],[0,160,0],[255,190,0],[230,220,180],[150,0,200],[255,0,0]],'uint8')
    Image.fromarray(col[K]).resize((800,800),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/98194ed8-9cf0-557f-9950-7fdf3aacfb0c/scratchpad/klas.png')
