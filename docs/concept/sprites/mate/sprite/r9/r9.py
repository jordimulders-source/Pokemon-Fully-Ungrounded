# Ronde 9: neus, mond, voeten en linkeroog UIT HET MODEL GEKNIPT en mechanisch verkleind (red9.py), als geheel geplakt
# op r8. Daarna alleen benoemde reparaties (FIX). Buiten de zones pixeldiff 0 met r8.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/mate/sprite/r9')
import numpy as np; from PIL import Image; import red9 as R
D=R.D; im=Image.open(D+'r8/mate.png'); PAL=im.getpalette(); r8=np.asarray(im).astype(int)
Y,X=np.mgrid[0:64,0:64]
kaal_all=np.zeros((64,64),int); kaal_g=np.zeros((64,64),int)
for y in range(64):
    for x in range(64): kaal_all[y,x]=R.red(x,y); kaal_g[y,x]=R.red(x,y,True)
GRN=lambda a:(a>=6)&(a<=8)
def rect(x0,y0,x1,y1): return (X>=x0)&(X<=x1)&(Y>=y0)&(Y<=y1)
# oog: rechthoek, maar alleen de cellen die in de reductie of in r8 bij het oog horen (rand of groen) -> geen huidruis
RO=rect(17,33,23,40); ZO=RO&((kaal_g==1)|GRN(kaal_g)|(r8==1)|GRN(r8))
ZN=rect(19,40,28,46)&~ZO                 # neus
ZM=rect(17,47,30,53)                     # mond + lichtere onderlip
ZVL=rect(17,56,26,60)                    # linkervoet
ZVR=rect(33,58,43,62)                    # rechtervoet
Z={'linkeroog':ZO,'neus':ZN,'mond':ZM,'linkervoet':ZVL,'rechtervoet':ZVR}
kaal=r8.copy()
for nm,z in Z.items():
    src=kaal_g if nm=='linkeroog' else kaal_all
    kaal[z]=src[z]
a=kaal.copy()
K={'.':0,'#':1,'a':2,'b':3,'c':4,'d':5,'G':6,'H':7,'I':8}
FIX=[]   # (x,y,kleur,reden) -- wordt hieronder gevuld
exec(open(D+'r9/fix9.py').read()) if __import__('os').path.exists(D+'r9/fix9.py') else None
for x,y,k,_ in FIX: a[y,x]=K[k]
OPS=_opschoon(a,ZA_:=(ZO|ZN|ZM|ZVL|ZVR)); FIX=FIX+OPS
for x,y,k,_ in OPS: a[y,x]=K[k]
if '-f' in sys.argv:
    for f in OPS: print('opschoning',f[:3])
np.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f952c4af-e06e-5b56-87d5-86ed60c9233c/scratchpad/kaal9.npy',kaal)
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save(D+'r9/mate.png',transparency=0)
ZA=np.zeros((64,64),bool)
for z in Z.values(): ZA|=z
d=a!=r8; print('buiten de zones anders dan r8:',int((d&~ZA).sum()))
for nm,z in Z.items(): print(nm,'anders dan r8:',int((d&z).sum()),' afwijkend van kale reductie:',int(((a!=kaal)&z).sum()))
ch='.#abcdGHIstu'
if '-p' in sys.argv:
    for x0,y0,x1,y1 in ((16,32,31,55),(15,54,45,63)):
        print('   r9'+' '*(x1-x0-1)+'r8'); print('   '+''.join(str(x%10) for x in range(x0,x1+1)))
        for y in range(y0,y1+1): print('%2d '%y+''.join(ch[v] for v in a[y,x0:x1+1]),' '+''.join(ch[v] for v in r8[y,x0:x1+1]))
