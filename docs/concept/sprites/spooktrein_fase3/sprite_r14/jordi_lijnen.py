# Jordi's schetslijnen uit de screenshot terugrekenen naar spritecoordinaten (schaal 8,52, offset (7,3), gemeten: kleurfout 0 met r13).
from PIL import Image; import numpy as np
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
s,ox,oy=8.52,7,3
J=np.array(Image.open(D+'jordi/koeienvanger_lijnen.png').convert('RGB')).astype(int)
r=Image.open(D+'sprite_r13/sprite.png').convert('RGBA'); b=Image.new('RGBA',r.size,(255,255,255,255)); b.alpha_composite(r); S=np.array(b.convert('RGB')).astype(int)
def lijnpixels():
    pts=[]
    for Y in range(J.shape[0]):
        for X in range(0,550):
            sx=(X-ox)/s; sy=(Y-oy)/s
            if not(0<=sx<64 and 0<=sy<64): continue
            c=J[Y,X]; e=S[int(sy),int(sx)]
            if c.max()<60 and np.abs(c-e).sum()>60 and (0.3*e[0]+0.59*e[1]+0.11*e[2])>70: pts.append((sx,sy))  # alleen zwart op een niet-donkere spritepixel = schetslijn
    return pts
if __name__=='__main__':
    P=lijnpixels(); print(len(P))
    g=np.zeros((64,64),int)
    for sx,sy in P: g[int(sy),int(sx)]+=1
    print('   '+''.join(str(x%10) for x in range(26)))
    for y in range(40,62): print('%2d '%y+''.join('#' if g[y,x]>=6 else '+' if g[y,x]>0 else '.' for x in range(26)))
    np.save(D+'sprite_r14/jordi_lijnen.npy',np.array(P))
