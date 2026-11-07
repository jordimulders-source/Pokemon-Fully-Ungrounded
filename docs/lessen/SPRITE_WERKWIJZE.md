# Sprite-werkwijze (compact)
Regels en eisen: `SPRITE_KERN.md`. Hier alleen de stappen en de commando's. Oude uitgebreide versie: `naslag/SPRITE_WERKWIJZE_oud.md`.

## Checklist (afgedwongen door het keurslot)
Jordi 3 nov: "het is elke keer opnieuw dat we instructies vastleggen die je elke keer opnieuw weer overslaat" → "doe allemaal". Daarom afgedwongen, niet alleen opgeschreven:
1. **Keurslot:** `.claude/hooks/sprite_keurslot.py` blokkeert elke afbeelding uit `docs/concept/sprites/` naar Jordi zonder `<bestand>.keuring.md` (nieuwer dan de afbeelding, met `Bron:`, 8×, 1×, per onderdeel "lijkt op / wijkt af in", `Oordeel: PASS`). Niet omzeilen (geen kopie buiten die map sturen).
2. **Keurvel:** `python3 tools/grounded/keurvel.py -o vel.png --werk werk.png --bron <echte sprites/foto's> --zoom x0,y0,x1,y1` → werk naast de bronnen op 8× en 1× (licht/donker) + close-ups, en een keuringssjabloon.
3. **Referentie eerst, per onderdeel** (hand, voet, kop, staart, patroon): 2–3 echte sprites of Jordi's eigen plaatje (stuurt Jordi een afbeelding, dan is díe de bron, niet de sprite van die soort uit de repo). Kenmerken zelf tellen/controleren op een close-up voor iets op een referentievel komt.
4. **Eén afwijking of twijfel = niet sturen.** Toets of het **leest** als een echte Pokémon, niet of het doet wat gevraagd werd.
5. **Onafhankelijke keurder bij elke mijlpaal** (pose akkoord, silhouet, kleur, af), vóór Jordi; zijn oordeel gaat in de keuring.
6. **Ritme:** een ronde helemaal afmaken, dan pas sturen; berichten van Jordi tijdens het werk verzamelen en samen verwerken, geen patch per bericht.
7. **Gereedschap per onderdeel:** het 3D-poppetje alleen voor massa/pose; dunne delen (handen, klauwen, vingers, oren) in de pixelstap naar een echte sprite, aangepast aan arm/maat/richting (nooit geplakt).

**Mappen:** `docs/concept/sprites/<naam>/` met `SPEC.md` (Jordi letterlijk, bevroren/open/afgekeurd), `referenties/`, `blender/`, `af/`.

| # | Stap | Wie | Klaar als |
|---|---|---|---|
| 0 | Types/evoluties uit de repo; SPEC en referenties klaarzetten | Claude | SPEC bestaat |
| 1 | Ontwerp: pose + kenmerken, foto van het echte dier | Jordi + Claude | Jordi kiest |
| 2 | Bron voor de vorm: foto in de juiste pose, óf (bij lastige 3/4) 3D-model in Blender met rondom-vel + 3 driekwart-standen | Claude | Jordi kiest |
| 3 | Silhouet uit de bron (foto-omtrek of render verkleind), dunne delen met de hand; bij een model: rode omtrek over de render | Claude/maker | Jordi keurt; bevroren |
| 4 | Kleur: studie (4–5 echte sprites op 8×) → tekstraster met de hand; toonkaart als schaduwgids | maker-agent | controlescript schoon |
| 5 | Claude 8× naast Taillow → verse keurder (blind eerst, PASS/FAIL met pixels) → reparaties via maker | Claude, keurder, maker | keurder GOED |
| 6 | Jordi ziet alleen de sprite; zijn punten → kleine benoemde rondes | Jordi | "prima" |
| 7 | `af/<naam>.png` + `normal.pal`; SPEC, CHANGELOG, Stand van zaken, lessen | Claude | gepusht |
Frame 2, rug, icoon, shiny, naam, data: later, voor alle soorten samen.

**Blender (optioneel, Jordi: "geen vereiste") in de cloud, eenmalig per container:**
```
python3.11 -m pip install bpy scikit-image
apt-get install -y libegl1 libgl1-mesa-dri
```
Voorbeeldmodel: `docs/concept/sprites/kolibrie_pre/blender/kolibrie_pre.py` (huid = smooth union van afstandsvelden, kleurvlakken per vlak, snavel/ogen/pootjes los; Workbench-render, 512 px = 8×, ortho 64 BU = spriteframe). Silhouet/vel: `kolibrie_pre/blender/A/maak.py`. Toonkaart: model met alle kleuren wit renderen, verkleinen, 4 tonen.

**Controlescript (elke ronde):** alpha-diff met het bevroren silhouet (0 of alleen in benoemde zones), open randen, losse pixels, clusters < 3 px, lijst gewijzigde pixels oud→nieuw. Voorbeeld: `kolibrie_pre/blender/A/kleur_r9/controle.py`.

**Opdracht aan een agent bevat altijd:** `SPRITE_KERN.md`, SPEC-pad, bevroren delen + toegestane zones, Jordi's woorden letterlijk, gewenste uitvoer (raster, png, pal, vel, NOTITIES met zwakke punten), "niet committen".

**Regional forms:** begin van de bestaande sprite van de soort; lessen (Uyuni-Silicobra, Salticonda) in `naslag/SPRITE_WERKWIJZE_oud.md`, "Regional forms".
**Silhouet naar sprite is niet 1 op 1** (Jordi, 5 nov, DJ Rotom): heeft een onderdeel in kleur meer ruimte nodig (gezicht, ogen), dan mag de sprite daar afwijken; in de sprite oplossen en de afwijking melden. **Vormen van een bestaande soort** (Rotom-vormen, regional forms): consistentie-analyse tegen alle bestaande vormen, zie naslag.

## Gemini-model namaken (Jordi, 6 nov: vaste methode)
**Trigger:** Jordi zegt dat hij een model (van Gemini) heeft dat precies nagemaakt moet worden. Gemini maakt het ontwerp (goed in ontwerp, luistert slecht naar instructies); Claude bouwt het 1-op-1 om naar een Emerald-sprite. Voorbeeld en naslag: poedelmot (`docs/concept/sprites/poedelmot/`, 21 rondes; doel: dit eindresultaat in ±5–8 rondes).

**Eisen (BELANGRIJKSTE REGEL, SPRITE_KERN):** alleen (1) heel accuraat op het model, (2) Gen 3 volgens onze eisen. Het model is perfect: niets toevoegen, weglaten of herinterpreteren. Niet genoemd = niet goedgekeurd. Nadruk van Jordi: belijning van kop, kraag/vacht en vleugels, en alle poten precies goed.

**Stappen (efficiënt):**
1. **Klaarzetten (Claude, ±10 min):** map `docs/concept/sprites/<naam>/` met `SPEC.md` (Jordi letterlijk), `referenties/`. Meerdere Gemini-plaatjes: kies per onderdeel de bron en leg ze over elkaar (zelfde koppositie meten op de ogen; `poedelmot/silhouet/seg.py` knipt onderdelen uit). Vraag alleen: eigen soort of vorm, welke fase (bepaalt de grootte).
2. **Silhouet = model verkleind** (`poedelmot/silhouet/sil.py`: uitsnede → 62 px breed, alpha ≥ 0,45, gaten dicht) + rode omtrek over het model + kleurgids. Silhouet meteen bevroren; niet aan Jordi voorleggen als het model al zijn pose is.
3. **Meetgereedschap vóór de eerste ronde** (dit kostte de poedelmot ±15 rondes): kopieer `poedelmot/kleur_r19/stappen/px.py` (modelhelderheid per spritepixel: gem/p15/max), `kleur_r20/stappen/box1x.py` (model op 1×) en de lijnkaart/overlay (spritelijnen over het model). De maker zet elke lijn, glans en tintgrens op een **gemeten** modelpixel.
4. **Eén maker** tekent met de hand op het raster (scripts alleen voor raster→png, controle en metingen), per onderdeel op 12× naast het model, en levert `vel.png` (rN | rN-1 | model op 8×, close-ups, 1× licht/donker). Zelfgenoemd zwak punt = eerst zelf repareren. **Verse maker** zodra een ronde > ±400k tokens kost (start vanaf de laatste ronde).
5. **Claude** bekijkt alleen het eindvel per ronde op 8× naast het model en stuurt alleen benoemde reparaties; commit + push na elke ronde.
6. **Keurder** pas als de maker geen zwakke punten meer ziet: vers, oordeelt eerst zelf, **meet** bij twijfel, toetst alleen de twee eisen, en op 1× naast het verkleinde model; afwijkingen kleiner dan 64 px kan tonen tellen niet. Spreken keurders elkaar tegen: de maker meet en volgt de meting.
7. **Eindkeuring Dragonfly Cave** (gidsen + FAKEMON_CHECKLIST, naast 4–5 Gen 3-sprites): alleen uitvoering, geen herontwerp; ontwerpvragen "ter info voor Jordi".
8. **Naar Jordi:** de sprite op 64×64 **én 8× vergroot** (`<naam>_8x.png` met keuring); daarna `af/`, CHANGELOG, Stand van zaken.

**Lessen poedelmot (goed):** het verkleinde model als silhouet was meteen goed (alpha-diff 0 alle rondes); meten per pixel (px.py, lijnkaart) loste in 4 rondes op wat 15 rondes op het oog niet lukte; een verse maker brak twee keer een vastgelopen reeks; Jordi's woorden letterlijk in SPEC en elke opdracht; commit na elke ronde.
**Lessen poedelmot (minder goed):**
- Een stijlkeurder (Gen 3-smaak zonder model) duwde de sprite weg: koele lila schaduw, extra aders, mond weg, "leest als vos". Nooit een keurder die het model mag herinterpreteren.
- Twee keurders tegelijk (gelijkenis + stijl) gaven tegenstrijdige opdrachten; één keurder met de twee eisen is beter.
- Herhaalde kleine patronen (schubben, sprietbaarden) worden op 64 px een raster/dambord/zebra: minder, grotere vormen op de modelplekken; textuur meten (gem/std) i.p.v. tekenen op het oog.
- Te licht of te wit zetten waar het model een middentint heeft (sprietnerf wit, middenstuk lila/grijs): tinten meten op het model.
- Claude zei "wat Jordi niet noemt niet veranderen": fout, niet genoemd = niet goedgekeurd.
- Rondes 1–10 ontwierpen opnieuw volgens Gen 3-regels i.p.v. het model te volgen; pas toen "alleen accuraat + Gen 3" de regel werd, ging het snel.
- De sprite op 64×64 naar Jordi sturen is te klein: altijd ook 8×.
