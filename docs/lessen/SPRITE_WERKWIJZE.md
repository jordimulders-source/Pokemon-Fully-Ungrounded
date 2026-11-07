# Sprite-werkwijze (compact)
Regels en eisen: `SPRITE_KERN.md`. Hier alleen de stappen en de commando's. Oude uitgebreide versie: `naslag/SPRITE_WERKWIJZE_oud.md`.

## Checklist (afgedwongen door het keurslot)
Jordi 3 nov: "het is elke keer opnieuw dat we instructies vastleggen die je elke keer opnieuw weer overslaat" → "doe allemaal". Daarom afgedwongen, niet alleen opgeschreven:
1. **Keurslot:** `.claude/hooks/sprite_keurslot.py` blokkeert elke afbeelding uit `docs/concept/sprites/` naar Jordi zonder `<bestand>.keuring.md` (nieuwer dan de afbeelding, met `Bron:`, 8×, 1×, per onderdeel "lijkt op / wijkt af in", `Oordeel: PASS`). Uitzondering: `docs/concept/sprites/showcase/` (vellen van al goedgekeurde sprites om te tonen, Jordi 5 nov). Het slot geldt alleen voor spritewerk, niet voor andere afbeeldingen buiten die map. Niet omzeilen (geen kopie buiten die map sturen).
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
