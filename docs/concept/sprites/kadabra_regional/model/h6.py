# v5: hand naar Jordi's schets: ronde handpalm met drie vingers die als waaier naar rechts wijzen (schuin omhoog, recht, schuin omlaag), elk met klauwtje
from PIL import Image
import numpy as np, math
a=np.asarray(Image.open('model/model_hand3_v4.png').convert('RGB')).copy()
P=7.3
COL={'W':(255,255,255),'o':(13,12,18),'d':(85,83,102),'b':(170,167,181),'c':(139,136,156)}
X0,X1,Y0,Y1=108,140,36,70
def px(i,j,col):
    x0,y0,x1,y1=int(round(i*P)),int(round(j*P)),int(round((i+1)*P)),int(round((j+1)*P)); a[y0:y1,x0:x1]=col
# oude hand weg
for j in range(36,54):
    for i in range(110,140): px(i,j,(255,255,255))
for j in range(54,68):
    for i in range(114,140): px(i,j,(255,255,255))
a[int(36*P):int(68*P), int(139.5*P):]=(255,255,255)
CX,CY,R=120.0,58.0,6.0
FING=[(52,17.0),(4,17.5),(-38,15.0)]   # hoek (graden omhoog), lengte vanaf het midden
def inside(x,y):
    if (x-CX)**2+(y-CY)**2<=R*R: return 1,None
    for k,(ang,ln) in enumerate(FING):
        ux,uy=math.cos(math.radians(ang)),-math.sin(math.radians(ang))
        t=(x-CX)*ux+(y-CY)*uy; s=abs(-(x-CX)*uy+(y-CY)*ux)
        if 3<=t<=ln:
            hw=3.1-(3.1-0.9)*(t-R+2)/(ln-R+2) if t>R-2 else 3.1
            if s<=hw: return 1,(k,ln-t)
    return 0,None
M={}; CL={}
for j in range(Y0,Y1):
    for i in range(X0,X1):
        n=0; cl=0
        for sx in (0.25,0.75):
            for sy in (0.25,0.75):
                v,f=inside(i+sx,j+sy); n+=v
                if f and f[1]<3.0: cl+=1
        if n>=2: M[(i,j)]=1; CL[(i,j)]=cl>=2
def m(i,j): return (i,j) in M
def dist(i,j,dx,dy):
    n=0
    while m(i+dx*(n+1),j+dy*(n+1)) and n<4: n+=1
    return n
for (i,j) in M:
    if CL[(i,j)]: ch='W'
    elif dist(i,j,-1,-1)<=1 and dist(i,j,0,-1)<=2: ch='b'
    elif dist(i,j,1,1)==0 or dist(i,j,0,1)==0: ch='d'
    else: ch='c'
    px(i,j,COL[ch])
for j in range(Y0,Y1):
    for i in range(X0,X1):
        if not m(i,j) and (m(i+1,j) or m(i-1,j) or m(i,j+1) or m(i,j-1)) and i>=114: px(i,j,COL['o'])
out=Image.fromarray(a); out.save('model/model_hand_v5.png')
out.crop((700,230,1024,540)).resize((648,620),Image.NEAREST).save('model/hand_v5_closeup.png')
