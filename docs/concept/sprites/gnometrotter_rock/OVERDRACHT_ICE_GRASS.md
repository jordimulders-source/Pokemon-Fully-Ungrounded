# Overdracht: Gnometrotter Ice en Grass (nieuwe sessie, 23 nov)

Plak in een nieuwe sessie (branch `ccr-e4619ef4-kb7349`):

> We gaan verder met Gnometrotter Ice en Grass. Lees eerst `docs/lessen/SPRITE_KERN.md`, `docs/concept/sprites/gnometrotter_rock/PLAN.md` (alle uitspraken van Jordi, bindend) en `docs/concept/sprites/gnometrotter_rock/OVERDRACHT_ICE_GRASS.md`. Rock is af (`gnometrotter_rock/af/`); doe Ice en Grass op precies dezelfde manier. Overleg eerst welke modelversie (gewoon of hybride) per vorm.

## Wat vastligt
- 3 vormen: Rock (af), Ice, Grass. Zelfde pose en maat als Rock (Wormadam: "hooguit paar pixels afwijking"); gedeelde verkleining `gnometrotter_rock/sprite/GEDEELD.md` + `reductie_gedeeld.py`; roze/blauw/zwart = Gnomad-kleuren en -indexen.
- Modellen: Ice `gnometrotter_ice/r3/gemini_r3_lijf.png` (of hybride `gnometrotter_ice/hybride/model_hybride.png`), Grass `gnometrotter_grass/r4/gemini_r4_lijf.png` (of hybride `gnometrotter_grass/hybride/model_hybride.png`). Bij de eerste ronde vond Jordi bij Ice de hybride "nog net wat beter, maar ook halfbakken".
- Jordi: geen gesp bij Rock en Ice; Grass heeft er geen ("ziet er prima uit"). Ice: afgekapte rechterschouder rond maken "zoals bij rock". Lijf: "slechts een paar materiaal vormen bij ijs en grass", vorm "zonder de kleur te veranderen van het roze en blauw". Oogstrook onder de muts dicht.
- Referenties: Ice: regice, glalie, snorunt, avalugg, bergmite, cryogonal, vanillish. Hout: nuzleaf, shiftry, seedot, trevenant, phantump (niet sudowoodo/bonsly). Plus onze eigen goedgekeurde sprites (Gnomad, Gnomini, Rock af, steenmozaiek, bloedmaan, corona).
- De sprites in `gnometrotter_ice/sprite*/` en `gnometrotter_grass/sprite*/` (nachtronde) vond Jordi "heel slordig"; het silhouet daarvan is wel "prima". Gebruik ze hooguit als silhouetbron.

## Werkwijze die bij Rock uiteindelijk werkte (r5 → r15)
1. Vormen eerst, uit het model (de maker tekent NOOIT opnieuw tenzij Jordi het vraagt); elke ronde zelf sprite naast het model op dezelfde schaal bekijken vóór Jordi.
2. Vormen bevriezen zodra Jordi zegt dat ze goed zijn ("de vorm laat je intact vanaf nu").
3. Dan alleen belijning/tinten/schaduw: zwartregel eerst meten in Gnomad/Gnomini/welp/steenjaguar (zwart = doorlopende strook rechts/onder; eigen donkerste tint links/boven; binnen alleen waar vorm over vorm valt; "geen zwarte lijnen onnodig"); één schaduwplan voor de hele figuur (licht linksboven); ≥3 tinten per vorm; naden/plaatlijnen precies zoals het model.
4. Krabbels van Jordi: kleuren in de screenshot meten (paneeloorsprong + pixelgrootte) en precies die pixels veranderen; stip = alleen die pixel; lever een raster met x/y-nummers en "krabbel | resultaat".
5. Eindkeuring (Dragonfly Cave-omlijning), reparaties als exacte pixellijst.

## Fouten die in deze sessie gemaakt zijn (niet herhalen)
- 5 sprites tegelijk in een nachtrun → allemaal slordig.
- "Netjes maken" liet de maker vormen hertekenen; Claude stopte het niet.
- Eigen analyse als excuus ("te druk/te groot") terwijl het slordig werk was.
- Krabbels te letterlijk of juist te ruim uitgevoerd; lijnen weggehaald die omlijning van de arm bleken.
