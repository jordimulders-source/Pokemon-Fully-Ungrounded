# probeer.py: vellen met probeersels (kop P1-P3, wang) op 8x/16x naast het model.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r2/gereedschap')
from fv import *; import palet, kijk, bouw_r2 as b
from PIL import ImageDraw
def snip(o,x0,y0,x1,y1,z): return palet.rgb(o[y0:y1,x0:x1]).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
def vel(items,uit,x0,y0,x1,y1,z,titel=True):
    w=(x1-x0)*z; h=(y1-y0)*z
    v=Image.new('RGB',(len(items)*(w+12),h+20),'white'); d=ImageDraw.Draw(v)
    for i,(nm,im) in enumerate(items):
        v.paste(im,(i*(w+12),18)); d.text((i*(w+12),2),nm,fill=(0,0,0))
    v.save(uit); return v
if __name__=='__main__':
    wat=sys.argv[1]
    if wat=='wang':
        x0,y0,x1,y1,z=31,40,40,51,24
        it=[('r1',snip(b.a0,x0,y0,x1,y1,z))]
        for wv in sys.argv[2:]: it.append((wv,snip(b.zet(b.a0,b.wang(wv)),x0,y0,x1,y1,z)))
        it.append(('model',kijk.modelblok(16,x0,y0,x1,y1,z)))
        vel(it,'/tmp/claude-0/wang_vel.png',x0,y0,x1,y1,z)
    if wat=='kop':
        x0,y0,x1,y1,z=18,40,40,56,8
        basis=b.zet(b.zet(b.A1,b.VLEUGEL),b.wang('W3'))
        it=[('r1 A',snip(b.A1,x0,y0,x1,y1,z))]
        vs=sys.argv[2:]
        for kv in vs: it.append((kv,snip(b.kap(basis,kv,False),x0,y0,x1,y1,z)))
        it.append(('model',kijk.modelblok(16,x0,y0,x1,y1,z)))
        v=vel(it,'/tmp/claude-0/kop_vel.png',x0,y0,x1,y1,z)
        # 1x en 2x rij eronder, licht en donker
        W=v.width; rij=Image.new('RGB',(W,150),'white')
        for i,kv in enumerate(['r1']+vs):
            o=b.A1 if kv=='r1' else b.kap(basis,kv,False)
            for j,bg in enumerate(((232,232,216),(40,48,56))):
                im=palet.rgb(o,bg); rij.paste(im,(i*((x1-x0)*z+12)+j*68,4))
            rij.paste(palet.rgb(o,(232,232,216)).resize((128,128),Image.NEAREST).crop((20,40,110,128)),(i*((x1-x0)*z+12),70))
        t=Image.new('RGB',(W,v.height+150),'white'); t.paste(v,(0,0)); t.paste(rij,(0,v.height)); t.save(sys.argv[0].replace('probeer.py','')+'../kop_probeersels.png' if False else '/tmp/claude-0/kop_vel.png')
