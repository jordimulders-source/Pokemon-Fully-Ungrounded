# rollen.npy (+ handreparaties in rollen_hand.txt als die er is) -> geindexeerde 64x64 varianten
import numpy as np, os, sys; from PIL import Image
if os.path.exists('rollen_hand.txt'):
    o=np.array([list(l.rstrip('\n')[3:]) for l in open('rollen_hand.txt') if l.strip()])
else: o=np.load('rollen.npy')
H,W=o.shape
CREME=[(246,236,202),(228,208,158),(186,156,104),(126,94,54)]   # L M D S
GEEL =[(255,238,139),(240,204,72),(196,150,40),(139,98,0)]
def pal(ledematen):
    L,M,D,S=ledematen
    return {'.':(0,0,0),'K':(16,14,22),
            '1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
            'L':L,'M':M,'D':D,'S':S,
            'B':(80,120,200),'b':(44,66,140),'R':(214,66,58),'r':(140,36,40),
            'W':(248,248,248),'w':(184,184,206)}
VOLG='.K123gLMDSBbRrWw'
# zones (rijen/kolommen in het raster)
def zone(j,i):
    if j<=22 and i<=6: return 'arm'
    if 32<=j<=42 and i>=23: return 'arm'
    if 23<=j<=26 and 11<=i<=22: return 'zig1'
    if 27<=j<=31 and 11<=i<=22: return 'zig2'
    return ''
def variant(naam, ledematen, zig1=None, zig2=None, armwissel=False):
    p=pal(ledematen); r=o.copy()
    wis={'B':'R','b':'r','R':'B','r':'b'}
    for j in range(H):
        for i in range(W):
            c=o[j,i]; z=zone(j,i)
            if armwissel and z=='arm' and c in wis: r[j,i]=wis[c]
            if z=='zig1' and zig1 and c in 'Bb': r[j,i]=zig1[c]
            if z=='zig2' and zig2 and c in 'Bb': r[j,i]=zig2[c]
    full=np.zeros((64,64),'uint8'); x0=(64-W)//2; y0=64-H
    for j in range(H):
        for i in range(W): full[y0+j,x0+i]=VOLG.index(r[j,i])
    im=Image.fromarray(full,'P'); flat=[v for k in VOLG for v in p[k]]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save(naam,transparency=0); return im
WIT={'B':'W','b':'w'}; ROOD={'B':'R','b':'r'}
variant('astro_A.png',CREME)
variant('astro_A_geel.png',GEEL)
variant('astro_B1.png',CREME,WIT,ROOD,True)
variant('astro_B2.png',CREME,ROOD,WIT,True)
print('ok',W,H)
