from proj import *
def foot(x,y,DY=-1):
    nx0,ny0=s2n(x,y,DY); nx1,ny1=s2n(x+1,y+1,DY)
    for ny in range(int(np.floor(ny0)),int(np.ceil(ny1))):
        for nx in range(int(np.floor(nx0)),int(np.ceil(nx1))):
            w=(min(nx1,nx+1)-max(nx0,nx))*(min(ny1,ny+1)-max(ny0,ny))
            if w>0.01: yield w,ny,nx
def frac(M,x,y,DY=-1):
    f=list(foot(x,y,DY)); W=sum(w for w,_,_ in f)
    return sum(w for w,ny,nx in f if M[ny,nx])/W
WIT=N.min(2)>215; G=(N[...,1]>N[...,0]+20)&~WIT
DARK=(LUM<80)&~G&~WIT
LIGHT=(LUM>150)&~G&~WIT
RUST=(N[...,0]-N[...,2]>45)&~G&~WIT&(LUM>=80)
