# r7: r5 als basis; kern/gas uit het model (r6-methode op r5-uitlijning), schotsnaden op modelranden, lichtere lijnen
import sys; sys.path.insert(0,'r7w')
from body import *
import p6
PAL=np.array(p6.PAL,float)
O=np.load('r7w/O.npy'); med=np.load('r7w/med.npy'); Fl=np.load('r7w/Fl.npy')
def nearest(md,cands): return I[cands[int(np.argmin([((md-PAL[I[c]])**2).sum() for c in cands]))]]
# --- body: gaten dichten
outside=flood(R,[(0,0)],~body)
body=~outside
outer=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    if body[j,i]:
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        y,x=j+dy,i+dx
        if not(0<=y<64 and 0<=x<64) or not body[y,x]: outer[j,i]=True
eye=isin(R,'erCg')
o=R.copy()
# --- 1. kern
core=np.zeros((64,64),bool)
for j in range(27,40):
  for i in range(21,32):
    if not body[j,i] and (isin(R,'cdG')[j,i] or (j>=30 and isin(R,'b')[j,i])): core[j,i]=True
for j,i in zip(*np.where(core)): o[j,i]=nearest(med[j,i],'abcdG')
# --- 4. gas: niet-lijf, niet-kern, licht (WLMG), verbonden met de rand van het masker
m=np.load('mask_r1.npy')
light=isin(R,'WLMDG')&~body&~core
edge=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    if m[j,i] and any(not(0<=j+dy<64 and 0<=i+dx<64) or not m[j+dy,i+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): edge[j,i]=True
gas=flood(R,list(zip(*np.where(edge&light))),light)
for j,i in zip(*np.where(gas)):
    o[j,i]=I['L'] if edge[j,i] else nearest(med[j,i],'WLG')
np.save('r7w/gas.npy',gas); np.save('r7w/core.npy',core); np.save('r7w/body2.npy',body); np.save('r7w/outer2.npy',outer)
# --- 2. naden + belichting in het lijf
seam=np.load(sys.argv[1]) if len(sys.argv)>1 else np.load('r7w/seam_auto.npy')
inter=body&~outer&~eye
for j,i in zip(*np.where(inter)):
    o[j,i]=I['S'] if seam[j,i] else nearest(med[j,i],'WLMD')
np.save('r7w/o_pre.npy',o)
p6.to_txt(o,'r7w/pre.txt')
