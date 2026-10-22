import re, json, glob, sys
root='/home/user/projectgrounded/src/data/pokemon/species_info/'
species={}
order=[]
for f in sorted(glob.glob(root+'gen_*_families.h')):
    gen=int(re.search(r'gen_(\d)',f).group(1))
    txt=open(f).read()
    parts=re.split(r'\n    \[(SPECIES_\w+)\] =', txt)
    for i in range(1,len(parts),2):
        sp=parts[i]; body=parts[i+1]
        # cut at next top-level closing "    },"
        m=re.search(r'\n    },',body); body=body[:m.start()] if m else body
        d={'gen':gen}
        t=re.findall(r'\.types = MON_TYPES\((TYPE_\w+)(?:, (TYPE_\w+))?\)',body)
        if t: d['types']=[x.replace('TYPE_','').title() for x in t[0] if x]
        else:
            M={'MAGNEMITE_FAMILY_TYPE2':'TYPE_STEEL','TOGEPI_FAMILY_TYPE1':'TYPE_FAIRY','RALTS_FAMILY_TYPE2':'TYPE_FAIRY','COTTONEE_FAMILY_TYPE2':'TYPE_FAIRY'}
            m=re.search(r'\.types = MON_TYPES\(([\w ,]+)\)',body)
            if m: d['types']=[M.get(x.strip(),x.strip()).replace('TYPE_','').title() for x in m.group(1).split(',')]
            elif 'CLEFAIRY_FAMILY_TYPES' in body: d['types']=['Fairy']
            elif 'JIGGLYPUFF_FAMILY_TYPES' in body: d['types']=['Normal','Fairy']
            elif 'ROTOM_FAMILY_TYPES' in body: d['types']=['Electric','Ghost']
        if 'types' in d:
            d['types']=list(dict.fromkeys(d['types']))
        a=re.findall(r'\.abilities = \{([^}]*)\}',body)
        if a: d['abil']=[x.strip().replace('ABILITY_','').replace('_',' ').title() for x in a[0].split(',')]
        n=re.search(r'\.speciesName = _\("([^"]*)"\)',body)
        if n: d['name']=n.group(1)
        nd=re.search(r'\.natDexNum = (NATIONAL_DEX_\w+)',body)
        if nd: d['nat']=nd.group(1)
        e=body.find('.evolutions = EVOLUTION(')
        evos=[]
        if e>=0:
            depth=0;j=e+len('.evolutions = EVOLUTION')
            start=j
            while True:
                c=body[j]
                if c=='(':depth+=1
                elif c==')':
                    depth-=1
                    if depth==0:break
                j+=1
            ev=body[start:j]
            for m in re.finditer(r'\{(EVO_\w+),\s*([^,]+),\s*(SPECIES_\w+)',ev):
                evos.append((m.group(1),m.group(2).strip(),m.group(3)))
        d['evos']=evos
        d['legend']=bool(re.search(r'\.isLegendary = TRUE|\.isMythical = TRUE|\.isUltraBeast = TRUE|isSubLegendary',body)) 
        d['flags']=[k for k in ['isLegendary','isMythical','isUltraBeast','isParadox','isRestrictedLegendary','isSubLegendary','isMegaEvolution','isGigantamax','isPrimalReversion','isUltraBurst','isTeraForm','isTotem','isAlolanForm','isGalarianForm','isHisuianForm','isPaldeanForm','isFrontierBanned','isBattleOnlyForm'] if re.search(r'\.'+k+r' = TRUE',body)]
        if sp not in species: order.append(sp)
        species[sp]=d
json.dump({'order':order,'sp':species},open(sys.argv[1],'w'),indent=0)
print(len(order))
