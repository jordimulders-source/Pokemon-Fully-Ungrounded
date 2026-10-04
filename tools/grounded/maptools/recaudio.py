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
# mGBA-buffer-glitch: af en toe een burst van ~10 samples met 0 / 15136 / 32520 om en om (geen muziek, wel een
# hoorbare tik). Herkennen aan een sprong > 12000 naar een sample dat buren met exact 0 heeft; lineair overbruggen.
st=a.reshape(-1,2).astype(np.int32); fixed=0
for c in (0,1):
    x=st[:,c]; i=1
    while i<len(x)-1:
        if abs(x[i]-x[i-1])>12000 and (x[i+1]==0 or x[i-1]==0):
            j=i
            while j<len(x)-1 and j-i<32 and (abs(x[j])>12000 or x[j]==0): j+=1
            lo=max(0,i-1); x[lo:j+1]=np.linspace(x[lo],x[min(j,len(x)-1)],j+1-lo).astype(np.int32); fixed+=1; i=j
        i+=1
a=np.clip(st,-32768,32767).astype(np.int16).reshape(-1)
if fixed: print('glitches weggewerkt:',fixed)
w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(32768); w.writeframes(a.tobytes()); w.close()
x=a.astype(float); print(out.split('/')[-1],'rms',int(np.sqrt((x*x).mean())),'peak',int(abs(x).max()),'clip%%%.2f'%(100*(abs(x)>=32000).mean()))
