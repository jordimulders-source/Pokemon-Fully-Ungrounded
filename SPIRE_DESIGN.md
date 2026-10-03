# The Spire – ontwerp (roguelike-faciliteit, Battle Frontier)

Stand: 3 okt 2026, gesprek Jordi + Claude. Dit document is de bron voor de volgende sessie.

**Gebouwd (v0.8.100):** rekenscript (`tools/grounded/spire/`) en een prototypegevecht (debugmenu > Utilities > Spire prototype) met ×HP, DEFEND/blok en intenties; code in `src/spire.c`, constanten in `include/spire.h`. Nog niet: toren, kaart, drops, winkel, relics, RUN = pauzeren/opgeven, Spire-codex, act-overgang.

## Concept
- Nieuwe, enorm hoge toren op het Battle Frontier-eiland: **The Spire**. Roguelike à la Slay the Spire.
- **3 acts**, per act verdiepingen met keuzes (gevecht, elite, winkel, rustplek, event) en een **baas**.
- Doel: snappy, methodisch, weinig RNG-pech; niet PokéRogue-achtig (geen tientallen one-shots).
- Zoveel mogelijk Pokémon-mechanics blijven overeind (crits blijven bestaan).

## Team
- **Rentals**, en je hebt er **altijd precies 2**. Je speelt **altijd doubles** (jij 2 Pokémon).
- Groot aantal Pokémon beschikbaar voor de speler; sommige zijn beter dan andere, dat is prima.
- Een nieuwe Pokémon (draft/event/shop) **vervangt** er één; de nieuwe komt met volle HP. Relics blijven.
- **Evolueren na act 1** (als de Pokémon dat kan).
- Flauwgevallen en toch gewonnen: doet het volgende gevecht weer mee met **1 HP**.
- **Switchen bestaat niet.**

## Tegenstanders
- **Geen trainers** (Jordi, v0.8.101): je vecht tegen losse Pokémon (wild dubbelgevecht met trainer-AI). Golven vragen nog engine-werk (wilde gevechten vullen niet aan).
- Intenties tonen **KO** (zeker dodelijk) of **KO?** (alleen met een hoge rol).
- 1 of meerdere tegenstanders: **2 tegen 1** (baas) kan, 2 tegen 2 ook. Meer dan 2 tegelijk kan de engine niet, wel **golven** (valt een lakei, dan komt de volgende uit de party).
- Bazen/lakeien: een **grote pool aan bazen** met vaste patronen (memoriseren zoals in Slay, maar meer variatie). Lakeien = zwakke support-Pokémon (weer, Tailwind, schermen, buffs).
- **Abilities van tegenstanders verborgen**; de ability-popup van expansion onthult ze. Idee: een **Spire-codex** (met R) die onthoudt wat je ooit zag (ability, moves, patroon).
- **Intenties**: de tegenstander legt zijn volgende move een beurt vooruit vast en toont die compact onder zijn levensbalk, bijv. `▶ EARTHQUAKE ⟷ beide ~38`, `▶ FLAMETHROWER → links ~65`, `▶ SWORDS DANCE  Atk^`. Pijl = doel (links/rechts/beide), getal = geschatte schade (bereik of max; crits kunnen erdoorheen). Iets liberaler met ruimte dan in normale gevechten mag.
- Kan de intentie niet doorgaan (doel flauw, Taunt, slaap, flinch, geen PP): gewone Pokémon-regels (ander doel / beurt kwijt).

## Gevechtsmenu
- **FIGHT / BAG / DEFEND / RUN**: het POKéMON-menu wordt **DEFEND**.
- **DEFEND**: kost de beurt van die Pokémon, gaat **altijd eerst** (prioriteit als Protect, +4), geeft **Blok** (getal dat deze beurt eerst wordt opgemaakt, vervalt aan het eind van de beurt).
  - Op **1 Pokémon** naar keuze, of **gespreid over beide** (elk iets meer dan de helft, voorstel 60%).
  - Hoeveelheid **schaalt met de verdediging** van de Pokémon die verdedigt (Def/Sp. Def) en **neemt per act toe**. Eerste schatting: ~15% van eigen max HP × verdedigingsfactor × act-factor (≈ één normale klap).
  - Blok werkt alleen tegen **directe schade van moves**, niet tegen brand/gif/weer/terugslag/Stealth Rock. Multi-hit eet het blok per klap op.
  - Beide Pokémon verdedigen: blokken tellen op.
- Andere verdedigende moves (Protect, Wide Guard, Follow Me, Reflect…) blijven zoals ze zijn.
- **BAG**: potions en battle items (X-items worden nuttig). Kopen in de winkel; aantal slots nog bepalen (Slay: 3).
- **RUN**: kiezen tussen **pauzeren** (run opslaan vanaf het begin van dit gevecht, eigen team terug, terug naar de overworld; later verder met dit gevecht) of **opgeven** (run eindigt, BP naar rato).
- Eigen ability/stats bekijken: L (of SELECT) opent de summary van je twee Pokémon.

## Moves als kaarten
- **4-movesprincipe blijft.**
- Elke rental begint met **startermoves** (zoals Strike/Defend in Slay).
- Na elk gevecht kies je een move uit een drop (zoals kaartbeloningen). **Elke Pokémon kan elke move leren** als hij hem in een drop krijgt. **STAB** blijft gelden.
- Moves gecategoriseerd zoals kaarten (aanval / skill / power), met **zeldzaamheid**: de echt goede moves zijn **rare drops**.
- **PP als kosten**: zeldzaam = sterk maar weinig PP. PP kan doorlopen over gevechten heen (bijv. Protect-achtige moves een paar keer per act, aangevuld op rustplekken).

## Relics, winkel, rust, events
- **Relics** = elite-drops, willekeurig uit een pool (run-brede effecten, simpele haken in de gevechtscode).
- **Winkel**: zelf kiezen welke moves, relics, een **ability** kopen, potions/items.
- **Rustplek**: helen, of een move verbeteren, of (vanaf act 1) evolueren.
- **Events**: tekstkeuzes met risico/beloning (Jordi's humor); ook kans op een andere Pokémon.
- **Kleine heal na elk gevecht** (orde 10%, exact getal bepalen tijdens het testen; relics kunnen het verhogen).

## Balans / HP
- **Rekenscript:** `tools/grounded/spire/balance.py` (echte Gen 5+-schadeformule, soorten/typetabel uit de broncode; `--run` speelt hele acts na, `--set sleutel=waarde` voor andere instellingen). Speler is een simpele bot zonder potions/relics/drops, dus de echte speler doet het beter.
- **Startwaarden (v0.8.100):**
  - HP-vermenigvuldiger: **speler ×4**, normale tegenstander ×1, elite ×2,5, baas ×4,5. Levels: speler 50, vijand 48 / 50 / 52 per act.
  - Normaal gevecht = **2 tegenstanders** (geen golf): ±3 beurten, ±15% HP kwijt. Elite ±4 beurten, ±25%. Baas (+ 2 support-lakeien) ±11 beurten, ±65%, bot wint 60–80%.
  - Klap van een tegenstander ≈ 7–15% van je max HP; jouw STAB-klap ≈ 45% van een normale tegenstander, 13–17% van een elite, ±7% van een baas.
  - **Bazen niet sterker laten slaan**: bewegingskracht 75/80/85 (STAB) per act; dreiging komt uit patronen en support (lakeien die de baas buffen: +15% schade per buff, max +60%), niet uit ruwe kracht. Met 90–110 kracht en een totem-boost won de bot <5%.
  - **Heal na gevecht 20%**, rustplek 50%. Met 10% / 30% strandde de bot al in de gewone gevechten van act 1.
  - **DEFEND**: 15% van eigen max HP × verdedigingsfactor × act-factor (1 / 1,25 / 1,5) ≈ één klap. Helpt vooral in act 3 (bot haalt act 3 in 68% i.p.v. 46%); in act 1 neutraal. Eventueel act 1 iets hoger (×1,2).
  - Resultaat bot per act (vers team): act 1 48%, act 2 74%, act 3 68% gehaald; vrijwel alleen gestrand op de baas.

## Beloning (BP naar rato)
- Ook bij een paar gewonnen gevechten BP. Voorstel: 1 BP per gevecht, 3 per elite, 10 per baas, bonus per act; act 2/3 ×2/×3. Volledige run grofweg 100–150 BP (tickets kosten 200).

## Technische notities
- De **Battle Pike** heeft al deur-keuzes met kamertypes en streak-opslag: bruikbaar als basis voor de verdiepingen (later eventueel een echt kaartscherm).
- Rentals/eigen team wisselen zoals de **Battle Factory**; run-state (act, verdieping, **seed** voor kaart en tegenstanders, valuta, relics als bitveld, 2 Pokémon) past in de Frontier-opslag (paar honderd bytes).
- Expansion heeft: `settotemboost` (bazen), starttoestand via var, 2-tegen-1 in doubles werkt in de engine.
- Blok: waarde per battler, eerst aftrekken bij schade, aan het eind van de beurt op 0; klein schildgetal bij de HP-balk.
- Intentie: AI kiest een beurt vooruit en moet zich eraan houden; schadeschatting uit de AI-schadeberekening.

## Nog open
- HP-vermenigvuldigers en Defend-formule: startwaarden staan hierboven; bijstellen na het prototype.
- Aantal verdiepingen per act, bag-slots, exacte heal na gevecht.
- Inhoud: rentalpool, startermoves per Pokémon, movepool met zeldzaamheden, relicpool, bazenpool met patronen, events.
- Prototype staat (zie boven); Jordi speelt het eerst. Daarna: toren, kaart, drops, winkel.
- Intenties staan nu in het vraagvak links onderin (bovenaan is geen ruimte: levensbalken en sprites vullen het scherm). Blok en schade in % van max HP, omdat je in doubles je eigen HP-getallen niet ziet.

## Schermen (mockups, akkoord Jordi)
- Flow: gevecht → beloningsscherm (3 moves, A kiezen, B overslaan, SELECT kaart) → act-kaart → volgende kamer. Geen overworld ertussen.
- Act-kaart scrolt (±4 verdiepingen in beeld), PokéNav-stippenachtergrond, schuine gele routes met rand, gelopen pad rood, Brendan- of May-hoofdje = speler (volgt het gekozen geslacht, zoals de Town Map), rode hoekhaken = cursor, alleen de baas zichtbaar (icoon op rood plateau).
- Kamericonen: gevecht = Poké Ball (item-icoon), elite = Substitute (overworld-sprite) met een klein geel Super Saiyan-aura, rust = Chansey (icoon), winkel = blauw Mart-embleem (dak), event = Unown-?.
- Relics: eerste twee in het zijpaneel + "+N"; R opent de relic-lijst met uitleg. Cursor in menu's = de PC-hand.
- Mockups: `tools/grounded/spire/mockups.py <uitmap> v2|v4`.

