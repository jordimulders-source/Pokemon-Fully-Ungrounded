# Alpaca fase 1, ronde 13: combinatie van ronde 11 en 12

Jordi over ronde 12: "Echt vele malen slechter. De kleuring en het lichaam zijn prima, maar ik wil de vuisten nog steeds op de grond, en wat heb je in hemelsnaam met het hoofd gedaan?"

Ronde 13 is daarom geen nieuw ontwerp. Het is een samenvoeging van bestaande, handgetekende rijen (`bron/delen.txt`, absolute coördinaten, per deel de herkomst erbij).

## Herkomst per deel
| Deel | Uit | Wijziging |
|---|---|---|
| Palet en shading (crème → oudroze → mauve → pruim, zwart alleen aan de schaduwkant) | ronde 12 (`palet.txt` ongewijzigd) | geen |
| Lijf, staart, beide achterpoten | ronde 12 | +3,+3 naar absolute coördinaten (was `@ 3 3`); de bovenste nekrij van het lijf (y27) is weggelaten |
| Verre voorpoot met wolverdikking, band en matte wolvuist op de grond | ronde 12 | geen |
| Kop: vorm, snuit, oren, franje, pompon | ronde 11 | 1 rij omlaag (y+1), x gelijk; ingekleurd met het ronde-12-palet doordat de letters (W w v u V K) gelijk zijn |
| Nek (lengte en breedte) | ronde 11, rij 21–26 | 1 rij omlaag; sluit op y28 aan op het lijf van ronde 12 |
| Ogen | ronde 11, plek en maat | nabij oog: dezelfde 3×4-vorm, nu met de witte glanspixel **binnen** het zwart (x27,y15) en de paarsblauwe reflectie rechtsonder; verre oog: 2×4-vorm van ronde 11, helemaal zwart (de glans van ronde 11 lag op de rand en smolt met de vacht, daardoor lazen de ogen grijs); oudroze randje (v) onder beide ogen |
| Nabije voorpoot | stand van ronde 11 | schuin naar voren uit de borst, vuist op de grond (laagste punt, y54); daarboven een kleine wolpluim (idee van ronde 12) die over de band valt |
| Gebreide manchet | ronde 11 (nabij: twee magenta strepen met roze hooglicht, geel/turquoise ruitjes) | geen |
| Nabije vuist | vorm van ronde 11, mat zoals ronde 12 | de witte glanspixel eruit, 1 rij korter, 1–3 px naar links zodat er een kolom lucht tussen de twee vuisten zit |
| Frame 2 | ronde 11/12 | kop, pompon en oren zakken 1 px |

## Cijfers
- **Oppervlak 923 px** (frame 2: 914). Ronde 11 had 869, ronde 12 1013. Ter vergelijking: Mudkip 852, Mareep 893, Treecko 967.
- **Zwart-aandeel rand 0,48.** 16 kleuren, index 0 transparant. `anim_front.png` is 64×128.
- Hoogte y4–y54 (ronde 11: y3–y52).

## Checklist (§0)
1. **Lijf én blik diagonaal:** ok. De kop staat 3/4 zoals in ronde 11 (twee ogen, verre oog smaller, snuit linksvoor); het lijf van ronde 12 heeft een borstvlak en een wijkende flank. Voethoogtes: nabije vuist y54, nabije achtervoet y51, verre vuist y50, verre achtervoet y47.
2. **Ledematen, oren en ogen geteld en verbonden:** ok. 4 poten (2 vuisten, 2 achterpoten), 2 oren, 2 ogen, neus en mond, pompon, staart. `bouw13.py` meldt geen open randen. Nek-kop (y22) en nek-lijf (y27/28) sluiten met doorlopende omlijning aan.
3. **Geen rechte lijnen in een ronde omtrek:** grotendeels ok. Over: de voorkant van de nek (7 px, een zuil, zoals ronde 11), de bovenrand van de rug bij de nekaanzet (8 px, uit ronde 12), schenen en onderkanten van voeten/vuisten (staan op de grond).
4. **Ogen geïntegreerd, verre oog geen kopie:** ok. Bijna-zwart (40,22,40), glans binnen het nabije oog, reflectie B, oudroze rand eronder; het verre oog is 2 breed en zonder glans. Geen zwaar ooglid: de pixels boven de ogen zijn licht gebleven, zoals in ronde 11.
5. **Silhouet leest op 1× als de soort:** ok volgens de knijp-je-ogen-test in `compare.png`: de lange nek met de kleine kop en V-oren van ronde 11 is terug, de vuisten staan op de grond.
6. **Formaat:** zie Cijfers; tussen ronde 11 en 12 in, binnen 870–950.
7. **Pose niet stijf:** ok. Schuine nabije voorpoot, gespreide stand, hakken in de achterpoten, knikje in frame 2.

## Bestanden
- `anim_front.png`, `normal.pal`
- `compare.png`: ronde 11, ronde 12, ronde 13 (frame 1 en 2) en Torchic, op wit, op de gevechtsgrond en op donker, telkens 1× en 3×.
- `bron/delen.txt`, `bron/palet.txt`, `bron/bouw13.py`, `bron/vergelijk13.py`, `bron/raster_f1.txt`, `bron/raster_f2.txt`. Gebruik vanuit de repo-root:
  - `python3 docs/concept/sprites/alpaca/ronde13/bron/bouw13.py docs/concept/sprites/alpaca/ronde13 [preview.png]`
  - `python3 docs/concept/sprites/alpaca/ronde13/bron/vergelijk13.py`

## Lessen
- **Wat Jordi goedkeurt, blijft letterlijk staan:** na "echt veel beter" (ronde 11) is de kop in ronde 12 toch "babystarter" gemaakt (grotere kop, kortere nek, zwaar ooglid) en dat maakte alles slechter. Een verzoek als "meer Pokémon" uitvoeren in palet/shading/details, niet door goedgekeurde verhoudingen te veranderen.
- **Een opdracht van de coördinator die een goedgekeurde pose verandert (geheven vuist) eerst als variant opleveren,** niet als de enige versie.
- **Absolute coördinaten bij combineren:** delen uit twee rondes samenvoegen gaat het snelst door alle rijen naar absolute x/y te zetten (`@`-verschuiving uitschrijven) en per deel de herkomst als commentaar te noteren.
- **Kop van ronde X op lijf van ronde Y:** de nek bepaalt de aansluiting; neem de neklengte (kin tot rugaanzet) mee met de kop en laat het lijf pas beginnen bij de rij waar de rug start, anders wordt de nek langer of korter dan bedoeld.
- **Glans hoort binnen het zwart:** een glanspixel op de rand van een klein oog smelt met de vacht en laat het oog grijs lezen; zet hem minstens aan twee kanten tegen zwart, of laat een 2 px breed verre oog helemaal zwart.
- **Twee vuisten naast elkaar:** houd één kolom lucht tussen de omlijningen, anders lezen ze op 1× als één rode klomp.
