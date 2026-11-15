# Archimedische spiraal rasteren met 4x4 supersampling: banden lila / donkere lijn / bruin (pitch P px per winding),
# optioneel een cremeboog als buitenrand (hoekbereik in graden, wiskundige richting, y omhoog).
import numpy as np, math
def spiral(cx,cy,R,P=3.0,rot=0.0,cw=1,boog=None,klassen=('lila','lijn','bruin'),sx=1.0,sy=1.0,kern=0.9):
    out={}
    N=4
    for y in range(int(cy-R-2),int(cy+R+3)):
        for x in range(int(cx-R-2),int(cx+R+3)):
            votes={}
            for j in range(N):
                for i in range(N):
                    px=(x+(i+0.5)/N-cx)/sx; py=(y+(j+0.5)/N-cy)/sy
                    r=math.hypot(px,py)
                    if r>R: continue
                    th=math.degrees(math.atan2(-py,px))%360
                    if boog is not None and r>R-1.0:
                        a0,a1=boog; inarc=((th-a0)%360)<=((a1-a0)%360)
                        k='creme' if inarc else None
                        if k: votes[k]=votes.get(k,0)+1
                        continue
                    if r<kern: k='kern'
                    else:
                        u=(r/P - cw*((th+rot)%360)/360.0)%1.0
                        k=klassen[int(u*len(klassen))]
                    votes[k]=votes.get(k,0)+1
            if votes:
                k,v=max(votes.items(),key=lambda t:t[1])
                if v>=N*N*0.45: out[(x,y)]=k
    return out
