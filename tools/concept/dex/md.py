import json,re,collections
exec(open('gen.py').read().split("rows=[]")[0])  # members, BIO etc
O=json.load(open('out.json'))
rows=O['rows']; leg=O['leg']
def expand(lst):
    prev=''
    for r in lst:
        if r['reason'].startswith('idem'): r['reason']=prev.split(';')[0]+r['reason'][4:]
        prev=r['reason']
expand(rows); expand(leg)
def fam_str(mem): return ' → '.join(n for n,_ in mem)
def typ_str(mem):
    out=[]
    for n,t in mem:
        s='/'.join(t)
        if out and out[-1][1]==s: out[-1][0].append(n)
        else: out.append([[n],s])
    if len(out)==1: return out[0][1]
    return '; '.join(f"{', '.join(n)}: {s}" for n,s in out)
def bio(r): return ', '.join(r['bio']) if r['bio'] else '–'
L=[]
A=[r for r in rows if r['cat']=='A']; B=[r for r in rows if r['cat']=='B']; C=[r for r in rows if r['cat']=='C']
C1=[r for r in C if re.search(r'botst|rol gaat|neemt|Rol gaat|overlap|Overlap|Afrika|Azië|Australië|noordpool|Japan|Hawaï|niche|via |volstaat|genoeg|dubbel|Dubbel|beter|liever|gaat naar|Hisui|Galar|Paldea|Alolan|Fossiel|fakemon',r['reason'])]
C2=[r for r in C if r not in C1]
nA=sum(len(r['mem']) for r in A); nB=sum(len(r['mem']) for r in B); nC=sum(len(r['mem']) for r in C)
RF=[l.rstrip('\n').split('|') for l in open('rf.txt') if l.strip() and not l.startswith('#')]
P=L.append
P("# Dex-nominaties (regionale dex)\n")
P("> Status (22 okt): voorstel van Claude, nog niet besloten door Jordi. Types, evoluties en abilities komen uit de repo (`src/data/pokemon/species_info/`, via een script); revisies uit `docs/ungrounded/CHANGELOG_UNGROUNDED.md`. Wat Jordi besluit, gaat naar `POKEMON.md`.\n")
P("## Samenvatting\n")
P("| Categorie | Lijnen | Soorten |\n|---|---|---|")
P(f"| 1. Past in Zuid-Amerika | {len(A)} | {nA} |")
P(f"| 2. Niet Zuid-Amerikaans, hoort er toch in (iconisch of Ungrounded-revisie) | {len(B)} | {nB} |")
P(f"| **Genomineerd (1 + 2)** | **{len(A)+len(B)}** | **{nA+nB}** |")
P(f"| 3. Twijfel / bewust niet (geen legendaries) | {len(C)} | {nC} |")
P(f"| Legendaries/mythicals (apart, sectie 4) | {len(leg)} | – |")
P(f"| Regional forms (sectie 5) | {len(RF)} lijnen (waarvan 1 besloten: Venomoth) | – |\n")
P(f"- **{nA+nB} soorten** uit de National Dex, binnen het doel van 400–500. Met ±100 fakemon en ±10–15 regional forms komt de regionale dex op ±575–600. Wil Jordi richting 400, dan zijn de B-lijnen zonder Zuid-Amerikaanse band en zonder Ungrounded-revisie het eerst te schrappen (Kanto-starters, Munchlax, Audino, Ditto, Happiny, Mimikyu e.d.).")
P("- Telling per soort: elke evolutie telt mee, ook baby's; Mega's en Gmax tellen niet. Regionale vormen van andere regio's tellen alleen mee als ze zelf genomineerd zijn (Alolan Sandshrew/Vulpix/Exeggutor, Hoenn-Grimer).")
P("- **Opvallendste nominaties:** Hippopotas (Escobars nijlpaarden in Colombia), Nosepass (moai, Paaseiland), Bidoof (bevers als ecologische ramp in Vuurland), Yamask (Chinchorro-mummies), Smeargle (Cueva de las Manos), Bouffalant (waterbuffelpolitie op Marajó), Combee (Afrikaanse 'killer bees' uit Brazilië), Tynamo (sidderaal), Squawkabilly (monniksparkieten-'bendes' in de steden), Mew (volgens de lore ontdekt in Guyana).")
P("- **Grootste gaten** (sectie 6–8): Fire en Fighting zijn het dunst; tepuis, Lípez/Uyuni, Galápagos en de vulkanen hebben te weinig bestaande soorten; de altiplano mist vroege Grass, Bug en Flying. Die plekken zijn voor de fakemon.\n")
P("**Biomes (codes in de tabellen):** " + '; '.join(f"`{k}` {v}" for k,v in BIO.items()) + ".\n")
def table(rs, revcol=True):
    P("| Lijn | Types (repo) | Reden | Biome | Ungrounded-revisie |" if revcol else "| Lijn | Types (repo) | Reden |")
    P("|---|---|---|---|---|" if revcol else "|---|---|---|")
    for r in rs:
        if revcol: P(f"| {fam_str(r['mem'])} | {typ_str(r['mem'])} | {r['reason']} | {bio(r)} | {r['rev'] or '–'} |")
        else: P(f"| {fam_str(r['mem'])} | {typ_str(r['mem'])} | {r['reason']} |")
    P("")
P(f"## 1. Past in Zuid-Amerika ({len(A)} lijnen, {nA} soorten)\n")
P("Gebaseerd op een Zuid-Amerikaans dier, plant of mythe, of ecologisch heel plausibel in een van de biomes. Besloten soorten (Slakoth, Pikipek, Flamigo, Minccino, Sigilyph, Heatmor, Alolan Exeggutor, Venomoth-vorm) staan er ook in.\n")
table(A)
P(f"## 2. Niet Zuid-Amerikaans, hoort er toch in ({len(B)} lijnen, {nB} soorten)\n")
P("Iconisch (mascottes, fan-favorieten, pseudo-legendaries), nodig voor de type-dekking van gyms/E4, of uniek veranderd in Ungrounded. Biome = waar hij het minst uit de toon valt.\n")
table(B)
P(f"## 3. Twijfelgevallen en bewust niet ({len(C)} lijnen, {nC} soorten)\n")
P("Als de regel 'alle Pokémon zijn te krijgen' uit Ungrounded blijft, kunnen deze soorten post-game komen (Safari, Spacetime, ruilen) zonder in de regionale dex te staan.\n")
P(f"### 3a. Botst met fakemon of immersie ({len(C1)} lijnen)\n")
table(C1, revcol=False)
P(f"### 3b. Geen band met de regio (eventueel post-game) ({len(C2)} lijnen)\n")
table(C2, revcol=False)
P("## 4. Legendaries en mythicals\n")
P("De regio krijgt een eigen trio (condor, poema, slang) en Pachamama. Bestaande legendaries alleen als ze er een echte band mee hebben, en dan als optionele of post-game-ontmoeting.\n")
P("| Pokémon | Types (repo) | Advies | Reden | Biome |\n|---|---|---|---|---|")
adv={'A':'past (post-game)','B':'optioneel/post-game','C':'niet in de regionale dex'}
for l in leg: P(f"| {l['name']} | {'/'.join(l['types'])} | {adv[l['cat']]} | {l['reason']} | {', '.join(l['bio']) or '–'} |")
P("\nNiet genoemde legendaries/mythicals (Kanto-vogels, Hoenn-weertrio, Sinnoh-goden, Swords of Justice, Tapu's, Ultra Beasts, Treasures of Ruin, Loyal Three, paradox-soorten, enz.): niet in de regionale dex.\n")
P("## 5. Mogelijke regional forms\n")
P("Bestaande lijnen die een Zuid-Amerikaanse vorm kunnen krijgen: een andere habitat, een Zuid-Amerikaanse variant van het echte dier, of een lokale mythe. Gecontroleerd tegen de geplande fakemon (lama's, coati-lijn, nachtaap-lijn, condor, kolibrie, cavia, viscacha, guácharo, oeakari/saki, vleermuislijn, capibara, pinguïns, mug, vlieg, poedelmot, voetbal, fruit en planten); niets hieronder dubbelt daarmee.\n")
P("| # | Lijn | Idee (type, uiterlijk) | Inspiratie | Waar |\n|---|---|---|---|---|")
for line,idee,insp,waar,top in RF:
    P(f"| {top if top not in ('','0') else ('besloten' if top=='0' else '')} | {line} | {idee} | {insp} | {waar} |")
P("\n### Top 10 sterkste kandidaten\n")
for line,idee,insp,waar,top in RF:
    if top and top!='0': P(f"{top}. **{line}**: {insp.split(';')[0].split(' (')[0]} ({idee.split(':')[0]}).")
P("\nWaarom deze tien: ze geven een bestaande soort een echt ander dier of een echte mythe uit de regio (geen kleurwissel), vullen biomes die anders leeg blijven (Golett en Tympole vroeg rond La Paz, El Tío in de mijnen, Boitatá en Mapinguari in de Amazone), en een deel ervan raakt het hoofdthema: natuur die verdwijnt (Boitatá beschermt het bos tegen branden, de Mapinguari is een uitgestorven reus, de brilbeer en reuzenotter zijn bedreigd).\n")
# type analysis
tc=O['tc']; tcl=O['tcl']
role={'Dark':'gym','Ice':'gym 2','Bug':'gym','Dragon':'gym','Ground':'gym 1','Grass':'gym','Fire':'gym','Poison':'gym','Electric':'E4','Flying':'E4','Ghost':'E4','Steel':'E4'}
P("## 6. Type-analyse (genomineerd, categorie 1 + 2)\n")
P("Soorten = elke soort met dat type (dubbeltypes tellen bij beide). Lijnen = lijnen waarin het type ergens voorkomt.\n")
P("| Type | Rol | Soorten | Lijnen | Opmerking |\n|---|---|---|---|---|")
notes={
'Fire':'Dunst van de gymtypes: Vulpix, Ponyta, Magby, Slugma, Houndour, Torkoal, Charmander, Volbeat, Heatmor, Larvesta, Sizzlipede, Scovillain. **Gat voor fakemon**; de regional forms Boitatá (Fire/Ghost) en huaco (Ground/Fire) helpen ook.',
'Fighting':'Laag, maar geen gym; de Fighting-starter (lama) en Flamigo vullen aan.',
'Fairy':'Laag; geen gym. Kandidaten voor fakemon (Pachamama-sfeer, bloemen).',
'Dragon':'Genoeg lijnen (zes pseudo-achtigen), maar weinig Zuid-Amerikaans: alleen Tropius, Alolan Exeggutor. Eigen draak (pitahaya-idee, Grass/Dragon) welkom.',
'Ice':'Genoeg voor gym 2 als de Cordillera vroeg komt: Alolan Sandshrew/Vulpix, Snorunt, Snover, Swinub, Sneasel, Snom, Cryogonal, Bergmite. Pinguïns en ijs-fakemon vullen aan.',
'Ground':'Goed voor gym 1 (Sandshrew, Nacli-zout is Rock, Gligar, Drilbur, Wooper, Silicobra, Hippopotas, Hoenn-Grimer, Doduo, Stunfisk).',
'Poison':'Goed (Croagunk, Venipede, Skorupi, Stunky, Foongus, Bellsprout, Spinarak, Hoenn-Grimer, Koffing, Trubbish, Mareanie, Skrelp, Glimmet).',
'Bug':'Ruim; veel echte Amazone-insecten.',
'Grass':'Ruim, maar vooral laagland. Weinig Grass op de altiplano.',
'Dark':'Ruim (Sneasel, Houndour, Purrloin, Zorua, Nickit, Stunky, Deino, Pawniard, Scraggy, Maschiff, Inkay, Carvanha).',
'Ghost':'Ruim (Gastly, Duskull, Misdreavus, Yamask, Sableye, Parasect, Gimmighoul, Dreepy, Phantump, Mimikyu, Sandygast, Dhelmise, Spiritomb).',
'Steel':'Goed (Magnemite, Skarmory, Aron, Beldum, Mawile, Pawniard, Durant, Bronzor, Riolu, Gholdengo, Alolan Sandshrew, Seviper, Exploud).',
'Electric':'Goed (Pichu, Elekid, Magnemite, Tynamo, Joltik, Grubbin, Rotom, Porygon, Wattrel, Exploud, Volbeat/Illumise, Chinchou, Stunfisk).',
'Flying':'Goed, veel echte vogels uit de regio; condor- en kolibrie-fakemon komen erbij.',
'Water':'Ruim (zee, rivieren, binnenzee).',
}
for t,_ in sorted(tc.items(),key=lambda x:-x[1]):
    P(f"| {t} | {role.get(t,'–')} | {tc[t]} | {tcl[t]} | {notes.get(t,'')} |")
P("")
# biome
P("## 7. Biome-analyse (genomineerd, categorie 1 + 2)\n")
P("Een lijn kan in meerdere biomes staan.\n")
P("| Biome | Lijnen | Soorten | Lijnen (eerste stadium) |\n|---|---|---|---|")
bc=O['bc']; bcs=O['bcs']
for b in BIO:
    ls=[r['mem'][0][0] for r in rows if r['cat'] in 'AB' and b in r['bio']]
    P(f"| {BIO[b]} (`{b}`) | {bc.get(b,0)} | {bcs.get(b,0)} | {', '.join(ls)} |")
P("")
P("## 8. Vroege game (La Paz, Cordillera, Uyuni/Lípez)\n")
P("- **Altiplano en La Paz:** Minccino, Sandshrew, Geodude, Roggenrola, Drilbur, Aron, Hoenn-Grimer, Mudbray, Nickit, Natu, Wooper en Psyduck (Titicaca, lagunes), Magikarp, Golett (Tiwanaku), Duskull (Ñatitas), Eevee, Cleffa. Plus de fakemon viscacha en cavia. **Ontbreekt:** een vroege vogel (de condor-lijn), een vroege Grass (aardappel, quinoa, yareta, coca) en een vroege Bug (boven 3000 m zijn er weinig insecten; de mug komt pas lager).")
P("- **Cordillera (sneeuw vroeg):** Alolan Sandshrew, Alolan Vulpix, Snorunt, Snover, Swinub, Sneasel, Snom, Cryogonal, Bergmite, Absol; Frigibax als zeldzame late evolueerder. Genoeg voor gym 2 (Ice).")
P("- **Uyuni/Lípez (gym 1 Ground, daarna geisers, vulkaan, sneeuw):** Nacli (zout), Flamigo (Laguna Colorada), Gligar, Castform, Vulpix, Slugma; Ground uit de altiplano. **Dun:** hier passen fakemon (vicuña, viscacha, zoutkristal, geiser) en de Volcanion-ontmoeting.")
P("- Gym 1 (Ground) heeft vroeg genoeg Ground: Sandshrew, Drilbur, Wooper, Gligar, Hoenn-Grimer, Mudbray, Diglett-tuco-tuco (als regional form), Golett.\n")
P("## 9. Gaten voor fakemon\n")
P("- **Fire** (dunst van de gymtypes): vulkanen van Lípez/Licancabur, chili (naast Capsakid), zonnegod-thema; een Fire-fakemon per biome zou het gym helpen.")
P("- **Tepuis/Gran Sabana:** alleen Bellsprout (Heliamphora) en Carnivine. Plek voor de Venezolaanse poedelmot, tepui-kikkers (Oreophrynella, 'rollende' padden), Angel Falls.")
P("- **Galápagos:** zeeleguaan, blauwvoetgent, darwinvinken (geen bestaande soort past); pinguïns (Galápagospinguïn) via de pinguïn-fakemon.")
P("- **Lípez/Uyuni:** vicuña → guanaco, viscacha, zout/geiser-wezens, Árbol de Piedra (steenboom).")
P("- **Altiplano vroeg:** vroege Grass (aardappel, quinoa, yareta, coca), vroege vogel (condorkuiken), eventueel een vroege Bug.")
P("- **Megafauna/fossielen:** de regio heeft geen eigen fossielen in de nominaties (Omanyte e.d. vallen af). Kandidaten: glyptodont (reuzengordeldier), Megatherium (zie Mapinguari-vorm), terreurvogel (Phorusrhacos), Titanoboa, Argentinosaurus.")
P("- **Mythen zonder bestaande soort:** Curupira (bosbeschermer met achterstevoren voeten), Pincoya (Chiloé), Yacumama (slang: overlap met Uku Pacha), Ekeko (eventueel via Gimmighoul-vorm), Chullachaqui.")
P("- **Fighting en Fairy** zijn laag maar geen gymtypes; de starters vullen Fighting en Psychic.")
P("- **Steden** zijn met 'iconische' B-soorten oververtegenwoordigd ten opzichte van Jordi's wens 'veel natuur, minder steden'; bij schrappen eerst daar kijken.")
open(__import__('os').path.join(__import__('os').path.dirname(__file__),'../../../docs/concept/DEX_NOMINATIES.md'),'w').write('\n'.join(L)+'\n')
print(len(L))
