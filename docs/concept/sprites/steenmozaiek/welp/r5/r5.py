# Ronde 5 (Jordi op r4: "het gezicht is echt veel minder mooi nu" · "het hele 3d idee is nu uit de sprite ook"):
# vlak- en schaduwopbouw (facetten) weer uit het model voor de HELE sprite. Van r4 blijven alleen: gladde rugomtrek,
# buitenlijn/selout-regels, minder zwarte losse binnenlijnen, heup A, oog 1 px links, geen korrels < 3 px.
import numpy as np
r4=np.load('welp_r4.npy'); r3=np.load('welp_r3_A_oog1.npy'); F=np.load('form.npy'); H,W=r4.shape
_,K,d,S,M,L,P,Q,R,g_,Wt,C,T,G=range(14)
BR={S,M,L}; log={}
a=r4.copy()
edge=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if r4[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or r4[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): edge[y,x]=True
kop=(F=='kop')
# 1. kop: pixels uit r3 (facetten snuit/wang/kaak/voorhoofd, neusrug, neus-mondlijn, oog oog1, oren); rand zoals r4;
#    zwarte binnenlijnen buiten oog/neus/mond/oren -> lijnbruin
feat=np.zeros((H,W),bool)
feat[8:12,8:15]=True; feat[13:17,1:7]=True; feat[16:24,2:14]=True; feat[0:9,4:10]=True; feat[0:9,16:25]=True; feat[9:11,3:5]=True
n_kop=0
for y,x in zip(*np.where(kop&~edge)):
    v=r3[y,x]
    if v==K and not feat[y,x]: v=d
    if a[y,x]!=v: a[y,x]=v; n_kop+=1
log['kop_px']=n_kop
# 2. rest van het lijf: elke bruine vulpixel van r4 krijgt de facettint van het model (r3);
#    waar r3 een (in r4 weggehaalde) lijn had of buiten r3's silhouet lag (rug): meerderheid van de bruine r3-buren
def r3buur(y,x):
    cnt={}
    for r in (1,2):
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and r3[yy,xx] in BR: cnt[r3[yy,xx]]=cnt.get(r3[yy,xx],0)+1
        if cnt: return max(cnt,key=cnt.get)
    return None
n_vul=0
for y,x in zip(*np.where(~kop&~edge&np.isin(r4,list(BR)))):
    v=r3[y,x] if r3[y,x] in BR else r3buur(y,x)
    if v is not None and a[y,x]!=v: a[y,x]=v; n_vul+=1
log['vul_uit_model']=n_vul
# 3. korrels < 3 px (bruin) naar de buurtint binnen dezelfde vorm; facetten van 3+ px blijven
n=0
for it in range(2):
    seen=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            if seen[j,i] or a[j,i] not in BR or feat[j,i]&kop[j,i]: continue
            c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==c: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<3:
                cnt={}
                for y,x in cl:
                    for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                        if 0<=yy<H and 0<=xx<W and a[yy,xx] in BR and a[yy,xx]!=c: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
                if cnt:
                    v=max(cnt,key=cnt.get)
                    for y,x in cl: a[y,x]=v; n+=1
log['korrels']=n
np.save('welp_r5.npy',a)
log['diff_r4']=int((a!=r4).sum()); log['diff_r3']=int((a!=r3).sum())
print(log)
