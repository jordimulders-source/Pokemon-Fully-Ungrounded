import re,glob,collections,sys
sys.path.insert(0,'docs/concept/sprites/showcase')
src="".join(open(f).read() for f in glob.glob('src/data/pokemon/species_info/*.h'))
T={}
ms=list(re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{',src))
for i,m in enumerate(ms):
    t=re.search(r'MON_TYPES\((TYPE_\w+)(?:,\s*(TYPE_\w+))?\)',src[m.end():ms[i+1].start() if i+1<len(ms) else None])
    if t: T[m.group(1)]={x[5:].lower() for x in t.groups() if x}
def const(n):
    n=n.strip(); f=re.match(r'(.*?) \((\w+)\)$',n); form=''
    if f: n,form=f.groups()
    c='SPECIES_'+re.sub(r'[^A-Z0-9]','',n.upper().replace(' ','_').replace('-','_')).replace('__','_')
    c='SPECIES_'+re.sub(r'[^A-Z0-9_]','',n.upper().replace(' ','_').replace('-','_').replace('♀','_F').replace('♂','_M'))
    c=c.replace('.','').replace('É','E')
    if form: c+='_'+form.upper()
    for k in (c,c.replace('_',''),c+'_NORMAL'):
        if k in T: return k
    alt=[k for k in T if k.startswith(c)]
    return alt[0] if alt else None
L=open('docs/concept/DEX_IN_ROM.md').read().split('\n')
lines=[]
for row in (L[27],L[29]):
    body=row.split(':**',1)[1].strip().rstrip('.')
    for ln in body.split('; '):
        ts=set(); miss=[]
        for n in ln.split(' → '):
            c=const(n)
            if c: ts|=T[c]
            else: miss.append(n)
        fix={'Scatterbug':{'bug','flying'},'Flabébé':{'fairy'},'Cleffa':{'fairy'},'Magnemite':{'electric','steel'},'Unown':{'normal'}}
        if miss and miss[0] in fix: ts|=fix[miss[0]]
        elif miss: print('MISS',miss,file=sys.stderr)
        lines.append([ln.split(' → ')[0],ts])
lines=[l for l in lines if l[0] not in ('Mew','Mewtwo','Zarude')]
lines.append(['Hitmontop',{'fighting'}])
# Cosmic-besluiten
for l in lines:
    if l[0] in('Lunatone','Solrock','Cleffa','Clefairy'): l[1].add('cosmic')
    if l[0]=='Elgyem': l[1]={'cosmic'}
# evoluties van bestaande soorten: types erbij in de basislijn
src_sv=open('docs/concept/sprites/showcase/maak_vel.py').read()
evo=re.findall(r"\('[^']*', '[^']*\((\w+)\)', '([^']*)'\)",src_sv)
fam={'Hitmontop':'Tyrogue','Octillery':'Remoraid','Banette':'Shuppet','Delibird':'Delibird','Dunsparce':'Dunsparce','Mightyena':'Poochyena','Bibarel':'Bidoof','Sunflora':'Sunkern','Kricketune':'Kricketot','Solrock':'Solrock','Lunatone':'Lunatone','Emolga':'Emolga','Ledian':'Ledyba'}
for base,t in evo:
    hit=[l for l in lines if any(fam.get(base,base)==x for x in [l[0]]) or fam.get(base,base) in l[0]]
    if hit: hit[0][1]|=set(t.replace('fight','fighting').split('/'))
    else: lines.append([base+'+evo',set(t.replace('fight','fighting').split('/'))]); print('evo los',base,file=sys.stderr)
# nieuwe en regionale lijnen uit het overzichtsvel
groups={
'New':None,'Regional':None}
def grp(items,keyfn):
    d=collections.OrderedDict()
    for p,n,t in items: d.setdefault(keyfn(p),set()).update(t.replace('fight','fighting').split('/'))
    return d
secs={k:v for k,v in re.findall(r'\("([^"]+)",\[(.*?)\]\)',src_sv,re.S)}
def items(k): return re.findall(r'\(\s*["\']([^"\']+)["\']\s*,\s*([\'"].*?[\'"])\s*,\s*["\']([^"\']+)["\']\s*\)',secs[k])
NEW={'alpaca':'alpaca','lama':'alpaca','olinguito_v2':'olin','coathief':'olin','wasbeer':'olin','nachtaap':'nacht','nachtaap_evo':'nacht','nachtaap_fase3':'nacht','cuyby':'cuy','cuyby_evo':'cuy','hatun_runa':'inca','awki':'inca','koningstiran':'inca','kolibrie_pre':'koli','kolibrie':'koli','picapau':'pica','picapau_evo':'pica','poedellarve':'poedel','poesrups':'poedel','poedelmot':'poedel','sneeuwbolslak':'slak','sneeuwbolslak_fase2':'slak','ijskomeet':'slak','blobfish':'blob','blobfish_fase2':'blob','spooktrein_fase1':'trein','spooktrein_fase2':'trein','spooktrein_fase3':'trein','pitahaya_draak':'pit','pitahaya_draak_fase2':'pit','pitahaya_draak_fase3':'pit','vuurwerk_fase1':'vw','vuurwerk_fase3':'vw','mate':'mate','mate_fase2':'mate','vlieglijn_fase1':'vlieg','vlieglijn_fase2':'vlieg','vuurduivel_fase1':'duivel','vuurduivel_fase2':'duivel','gnomini':'gnome','gnomad':'gnome','gnometrotter_rock':'gnome','gnometrotter_ice':'gnome','gnometrotter_grass':'gnome','satelliet_lijn':'sat','satelliet_fase2':'sat','satelliet_fase3':'sat','capybarrel':'capy','capykart':'capy','guarana':'gua','guarana_fase2':'gua','sneeuwmonster':'sm','sneeuwmonster_fase2':'sm','sneeuwmonster_fase3':'sm'}
d=grp(items('New'),lambda p:NEW.get(p.split('/')[0],p.split('/')[0]))
R={'silicobra_uyuni':'sil','salticonda':'sil','abra_regional':'abra','kadabra_regional':'abra','alakazam_regional':'abra','dustly':'gas','hauntflare':'gas','gengas':'gas','rufflet_regional':'ruf','harpij_braviary':'ruf','mrmime_regional':'mime','mr_prime':'mime','poliwag_regional':'poli','poliwhirl_regional':'poli','poliwrath_regional':'poli','grimer_hoenn':'grim','muk_hoenn':'grim'}
r=grp(items('Regional forms / convergent Pokémon'),lambda p:R.get(p.split('/')[0],p.split('/')[0]))
g=grp(items('Legendaries'),lambda p:p)
E=collections.Counter()
for b,t in evo: E.update(t.replace('fight','fighting').split('/'))
print('nieuw',len(d),'regionaal',len(r),'bestaand',len(lines),'legendaries(af)',len(g))
C=collections.Counter(); Cn=collections.Counter()
for ts in [l[1] for l in lines]+list(r.values()): C.update(ts)
for ts in d.values(): C.update(ts); Cn.update(ts)
print('totaal lijnen',len(lines)+len(r)+len(d))
Rn=collections.Counter()
for ts in r.values(): Rn.update(ts)
print('evo-designs',len(evo))
for t,n in C.most_common(): print(f"{t:9} orig {Cn[t]:3}  regio {Rn[t]:3}  evo {E[t]:3}  nieuw-tot {Cn[t]+Rn[t]+E[t]:3}  hele dex {n:3}")
