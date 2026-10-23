# Olinguito (Dark-starter fase 1), ronde 8: van nul af aan

Schone lei: geen eerdere olinguito-sprites of -modeltekeningen bekeken. Referenties alleen echte Gen 3 (Teddiursa, Zigzagoon, Poochyena, Sneasel, Sandshrew, Eevee), Drilbur/Sandslash voor de klauwen en Cuyby ronde 3 als niveau-maatstaf.

## Bestanden
- `anim_front.png`: 64×128, twee frames, geïndexeerd, index 0 transparant, 15 van de 16 kleuren gebruikt.
- `normal.pal`: JASC-PAL, 16 kleuren (index 15 = rood, vrij voor later).
- `compare.png`: naast Teddiursa, Zigzagoon, Poochyena, Sneasel en Sandshrew, op 1× en 3×.
- `schetsen.png`: drie ruwe schetsen (A zittend met klauwen omhoog, B op vier poten, C rechtop met babyverhoudingen).
- `bron/`: de handgetekende tekstrasters per lichaamsdeel (`kop`, `lijf`, `arm_voor`, `klauw_voor`, `arm_achter`, `voeten`, `staart`), `build.py` (zet de rasters op elkaar, verder niets) en `export.py` (frames, palet, vergelijkingsvel). `schets.py` maakte alleen de ruwe schetsen.

## Keuzes
- **Pose:** schets C (rechtop zittend, babyverhoudingen), met de klauw voor het lijf zoals bij A. Schets B (op vier poten) was meer coati, maar dan wordt de kop klein en verdwijnen de klauwen onder het lijf.
- **Kop groot:** de schedel is 23 px breed op een lijf van ±19; met de snoet erbij is de kop 31×20, ongeveer de helft van de figuur.
- **Kenmerk 1, de snoet:** kort maar duidelijk spits, roomkleurig, met een dikke zwarte neus met glanspixel. Hij steekt als eerste uit het silhouet.
- **Kenmerk 2, de klauwen:** twee dikke haken die samen één gereedschap vormen (zoals bij Drilbur en Sandslash): eerst naar voren, dan omlaag, met de punten naar binnen gekruld. Ze komen onder een ronde 'want' vandaan. Ivoor, met omlijning in de klauwschaduwkleur aan de lichte kant en zwart aan de binnenbocht. Eerst probeerde ik drie dunne sikkels; die lazen als een vork of bezem, dus het zijn er twee geworden, breder.
- **Donker:** het lijf is vooral de schaduwtint (68,44,38) met de basistint als eerste laag licht (Scorplack-aanpak), en een klein hooglicht linksboven op schedel, want en staart.
- **Masker:** een bijna zwartbruine band over beide ogen met roomkleurige 'wenkbrauwvlekjes' erboven (coati-tekening). Er is geen aparte maskerkleur: het masker is de omlijningsbasis van de vacht.
- **Ogen:** in de eerste versie waren de ogen zwart en verdwenen ze op 1× in het masker. Daarom nu **gouden irissen** met een zwarte pupil naar voren (links), een witte glans linksboven en een donkergouden rand onderaan. Goud op zwart springt eruit op 1× en past bij Dark (vgl. Umbreon, Poochyena). Het verre oog is versmald (4 breed), het nabije oog is 5×6.
- **Staart:** bijzaak. Rechtop zoals bij een coati, licht gebogen, drie donkere ringen.
- **Kleuren:** bruin (4 tinten + zwart), room (3), ivoor (3), goud (2), wit. Drie hoofdkleuren: donkerbruin, room en ivoor; goud alleen in de ogen.
- **Frame 2:** kop, poot, klauwen, achterarm en staart 1 px omhoog (ademhaling); lijf en voeten blijven staan.

## Checklist SPRITING.md
- [x] Alles met de hand per pixel (tekstrasters per lichaamsdeel); geen vormfuncties, geen automatische schaduw of omlijning. Alleen de wegwerpschetsen zijn met ellipsen gemaakt.
- [x] Per lichaamsdeel opgebouwd en gladgestreken (kop, lijf, voorste poot, klauwen, achterarm, voeten, staart).
- [x] 3/4-pose naar links, licht van linksboven; de oren, ogen en voeten verschillen links en rechts in vorm (niets gespiegeld).
- [x] Curven: geen hoekjes in de schedel-, wang- en klauwcurven; de segmentlengtes lopen op of af. *Rest:* de rechterkant van de schedel is nog een rechte lijn van 8 px.
- [x] Omlijning per kleurgroep: zwart aan de schaduwkant (rechts, onder), de omlijningsbasis linksboven, room met een eigen lichtere rand, klauwen met de schaduwtint aan de lichte kant. Geen lichte pixels buiten de lijn.
- [~] Zwart-aandeel van de buitenrand: **0,64** (doel 0,35–0,6). Iets te hoog, want het lijf is overwegend schaduw; de bovenranden zijn al zoveel mogelijk omlijningsbruin.
- [x] Ogen: witte glans plus een gekleurde (gouden) reflectie/iris; ze staan logisch in het masker, het verre oog dicht bij de snoetbasis.
- [x] Slagschaduw van de kop op de borst in de schaduwtint; vachtgrens licht gekarteld.
- [x] 64×64 per frame, 2 frames, 16 kleuren, index 0 transparant.
- [~] Oppervlak: **1081 px** (frame 1), boven het doel van 750–900. Ter vergelijking: Treecko 967, Sneasel 948, Zigzagoon 1315. De eerste opzet was 1660 px en is op ¾ schaal opnieuw getekend; nog kleiner gaat ten koste van de ogen en de klauwen.

## Eigen oordeel
- Goed: het silhouet (snoet links, klauwen eronder, staart rechtop) is op 1× herkenbaar; de ogen zijn eindelijk sterk; hij is donker; de snoet en de klauwen dragen het ontwerp.
- Zwakker: het lijf is nog wat blokkig vergeleken met Teddiursa/Sandshrew (rechte flanken, weinig hooglicht); de klauwpunten mogen spitser; hij is iets groot.
