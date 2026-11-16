# Model op treinschaal (mediaan celmidden uit model.webp, K=13,77 px per spritepx; sprite (0,2) = model (102,71)) voor de koeienvanger.
from PIL import Image; import numpy as np
m=Image.open('model/model.webp').convert('RGB'); K=13.77
X0=102; Y0=71-2*K
M=np.array(m).astype(int)
def cel(x,y,r=2): # mediaan van het celmidden (5x5 modelpx): houdt de modeltinten scherp
    cx=102+(x+0.5)*K; cy=71+(y-2+0.5)*K
    return np.median(M[int(cy-r):int(cy+r+1),int(cx-r):int(cx+r+1)].reshape(-1,3),axis=0)
B=np.array([[cel(x,y) for x in range(64)] for y in range(64)]).astype(int)
def soort(c):
    r,g,b=c
    if c.min()>215: return '.'
    if g>r+20: return 'g'
    L=0.3*r+0.59*g+0.11*b
    roest = r-b>45
    return ('R' if roest else 'S'), L
if __name__=='__main__':
    print('   '+''.join(str(x%10) for x in range(26)))
    for y in range(42,62):
        row=''
        for x in range(26):
            s=soort(B[y,x])
            if isinstance(s,str): row+=s
            else:
                k,L=s; row+= (k.lower() if L<60 else k) if k=='R' else ('1' if L<45 else 'C' if L<85 else 'B' if L<120 else 'A' if L<150 else '7')
        print('%2d '%y+row)
