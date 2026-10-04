# QA-rapport Project Grounded (nachtelijke testronde, 4 okt 2026)

Basis: branch `claude/amazing-wozniak-2iz078` op `acbcec65`. Getest in mGBA (headless) met een eigen test-ROM (tijdelijke hook: geforceerde transitie, flags/vars zetten, warp naar elke plek; nooit gecommit) plus statische controles op de data. Alle bewijsbeelden staan in de scratchpad (`.../scratchpad/qa/bewijs/`, zie onderaan).

## Samenvatting

- **Gerepareerd (5):** witte/terugflitsende eindframes van 7 route-transities, elemental monkeys in de Spire-draft, 2 tekstvakken met een derde regel (Mossdeep Gym), 8 te brede regels met `{POKEBLOCK}`, en de oorzaak daarvan in de Dialoogstudio-import.
- **Geen vastlopers gevonden** in: 8 gymleiders, alle Birch-gevechten, Oak, Brock, Mimi, Timothy, Colress (Mauville + Magma Hideout), Zinnia, Heatran-cutscene + Heatran, Raikou (schakelaar + gevecht), Entei, Suicune, alle vijf Regi-stippenpuzzels + Regi's, Regigigas, Keccles 1, Gabby & Ty, Wally (Meteor Falls en tag battle Mt. Chimney), Keccles-multi in Sootopolis, rivaal Route 136, Eon Ticket (Lilycove), Rotom, de opening (huis, klok, buren, Route 101, starter, lab), en drie volledige Spire-runs.
- **Belangrijkste open punt:** in de Spire kan een vergeten move een **leeg move-slot** achterlaten (ook slot 1); in gevecht staat de cursor dan op "-" en doet A niets.

## 1. Gevechtstransities

**Getest:** alle 73 transities (vanilla + alle Grounded-transities) geforceerd vanaf dezelfde plek, per frame vastgelegd tot het gevecht begint; per transitie de helderheid per frame en een strook van de laatste 72 frames. Daarnaast 14 route-transities op hun echte kaart (via "Wild battle (map)"), en de trainer-transities (Birch, Colress, Gabby & Ty, Aqua/Magma, mugshots) in echte gevechten.

**Gevonden en gerepareerd** (`src/battle_transition.c`):
- **De wereld flitste terug vlak voor het wit.** Bij Sky Pillar, Meteor Falls, regenwoud, Psyduck, strandbal en Gabby & Ty werd het beeld eerst getint (blauw/donker/geel/grijs) en aan het eind naar wit geblend met `BlendPalettes(PALETTES_ALL, …)`. Die rekent vanaf de ongetinte paletten, dus het eerste frame van de fade (coëfficiënt 0) toonde **de gewone overworld in volle kleur**, en daarna een wit waas over de wereld. Nieuw hulpje `RT_FreezePalettes()` zet het getinte beeld eerst vast (zoals de runner zelf al doet bij de fade naar zwart).
- **Onnodig wit aan het eind** bij **Meteor Falls, Jagged Pass, regenwoud en Psyduck**: in het ontwerp (changelog) hoort daar geen witte flits bij. Ze faden nu naar zwart terwijl ze nog bewegen. De totale lengte is gelijk gebleven.
- Bewust wit gelaten (hoort bij het idee volgens de changelog): sneeuw, Sky Pillar ("alles wordt wit"), strand (golf spat over je heen), strandbal, Gabby & Ty (flits), Colress (flits), Cycling Road, Safari (open plek), Raikou (bliksem), Entei, Aurora, hittegolf en as (licht/grijs). Vanilla-transities zijn niet aangepast.
- Bewijs: `bewijs/transities_voor_na.png` (voor/na), `bewijs/montage_*.png` (alle transities, laatste 72 frames, vóór de fix), `bewijs/route_transities_echte_kaarten.png` (na de fix, echte kaarten).

**Niet gerepareerd (voorstel):**
- De vier transities die nu naar zwart gaan hebben daarna nog ~0,7 s zwart (10 frames vasthouden + fade van zwart naar zwart in `RouteTransition_Run`). Dat was vóór de fix even lang (toen wit). Voorstel: een vlag in `struct RouteTransition` om stap 2/3 over te slaan als het beeld al zwart is; dat scheelt ~40 frames per gevecht.
- Vanilla **mugshot** (gymleiders, rivalen, Archie/Maxie) eindigt met een witte flits; vanilla **Shred Split** (alleen Battle Frontier) toont 1 frame de overworld vlak voor het gevecht. Beide vanilla; alleen aanpassen als je dat wilt.

## 2. Verhaal en events (emulator)

**Methode:** per event de juiste flags/vars zetten, naar de plek warpen, het script starten zoals een speler (praten, op een trigger stappen, bord lezen) en door alle tekst en gevechten heen drukken; vastloper = script loopt nog en het beeld verandert 80 drukken lang niet. Testteam: Arceus lv 100 (2x voor dubbel/multi), alle badges.

| Onderdeel | Resultaat |
|---|---|
| Opening (zonder debug): eigen huis, mama, klok, buren + rivaal, Route 101, Birch redden, starter, gevecht, lab, bijnaam | werkt, geen vastloper |
| Gymleiders 1–8 (incl. Tate & Liza dubbel) | allemaal gevecht + badge/TM, geen vastloper |
| Birch: Route 109 → Verdanturf (Hoenn-Grimer) → Route 135, Mossdeep, onder water Route 124 | werkt (Verdanturf-Birch verschijnt pas na Route 109, zoals bedoeld) |
| Oak (Slateport, starterkeuze), Brock, Mimi, Timothy (Route 119, TM58), Keccles 1 (Route 115) | werkt |
| Colress Mauville (coord-trigger + gevecht + tandwielen), Colress Magma Hideout | werkt |
| Zinnia (Sky Pillar), Heatran-cutscene Route 111, Heatran-hol | werkt |
| Raikou: schakelaar → wand open → trap → datacenter → gevecht; Entei; Suicune | werkt |
| Regi-stippen in alle vijf grotten (muur bekijken, stippen in volgorde, ingang gaat open) + gevechten; Regieleki-luik; Regigigas | werkt |
| Wally Meteor Falls; tag battle met Wally op Mt. Chimney (partij kiezen, 2v2, Archie daarna) | werkt |
| Sootopolis na Rayquaza: Keccles op Tropius, multi tegen Archie + Maxie | werkt |
| Rivaal Route 136 (trigger), rivaal Lilycove (Eon Ticket), Gabby & Ty Route 111, Rotom-tv | werkt |
| Spire- en Stadium-lobby (NPC's, balies) | werkt (Stadium alleen tot de teamkeuze getest) |

**Warps van alle nieuwe kaarten** (Ashfrost + huizen/PC/Mart, Route 135/136, Coldstep, Crystal Cavity, Suicune-grot, Heatran-hol, Entei-gang/-hol, datacenter, Regieleki/Regidrago, Regigigas-tempel, Meteor Falls-krater, Rotom-kelder, Spire- en Stadium-lobby): elke warp echt genomen; je komt overal op een begaanbare tegel uit en kunt weglopen. Bewijs: `bewijs/warps_nieuwe_kaarten.png`. Statisch: geen warp naar een niet-bestaande kaart of warp-id (verschil met vanilla: alleen de nieuwe kaarten, allemaal in orde).

**Kleine observaties (geen bug):**
- De klok bij de start vraagt "Is this the correct time?" met de cursor op **NO** (vanilla). Past niet bij "geen onnodige ja/nee-vragen"; voorstel: standaard YES of de vraag overslaan (`src/wallclock.c`, `CreateYesNoMenu(..., 1)` → `0`).
- Ashfrost PC 2F: de warps van de Union Room/Trade Center-deuren wijzen naar de 1F-ingang. Onschadelijk (die deuren zijn dicht).

## 3. Statische controles

- **Wilde Pokémon:** alle tabellen hebben het juiste aantal slots en `min_level`/`max_level`; geen min > max; geen elemental monkeys. **Dubbele soorten** (tegen de 12-unieke-regel) in nog ±60 tabellen, o.a. Route 101 (Snom 3x), Route 102 (Ralts 3x, Rellor 3x), 103, 104, 110, 111, 112, 113, 114, 117, 118 (Dreepy 2x), Petalburg Woods, Rusturf, Granite Cave, Mt. Pyre (alle verdiepingen), Fiery Path, Jagged Pass, Route 115 (Chansey/Blissey 2x), 120, 121, 123, Seafloor Cavern, Victory Road, Meteor Falls, Shoal Cave, Sky Pillar, Safari. (Altering Cave, Artisan Cave, Battle Pyramid/Pike zijn bewust zo.) Niet aangepast: dat is ontwerpwerk.
- **Levels wild vs. trainers per kaart:** opvallend is **Route 115** (wild lv 30–50, trainers 13–33; het zuidelijke stuk is al na Rustboro bereikbaar). Graag even checken of dat bedoeld is.
- **Trainers (`trainers.party`):** geen illegale abilities, geen monkeys, geen onbekende soorten. Geëvolueerd onder het evolutielevel van dit project:
  - Archie: Archaludon lv 49 (Duraludon → 50).
  - Katelynn: Kingambit lv 48 (Bisharp → 49).
  - Blissey lv 27–35 (Chansey → 36): Nob_2/3/4, Cyndy_2/3, Miguel_1 (4x Blissey lv 27; Miguel is Jordi's eigen ontwerp, mogelijk een grap).
  - Battle Stadium: Jupiter heeft Golbat lv 50 (Crobat vanaf 35); andere sessie werkt daar.
  - De overige "niet geëvolueerd"-meldingen zijn evoluties op item/move/plek (Gligar, Magneton, Primeape, Girafarig, ...) en dus in orde.
- **Tekstvakken** (breedte 216 px, max. 2 regels per vak), vergeleken met vanilla: 9 problemen, alle 9 gerepareerd (zie §5). Coord-triggers: alle nieuwe triggers die `lockall` doen eindigen met `releaseall` (of een warp/gevecht).
- **Items:** alle items hebben een beschrijving; beschrijvingen passen (max. 102 px, zoals vanilla). Items met een ?-icoon (o.a. de nieuwe Mega Stones van Z-A, TM59–100, de Paldea-snacks) zijn nergens te krijgen.
- **Soorten:** alle soorten in wilde tabellen, trainers, scripts (`givemon`/`setwildbattle`) en de Spire hebben echte data en graphics; geen "??????????" bereikbaar.

## 4. The Spire

Drie runs met de testbot (debugwarp → receptioniste → draft → kaart → gevechten, winkel, kamp, events, beloningen, acts, baas → lobby): één volledige run tot en met de act 3-baas zonder vastloper; twee runs eindigden in een verloren run (normaal).

**Gevonden en gerepareerd:**
- De draft bood **Pansear** aan (en Pansage/Panpour met hun evoluties): de elemental monkeys zijn bewust uit de game. `tools/grounded/spire/spire_pool.py` filtert ze nu bij het schrijven van `src/data/spire_pool.h` (ze tellen nog mee voor de tier-grenzen, zodat de rest van de pool niet verschuift). Bewijs: `bewijs/spire_draft_pansear.png`. `SPIRE_BALANS.md` is niet opnieuw gegenereerd (dat doen `encounters.py`/`events.py` erbij en daar werkt een andere sessie aan); daar staan ze dus nog in het rapport.

**Niet gerepareerd (voorstel):**
- **Lege move-slots.** "Forget move" (o.a. Litwick's Candle, het rad, de Collector) zet `MOVE_NONE` in het gekozen slot zonder de moves op te schuiven (`src/spire_event.c`: `ForgetRandomMove`, `ChooseSlot`; ook `CreateFoe` in `src/spire_run.c` voor verboden moves). Is slot 1 leeg, dan staat de cursor in gevecht op "-" en doet A niets; je moet zelf naar een andere move. Bewijs: `bewijs/spire_litwick_vergeet_move.png` → `bewijs/spire_leeg_moveslot.png` (Natu: "- / Gust / Cosmic Power / Tailwind"). Voorstel: na het vergeten de moves (en de upgrade-bits per slot) opschuiven, of in het gevechtsmenu de cursor op de eerste gevulde move zetten.

## 5. Wat er in deze commit is aangepast

1. `src/battle_transition.c`: `RT_FreezePalettes()`; Sky Pillar, Gabby & Ty en strandbal blenden naar wit vanaf het getinte beeld; Meteor Falls, Jagged Pass, regenwoud en Psyduck faden naar zwart in plaats van wit.
2. `tools/grounded/spire/spire_pool.py` + `src/data/spire_pool.h`: geen Pansage/Pansear/Panpour (en evoluties) in de Spire.
3. `data/maps/MossdeepCity_Gym/scripts.inc`: Nate en Nicholas hadden een `\n` na een `\l` (derde regel liep uit het tekstvak) → `\l`.
4. Te brede regels met `{POKEBLOCK}` opnieuw afgebroken (woorden en grappen ongewijzigd): `LilycoveCity_House3` (2 teksten), `LilycoveCity` (2), `MossdeepCity_House1`, `SlateportCity_PokemonFanClub`, `Route117_Text_LydiaPostRematch` (`data/text/trainers.inc`).
5. `tools/dialogen/import.py`: telde tekenmacro's als `{POKEBLOCK}` (35 px) en `{PKMN}` (16 px) als 0 px breed, waardoor bovenstaande regels te breed werden. Telt ze nu mee. (De editor in de Dialoogstudio rekent waarschijnlijk hetzelfde; die is niet aangepast.)

`make -j4` slaagt; `data/scripts/debug.inc` en `src/battle_setup.c` zijn ongewijzigd.

## 6. Prioriteiten voor Jordi

1. **Spire: lege move-slots** na "forget move" (cursor op "-"). Opschuiven of cursor verzetten.
2. **Route 115**: wilde levels 30–50 op een route die al na Rustboro bereikbaar is; bedoeld?
3. **Trainers onder hun evolutielevel**: Archie (Archaludon 49), Katelynn (Kingambit 48), Blissey bij Nob/Cyndy-rematches (en Miguel, als dat geen grap is).
4. **Dubbele soorten** in ±60 wilde tabellen (lijst in §3).
5. **Transities**: ~0,7 s zwart aan het eind van de route-transities inkorten (QoL); zelf de nieuwe zwarte afloop van Meteor/Jagged/regenwoud/Psyduck bekijken.
6. **Klok bij de start**: ja/nee standaard op YES of weg.
7. Dialoogstudio-editor: `{POKEBLOCK}`/`{PKMN}` meetellen bij het afbreken, zoals `import.py` nu doet.
8. Bij de volgende Spire-ronde `spire_pool.py`, `encounters.py` en `events.py` opnieuw draaien, zodat ook `SPIRE_BALANS.md` de monkeys niet meer noemt.

## Bewijsbeelden

Map: `/tmp/claude-0/-home-user-projectgrounded/38f4f0b0-30aa-54ec-9738-2a3fa6fa6220/scratchpad/qa/bewijs/`
- `transities_voor_na.png`: de 7 aangepaste transities, voor en na.
- `montage_0_12.png` … `montage_67_72.png`: alle 73 transities, laatste 72 frames (vóór de fix).
- `route_transities_echte_kaarten.png`: route-transities op hun eigen kaart (na de fix).
- `warps_nieuwe_kaarten.png`: aankomst via elke warp van/naar de nieuwe kaarten.
- `mt_chimney_tag_battle.png`, `sootopolis_keccles_multi.png`: de multi battles.
- `spire_draft_pansear.png`, `spire_litwick_vergeet_move.png`, `spire_leeg_moveslot.png`: Spire-bevindingen.

Testscripts (scratch, niet in de repo): `.../scratchpad/qa/` (`qa_build.py` bouwt de test-ROM met hook, `trans_all.py` transities, `t_events*.py`/`t_gyms.py`/`t_regidots.py`/`t_opening*.py` events, `t_warps.py` warps, `spirebot.py` Spire, `*_check.py` statische controles).
