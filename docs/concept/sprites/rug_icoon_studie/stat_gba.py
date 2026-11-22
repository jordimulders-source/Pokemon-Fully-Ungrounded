import json,numpy as np,sys
from collections import Counter
S=sys.argv[1]
R=json.load(open(S+'/meet.json'))
H=set(open(S+'/g3.txt').read().split())
def st(name,vals):
    v=np.array([x for x in vals if x is not None],float)
    print(f"{name:34s} n={len(v):3d} med={np.median(v):6.2f} p10={np.percentile(v,10):6.2f} p90={np.percentile(v,90):6.2f}")
for setn,sel in [('ALLE 1-386',R),('GEN3',[r for r in R if r['sp'] in H])]:
  print('==',setn)
  for s in 'gn':
    q=[r for r in sel if s+'fw' in r]
    print('-- set',s)
    st('front h',[r[s+'fh'] for r in q]); st('front w',[r[s+'fw'] for r in q])
    st('back h',[r[s+'bh'] for r in q]); st('back w',[r[s+'bw'] for r in q])
    st('back/front w',[r[s+'bw']/r[s+'fw'] for r in q]); st('back/front h',[r[s+'bh']/r[s+'fh'] for r in q])
    st('back/front area(wh)',[r[s+'bw']*r[s+'bh']/(r[s+'fw']*r[s+'fh']) for r in q])
    st('back bottom row y',[r[s+'bbot'] for r in q]); st('back cut fill',[r[s+'bcut'] for r in q])
    print('   frac back reaches y63:',np.mean([r[s+'bbot']==63 for r in q]))
    st('front bottom y',[r[s+'fbot'] for r in q])
    st('front cx',[r[s+'fcx'] for r in q]); st('back cx',[r[s+'bcx'] for r in q])
    st('back extra idx not in front',[r[s+'bonly'] for r in q])
    st('front colors',[r[s+'fcol'] for r in q]); st('back colors',[r[s+'bcol'] for r in q])
    qi=[r for r in q if s+'ih' in r]
    st('icon h',[r[s+'ih'] for r in qi]); st('icon w',[r[s+'iw'] for r in qi]); st('icon bot',[r[s+'ibot'] for r in qi])
    st('icon h / front h',[r[s+'ih']/r[s+'fh'] for r in qi])
    st('icon w / front w',[r[s+'iw']/r[s+'fw'] for r in qi])
    st('icon colors',[r[s+'icol'] for r in qi])
    st('icon f2 diff after best shift',[r[s+'idiff'] for r in qi])
    print('   f2 top shift',Counter([r[s+'idytop'] for r in qi]).most_common(5),' bottom',Counter([r[s+'idy'] for r in qi]).most_common(4))
  q=[r for r in sel if 'ows' in r]
  print('-- overworld sizes',Counter(r['ows'] for r in q))
  q=[r for r in q if r['ows']==32 and 'os1h' in r]
  for k in ['s1','n1','w1']:
    st('ow '+k+' h',[r['o'+k+'h'] for r in q]); st('ow '+k+' w',[r['o'+k+'w'] for r in q]); st('ow '+k+' bot',[r['o'+k+'bot'] for r in q])
  st('ow s1 h / front(new) h',[r['os1h']/r['nfh'] for r in q if 'nfh' in r])
  st('ow s1 h / front(gba) h',[r['os1h']/r['gfh'] for r in q if 'gfh' in r])
  st('ow s1 h / icon(gba) h',[r['os1h']/r['gih'] for r in q if 'gih' in r])
  st('ow colors',[r['ocol'] for r in q])
  st('ow s2 bot - s1 bot',[r['os2bot']-r['os1bot'] for r in q]); st('ow s2 h - s1 h',[r['os2h']-r['os1h'] for r in q])
  print('   ipi',Counter(r['ipi'] for r in sel).most_common())
