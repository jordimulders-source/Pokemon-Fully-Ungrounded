# Groen spookwiel: het wiel uit r6 (natief r6, middelpunt (89,149), straal 16) uitgesneden, geschaald naar het r5-wiel
# (middelpunt (95.5,135.5), straal 10.5 -> factor 0.656) en op die plek gelegd; daarna verkleind naar de sprite:
# per spritepixel het natieve r6-blok, "donkerste wint": aandeel donkere ringpixels >= T -> #467e4b, anders
# middentoon-meerderheid -> #67b370, anders licht #72d779. Alleen groene r3-pixels binnen de wielschijf. Niets getekend.
import sys, numpy as np; from PIL import Image
T=float(sys.argv[1]) if len(sys.argv)>1 else 0.35
b=np.asarray(Image.open('natief_r6.png').convert('RGB')).astype(int); Lb=b@[0.3,0.59,0.11]
s,X0,Y0,oy,XC,k=[float(v) for v in open('r1.meta').read().split()]
r3=np.asarray(Image.open('../sprite_r3/sprite.png')).astype(int)
C5=(95.5,135.5); C6=(89.0,149.0); R6=16.0; F=10.5/R6
def to6(nx,ny): return C6[0]+(nx-C5[0])/F, C6[1]+(ny-C5[1])/F
def build(T,R=R6):
    o=r3.copy(); n=0; zone=np.zeros((64,64),bool)
    for j in range(64):
        for i in range(64):
            if r3[j,i] not in (3,4,5): continue
            sub=[]
            for dy in (np.arange(8)+0.5)/8:
                for dx in (np.arange(8)+0.5)/8:
                    nx=X0+(i+dx)/s; ny=Y0+(j-oy+dy)/s; x6,y6=to6(nx,ny)
                    if (x6-C6[0])**2+(y6-C6[1])**2<=R**2: sub.append(Lb[int(y6),int(x6)] if b[int(y6),int(x6)][1]>b[int(y6),int(x6)][0]+10 else 60.0)
            if len(sub)<32: continue          # pixel valt voor minder dan de helft in de wielschijf
            zone[j,i]=True; sub=np.array(sub)
            if (sub<115).mean()>=T: v=5
            elif (sub<150).mean()>=0.5: v=4
            else: v=3
            if v!=o[j,i]: o[j,i]=v; n+=1
    return o,n,zone
if __name__=='__main__':
    o,n,z=build(T); print('T',T,'gewijzigd',n,'zone',z.sum())
    ch={0:'.',1:'O',3:'+',4:'o',5:'#',6:'N'}
    for y in range(42,60): print(y,''.join(ch.get(v,'w') for v in o[y,14:36]))
    np.save(f'w6_T{T}.npy',o); np.save('zone.npy',z)
