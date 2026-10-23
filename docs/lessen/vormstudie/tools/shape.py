import sys,json;sys.path.insert(0,'.')
from lib import *
import statistics as st
def hull_area(pts):
    pts=sorted(set(pts))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    h=lo[:-1]+up[:-1]
    return abs(sum(h[i][0]*h[(i+1)%len(h)][1]-h[(i+1)%len(h)][0]*h[i][1] for i in range(len(h))))/2
def shape(im):
    px=im.load(); S={(x,y) for y in range(64) for x in range(64) if px[x,y][3]}
    xs=[p[0] for p in S];x0,x1=min(xs),max(xs)
    # mirror symmetry IoU around bbox mid
    M={(x0+x1-x,y) for x,y in S}
    sym=len(S&M)/len(S|M)
    # also best IoU over shifts -3..3
    best=max(len(S&{(x+d,y) for x,y in M})/len(S|{(x+d,y) for x,y in M}) for d in range(-4,5))
    # corners (4-pts hull, use pixel corners)
    hp=[]
    for x,y in S: hp+= [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
    sol=len(S)/hull_area(hp)
    per=sum(1 for x,y in S for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (x+dx,y+dy) not in S)
    # holes: transparent pixels not reachable from border
    out=set();stack=[(x,y) for x in range(64) for y in (0,63)]+[(x,y) for y in range(64) for x in (0,63)]
    while stack:
        p=stack.pop()
        if p in out or p in S or not(0<=p[0]<64 and 0<=p[1]<64): continue
        out.add(p); x,y=p; stack+=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    holes=64*64-len(S)-len(out)
    # dark pixel share (luma<60) as outline proxy
    dark=sum(1 for p in S if 0.3*px[p][0]+0.59*px[p][1]+0.11*px[p][2]<55)/len(S)
    return dict(sym=round(best,3),sol=round(sol,3),comp=round(per*per/len(S),1),holes=holes,dark=round(dark,3))
if __name__=='__main__':
    rows=json.load(open('metrics.json'))
    for r in rows:
        r.update(shape(load(r['n'],r['gba'])))
    json.dump(rows,open('metrics2.json','w'))
    def q(sel,k): 
        v=sorted(r[k] for r in sel); return f"{k}: p10={v[len(v)//10]} med={v[len(v)//2]} p90={v[9*len(v)//10]}"
    for lab,sel in [('g3',[r for r in rows if r['gba']]),('g4+',[r for r in rows if not r['gba'] and r['dex']>386])]:
        print(lab,len(sel)); 
        for k in ['sym','sol','comp','holes','dark','fill']: print('  ',q(sel,k))
        print('   head links (head<-0.02):',sum(r['head']<-0.02 for r in sel),' rechts(>0.02):',sum(r['head']>0.02 for r in sel))
        print('   holes>0:',sum(r['holes']>0 for r in sel))
    P=R+'docs/concept/sprites/'
    for s in ['alpaca/ronde15','olinguito/ronde18','nachtaap/ronde10','cuyby/ronde3','cuyby_evo/ronde4']:
        print(s,shape(load(None,p=P+s+'/anim_front.png')))
