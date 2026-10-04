# recaudio.py rom state k seconds out.wav  (state "-" = koude start, k 0 = geen debugscript). Leest de audiobuffer ELKE frame uit (ook tijdens menu-navigatie), anders loopt hij over en neem je ruis op.
from emu import *
import sys, wave, numpy as np
rom,st,k,sec,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
e=Emu(rom)
if st!='-': load(e,st)
buf=e.core.get_audio_channels(); buf.set_rate(32768)
rec=[]; on=[False]; orig=e.core.run_frame
def rf():
    orig(); av=buf.available
    if av:
        s=buf.read(av)
        if on[0]: rec.extend(s)
e.core.run_frame=rf
if k:
    e.press('START', after=30); e.press('A', after=30)
    for _ in range(5): e.press('DOWN', after=6)
    e.press('A', after=30)
    for _ in range(k-1): e.press('DOWN', after=6)
    e.press('A', after=0)
on[0]=True; e.run(int(60*sec))
a=np.array(rec,dtype=np.int16)
w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(32768); w.writeframes(a.tobytes()); w.close()
x=a.astype(float); print(out.split('/')[-1],'rms',int(np.sqrt((x*x).mean())),'peak',int(abs(x).max()),'clip%%%.2f'%(100*(abs(x)>=32000).mean()))
