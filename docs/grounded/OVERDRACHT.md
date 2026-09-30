# Overdracht voor een nieuwe Claude-sessie

Lees dit bestand plus `CLAUDE.md` bij de start van een sessie. Werk dit bestand bij aan het eind van een sessie (of als Jordi erom vraagt), zodat de volgende sessie meteen verder kan.

## Werkwijze
- Branch: `claude/hopeful-brahmagupta-hsth8c`, PR naar `master` (jordimulders-source/projectgrounded, PR 5). Commit + push na elk afgerond stuk, met een changelogsectie.
- Jordi wil van **elke kaart** die af is screenshots (render + emulator), zodat hij kan tweaken.
- Kaartgereedschap en testrecept: `tools/grounded/maptools/README.md`.
- Jordi schrijft de humor/dialogen. Nieuwe NPC-teksten zijn neutrale placeholders tot hij ze schrijft (Dialoogstudio).

## Stand van zaken (laatste sessie)
- **Coldstep Cave** (Route 115 → tunnel → ijskamer 1 → ijskamer 2): af en goedgekeurd. IJskamer 2 heeft een puzzel van 28 zetten die voor elke combinatie van opgepakte items oplosbaar blijft. Items: Ice Stone, Focus Sash, PP Up (kamer 2), Max Revive, Rare Candy (kamer 1). De uitgangsladder (15,3) van kamer 2 leidt naar Route 135.
- **Keccles 1 en 2** (Route 115, Fortree Gym), **Seltzer Surge** (TM51), muziekcredits: af.
- **Route 135** (60×40, sneeuw): terrassen, brede waterval (Ever Grande-stijl) met Life Orb erboven, meer met oevers, besneeuwde Hoenn-randbomen, huisje rechtsboven (`Route135_House`, nog leeg), hikers Edmund & Tenzing (dubbel), Birch-gevecht 2 (Macarena). Bouwscript: `tools/grounded/maptools/route135.py`. Jordi's laatste feedback is verwerkt; wacht op zijn reactie op de randbomen en het huisje.
  - Placeholders voor Jordi: teksten van Birch 2, Edmund, Tenzing; wie er in het huisje woont.
  - Uitgang zuidoost (x 50–53, onderrand) is waar Route 136 op aansluit (connectie `down`).
  - Op de Town Map valt `MAPSEC_ROUTE_135` nog onder Route 115 (alias in `src/region_map.c`).

## Openstaande taken (in volgorde)
1. **Route 136** (sneeuw, klimt verder de bergen in; hoog maar niet hoger dan Mt. Chimney):
   - Bomengang met een item, geblokkeerd door een onzichtbare Keccles (Devon Scope, zoals bij Fortree).
   - Rivaalgevecht May/Brendan, een Bird Keeper, een zwemmer aan de waterkant ("Wim Hof"-idee van Jordi).
   - Dynamisch weer: sneeuw en as wisselen (ook voor Route 135).
   - Ongeveer gemiddelde routelengte (mediaan landroutes ≈ 2400–3200 tiles).
2. **Ashfrost Town**: paradijselijk dal met een meertje in het midden, een man die daar vist, huizen eromheen (sommige op verhoging), Pokémon Center, Mart, een paar huizen. De sneeuwpop (tileset `snowman`) hoort hier. Gebouwen staan in de bronsheet (rijen 104–134); waarschijnlijk is een eigen stads-tileset nodig (tile-budget).
3. **Town Map**: Route 135/136 en Ashfrost toevoegen (lege hooglanden rond mapsec x3–4, y1–4; regionmap-coördinaat = tile − (1,2)).
4. **Ditto-trainer** (Pokopia-idee), **gepauzeerd** door Jordi. Opties die al besproken zijn: vermomde trainer (onthulling), team van Imposter-Ditto's met verschillende items, of een trainer die jouw team kopieert. Plek: Route 115 (hengeltabel vol Ditto) of Ashfrost.

## Valkuilen
- Savestates zijn ongeldig na een rebuild; `debug.inc` nooit committen.
- `wild_encounters.json` en `trainers.party`: tekstueel invoegen, niet via `json.dump` herschrijven (anders wordt het hele bestand opnieuw geformatteerd).
- Trainer-AI-namen in `trainers.party`: gebruik bestaande combinaties (bijv. `Check Bad Move / Try To Faint`).
- Sneeuwtileset: nieuwe metatiles alleen achteraan.
