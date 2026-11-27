# Ronde 9: r9/kudu_r9_<manier><N>.png (+_8x), r9/vel.png (keuzevel), r9/telling.txt, r9/bronnen.txt. Oog K4.
import r9, r8lib as L, vel8
from PIL import Image, ImageDraw
POOT={(x,y) for y in range(46,56) for x in range(15,22) if L.R6[y][x] in 'D0'}
NAAM={'A':'A: pluizige kraag met puntjes (Arcanine)','B':'B: lang hangend kapsel, gerafelde onderrand'}
tel=open('r9/telling.txt','w'); bron=open('r9/bronnen.txt','w'); res={}
for m in 'AB':
    for N in r9.VORMEN:
        v,g=r9.bouw(N,m); g=vel8.met_oog(g); k='%s%d'%(m,N)
        diff={(x,y) for y in range(L.H) for x in range(L.W) if g[y][x]!=vel8.REF[y][x]}
        buiten=diff-L.ZONE; oog=diff&vel8.OOG; hals=[p for p in L.HALS if g[p[1]][p[0]]!='M']
        gap=min(max(abs(px-mx),abs(py-my)) for px,py in POOT for mx,my in v.mask)
        tel.write('%s (%s, onderrand borstkant %d px hoger): %d px anders dan r6+K4; buiten manen+vrijgekomen zone: %d; oogvlak: %d; halsstrook: %d; '
                  'rechte manenlijnen >3 px: %s; kleinste afstand manen-voorpoot: %d px; vrijgekomen borst: %d px; kleuren: %d\n'%(
                  k,NAAM[m],N,len(diff),len(buiten),len(oog),len(hals),L.rechte(g,v.mask) or 'geen',gap,len(v.lijf),len(set(c for r in g for c in r))))
        bron.write('== %s\n  stukken: %s\n'%(k,'; '.join('%s <- %s (%d,%d)-(%d,%d) op (%d,%d)%s'%(s[3],s[0][0],*s[0][1:],s[1],s[2],' gespiegeld' if len(s)>5 and s[5] else '') for s in v.stukken)))
        for p in sorted(diff,key=lambda p:(p[1],p[0])):
            bron.write('  (%d,%d) %s -> %s  %s\n'%(p[0],p[1],vel8.REF[p[1]][p[0]],g[p[1]][p[0]],' '.join(map(str,v.bron.get(p,('?',))))))
        L.png(g,'r9/kudu_r9_%s.png'%k); L.rgba8(g).resize((512,512),0).save('r9/kudu_r9_%s_8x.png'%k)
        res[k]=g; print(k,len(diff),len(buiten),len(oog),len(hals),gap)
tel.close(); bron.close()
# keuzevel: kolommen = vorm (N), rijen = manier; per cel 8x (crop van kop t/m poten) + 1x licht/donker
CW,CH=8*44,8*48
V=Image.new('RGB',(3*(CW+20)+20,2*(CH+130)+40),'white'); d=ImageDraw.Draw(V)
d.text((20,8),'Kudu r9 - kolommen: onderrand van de manen aan de borstkant 3 / 6 / 9 px hoger; rijen: manier A / B. Oog K4. Rechts onder elke 8x: 1x op licht en donker.',fill=(0,0,0))
for j,m in enumerate('AB'):
    for i,N in enumerate(r9.VORMEN):
        k='%s%d'%(m,N); g=res[k]; x=20+i*(CW+20); y=30+j*(CH+130)
        d.text((x,y),'%s  |  %d px hoger'%(NAAM[m],N),fill=(0,0,0))
        V.paste(L.rgba8(g).crop((2,16,46,64)).resize((CW,CH),0),(x,y+14))
        for t,bg in enumerate([(255,255,255),(40,44,52)]):
            V.paste(Image.new('RGB',(84,74),bg),(x+t*90,y+CH+22)); V.paste(L.rgba8(g,bg),(x+10+t*90,y+CH+27))
        d.text((x+190,y+CH+40),'r9_%s'%k,fill=(0,0,0))
V.save('r9/vel.png')
