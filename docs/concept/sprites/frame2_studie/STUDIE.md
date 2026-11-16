# Studie: hoe frontsprites bewegen en of Claude frame 2 betrouwbaar kan bouwen (16 nov)

Aanleiding: Jordi vroeg om een studie naar hoe sprites in de game bewegen en of Claude de tweede frames van de nieuwe designs betrouwbaar kan bouwen. Dit is een studie, geen productie: de volgorde "eerst alle frontsprites, frame 2 later voor alle soorten samen" (Jordi, 5 nov) blijft staan.

## 1. Hoe de engine een frontsprite laat bewegen
- Een frontsprite is een vel van 64×128: frame 1 boven, frame 2 eronder, zelfde palet (`anim_front.png`).
- Per soort in `src/data/pokemon/species_info/*`:
  - `.frontAnimFrames`: welk frame hoe lang (in GBA-frames van 1/60 s). Typisch `FRAME(0, 10–15)` / `FRAME(1, 10–15)`, soms een paar keer om en om. **Frame 2 staat dus maar 0,1–0,25 s in beeld**, vaak 1–3 keer.
  - `.frontAnimId`: tegelijk een transformatie van de hele sprite (`src/pokemon_animation.c`). Meest gebruikt: `ANIM_V_SQUISH_AND_BOUNCE` (490×), `ANIM_V_STRETCH` (85×), `ANIM_GROW_VIBRATE` (56×), schudden en glijden. Het indrukken/springen komt dus van de engine, niet van frame 2.
  - `.frontAnimDelay` (74 soorten): wachttijd vóór de animatie.
- **Waar het speelt:** wilde Pokémon/trainer stuurt uit (`pokeball.c`), samenvattingsscherm (`PokemonSummaryDoMonAnimation`), evolutie, ei uitkomen, Hall of Fame, contests. Niet in de Pokédex. Daar staat frame 1 stil.
- **Frame 2 is optioneel:** 400 soorten in de expansion gebruiken `sAnims_SingleFramePlaceHolder` (alleen frame 1) en bewegen alleen via `frontAnimId`. Dat geeft een terugvaloptie voor lastige ontwerpen.

## 2. Wat Game Freak in frame 2 doet (meting op 384 originele Gen 3-sprites, `anim_front_gba.png`)
Script: `analyse.py` (resultaat per soort in `res.json`). Per blok van 4×4 pixels in frame 2 zoekt het de best passende plek in frame 1 binnen ±4 px. Wat dan nog niet klopt, is **nieuw getekend**.

| Nieuw getekend in frame 2 | Aantal | Wat het is | Voorbeelden |
|---|---|---|---|
| < 5% | 15 | vrijwel stil | Shelgon, Cascoon, Slakoth, Duskull |
| 5–15% | 82 | onderdelen verschoven (kop, oor, staart ±1–2 px) | Whismur, Abra, Gulpin, Meditite, Swablu, Shroomish |
| 15–30% | 139 | verschoven + naden en wat herschaduwing | Treecko, Torchic, Sableye, Numel, Plusle, Raticate |
| > 30% | 148 | echte actiepose: bek open, vleugels/armen omhoog | Mudkip, Poochyena, Pikachu, Rattata, Taillow (68%), Combusken (76%) |

- Mediaan: 25% van frame 2 is nieuw getekend; 28% van de pixels staat identiek op dezelfde plek.
- Bij 201 van de 384 blijft de onderste rij (de voeten) precies gelijk.
- Bevestigt SPRITE_PLAN §1.7: frame 2 is bij Game Freak meestal een actiepose, geen verschuiving. Maar een kwart van de sprites komt toe met verschoven onderdelen.

## 3. Proef: viscacha (Zapacha)
Kop + snorharen 1 px omhoog, staartpluim 1 px schuin omhoog, verder niets (`viscacha_naief.png`, `viscacha_poging2.png`, `viscacha_poging2.gif`).
- Naïef plakken: snorharen dubbel (de oude pixels bleven staan).
- Eerst weghalen, dan plakken: **gaten in de borst** waar de snorharen over het lijf liepen. Wat achter een bewegend onderdeel zat, bestaat in frame 1 niet en moet getekend worden.
- Les: verschuiven gaat foutloos met een script; de **naden en de verborgen stukken** zijn het echte werk. Dat is tekenwerk binnen het bestaande palet en de bestaande vormen: klein (hier ±10–20 px), maar wel handwerk.

## 4. Oordeel: kan Claude frame 2 betrouwbaar bouwen?
- **Ja, voor verschuif-frames (klasse 5–30%, zoals Whismur/Treecko):** onderdeel kiezen, verschuiven met een script, daarna een maker-agent die alleen de naden en verborgen pixels tekent, met automatische controles (geen open randen, geen gaten, voeten gelijk, zelfde palet, geen pixels buiten de benoemde zones). Frame 1 blijft daarbij onaangeroerd; het risico is klein en een keuring is snel.
- **Alleen via een model, voor echte actieposes (> 30%: bek open, vleugels/armen omhoog):** dat is net zo moeilijk als een nieuwe frontsprite en Claude tekent niet uit zichzelf (SPRITE_KERN). Betrouwbaar wordt het als Jordi een Gemini-model van de tweede pose kiest en we alleen **het bewegende onderdeel** uit dat model overnemen in frame 1 (de rest blijft pixel voor pixel frame 1). Anders flikkeren verhoudingen en details tussen de twee frames.
- **Terugval:** geen frame 2, alleen `frontAnimId` (zoals 400 soorten in de expansion). Frame 2 is kort in beeld en de engine-animatie geeft al beweging.

## 5. Open voor Jordi (niet ingevuld)
- Welke beweging per soort (kop, oor, staart, bek open, vleugels): dat is een ontwerpkeuze.
- Of een verschuif-frame genoeg is of dat elke soort een actiepose moet krijgen zoals in SPRITE_PLAN §1.7/§1.12 staat ("Frame 2 = frame 1 een pixel verschoven" staat daar onder Nooit, behalve bij vormloze soorten).

## 6. Poging 3 viscacha (Jordi 16 nov: "verschuif-frames mogen"; poging 2 "lijkt net een muppet")
- Poging 2 bewoog de kop los van het lijf; daardoor klapperde hij als een pop.
- Poging 3 (`viscacha_f2.py`, `viscacha_poging3.png/.gif`, vel `viscacha_anim_front.png`): het lijf en de kop staan stil; alleen de oortoppen kantelen 1 px naar achteren en de staartpluim zwiept 1 px. Dat zijn onderdelen die aan lucht grenzen, dus er komt niets bloot en er hoeft niets getekend te worden (81 px gewijzigd, geen nieuwe kleuren, onderste 24 rijen gelijk).
- Les: kies voor verschuif-frames onderdelen met lucht eromheen (oren, staart, pluimen, antennes), schuif rij voor rij met hooguit 1 px trap per rij (anders breekt de omlijning), en beweeg de kop niet los van een kaak/borst die blijft staan.

## 7. Betere studie (16 nov): wat beweegt er echt (Jordi: "een paar pixels die op en neer bewegen is geen beweging")
Poging 3 is afgekeurd. De meting in §2 zei alleen *hoeveel* er verandert, niet *wat*. Nieuw:
- `vel.py`: vellen frame 1 | frame 2 | verschil (grijs gelijk, rood alleen frame 2, blauw alleen frame 1, geel andere kleur). `vel_gba_knaagdieren.png`, `vel_gba_klein.png`, `vel_ds_knaagdieren.png` (de DS-stijl is wat de game nu toont, `P_GBA_STYLE_SPECIES_GFX FALSE`).
- `banden.py`: per sprite de beste verschuiving van de bovenkant (35% bovenaan) en van de voeten (15% onderaan).

| | Gen 3 (384) | DS-stijl (844) |
|---|---|---|
| bovenkant beweegt, voeten bewegen ook (sprong, hele figuur) | 58% | 52% |
| bovenkant beweegt, voeten vast (strekken, leunen, buigen) | 29% | 37% |
| bovenkant stil (alleen kleine delen) | 11% | 9% |

- Bij vaste voeten beweegt de bovenkant meestal **2 tot 4 px of meer** (Gen 3: 1 px 29×, 2 px 29×, 3 px 18×, ≥4 px 39×); omhoog en omlaag komen allebei voor.
- Wat je op de vellen ziet: **het hele lijf beweegt als één geheel**, vanuit de voeten: Sentret en Cinccino strekken zich omhoog, Pachirisu en Furret leunen, Lillipup en Plusle springen, Zigzagoon duikt met de kop omlaag. Oren en staart bewegen mee of tegen (Eevee, Linoone, Minccino: staart zwaait 4–8 px). Daarbovenop vaak een getekend detail (bek open, ogen dicht).
- Dus fout in poging 2: kop los van het lijf (muppet). Fout in poging 3: alleen puntjes van 1 px; dat doet Game Freak bijna nooit.

### Poging 4 viscacha: het hele lijf (`viscacha_poging4.png`, `_strek.gif`, `_strek_leun.gif`, vellen `viscacha_anim_front_A/B.png`)
- **A strekken:** drie rijen gedupliceerd (in de borst en in de poten); alles boven de poten komt 3 px omhoog, de voeten blijven staan. Hij gaat alerter rechtop staan, met langere poten.
- **B strekken + leunen:** als A, en de bovenkant leunt daarna oplopend tot 2 px naar voren.
- Er hoeft niets bijgetekend te worden, want rijen dupliceren laat niets bloot. Wel nadelen: gerekte diagonalen krijgen een trapje, en bij B vallen 2 px snorhaar links buiten het vak.

### Oordeel, bijgesteld
- Een frame waarin het hele lijf strekt, leunt of duikt (zoals Sentret, Pachirisu, Cinccino), kan Claude met een script als onderlaag bouwen; een maker ruimt daarna alleen de trapjes op.
- Een beweging plus getekend detail (bek open, staart die echt zwaait, poot omhoog) blijft tekenwerk: via een maker-agent of een model van Jordi.
- Welke beweging een soort krijgt, kiest Jordi.

## 8. Geslaagd: Gemini-bewerking van de sprite zelf (viscacha, 16 nov)
- Jordi gaf Gemini de 8×-sprite + de prompt uit `viscacha/gemini/PROMPT_FRAME2.md`. Resultaat (`viscacha/gemini/frame2_ronde1.png`, gif ernaast): exact op het 16×-raster van de sprite, lijf/achterpoten/staart pixel voor pixel gelijk aan frame 1, kop naar achteren met open bek en voorpoten tegen de borst. Jordi: "echt verbazingwekkend goed"; alleen de snorharen ontbreken ("goed te fixen").
- Werkwijze frame 2 voortaan: **de sprite zelf (8×) als bijlage**, prompt "keep pixel grid and palette, change only X", terugzetten met de middelste pixel per 16×16-vak, dan opschonen.
- Volgende: Gengas (manen bewegen; Hoopa Unbound doet iets vergelijkbaars, zie `hoopa_unbound.gif`), prompt in `gengas/gemini/PROMPT_FRAME2.md`.

## 9. Waarom Gemini de viscacha wel en Gengas niet kon (16 nov)
- Gemini heeft geen knippen-en-plakken: een "bewerking" tekent het hele beeld opnieuw, gestuurd door de bijlage. Wat het beeld al "weet", blijft staan; wat je vraagt, tekent het opnieuw.
- **Viscacha:** de vraag was een **handeling van een dier** ("roept met open bek, poot omhoog"). Daar is Gemini op getraind; het lijf werd niet genoemd, dus bleef het staan.
- **Gengas:** de vraag was **meetkunde** ("schuif 3 px omhoog", "6 px naar links"). Getallen en precieze verplaatsingen kan het niet; "verplaats de maan" werd "teken een maan daar" (ronde 2: zes manen). Daarnaast is Gengas een ongewoon ontwerp (losse manen als handen/voeten) dat het niet als ledematen herkent, en vult de bol bijna het hele vak, zodat "omhoog" een platgedrukte bol wordt.
- Les: **Gemini voor poses (in woorden als handeling: lachen, juichen, zwaaien), een script voor pure verplaatsing.** Een vraag in getallen of posities aan Gemini werkt niet.

## 10. Gengas: Gemini kan geen knik bij een bol (16 nov)
- Bijlage zonder manen + "the creature nods, lifts its head": Gemini gaf dezelfde bol terug (op 11× i.p.v. 16×), alleen de oren iets anders (`gengas/frame2/gemini_knik_r1.png`). Een bol heeft geen nek; "hoofd omhoog" is voor Gengas pure verplaatsing.
- Daarom alles per script (`gengas/frame2/frame2.py`): ronde bol (v15, door maker-agents) 3 px omhoog, de vier manen (uit `af/gengas.png`) los verplaatst; niets getekend. Uitvoer: `gengas_frame2.png/.gif`, vel `gengas_anim_front.png`.
- Werkwijze frame 2 samengevat: **lijf met anatomie (poten, bek) → Gemini (handeling in woorden); losse delen of een vormloos lijf → script (verplaatsen); wat bij verplaatsen bloot komt → maker-agent rond/dicht maken.**

## 11. Viscacha in één keer goed, Gengas na zeven prompts niet: waarom (16 nov)
- **Lokaal vs. alles:** bij de viscacha veranderde een deel (kop, voorpoten); ±70% bleef staan en dat kopieerde Gemini gewoon. Bij Gengas moet de hele figuur bewegen (de bol ís het hoofd); dan moet Gemini alles opnieuw tekenen en verloopt alles (vorm, banden, ogen, oren).
- **Bekend vs. ongewoon:** "een knaagdier roept met open bek" kent Gemini; een bol met Gengar-gezicht en gasoren niet, en het trekt naar Gengar of een generieke bol.
- **Ruimte:** Gengas vult het vak; "hoger" vraagt een nieuwe compositie.
- Les: **Gemini voor lokale poseveranderingen; beweging van de hele figuur (opveren, kantelen, knikken) via de engine-animatie (`frontAnimId`) of een script.**

## 12. Werkwijze frame 2 (besloten na de viscacha- en Gengas-test, 16 nov)
Jordi over Gengas variant C met V_SLIDE: "de tweede gif van de 3 vind ik echt uitstekend". Daarmee zijn beide tests geslaagd. Werkwijze:
1. **Lokale pose met anatomie** (bek open, poot/arm omhoog): Gemini bewerkt de 8×-sprite zelf met een handeling in woorden ("cries out with its mouth open, raised paw lifted higher"); terugzetten met de middelste pixel per 16×16-vak; kleine reparaties door een maker-agent (viscacha: snorharen).
2. **Hele figuur beweegt** (bol, kop is het lijf): per script — onderdeel draaien met nearest-neighbour (zoals de engine) en/of verschuiven; geen Gemini (verloopt of doet niets).
3. **Losse delen** (manen, zwevende handen): per script verplaatsen, **in tegenbeweging** met het lijf (lijf omhoog/rechtsom → delen omlaag/de andere kant op), anders lees je hun beweging niet.
4. **Wat bij verplaatsen bloot komt of door draaien rafelt:** maker-agent maakt het rond/dicht/schoon, vorm en hoek bevroren.
5. **Engine-animatie erbij** (`frontAnimId`): kies er een die de beweging versterkt (Gengas: `ANIM_V_SLIDE`); frame 2 lang genoeg in beeld (Gengas: ±34 tikken). Eerst als gif simuleren (`gengas/frame2/combi_c.py`, nagerekend uit `src/pokemon_animation.c`), daarna in de emulator.
