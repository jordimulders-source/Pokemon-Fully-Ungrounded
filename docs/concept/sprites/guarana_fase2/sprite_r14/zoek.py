# zoek.py: per tros de grootste schaal die past (trossen raken elkaar niet: >= 2 px ruimte; binnen 64x64; onderkant <= 50)
import sys; sys.path.insert(0,'sprite_r14'); import bouw14 as B
def m(n,sp,sr,dx=0,dy=0):
    s=set()
    for f in B.tros(n,sp,sr,dx,dy): s|=f['F']
    return s
def dil(s,r=2): return {(x+a,y+b) for x,y in s for a in range(-r,r+1) for b in range(-r,r+1)}
def past(s): return min(x for x,y in s)>=0 and max(x for x,y in s)<=63 and max(y for x,y in s)<=50
for sr in (1.55,1.6,1.65,1.7):
    for spM in (1.0,1.05,1.1,1.15,1.2):
        Mm=m('M',spM,sr); dM=dil(Mm)
        if not past(Mm): continue
        L=[(spL,dx,dy) for spL in (0.95,1.0,1.05,1.1,1.15) for dx in range(-3,-8,-1) for dy in (0,1)
           if past(m('L',spL,sr,dx,dy)) and not (dM&m('L',spL,sr,dx,dy))]
        R=[spR for spR in (1.1,1.2,1.25,1.3,1.4) if past(m('R',spR,sr)) and not (dM&m('R',spR,sr))]
        if L and R: print(sr,spM,'L',sorted(L,key=lambda t:(-t[0],-t[1],t[2]))[:3],'R max',max(R))
