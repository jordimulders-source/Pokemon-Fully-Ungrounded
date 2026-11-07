# DJ Rotom – kleur3 (reparatie van kleur2 B)

Basis: `../kleur2/dj_rotom_B.png` (gekozen na `../kleur2/KEURING.md`). Alleen de benoemde zones zijn gewijzigd.
Jordi: "bliksem noot mag idd dikker dan". Smaakkeuzes uit de keuring (gloed, ronde ogen, kubus) zijn niet aangeraakt.

## Bestanden
- `dj_rotom.png` (64×64, geïndexeerd, transparency=0), `normal.pal` (= kleur1/kleur2), `vel.png`.
- `bron/dj_rotom.txt`: het tekstraster, een kopie van B met de hand bewerkt via `bron/zet.py` (rij, x, tekens).
- `bron/controle.py`: open randen, losse pixels, diff per zone t.o.v. B. `bron/render.py`, `bron/vel.py`.

## Reparaties (gewijzigde px t.o.v. B)
| zone | px | wat |
|---|---|---|
| 1 bliksem x19–30 y14–25 | 67 | Nieuw getekend. Bovenblok is een parallellogram (bovenrand y14 x22–29, linkerrand leunt "/", scherpe punt linksonder op (19–20,22)). Rechts een inham die diagonaal naar binnen loopt (x28→x25, y17–20), daarna een uitsteker naar rechts met punt (30,21–22) = de Z-knik. Staart met een kern van 2 px `33` (x26–27, y22–25) die in de spitspunt (27,26) loopt. Rechtopstaande witte achtste noot: steel x25 y15–19, vlag (26,15)+(27,16), kop 2×2 (23–24, y19–20); alleen mint `2` eromheen. 2 px breder naar rechts dan B. |
| 2 kop x31–32 y32–57 | 34 | x31–32 is voorvlak geworden (y32 `6`, y33 `4`, verder `5`). Het zijvlak is nu x33–34 met naad x35; rechts van het rechteroog blijft 2 px oranje over. De omtrek is niet veranderd. |
| 3 conussen rechts x40–50 y34–55 | 44 | Grijs streepje weg (navy). Stofkap 3×3 `a` op x44–46 y38–40 en y49–51, met één glans `b` linksboven ((44,38), (44,49)). De zwarte kom is bovenaan 1 rij dunner (y36 resp. y47 grotendeels navy). |
| 3 conussen links x6–12 y41–53 | 5 | Kleine conus: glans naar (9,43), (9,44) zwart. Grote conus: glans naar linksboven op de stofkap (8,50), het onderste glansje is weg. |
| 4 hoek rechtsonder | 4 | (59,59) en x55–57 y60 → `7` (donkerbruine rand). Geen zwart meer in de hoek. |
| 5 snoer | 1 | (17,51) → zwart: het snoer raakt het display. |
| 5 schaduw kopvoorvlak | 28 | y55–56 x17–32 → `6`, kolom x32 y45–56 → `6` (zoals Frost onderaan). |
| losse pixel iris | 1 | (28,38) `d`→`c`, zodat de losse irispixel (27,38) een buur heeft. Het enige pixel buiten de zones. |
**Totaal 184 px gewijzigd t.o.v. B**, waarvan 1 buiten de zones (de irisreparatie). Alpha verschilt 37 px van B, allemaal in de bliksemzone (de verbreding).

## Checks (`bron/controle.py`)
- Open randen: **geen**.
- Losse pixels (geen 8-buur met dezelfde index), 10 over, allemaal bewust:
  - 4 glanspixels `b`: (44,38), (44,49), (9,43), (8,50). Gevraagd als "één glanspixel"; een glans is per definitie één pixel.
  - 6 equalizerpixels van de staafjes van 1 px (B): toppen `2` (23,50), (27,50), (21,51), (25,52) en voetjes `e` (19,53), (25,53).
- Opgelost: (25,16) en (27,22) in de bliksem (nieuw getekend), (27,38) iris, (9,44) kleine conus, (59,59) zwarte hoek.

## Toets
- 1× naast Heat/Wash/Frost: een Rotom-vorm uit dezelfde game. Speakers, kop met gezicht en display met equalizer lezen als DJ Rotom.
- De bliksem leest nu als bliksem (wig, knik, staart in de spits) en niet meer als blaadje.
- Conussen lezen als speakerconus met stofkap, niet meer als sleutelgat.
- De kop heeft volume (schaduw onderaan en rechts) en oranje rechts van het rechteroog.

## Wat nog niet (helemaal) klopt
- **De noot is op 1× een klein wit ♪-vormpje** (11 px in een vlak van 7×6). Vanaf 2× leest hij duidelijk als achtste noot. Groter kan niet binnen de bliksemzone (6 rijen hoog). Een donkere schaduw naast de steel heb ik geprobeerd; dat hielp op 1× niet en is teruggedraaid. Oplossing als Jordi het op 1× wil: de bliksemzone 2–3 rijen hoger laten beginnen (y11–12, zoals in s1.25).
- De linkerrand van het bovenblok is een trap van 1 px per 2 rijen; op 4× iets rond in plaats van strak schuin.

## Lessen
- Een bliksem leest als blad als hij vooral rond is: de punt linksonder en de uitsteker na de inham moeten echt uitsteken (≥ 2 rijen dik), anders blijft het een vlek.
- Een achtste noot op ±7×6: steel 5, kop 2×2 linksonder, vlag 2 px diagonaal vanaf de steeltop. Een vlag die lager begint dan de steeltop leest als een vork.
- Een donkere schaduw naast wit op lichtmint helpt op 1× nauwelijks; grootte telt meer dan contrast.
- De diff per zone met een script geeft meteen het bewijs voor "de rest pixel-gelijk".
