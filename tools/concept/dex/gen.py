import json,re,collections
D=json.load(open('sp.json'));sp=D['sp']
F=json.load(open('fams.json'))
REG=('_ALOLA','_GALAR','_HISUI','_PALDEA','_HOENN')
MANUAL={
 'ORICORIO':['SPECIES_ORICORIO_BAILE','SPECIES_ORICORIO_POM_POM','SPECIES_ORICORIO_PAU','SPECIES_ORICORIO_SENSU'],
 'BURMY':['SPECIES_BURMY_PLANT','SPECIES_WORMADAM_PLANT',('Mothim',['Bug','Flying'])],
 'UNOWN':[('Unown',['Psychic'])],
 'CASTFORM':['SPECIES_CASTFORM_NORMAL'],
 'MIMIKYU':['SPECIES_MIMIKYU_DISGUISED'],'MORPEKO':['SPECIES_MORPEKO_FULL_BELLY'],
 'SCATTERBUG':[('Scatterbug',['Bug']),('Spewpa',['Bug']),('Vivillon',['Bug','Flying'])],
 'FLABEBE':[('Flabébé',['Fairy']),('Floette',['Fairy']),('Florges',['Fairy'])],
 'TATSUGIRI':['SPECIES_TATSUGIRI_CURLY'],'INDEEDEE':['SPECIES_INDEEDEE_M'],
 'MINIOR':[('Minior',['Rock','Flying'])],'DEERLING':['SPECIES_DEERLING_SPRING','SPECIES_SAWSBUCK_SPRING'],
 'SQUAWKABILLY':['SPECIES_SQUAWKABILLY_GREEN'],'WISHIWASHI':['SPECIES_WISHIWASHI_SOLO'],
 'PUMPKABOO':['SPECIES_PUMPKABOO_AVERAGE','SPECIES_GOURGEIST_AVERAGE'],
 'SINISTEA':['SPECIES_SINISTEA_PHONY','SPECIES_POLTEAGEIST_PHONY'],'EISCUE':['SPECIES_EISCUE_ICE'],
 'FURFROU':[('Furfrou',['Normal'])],
 'POLTCHAGEIST':['SPECIES_POLTCHAGEIST_COUNTERFEIT','SPECIES_SINISTCHA_UNREMARKABLE'],
 'GIMMIGHOUL':['SPECIES_GIMMIGHOUL_CHEST','SPECIES_GHOLDENGO'],
 'SHELLOS':['SPECIES_SHELLOS_WEST','SPECIES_GASTRODON_WEST'],
 'BASCULIN':['SPECIES_BASCULIN_RED_STRIPED','SPECIES_BASCULEGION_M'],
}
APPEND={'CHERUBI':['SPECIES_CHERRIM_OVERCAST'],'DARUMAKA':['SPECIES_DARMANITAN_STANDARD'],'DUNSPARCE':['SPECIES_DUDUNSPARCE_TWO_SEGMENT'],
 'ESPURR':['SPECIES_MEOWSTIC_M'],'HONEDGE':['SPECIES_AEGISLASH_SHIELD'],'LECHONK':['SPECIES_OINKOLOGNE_M'],'TANDEMAUS':['SPECIES_MAUSHOLD_THREE'],
 'FINIZEN':['SPECIES_PALAFIN_ZERO'],'ROCKRUFF':['SPECIES_LYCANROC_MIDDAY'],'TOXEL':['SPECIES_TOXTRICITY_AMPED'],'MILCERY':[('Alcremie',['Fairy'])],
 'TYPE_NULL':[('Silvally',['Normal'])],'KUBFU':['SPECIES_URSHIFU_SINGLE_STRIKE']}
def members(key):
    out=[]
    if key in MANUAL: lst=MANUAL[key]
    else:
        lst=[m for m in F['SPECIES_'+key] if not (any(r in m for r in REG) and not any(r in key for r in REG) and m!='SPECIES_EXEGGUTOR_ALOLA')]
        lst+=APPEND.get(key,[])
    for m in lst:
        if isinstance(m,tuple): out.append(m)
        else:
            nm=sp[m].get('name',m); 
            if any(r in m for r in REG): nm=nm+' ('+{'_ALOLA':'Alola','_GALAR':'Galar','_HISUI':'Hisui','_PALDEA':'Paldea','_HOENN':'Hoenn'}[[r for r in REG if r in m][0]]+')'
            out.append((nm,sp[m]['types']))
    # dedupe
    seen=set();res=[]
    for n,t in out:
        if n in seen: continue
        seen.add(n);res.append((n,t))
    return res
BIO={'ALT':'Altiplano/puna (La Paz, Titicaca)','IJS':'Cordillera/gletsjers','LIP':'Uyuni/Lípez (zout, lagunes, geisers)','VULK':'Vulkanen','ATA':'Atacama','NEV':'Nevelwoud/yungas (Salento, Machu Picchu)','AMA':'Amazone/verdronken woud','PAN':'Pantanal/llanos (moeras)','TEP':'Tepuis/Gran Sabana','PAM':'Pampa/Chaco','PAT':'Patagonië','GAL':'Galápagos/eilanden','KUST':'Kust (Caribisch, Atlantisch, Humboldt)','ZEE':'Open zee/diepzee','STAD':'Steden/ruïnes','GROT':'Grotten/mijnen'}
rows=[]
for l in open('nom.txt'):
    l=l.rstrip('\n')
    if not l.strip() or l.startswith('#'): continue
    k,c,b,r,rev=(l.split('|')+['',''])[:5]
    rows.append(dict(key=k,cat=c,bio=[x for x in b.split(',') if x],reason=r,rev=rev,mem=members(k)))
leg=[]
for l in open('leg.txt'):
    k,c,b,r=(l.rstrip('\n').split('|')+['',''])[:4]
    t=sp['SPECIES_'+k]['types'] if 'SPECIES_'+k in sp else []
    nm=sp['SPECIES_'+k].get('name',k) if 'SPECIES_'+k in sp else k
    leg.append(dict(key=k,cat=c,bio=[x for x in b.split(',') if x],reason=r,name=nm,types=t))
def fam_str(mem): return ' → '.join(n for n,_ in mem)
def typ_str(mem):
    out=[]
    for n,t in mem:
        s='/'.join(t)
        if not out or out[-1][1]!=s: out.append([n,s])
    if len(out)==1: return out[0][1]
    return '; '.join(f"{n.split(' (')[0]} {s}" for n,s in out)
cnt={c:[0,0] for c in 'ABC'}
for r in rows:
    cnt[r['cat']][0]+=1; cnt[r['cat']][1]+=len(r['mem'])
# type counts for A+B (species)
tc=collections.Counter(); tcl=collections.Counter(); bc=collections.Counter(); bcs=collections.Counter()
for r in rows:
    if r['cat'] in 'AB':
        fam_types=set()
        for n,t in r['mem']:
            for x in t: tc[x]+=1; fam_types.add(x)
        for x in fam_types: tcl[x]+=1
        for b in r['bio']: bc[b]+=1; bcs[b]+=len(r['mem'])
json.dump(dict(rows=rows,leg=leg,cnt=cnt,tc=tc,tcl=tcl,bc=bc,bcs=bcs),open('out.json','w'),ensure_ascii=False)
print(cnt); print(sorted(tc.items(),key=lambda x:-x[1])); print(sorted(tcl.items(),key=lambda x:-x[1])); print(sorted(bc.items(),key=lambda x:-x[1])); print(sorted(bcs.items(),key=lambda x:-x[1]))
