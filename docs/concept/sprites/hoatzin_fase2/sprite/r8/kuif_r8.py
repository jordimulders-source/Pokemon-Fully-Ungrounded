# ---- kuif r8: plukken met volume, tonen uit het model (bruine modelpixels per cel, kuifkaart.py) ----
KL=np.load('kuif_L.npy')
PAL[6]=tuple(int(v) for v in os.environ.get('P6','132,72,40').split(','))    # bruin midden
PAL[7]=tuple(int(v) for v in os.environ.get('P7','192,122,66').split(','))   # bruin licht; donker = 2 (schaduw, zoals het lijf), lijn = 1
M0=kz&((K[0]>=0.30)|(rand&np.isin(S0,[6,7])))
def glad(v,m):
    o=np.zeros_like(v)
    for y,x in zip(*np.where(m)):
        w=[v[y+d,x+e] for d in (-1,0,1) for e in (-1,0,1) if ok(y+d,x+e) and m[y+d,x+e] and v[y+d,x+e]>0]
        o[y,x]=(2*v[y,x]+sum(w))/(2+len(w)) if v[y,x]>0 else (np.mean(w) if w else 0)
    return o
LB=float(os.environ.get('LB',1.2))
TK=glad(KL,M0)-LB*((xx-12)+(yy-14))      # modeltoon + licht linksboven
vals=TK[M0&~rand]
c=np.percentile(vals,[20,50,85])
for _ in range(50):
    k=np.argmin(abs(vals[:,None]-c[None]),1); c=np.array([vals[k==i].mean() for i in range(3)])
t1,t2=(c[0]+c[1])/2,(c[1]+c[2])/2
print('kuif tonen centra',c.round(1))
def toon(y,x): return 7 if TK[y,x]>=t2 else 6 if TK[y,x]>=t1 else 2
def specks(S2,m,cols,minn=3):
    for it in range(3):
        seen=np.zeros((64,64),bool); n=0
        for y,x in zip(*np.where(m)):
            t=S2[y,x]
            if seen[y,x] or t not in cols: continue
            st=[(y,x)];cc=[];seen[y,x]=1
            while st:
                a_,b_=st.pop();cc.append((a_,b_))
                for d,e in N4:
                    q,r=a_+d,b_+e
                    if ok(q,r) and m[q,r] and not seen[q,r] and S2[q,r]==t: seen[q,r]=1;st.append((q,r))
            if len(cc)<minn:
                nb=[S2[a_+d,b_+e] for a_,b_ in cc for d,e in N4 if ok(a_+d,b_+e) and m[a_+d,b_+e] and S2[a_+d,b_+e] in cols and S2[a_+d,b_+e]!=t]
                if nb:
                    for q in cc: S2[q]=max(set(nb),key=nb.count); n+=1
        if not n: break
def bouw(var):
    S2=BASIS.copy()
    for y,x in zip(*np.where(kz&~rand)): S2[y,x]=achter(y,x)          # vleugel erachter
    if var=='K1':   # hele haardos omlijnd: masker gesloten (1 px gaten dicht), buitenrand = lijn
        H=M0.copy()
        for y,x in zip(*np.where(kz&~M0)):
            if sum(M0[y+d,x+e] for d,e in N4 if ok(y+d,x+e))>=3: H[y,x]=True
        for y,x in zip(*np.where(H)): S2[y,x]=toon(y,x) if M0[y,x] else 2
        specks(S2,H&~rand,(2,6,7))
        for y,x in zip(*np.where(H)):
            nbs=[(d,e) for d,e in N4 if not ok(y+d,x+e) or not H[y+d,x+e]]
            if nbs: S2[y,x]=1 if any(d==1 or e==1 for d,e in nbs) else 2   # zwart schaduwkant, donkere selout lichtkant
    if var=='K2':   # plukken: model-tonen, schaduwkant van elke pluk donker, buitenrand tegen de achtergrond zwart/selout
        for y,x in zip(*np.where(M0)): S2[y,x]=toon(y,x)
        specks(S2,M0&~rand,(2,6,7))
        for y,x in zip(*np.where(M0)):
            if rand[y,x]:
                S2[y,x]=1 if any(not ok(y+d,x+e) or not fg[y+d,x+e] for d,e in ((1,0),(0,1))) else 2
            elif any(ok(y+d,x+e) and not M0[y+d,x+e] for d,e in ((1,0),(0,1))) and S2[y,x]!=7: S2[y,x]=2
    return S2
out={}
for kv in ('K1','K2'):
    S2k=bouw(kv)
    for ov,ring in (('A',1),('B',8)):
        S2=S2k.copy(); zet_oog(S2,ring)
        assert ((S2!=0)==fg).all()
        im=Image.fromarray(S2.astype('uint8'),'P'); flat=[v for c_ in PAL for v in c_]; im.putpalette(flat+[0]*(768-len(flat)))
        im.save('kop_%s_oog%s.png'%(kv,ov),transparency=0)
R7=np.array(Image.open('r7.png'))
for f in ('kop_K1_oogA.png','kop_K2_oogB.png'):
    a_=np.array(Image.open(f)); kopz=kz|face|snavel
    print(f,'buiten kopzone anders dan r7 B:',int(((a_!=R7)&~kopz).sum()))
with open('normal.pal','w') as f: f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%tuple(c_) for c_ in PAL))
print(json.dumps(log,indent=1,ensure_ascii=False))
np.save('kuifzone.npy',kz)
