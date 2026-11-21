# schrijft samba_A.png, samba_B.png, samba.png (=A) + log; python3 maak.py
import json
exec(open('bouw.py').read())
def save(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL+[0]*(768-48)); im.save(naam,transparency=0)
out={}
for opt in 'AB':
    o[:]=BASIS; n0=o.copy(); geel(opt); LOG['S8_geel_'+opt]=int((n0!=o).sum()); out[opt]=o.copy(); save(o,'samba_%s.png'%opt)
save(out['A'],'samba.png')
# bewaking: alpha-diff en bevroren zones
for opt in 'AB':
    a=out[opt]; al=int(((a>0)!=(R1>0)).sum()); fz=int(((a!=R1)&FROZEN).sum())
    LOG['controle_'+opt]={'alpha_diff_vs_r1':al,'bevroren_lijf_kop_oog_snavel_poten_gewijzigd':fz,'herkleurd_totaal':int(((a!=R1)&(a>0)&(R1>0)).sum()),
        'kleuren_gebruikt':len(np.unique(a)), 'kuif':int(((a!=R1)&KUIF).sum()),'waaier':int(((a!=R1)&FAN).sum()),'vleugel_L':int(((a!=R1)&WL).sum()),'vleugel_R':int(((a!=R1)&WR).sum())}
    print(opt,LOG["controle_"+opt])
    assert al==0 and fz==0 and len(np.unique(a))<=16
json.dump(LOG,open('log.json','w'),indent=1); print(json.dumps(LOG,indent=1))
