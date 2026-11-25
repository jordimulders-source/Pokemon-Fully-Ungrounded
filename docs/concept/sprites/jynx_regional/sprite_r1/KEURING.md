# Keuring regionale Jynx (sirene), sprite r1

Keurder: vers, onafhankelijk (25 nov). Eerst blind gekeken (eigen vellen: sprite 8× naast model, sprite 1× naast een eigen BOX-reductie van het model op dezelfde maat, gezicht 16× naast het model, naast Jynx `anim_front_gba.png` + `normal_gba.pal`, Dundragoon en Awki), daarna pas `NOTITIES.md` gelezen.

## Eindoordeel: **BIJNA**

Eis 1 (trouw) is in orde. Eis 2 (Gen 3) is bijna in orde; het grootste punt is het volume van het haar, daarna een paar lijn- en ruisfouten.

### Eis 1: trouw aan het model: in orde
- Silhouet, pose, vleugels, halskraag, rok met vouwlijnen, achterhaar rechts en klauwvoeten liggen op de modelplekken. Mijn eigen reductie (54×58) en de sprite vallen op 1× samen.
- **Gezicht:** vorm (rond, met de scheiding/inham bovenaan), beide ogen (wimper + rode iris, grijze oogschaduw erboven, het losse zwarte binnenhoekje van het rechteroog staat ook in het model), lippen met bultjes bovenop, open mond met donkere binnenkant en roze tong: alles is aanwezig en staat goed. Niets toegevoegd of weggelaten dat 64 px kan tonen.
- De gezichtscontour is haar-donker in plaats van het modelzwart. Dat is een Gen 3-binnenlijn, geen herinterpretatie.

### Eis 2: Gen 3
- **Volume (eerst getoetst):**
  - **Vleugels:** in orde (licht, midden en schaduw met veerlijnen).
  - **Rok:** voldoende (licht links, midden, schaduw rechts en rechtsonder).
  - **Gezicht:** in orde (grijze schaduw rechts en onder, oogschaduw).
  - **Haar: onvoldoende.** De kruin en de linkerlokken zijn één middentint `h` (164,114,72) met donkere streng-lijnen. Er is geen hooglicht op de bolling en geen tintverdeling binnen de lokken. De schaduwtint `B` komt maar op 74 px voor. Gen 3-Jynx heeft op dezelfde plek duidelijke lichte en donkere lokken. Gemeten: het model zelf is hier ook vlak (kruin bijna alleen (160,112,72)). Kleur en volume mogen afwijken van het model (SPRITE_KERN), dus dit moet naar Gen 3, wel op de lokvormen van het model.
- **Contrast:** stappen veren ±32/34/38 en haar ±35/31. In orde.
- **Belijning:** de buitenlijn is overal 1 px, met selout linksboven en zwart rechts en onder. Binnenlijnen in de eigen donkerste tint. Eén plek zwart om en om (punt 3).
- **Tinten:** ≤ 3 per groep + lijn. Geen banding behalve wat uit het model komt: de lichtere band langs de buitenrand van het achterhaar rechts staat zo in het model en is goed.

## Reparaties (prioriteit eerst)

1. **Haarvolume (kruin x19–36 y6–13, linkerlokken x15–18 y14–40).**
   - Maak een paletplek vrij. Iris (160,64,60) en lipmidden (144,54,74) liggen dicht bij elkaar, dus zet de 6 irispixels op index 12. Een andere optie is klauwen (100,80,64) → haar-schaduw `B`.
   - Voeg op die plek een lichte haartint toe, ±(200,154,104).
   - Zet die tint per lok aan de linkerbovenkant van elke lok, tussen de streng-lijnen uit het model: een gebogen hooglicht op de bolling links van de scheiding (rijen 7–11), plus het bovenste stuk van de linkerlok waar die over de schouder buigt.
   - Langs de rechterkant van elke streng-lijn komt `B` (124,80,46) als schaduw, zodat de lok rond leest.
   - Grenzen gebogen en volgens de lokvorm. Geen band parallel aan de buitenlijn en geen nieuwe strengen: alleen tinten op de vormen die er al zijn.
2. **Ruis in het haar rechtsboven (x40–46, y11–22).** De streng-lijnen wisselen per pixel tussen `B` en `b` (bijv. rij 16 x42–44 `B b B`, rij 17 x43–46 `b B B b`). Elke streng uit het model krijgt één doorlopende lijntint `b`, met `B` als schaduw ernaast. Geen dambord.
3. **Linkervleugel, bovenrand (9,17) en (10,17): zwart → selout `d` (120,48,24).** Deze rand ligt aan de lichtkant. Nu loopt de lijn `d`(8,16) → `K K` → `d`(11,18): zwart en selout om en om.
4. **Onderlip (x20–25, y23–25).**
   - Nu staan donker en midden door elkaar (rij 23 `m M m m M M`, rij 24 `m M m m`), en (25,23) `M` raakt het wit zonder lijn (open rand).
   - Neem de ring over uit het model: donkere lipomlijning langs de onderkant en rechts (ook (25,23)–(25,24)) en de middentint als één band tussen mondopening en omlijning.
5. **Onderbroken vouwlijn in de rok (x33–47, y46–48).** Rij 47 `d d o o d o d d o d d d d d` leest als een stippellijn of ruis. Maak er één doorlopende 1 px-lijn `d` van langs het modelpad; de losse `o`-gaatjes in de lijn worden lijn of vlak, nergens om en om.
6. **Ter keuze (licht):** het rechterrokpaneel onder de arm (x36–43, y34–46) staat in `L`.
   - Gemeten in het model: dit paneel is maar 9 helderheid lichter dan het rokmidden (155 tegen 146). In de sprite is dat 28 geworden, zo licht als de linkerkant. Daardoor lijkt de rechterkant van het lijf aan de schaduwkant opgelicht.
   - Voorstel: `L` alleen langs de linkerbovenrand van dat paneel (tegen de arm), de rest `o`. Concrete tintwissel, geen vormwijziging.
7. **Ter info:** (22,10) is één losse witte pixel in de haarlijn. Hij komt uit het model (W 49 %), maar leest op 8× als vlekje. Alleen aanpassen als Jordi het ziet.

Niet aanpassen:
- Silhouet, gezichtsvorm, ogen en mondopening.
- Voeten: druk op 8×, maar ze lezen op 1× goed als klauwvoeten.
- Achterhaar rechts: komt uit het model.
