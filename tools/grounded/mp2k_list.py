"""Project Grounded: lijst van de nummers in de songtabel van een MP2K-ROM met hun lengte, loop en lengte bij twee keer
afspelen (om ze te vergelijken met een soundtracklijst). Gebruik: python3 tools/grounded/mp2k_list.py <rom.gba> <songtabel-hex>"""
import struct,sys
rom=open(sys.argv[1],'rb').read(); TBL=int(sys.argv[2],16)-0x08000000
u32=lambda o: struct.unpack_from('<I',rom,o)[0]
off=lambda p: p-0x08000000 if 0x08000000<=p<0x08000000+len(rom) else None
W=list(range(25))+[28,30,32,36,40,42,44,48,52,54,56,60,64,66,68,72,76,78,80,84,88,90,92,96]
ARG1={0xBA,0xBB,0xBC,0xBD,0xBE,0xBF,0xC0,0xC1,0xC2,0xC3,0xC4,0xC5,0xC8}
def track(o):
    t=0; pos={}; rs=None; loop=None; tempos=[]; stack=[]
    for _ in range(400000):
        pos.setdefault(o,t); b=rom[o]
        if b>=0x80:
            c=b; o+=1
            if c>=0xBD: rs=c
        else:
            if rs is None: break
            c=rs
        if c<=0xB0: t+=W[c-0x80]; continue
        if c==0xB1: break
        if c==0xB2:
            loop=pos.get(off(u32(o))); break
        if c==0xB3: stack.append(o+4); o=off(u32(o)); continue
        if c==0xB4:
            if stack: o=stack.pop()
            continue
        if c==0xB5: o+=5; continue
        if c==0xB9: o+=3; continue
        if c==0xBB: tempos.append((t,rom[o]*2)); o+=1; continue
        if c in ARG1: o+=1; continue
        if c==0xCD: o+=2; continue
        if c==0xCE:
            if rom[o]<0x80: o+=1
            continue
        if c>=0xCF:
            if rom[o]<0x80:
                o+=1
                if rom[o]<0x80:
                    o+=1
                    if rom[o]<0x80 and c!=0xCF: o+=1
            continue
    return t,loop,tempos
def secs(ticks,tempos):
    s=0; last=0; bpm=150
    for at,b in tempos:
        if at>ticks: break
        s+=(at-last)/(24*bpm/60); last=at; bpm=max(1,b)
    return s+(ticks-last)/(24*bpm/60)
i=0
while True:
    hp=u32(TBL+i*8); mp=struct.unpack_from('<H',rom,TBL+i*8+4)[0]; h=off(hp)
    if h is None: break
    i+=1; ntr=rom[h]
    if not 1<=ntr<=16: continue
    best=None
    for k in range(ntr):
        tp=off(u32(h+8+4*k))
        if tp is None: continue
        t,loop,tempos=track(tp)
        if best is None or t>best[0]: best=(t,loop,tempos)
    t,loop,tempos=best
    tot=secs(t,tempos)
    if tot<20: continue
    lp=secs(loop,tempos) if loop is not None else None
    two=(lp+2*(tot-lp)) if lp is not None else tot
    print('song %3d sp%d %2d sporen  %5.1f s  loop %s  2x %4.0f s'%(i-1,mp,ntr,tot,('%.1f'%lp) if lp is not None else '  -  ',two))
