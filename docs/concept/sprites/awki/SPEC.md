# Awki (koningstiran fase 2) – SPEC

Lijn: hatun runa (Normal/Flying, `../hatun_runa/af/`) → **awki** (Fire/Flying) → Sapa Inca (Fire/Psychic, `../koningstiran/af/sapa_inca.png`). Zie `docs/concept/POKEMON.md` (Koningstiran-lijn). Werkwijze: **Gemini-model namaken** (`docs/lessen/SPRITE_WERKWIJZE.md`, poedelmot-regels) + `docs/lessen/GEMINI.md` + `docs/lessen/SPRITE_KERN.md`. Voorbeeld van een geslaagde vertaling in deze lijn: `../hatun_runa/` (kleur_r1–r5, gereedschap in `kleur_r1/stappen/`).

## Model (bevroren)
`referenties/model_gekozen.png` = Gemini-ronde 4 (`../koningstiran/gemini/awki_r4_v6.png`) met Claude's kleuraccenten (door Jordi goedgekeurd): lavendel punt aan de kuif en een rood vlakje tussen snavel en oog. Origineel zonder accenten: `referenties/gemini_r4_origineel.png`. Kijkt al naar links: niet spiegelen.
Inhoud: koningstiran met gesloten kuif als vlammende waaier (rood → oranje, punt lavendel), schuin naar achteren-boven; geel voorhoofdsrandje, zwart masker met oog, rood vlakje tussen snavel en oog, witte keel, gouden oorvlek; verre vleugel opgeheven vóór de borst (links), open, vuurkleuren per veerrij (bruin bij de schouder → donkerrood → oranje → geel aan de punten); nabije vleugel gevouwen, bruin (rechts); goudoker buik, roestbruine staart rechtsonder, donkere poten.

## Jordi letterlijk
- (7 nov) "dit heeft wel iets, mooi zon achtig patroon ook, de pose waardeer ik"
- (7 nov) over de accenten: "ja het anders kleuren kan jij wel he" / "wat accenten aanbrengen bijv" / "pose en vormen van onderdelen dat is voor jou lastiger" → "prima, ga maar bouwen, met de poedelmot regels"
- (7 nov) "ik heb sowieso al besloten dat dit een best wel latere evolutie wordt, deze fire/flying vogel ziet er al vrij sterk uit en fully evolved, dat is niet erg, dan maken we er gewoon een bisharp idee van, dat de sapa inca gewoon echt heel goed wordt"

## Formaat
Fase 2, late evolutie die er al volgroeid uitziet: model op **56 px breed** verkleind = ±1400 px, hoogte y2–60 (hatun runa 971, Sapa Inca 1560). Silhouet `silhouet/silhouet.png` (`sil.py 56`), bevroren.

## Aandachtspunten (alleen uitvoering, geen ontwerp)
- Kop en oog op 1×: oog in het zwarte masker met glanspixel (hatun runa-les: zonder glans leest het niet).
- Opgeheven vleugel: kleurbanden per veerrij zoals het model; veren als minder, grotere vormen op de modelplekken (geen zebra/raster).
- Kuif: vlammende waaier met lavendel punt; de gloed van Gemini wordt gewone pixels (geen gloed/halo).
- Rood vlakje bij de snavel: klein, zoals het model; geen bol/neus.
