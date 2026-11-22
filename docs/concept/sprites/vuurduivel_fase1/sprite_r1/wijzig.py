# wijzig.py: handmatige reparaties op raster_auto.txt -> raster_r1.txt ; elke pixel met reden (alle naar het model)
import sys
R=[list(r.rstrip('\n')) for r in open('raster_auto.txt')]
E={}
def zet(x,y,c,reden): E[(x,y)]=(R[y][x],c,reden); R[y][x]=c
# --- ver oog (reductie verloor het oogwit): naar natieve cellen sx16-18, y32b-34a
zet(16,32,'#','ver oog: bovenlid (model zwart 32a)')
zet(18,32,'#','ver oog: lid sluit aan op wenkbrauw (model #m 32b)')
zet(16,33,'W','ver oog: oogwit (model dW/dW)')
zet(17,33,'W','ver oog: oogwit (model W#/W#)')
zet(18,33,'#','ver oog: pupil rechts (model W#/#W, ## eronder)')
# --- neus: grijs puntje in het model (natief 35a sx20 'l')
zet(20,35,'l','neus: lichtgrijs puntje uit het model')
exec(open('wijzig_extra.py').read()) if __import__('os').path.exists('wijzig_extra.py') else None
open('raster_r1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
with open('wijzigingen.txt','w') as f:
    for (x,y),(a,b,r) in sorted(E.items(),key=lambda t:(t[0][1],t[0][0])): f.write('(%d,%d) %s->%s  %s\n'%(x,y,a,b,r))
print(len(E),'pixels met de hand')
