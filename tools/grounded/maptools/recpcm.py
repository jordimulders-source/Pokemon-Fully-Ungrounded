"""recpcm.py rom state k seconds out.wav [gSoundInfo-adres]: neemt het geluid op uit de mixbuffer van de game zelf
(gSoundInfo.pcmBuffer, wat de GBA echt afspeelt; mono, 13379 Hz). Zonder de resampler-glitches van mGBA.
Let op: alleen DirectSound; PSG-sporen (vierkant/ruis) zitten er niet in -> gebruik dan recaudio.py."""
import re
from emu import *
import sys, numpy as np, wave
rom,st,k,sec,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
SI=int(sys.argv[6],16) if len(sys.argv)>6 else int(re.search(r'(0x[0-9a-f]+)\s+gSoundInfo\n',open('pokeemerald.map').read()).group(1),16)
e=Emu(rom); load(e,st)
mem=e.core.memory
def rd(addr,n): return bytes(mem.u8[addr:addr+n])
if k:
    e.press('START', after=30); e.press('A', after=30)
    for _ in range(5): e.press('DOWN', after=6)
    e.press('A', after=30)
    for _ in range(k-1): e.press('DOWN', after=6)
    e.core.set_keys(KEYS['A'])       # laatste A pas in de opnamelus loslaten: anders mis je het begin van het nummer
per=mem.u8[SI+11]; spv=int.from_bytes(rd(SI+16,4),'little'); freq=int.from_bytes(rd(SI+20,4),'little')
print('period',per,'samples/vblank',spv,'freq',freq,'maxChans',mem.u8[SI+6])
BUF=SI+848
seg=[]; prev=np.frombuffer(rd(BUF,1584),np.int8).copy(); last=None
for f in range(int(60*sec)):
    if f==4: e.core.set_keys()
    e.core.run_frame()
    cur=np.frombuffer(rd(BUF,1584),np.int8).copy()
    ch=[(cur[i*spv:(i+1)*spv]!=prev[i*spv:(i+1)*spv]).sum() for i in range(per)]
    i=int(np.argmax(ch))
    if ch[i]==0 and last is not None: i=(last+1)%per      # stilte: gewoon het volgende stuk
    if last is not None and i!=(last+1)%per:
        print('LET OP: frame %d sprong van stuk %d naar %d'%(f,last,i))
    seg.append(cur[i*spv:(i+1)*spv]); prev=cur; last=i
x=np.concatenate(seg).astype(float)
jumps=int((abs(np.diff(x[int(freq*0.1):]))>40).sum())
print(out.split('/')[-1],'sprongen>40/128:',jumps)
best=(0,0,x)
x=(best[2]*256).clip(-32768,32767).astype(np.int16)
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(freq); w.writeframes(x.tobytes()); w.close()
