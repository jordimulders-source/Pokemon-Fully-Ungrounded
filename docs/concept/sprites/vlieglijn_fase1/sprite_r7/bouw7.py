# r7: start r5 B.  python3 bouw7.py NAAM dx dy
# - oude verre poten van r5 (strook links van de nabije middenpoot, strook bij de nabije achterpoot) weg
# - verre ACHTERpoot = de donkere schuine poot uit r9, 1-op-1 (vorm/plek/richting); technisch: randcellen -> omlijning,
#   binnen -> kabel in schaduwtint (8 glans aan de lichtkant, 7), voetje -> donker koper 15
# - verre MIDDENpoot = kopie van de nabije middenpoot in schaduwtint (zoals r6), verschoven (dx,dy), alleen op lege pixels
# - r6-reparaties: schoon achtervoetje + lijn rond alle koperklauwtjes
import numpy as np, sys; from PIL import Image
PAL=[(255,0,255),(16,16,20),(32,32,36),(60,60,66),(104,104,110),(156,156,160),(188,188,192),
     (50,60,74),(86,100,118),(132,148,162),(234,248,252),(208,232,240),(116,146,162),(160,72,214),(224,116,52),(146,64,34)]
naam=sys.argv[1]; dx,dy=int(sys.argv[2]),int(sys.argv[3]); voor=len(sys.argv)>4  # 'voor': middenpoot vóór de verre achterpoot
r5=np.loadtxt('../sprite_r5/vlieg_r5_B.txt',dtype=int); basis=np.loadtxt('../sprite_r5/r5_basis_vol.txt',dtype=int)
r9=np.loadtxt('../sprite_r6/r9_nat_idx.txt',dtype=int)   # natief r9 (natief.py in sprite_r6)
f=r5.copy(); N=((1,0),(-1,0),(0,1),(0,-1)); log={}
oud=[(x,y) for y,x in zip(*np.where(r5!=basis))]
for x,y in oud: f[y,x]=basis[y,x]
log['oude verre poten r5 weg']=oud
for (x,y),v in {(47,57):1,(48,57):14,(46,57):0}.items(): f[y,x]=v      # achtervoetje schoon (r6)
# verre achterpoot uit r9
vorm={(x,y) for y in range(44,56) for x in range(32,42) if r5[y,x]==0 and r9[y,x] in (1,2,3,7)}
koper={(x,y) for y in range(44,56) for x in range(32,42) if r5[y,x]==0 and r9[y,x] in (14,15)}
achter=vorm|koper
for x,y in vorm: f[y,x]=1 if any(f[y+a,x+b]==0 and (x+b,y+a) not in achter for a,b in N) else 7
for x,y in sorted(vorm):
    if f[y,x]==7 and f[y,x-1] not in (7,8): f[y,x]=8
for x,y in koper: f[y,x]=15
log['verre achterpoot (r9)']=sorted(achter)
# verre middenpoot: kopie nabije middenpoot (schaduwtint)
base=f.copy(); POOT={7,8,9,10,11,12,14,15}; S={7:7,8:7,9:8,10:11,11:12,12:12,14:15,15:15,1:1}
m=[(x,y) for y in range(41,62) for x in range(26,40) if basis[y,x] in POOT or (basis[y,x]==1 and any(basis[y+a,x+b] in POOT for a,b in N))]
ns=set()
for x,y in m:
    X,Y=x+dx,y+dy
    if base[Y,X]!=0 and not (voor and (X,Y) in achter): continue
    if basis[y,x]!=1 and any(base[Y+a,X+b] in (14,15) and (X+b,Y+a) not in achter for a,b in N): continue
    f[Y,X]=S[basis[y,x]]; ns.add((X,Y))
for X,Y in list(ns):
    if f[Y,X]==1 and not any((X+b,Y+a) in ns and f[Y+a,X+b]!=1 for a,b in N): f[Y,X]=0; ns.discard((X,Y))
# restjes van de verre achterpoot die na 'voor' los liggen (<=2 kleurpixels) -> omlijning
rest={(x,y) for x,y in achter if f[y,x] not in (0,1) and (x,y) not in ns}; gezien=set()
for p in rest:
    if p in gezien: continue
    comp=[p]; gezien.add(p); i=0
    while i<len(comp):
        x,y=comp[i]; i+=1
        for a,b in N:
            q=(x+b,y+a)
            if q in rest and q not in gezien: gezien.add(q); comp.append(q)
    if len(comp)<=2:
        for x,y in comp: f[y,x]=1
log['verre middenpoot (kopie)']=sorted(ns)
dicht=[]
for y in range(41,63):
    for x in range(1,63):
        if f[y,x] in (14,15) or (((x,y) in achter or (x,y) in ns) and f[y,x]!=1):
            for a,b in N:
                if f[y+a,x+b]==0: f[y+a,x+b]=1; dicht.append((x+b,y+a))
log['lijn gesloten']=dicht
np.savetxt(f'vlieg_r7_{naam}.txt',f,fmt='%2d')
im=Image.fromarray(f.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save(f'vlieg_r7_{naam}.png',transparency=0)
Image.fromarray(np.array(PAL)[f].astype('uint8')).resize((512,512),Image.NEAREST).save(f'vlieg_r7_{naam}_8x.png')
print(naam,(dx,dy),{k:len(v) for k,v in log.items()}); ns=log['verre middenpoot (kopie)']; print('  verre middenpoot bbox x',min(p[0] for p in ns),'-',max(p[0] for p in ns),' y',min(p[1] for p in ns),'-',max(p[1] for p in ns))
