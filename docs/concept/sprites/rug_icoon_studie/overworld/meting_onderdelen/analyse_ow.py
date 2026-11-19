"""Meetstudie overworld (HGSS, 32x32) per onderdeel t.o.v. front en icoon.
Gebruik: python3 analyse_ow.py [--vel]   (vanuit elke map)
In:  punten_ow.json (OW, met de hand afgelezen), ../../verhoudingen/data/punten.json (front + icoon).
Uit: metingen_ow.csv, samenvatting_ow.json, tabellen op stdout; met --vel ook vel_ow_1.png en vel_ow_2.png."""
import os,sys,json,csv,numpy as np
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from laad_ow import ROOT,frame,pal,rgba
PO=json.load(open(H+'/punten_ow.json')); PF=json.load(open(H+'/../../verhoudingen/data/punten.json'))
SOORTEN=[k for k in PO if not k.startswith('_')]; VIEW={'v':0,'a':2,'z':4}; NAAM={'v':'voor','a':'achter','z':'opzij'}
def bbox(m):
    ys,xs=np.nonzero(m); return int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())
def fbox(sp):
    D=ROOT+'/graphics/pokemon/'+sp; p=D+'/anim_front.png' if os.path.exists(D+'/anim_front.png') else D+'/front.png'
    return bbox(np.array(Image.open(p))[:64,:64]>0)
def ibox(sp): return bbox(np.array(Image.open(ROOT+'/graphics/pokemon/%s/icon.png'%sp))[:32,:32]>0)
w=lambda b:b[2]-b[0]+1; h=lambda b:b[3]-b[1]+1
def omlijning(ix,P):
    """meest voorkomende index aan elke kant (eerste gevulde pixel per rij/kolom) + binnenlijnen"""
    out={}; m=ix>0
    for kant in 'blro':
        c=[]
        if kant in 'lr':
            for y in range(32):
                xs=np.nonzero(m[y])[0]
                if len(xs): c.append(ix[y,xs[0] if kant=='l' else xs[-1]])
        else:
            for x in range(32):
                ys=np.nonzero(m[:,x])[0]
                if len(ys): c.append(ix[ys[0] if kant=='b' else ys[-1],x])
        k=int(np.bincount(c).argmax()); out[kant]=(k,'%02x%02x%02x'%P[k],round(float(np.mean(np.array(c)==k)),2))
    # binnenlijnen: pixels in een omlijningskleur die niet aan de rand liggen
    lijn={out[k][0] for k in 'blro'}; pad=np.pad(m,1); rand=~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    binnen=int((np.isin(ix,list(lijn))&m&~rand).sum()); out['binnen']=binnen; return out
rows=[]
for sp in SOORTEN:
    fb=fbox(sp); F=PF.get(sp,{}).get('f'); I=PF.get(sp,{}).get('i'); ib=ibox(sp); P=pal(sp)
    for v,k in VIEW.items():
        p=PO[sp][v]; ix=frame(sp,k); ob=bbox(ix>0); r=dict(sp=sp,v=v)
        r['fh'],r['ih'],r['oh'],r['ow']=h(fb),h(ib),h(ob),w(ob)
        tops=[p['kop'][1]]+[p[q][1] for q in ('lijf','staart','kuif','kraag') if p.get(q)]
        r['oh_zo']=ob[3]-min(tops)+1; r['S']=r['oh']/r['fh']; r['S_zo']=r['oh_zo']/r['fh']
        kb,kh=w(p['kop']),h(p['kop']); r['kop_b'],r['kop_h']=kb,kh; r['kopdeel_ow']=kh/r['oh']
        r['vs_icoon_h']=r['oh']/r['ih']
        if I: r['kopdeel_i']=h(I['kop'])/r['ih']; r['kop_h_vs_icoon']=kh/h(I['kop']); r['kop_b_vs_icoon']=kb/w(I['kop'])
        if F:
            r['kopdeel_f']=h(F['kop'])/r['fh']; r['kop_h_x']=kh/h(F['kop'])/r['S']; r['kop_b_x']=kb/w(F['kop'])/r['S']
            r['f_kop_b'],r['f_kop_h']=w(F['kop']),h(F['kop'])
        o=p['ogen']
        if o:
            r['oog_b'],r['oog_h']=o[0][2],o[0][3]; r['n_ogen']=len(o)
            r['oog_y_rel']=(o[0][1]-p['kop'][1])/(p['kop'][3]-p['kop'][1])
            if v=='z': r['oog_x_rel']=(o[0][0]-p['kop'][0])/(p['kop'][2]-p['kop'][0])
            if len(o)==2: r['oog_afst']=abs(o[1][0]-o[0][0]); r['oog_afst_rel']=r['oog_afst']/kb
            if F:
                r['f_oog_b'],r['f_oog_h']=F['oog'][2],F['oog'][3]
                fk=F['kop']; r['f_oog_y_rel']=(F['oog'][1]-fk[1])/(fk[3]-fk[1])
                if not PF[sp].get('frontaal'): r['f_oog_x_rel']=(F['oog'][0]-fk[0])/(fk[2]-fk[0])
            if I: r['i_oog_b'],r['i_oog_h']=I['oog'][2],I['oog'][3]
        else: r['n_ogen']=0
        if p['oor']:
            r['oor']=p['kop'][1]-p['oor'][1]; r['oor_b']=w(p['oor']); r['oor_kader']=max(w(p['oor']),h(p['oor']))
            if F and F.get('oor') is not None:
                r['f_oor']=F['kop'][1]-F['oor']
                if r['oor']>0: r['oor_x']=r['oor']/r['f_oor']/r['S']
        if p['lijf']:
            r['lijf_b'],r['lijf_h']=w(p['lijf']),h(p['lijf'])
            if v=='z': r['kop_lijf']=kb/r['lijf_b']
            if v=='z' and F and F.get('romp'):
                fr=F['romp'][1]-F['romp'][0]+1; r['f_kop_lijf']=w(F['kop'])/fr; r['kop_lijf_x']=r['kop_lijf']/r['f_kop_lijf']; r['lijf_x']=r['lijf_b']/fr/r['S']
        if p['poot']:
            r['poot']=p['poot'][1]-p['poot'][0]+1; r['n_poten']=p['poot'][2]
            if F and F.get('vp') and F.get('buik'): r['f_poot']=F['vp']-F['buik']; r['poot_x']=r['poot']/r['f_poot']/r['S']
        else: r['n_poten']=0
        if p['staart']:
            s=p['staart']; r['staart']=max(w(s),h(s)); r['staartplek']=p['staartplek']
            if F and F.get('staart'): fs=F['staart']; r['f_staart']=max(fs[2]-fs[0]+1,fs[3]-fs[1]+1); r['staart_x']=r['staart']/r['f_staart']/r['S']
        r['aanzicht']=p.get('aanzicht',''); r['lijfstand']=p.get('lijfstand','')
        om=omlijning(ix,P); r['omlijning']=' '.join('%s:%x/%s(%d%%)'%(q,om[q][0],om[q][1],om[q][2]*100) for q in 'bolr'); r['binnenlijn_px']=om['binnen']
        for q in 'bolr': r['zwart_'+q]=int(om[q][1] in ('000000','101010','080807'))
        if 'oog_x_rel' in r and 'f_oog_x_rel' in r: r['oog_x_shift']=r['oog_x_rel']-r['f_oog_x_rel']
        if 'oog_y_rel' in r and 'f_oog_y_rel' in r: r['oog_y_shift']=r['oog_y_rel']-r['f_oog_y_rel']
        r['lijn_zwart']=sum(om[q][1] in ('000000','101010','080807') for q in 'bolr')
        rows.append(r)
# opslaan
keys=sorted({k for r in rows for k in r},key=lambda k:(k not in('sp','v'),k))
with open(H+'/metingen_ow.csv','w',newline='') as f:
    wr=csv.DictWriter(f,keys); wr.writeheader()
    for r in rows: wr.writerow({k:(round(x,3) if isinstance(x,float) else x) for k,x in r.items()})
def st(xs):
    xs=[x for x in xs if x is not None]
    if not xs: return None
    return dict(n=len(xs),med=round(float(np.median(xs)),2),p25=round(float(np.percentile(xs,25)),2),p75=round(float(np.percentile(xs,75)),2))
def col(k,v): return [r[k] for r in rows if r['v']==v and k in r]
def fmt(s): return '–' if not s else '**%.2f** (%.2f–%.2f) n=%d'%(s['med'],s['p25'],s['p75'],s['n'])
def fit(xk,yk,views):
    X=[r[xk] for r in rows if r['v'] in views and xk in r and yk in r]; Y=[r[yk] for r in rows if r['v'] in views and xk in r and yk in r]
    if len(X)<3: return None
    b,a=np.polyfit(X,Y,1); res=np.array(Y)-(a+b*np.array(X)); return dict(a=round(float(a),2),b=round(float(b),2),rest=round(float(np.sqrt(np.mean(res**2))),2),n=len(X))
SAM={}
T=[('S = OW-hoogte / front-hoogte','S'),('OW-hoogte zonder oren / front-hoogte met oren','S_zo'),('OW-hoogte / icoonhoogte','vs_icoon_h'),
   ('kop deel van figuurhoogte (OW)','kopdeel_ow'),('kop deel van figuurhoogte (front)','kopdeel_f'),('kop deel van figuurhoogte (icoon)','kopdeel_i'),
   ('kopbreedte (px)','kop_b'),('kophoogte (px)','kop_h'),('kophoogte × t.o.v. S','kop_h_x'),('kopbreedte × t.o.v. S','kop_b_x'),('kophoogte OW / icoon','kop_h_vs_icoon'),('kopbreedte OW / icoon','kop_b_vs_icoon'),
   ('kop / lijf (OW, lengte)','kop_lijf'),('kop/lijf OW ÷ kop/lijf front','kop_lijf_x'),('lijflengte × t.o.v. S','lijf_x'),
   ('oog verticaal in de kop (0 = kopboven, 1 = kin)','oog_y_rel'),('idem front','f_oog_y_rel'),('oog horizontaal (0 = snuit, 1 = achterkant)','oog_x_rel'),('idem front','f_oog_x_rel'),
   ('verschuiving oog verticaal OW − front (zelfde soort)','oog_y_shift'),('verschuiving oog horizontaal OW − front (niet-frontaal)','oog_x_shift'),('oogafstand (px, midden–midden)','oog_afst'),('oogafstand / kopbreedte','oog_afst_rel'),
   ('oorlengte (px, kopboven − oortop)','oor'),('oorlengte × t.o.v. S (alleen oren > 0)','oor_x'),('oorbreedte (px)','oor_b'),
   ('poot zichtbaar (px)','poot'),('poten zichtbaar (aantal)','n_poten'),('poot × t.o.v. S','poot_x'),('staart langste zijde (px)','staart'),('staart × t.o.v. S','staart_x'),
   ('oog b (px)','oog_b'),('oog h (px)','oog_h'),('binnenlijn-pixels','binnenlijn_px'),('zijden met zwarte omlijning (van 4)','lijn_zwart'),('boven zwart (aandeel)','zwart_b'),('onder zwart (aandeel)','zwart_o'),('links zwart (aandeel)','zwart_l'),('rechts zwart (aandeel)','zwart_r')]
print('| maat | voor | achter | opzij |\n|---|---|---|---|')
for naam,k in T:
    SAM[k]={v:st(col(k,v)) for v in 'vaz'}
    print('| %s | %s | %s | %s |'%(naam,fmt(SAM[k]['v']),fmt(SAM[k]['a']),fmt(SAM[k]['z'])))
FITS={'oog_h (OW = a + b × front)':fit('f_oog_h','oog_h','vz'),'oog_b':fit('f_oog_b','oog_b','vz'),
      'oog_h t.o.v. icoon':fit('i_oog_h','oog_h','vz'),'oog_b t.o.v. icoon':fit('i_oog_b','oog_b','vz'),
      'kop_h opzij (px)':fit('f_kop_h','kop_h','z'),'kop_b opzij (px)':fit('f_kop_b','kop_b','z'),
      'kop_b voor (px)':fit('f_kop_b','kop_b','v'),'kop_h voor (px)':fit('f_kop_h','kop_h','v'),
      'oor opzij (px)':fit('f_oor','oor','z'),'oor voor (px)':fit('f_oor','oor','v'),'staart opzij (px)':fit('f_staart','staart','z'),'poot opzij (px)':fit('f_poot','poot','z')}
print('\nPixelregels (OW = a + b × front; rest = rms-afwijking in px):')
for k,f in FITS.items(): print(' ',k,f)
# tellingen
tel={'twee ogen voor':sum(r['n_ogen']==2 for r in rows if r['v']=='v'),'één oog opzij':sum(r['n_ogen']==1 for r in rows if r['v']=='z'),
     'profiel opzij':sum(r['aanzicht'].startswith('profiel') for r in rows if r['v']=='z'),
     'staart zichtbaar voor':sum('staart' in r for r in rows if r['v']=='v'),'staart zichtbaar achter':sum('staart' in r for r in rows if r['v']=='a'),
     'lijfstand opzij':{s:sum(r['lijfstand']==s for r in rows if r['v']=='z') for s in {r['lijfstand'] for r in rows if r['v']=='z'}},
     'oogbouw voor':{sp:PO[sp]['v'].get('oogbouw') for sp in SOORTEN}}
print('\n',json.dumps(tel,ensure_ascii=False,indent=0))
print('\nOmlijning per soort/aanzicht (kant:index/RGB(aandeel)):')
for r in rows: print(' %-10s %s  %s  binnen=%d'%(r['sp'],r['v'],r['omlijning'],r['binnenlijn_px']))
json.dump(dict(stat=SAM,pixelregels=FITS,tellingen=tel),open(H+'/samenvatting_ow.json','w'),indent=1,ensure_ascii=False)
# controlevellen
if '--vel' in sys.argv:
    from laad_ow import rgba as R
    sys.path.insert(0,H+'/../../verhoudingen'); from laad import front
    def teken(d,b,Z,ox,oy,kl,wd=2): d.rectangle([ox+b[0]*Z,oy+b[1]*Z,ox+(b[2]+1)*Z-1,oy+(b[3]+1)*Z-1],outline=kl,width=wd)
    def kruis(d,x,y,Z,ox,oy):
        X,Y=ox+(x+.5)*Z,oy+(y+.5)*Z; d.line([(X-Z*.6,Y),(X+Z*.6,Y)],fill=(255,0,0),width=2); d.line([(X,Y-Z*.6),(X,Y+Z*.6)],fill=(255,0,0),width=2)
    Z=8; FZ=3; bw=64*FZ+3*32*Z+50; bh=32*Z+30
    for vel,deel in ((1,SOORTEN[:8]),(2,SOORTEN[8:])):
        img=Image.new('RGB',(bw,bh*len(deel)),(255,255,255)); d=ImageDraw.Draw(img)
        for i,sp in enumerate(deel):
            oy=i*bh+20; d.text((4,oy-16),sp+'   front 3× | OW voor, achter, opzij 8× (paars kop, rood oog, rode lijn oortop, blauw lijf, groen poot, oranje staart)',fill=(0,0,0))
            fa=front(sp); bg=Image.new('RGB',(64*FZ,64*FZ),(150,210,180)); fi=Image.fromarray(fa).resize((64*FZ,64*FZ),Image.NEAREST); bg.paste(fi,(0,0),fi); img.paste(bg,(0,oy))
            F=PF.get(sp,{}).get('f')
            if F:
                teken(d,F['kop'],FZ,0,oy,(160,0,200)); kruis(d,F['oog'][0],F['oog'][1],FZ,0,oy)
            for j,(v,k) in enumerate(VIEW.items()):
                ox=64*FZ+10+j*(32*Z+10); a=R(frame(sp,k),pal(sp)); bg=Image.new('RGB',(32*Z,32*Z),(150,210,180)); fi=Image.fromarray(a).resize((32*Z,32*Z),Image.NEAREST); bg.paste(fi,(0,0),fi); img.paste(bg,(ox,oy))
                p=PO[sp][v]; teken(d,p['kop'],Z,ox,oy,(160,0,200))
                if p['lijf']: teken(d,p['lijf'],Z,ox,oy,(0,60,255))
                if p['staart']: teken(d,p['staart'],Z,ox,oy,(255,140,0))
                if p['oor']: y=oy+p['oor'][1]*Z; d.line([(ox+p['oor'][0]*Z,y),(ox+(p['oor'][2]+1)*Z,y)],fill=(255,0,0),width=3)
                if p['poot']: y=oy+(p['poot'][1]+1)*Z-1; d.line([(ox,y),(ox+32*Z,y)],fill=(0,170,0),width=2)
                for e in p['ogen']: kruis(d,e[0],e[1],Z,ox,oy)
        img.save(H+'/vel_ow_%d.png'%vel)
