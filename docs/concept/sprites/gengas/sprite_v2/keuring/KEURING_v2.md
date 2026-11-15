# Keuring Gengas sprite v2 (15 nov)
Keurder: onafhankelijk, alleen de twee eisen (trouw aan het model + Gen 3-techniek). Coördinaten (x,y), 0-gebaseerd, x = kolom.
Vergelijkingsplaatjes in deze map: `blind.png` (1×/2×/8×), `model_vs_sprite_8x.png`, en per onderdeel model64 | sprite | natief:
`gezicht.png`, `krul.png`, `oren.png`, `rechteroor.png`, `maan_*.png`; zones gemarkeerd in `gezicht_zones_14x.png`; Gengar ter vergelijking `gengar_gezicht.png`.

## Eerste indruk (blind, vóór vergelijken)
- 1×/2×: leest meteen als een Gengar-achtige bol met vier grijze brokken eromheen; grijns en ogen dragen de herkenning. Licht linksboven, schaduw rechtsonder: goed.
- 8×: lijf en banden rustig; de krul rechts leest als een ring met een streepje, niet als spiraal. Links van het gezicht twee vlakke rechthoekige stukken (donker boven, lichtroze onder) met een rechte naad; rechtsonder de grijns een rechthoekig lichtroze inhammetje. Wit puntje tussen de rookarm en de rechtermaan. Manen korrelig maar herkenbaar als brokken met vingers/tenen.

## Hoofdvraag: is dit een goede eindversie? **BIJNA**
Silhouet, oren, manen, rookarm, banden en lichtvlek zijn vrijwel pixelgelijk aan `model_64_geschrapt` (op het gezichtsblok na); de bol is een bol. De klachten van de eigenaar over r2/r3 zijn hiermee grotendeels opgelost (zie onder). Wat nog fout is zit in de naden van de gezichtsverschuiving (precies de klacht "lijken teveel erop geplakt"), de krul en één witte pixel.

### Controle van de eerdere klachten
| klacht | oordeel |
|---|---|
| manen als willekeurige vormen | OPGELOST: silhouet en binnenvormen van alle vier = model (alleen randselout aangepast). |
| linkeroor niet nagedaan | OPGELOST: oor = model (vorm, binnenschaduw, gaspunt bovenaan). |
| vlak onder het rechteroor dat er niet is | OPGELOST: daar staat nu alleen de rookarm uit het model; maar zie MOET 1 (witte pixels). |
| krul in de planeet niet mooi | NIET OPGELOST: zie MOET 4. |
| schaduwen niet mooi | Lijf grotendeels OK (= model); de vulstroken bij het gezicht zijn vlak en recht (MOET 2–3). |
| gezicht geplakt (kleur, schaduw, lijnen) | BIJNA: kleuren en lijnen van ogen/grijns zelf zijn het model; de aansluiting faalt op de naden (MOET 2, 3, 5). |

## MOET
1. **Witte pixels in de rookarm** (51,22) en (52,22): opaak wit (254,254,254, letter W). In het model is dit een gat (achtergrondwit 255) tussen rookarm en rechtermaan. Op een gevechtsachtergrond wordt dit een wit vlekje. Transparant maken (of de kleur van de buren a/K), zoals het model.
2. **Naad rechtsonder de grijns** (zone x27–33, y43–47): de donkere band (b) begint op rij 43–46 allemaal op x33 (verticale rand van 4 px) en springt op rij 47 naar x27 (horizontale trede van 6 px): de rand van het verschoven gezichtsblok is zichtbaar als rechthoekig lichtroze inhammetje. Model: de bovenrand van deze band loopt diagonaal (rij 43 x32 → rij 44 x30 → rij 46 x28 → rij 47 x27). Bandgrens weer diagonaal laten lopen, ±1 px per rij, van ±(33,42) naar (27,47), met de grijns ongemoeid.
3. **Naad links van het gezicht** (vulstrook): blok (8–12, 29–37) is vlak b en blok (8–13, 38–46) is vlak l, met een rechte horizontale grens van 6 px op y37/38 (x8–13). Dat is de "geplakt"-rand: in het model buigt de maskerrand schuin naar de mondhoek. Grens schuin laten lopen van ±(8,36) naar de mondhoek (14,38/39), en de lichte strook dezelfde overgang l→m→r naar de buitenrand geven als de band eronder in het model (rij 45–46: `Klmllm`, `Krmmmm`), zodat hij niet als effen plak leest.
4. **Krul** (x37–43, y33–38): leest als ring met los streepje, niet als spiraal. Natief model (`gekozen_v3_natief.png` rij 37–46, x43–52) toont een doorlopende spiraal van één lijn. Nu: lijntinten gemengd a/b ((37,36) a, (38,37) a, (42,38) a, rest b), linkerzijde maakt een uitstulping op (37,36), en het middenstreepje (40–41,36) zit los van de ring. Eén lijn in één tint (b) die bij het open eind linksboven begint, rechts en onder rondloopt en naar binnen eindigt in het midden, zoals natief; de lichte rand (l) eromheen houden. Geen nieuwe vorm: de spiraal van het natieve model op 64 px leggen (bij het schrappen ging hij stuk).
5. **Lichte wig tussen/boven de ogen weg** (model kleur 121,70,91, model-pixels (10–13, 25–28) en (13–21, 29–34) → in de sprite verschoven ±(14–18, 26–29) en (18–26, 30–35)): nu allemaal effen b; daardoor is het masker één donkere plak en mist het de wenkbrauw-/neusbrugvorm die het model heeft. Terugzetten. Palet is vol (15 + transparant): ruil bij voorkeur de kleinste tint die het minst verlies geeft (bv. w, kern lichtvlek 19 px → v), of gebruik m als het verlies kleiner blijkt; meten, niet gokken.

## MAG
- **Lichte streep boven de ogen dubbel** (14–23, 28) origineel + (19–28, 29) verschoven kopie: de streep is links 1 rij dikker dan in het model. Mag één van beide rijen terug naar b/m.
- **Manen korrelig**: 15 losse 1-px tintpixels (8-buren) in de vier manen, o.a. g(27,1), H(28,2), g(31,4), G(32,6), g(33,6), g(28,8), g(30,9), G(56,21), G(44,51), g(43,52), G(52,52), g(42,54), h(43,57), G(53,57), G(48,59). Model heeft dezelfde kraterkorrel; per maan kraters samenvoegen tot 2–3-px vlekjes (zoals natief) mag, silhouet en omlijning bevroren.
- **Zwarte omlijning aan de lichte linkerkant** (x7–11, y16–40): Gen 3 wil daar liever selout, maar het model is daar ook (bijna) zwart; laten zoals het model is verdedigbaar.
- **Gaspunten zonder omlijning** (linkeroor (15–22, 5–8), rookslierten (57–58,16)): model, bewust; laten.
- **Tinten lijf**: lichte groep m/l/v/w = 4 tinten + donkere groep a/b; w is de glans (19 px), dus binnen de regel. Geen banding of pillow shading gevonden.
- Pupil rechteroog (27,34),(28,34),(28,35) is Gengar-vorm en toegestaan; geen punt.
