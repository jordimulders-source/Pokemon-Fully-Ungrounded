# Ribben uit het model: donkergroene modellijnen (groen, lum < 72) -> skelet -> spriteraster; alleen componenten >= LMIN natieve px.
# Gebruik als module: ribkaart(LMIN) -> (cnt, ln) 64x64
import sys,numpy as np; sys.path.append('../sprite_r2')
from groepen import laad; from lijnen import projecteer
def ribkaart(LMIN=15,lummax=72):
    a,lum,g=laad('../sprite_r2/natief.png'); geo=np.load('../sprite_r2/kaal_info.npz')['geo']
    cnt,ln,sk=projecteer(g,geo,(g==4)&(lum<lummax))
    return np.where(ln>=LMIN,cnt,0),ln
if __name__=='__main__':
    from tekstraster import lees,CH
    o=lees(sys.argv[1]); c,ln=ribkaart(int(sys.argv[2]) if len(sys.argv)>2 else 15)
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(13,63): print('%2d '%y+''.join(('R' if c[y,x] else CH[o[y,x]]) if o[y,x] else '.' for x in range(64)))
