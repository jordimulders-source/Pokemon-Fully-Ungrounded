# Capykart eindkeuring_dc variant c (24 nov): vanuit b, alleen in de kop.
# Jordi over b: "het oog is heel raaar, de neus is effen, hadden we dat afgesproken? oren zijn ook anders dan het model en grijze streep is ook weg, is niet bewust neem ik aan?"
# 1 snuit: opbouw van r17b (snuitplaat, verticale snuitlijn, neusgaten, mond) met tinten op het nieuwe palet
# 2 oren: r17b (donkere binnenkant, randen) op het nieuwe palet
# 3 morrillo: donkergrijs van r17b (76,74,84)
# 4 oog + wenkbrauw: r15b x28-31 y16-20 als één geheel, op de oogplek (+1,+1) zoals in r17
import sys; _argv=sys.argv[:]
g_=dict(__name__='bouw_b_import'); exec(open('eindkeuring_dc/bouw_b.py').read(),g_)
globals().update({k:v for k,v in g_.items() if not k.startswith('__')}); sys.argv=_argv
r17b=np.array(Image.open('sprite/r17b/capykart.png'))
r15b=np.array(Image.open('sprite/r15b/capykart_creme.png'))
b_n=n.copy()
logc={}
def zet(lijst,naam,x,y,t):
    if n[y,x]!=t: lijst.append((x,y,int(n[y,x]),int(t)))
    n[y,x]=t
# 3 morrillo-kleur (HD wordt exact r17b; HD is ook hoepel donker en tandschaduw)
PAL[HD]=(76,74,84)
# 1 snuit (r17b-tinten -> nieuw palet; plaat = r17b 3)
SNUIT={1:B0,2:B1,3:B2,4:B3,5:B4}
L1=[]
for y in range(19,32):
    for x in range(15,24):
        if o[y,x]==0 or ring[y,x] or (x,y) in BESCHERMD or d[y,x] not in (1,14): continue
        k=r17b[y,x]
        if k in SNUIT: zet(L1,'snuit',x,y,SNUIT[k])
logc['1 snuit']=L1
# 2 oren (r17b; rand zoals r17b: zwart blijft zwart, lijnbruin -> B0)
OOR={2:B0,3:B1,4:B3,5:B4}
L2=[]
oorpix=[(x,y) for y in range(11,15) for x in range(24,29)]+[(x,15) for x in range(24,27)]
oorpix+=[(x,y) for y in range(12,18) for x in range(33,41)]
for x,y in oorpix:
    if o[y,x]==0 or (x,y) in BESCHERMD: continue
    k=r17b[y,x]
    if k==1: t=K if ring[y,x] else B0     # binnenlijn in het oor: donkerste eigen tint (punt 1 van b)
    elif k in OOR: t=OOR[k]
    else: continue
    zet(L2,'oor',x,y,t)
logc['2 oren']=L2
# 4 oog + wenkbrauw uit r15b (r15b: 1 zwart, 4 donkerste vacht, 3 midden, 2 licht, 14 hoog)
OOG={1:K,4:B1,3:B2,2:B3,14:B4}
L4=[]
for y in range(16,21):
    for x in range(28,32):
        k=r15b[y,x]
        if k in OOG: zet(L4,'oog',x+1,y+1,OOG[k])
logc['4 oog+wenkbrauw']=L4
assert ((n==0)==(o==0)).all(), 'silhouet'
buiten=[(x,y) for y,x in zip(*np.where(n!=b_n)) if not (15<=x<=40 and 11<=y<=31)]
assert not buiten, buiten
if __name__=='__main__':
    opslaan(n,'eindkeuring_dc/capykart_c.png'); np.save('eindkeuring_dc/_n_c.npy',n)
    rgb(n,(255,255,255)).resize((512,512),Image.NEAREST).save('eindkeuring_dc/capykart_c_8x.png')
    nm={K:'K',B0:'B0',B1:'B1',B2:'B2',B3:'B3',B4:'B4',HD:'HD'}
    print('silhouet-diff',int(((n==0)!=(o==0)).sum()),'kleuren',len(set(n.ravel())),'px anders dan b',int((n!=b_n).sum()))
    for k,l in logc.items(): print(k,len(l),' '.join('(%d,%d)%s>%s'%(x,y,nm.get(a,a),nm.get(t,t)) for x,y,a,t in l))
