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
