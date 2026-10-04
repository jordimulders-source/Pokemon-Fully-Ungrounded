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
    x=st[:,c]
    for _ in range(4):                     # herhalen tot er geen sprongen meer zijn
        bad=np.where(abs(np.diff(x))>12000)[0]
        if not len(bad): break
        i=0
        while i<len(bad):
            j=i
            while j+1<len(bad) and bad[j+1]-bad[j]<24: j+=1
            lo=max(0,bad[i]-2); hi=min(len(x)-1,bad[j]+18)
            x[lo:hi+1]=np.linspace(x[lo],x[hi],hi+1-lo).astype(np.int32); fixed+=1; i=j+1
    left=len(np.where(abs(np.diff(x))>12000)[0])
    if left: print('LET OP: nog %d sprongen in kanaal %d'%(left,c))
a=np.clip(st,-32768,32767).astype(np.int16).reshape(-1)
if fixed: print('glitches weggewerkt:',fixed)
w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(32768); w.writeframes(a.tobytes()); w.close()
x=a.astype(float); print(out.split('/')[-1],'rms',int(np.sqrt((x*x).mean())),'peak',int(abs(x).max()),'clip%%%.2f'%(100*(abs(x)>=32000).mean()))
