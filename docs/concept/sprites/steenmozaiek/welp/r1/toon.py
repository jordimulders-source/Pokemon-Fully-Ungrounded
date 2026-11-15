# Meting: per vak gemiddelde helderheid van de vlakpixels (omlijning 1/2 eruit) in sprite vs model (zelfde spritepixels).
import sys,numpy as np; from PIL import Image; from palet import PAL,CH
a=np.asarray(Image.open('natief.png')).astype(float); L=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
s=165/46
rows=[l.rstrip('\n') for l in open(sys.argv[1]) if l.strip()]
pl=[0.299*r+0.587*g+0.114*b for r,g,b in PAL]
def mod(x,y):
    ya=37+(y-22)*s; xa=18+(x-9)*s; return L[int(ya):int(ya+s),int(xa):int(xa+s)].mean()
vakken={'voorhoofd':(13,24,20,29),'snuit':(12,32,20,36),'wang':(24,30,30,35),'oor_r':(27,23,31,29),'nek':(20,36,30,41),
        'poot_op':(10,43,17,48),'onderarm':(16,44,23,50),'borst':(20,42,25,49),'schouder':(25,40,36,51),'rug':(36,40,46,49),
        'voorpoot':(25,50,33,57),'heup':(36,48,48,57),'achtervoet':(37,58,46,61),'voorvoet':(23,57,32,62),'staart':(46,50,55,57)}
for n,(x0,y0,x1,y1) in vakken.items():
    sp=[];md=[]
    for y in range(y0,y1):
        for x in range(x0,x1):
            c=CH.index(rows[y][x])
            if c in (0,1,2): continue
            sp.append(pl[c]); md.append(mod(x,y))
    if sp: print('%-11s sprite %5.1f  model %5.1f  diff %+5.1f'%(n,np.mean(sp),np.mean(md),np.mean(sp)-np.mean(md)))
