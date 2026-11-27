# Ronde 10: minder wollerig, uitgaande van B6/B9. a = zelfde omtrek, rand rustig (alleen punten onderaan);
# b = slanker en hangend (smal achter de oren, breder over de schouder), gerafelde onderrand.
import r9lib as R, r8lib as L, r8, r9
def bouw(N,v_):
    v=R.Vorm9(N,slank=(v_=='b')); v.veld(*r8.VELD,label='vlak: Arcanine-rugpluk (x33-60,y2-26) op (7,23)')
    links=min(x for x,y in v.mask0 if y>=33); st=[]
    for x in (8,11,14,17):
        x=max(x,links-1); b=r9.onderrand(v.mask0,x+2)
        if b is not None: st.append((r8.A_DOWN,x,b-3,'onderpunt x%d'%x,1))
    if v_=='a': st.append((r8.A_DOWN,25,27,'punt onder de kam (over de rug)',1))
    for s in st: v.rand(*s[0],s[1],s[2],False,label=s[3],diepte=s[4])
    v.stukken=st
    return v,v.maak()
if __name__=='__main__':
    import sys
    from PIL import Image
    V=Image.new('RGB',(4*300,300),'white')
    for i,k in enumerate(['6a','9a','6b','9b']):
        v,g=bouw(int(k[0]),k[1]); print(k,L.rechte(g,v.mask)); L.toon(g,22,46,36)
        V.paste(L.rgba8(g).crop((2,16,38,52)).resize((288,288),0),(i*300,0))
    V.save(sys.argv[1])
