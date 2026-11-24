import json,numpy as np
D=json.load(open("scored.json"))
P={
"A ≤12 nov (handwerk/eerste Gemini)":["Cuyby","Cuychu","Princadee","Sunperor","Kiskiddo","Bootoo","Zapacha","Bandolingo","Hitmongroove","Curiqui","Lanymph","Pupoodle","Vigiloot","Salticonda","Silicobra","DJ Rotom","Cholucha"],
"B 13–18 nov (Gemini overnemen)":["Krassault","Kadabra","Alakazam","Mosaguar","Globsnail","Purrpillar","Abra","Steenjaguar-welp","Gengas","Hauntflare","Dustly","Clionice","Cryomet","Hexpress","Blobfish (winegum)","Blobfish (pudding)","Pyrowyrm","Pitaling","Mate-kalebas","Rowmate","Wagogogon","Tejuice","Shuppetto","Pitahaya-draak fase 3"],
"C 19–20 nov (opknapronde + nieuw)":["Skinguin","Axolaunch","Harpiary","Rufflet","Oddish","Gloom","Hummlet","Nocticue","Soulibri","Coathief","Moonkey","Picapau","Picaraio","Palpaca"],
"D 21–24 nov":["Vileplume","Llamauler","Flytron","Buzzquito","Dundragoon","Oricorio (cumbia)","Oricorio (tango)","Oricorio (samba)","Swablu","Altaria","Solrock","Vuurduivel fase 1","Vuurduivel fase 2","Gnomini","Gnomad","Krickestro","Alphyena","Sunflora","Bloedmaan","Gnometrotter\" (Rock)","Gnometrotter\" (Ice)","Gnometrotter\" (Grass)","Claydol","Wingsuit","Fruitvampier","Pincurchin","Satelliet","Capybarrel","Levende tempel","Spooktrein fase 1"]}
used=set()
for k,names in P.items():
    s=[]
    for n in names:
        m=[d for d in D["ours"] if d["name"].startswith(n) or d["name"].startswith('"'+n)]
        m=[d for d in m if d["name"] not in used][:1]
        if not m: print("mis",n); continue
        used.add(m[0]["name"]); s.append(m[0])
    f=lambda key:np.median([d[key] for d in s])
    print(f"{k:38} n={len(s):2} score{f('score'):.2f} zwart-lichtkant{f('lite_dark'):.2f} binnenruis{f('inoise'):.2f} clustergr{f('meancl'):.1f} contrast{f('lr'):.0f}")
print("rest:",[d["name"] for d in D["ours"] if d["name"] not in used])
