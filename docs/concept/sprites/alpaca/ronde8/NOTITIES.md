# Alpaca fase 1, ronde 8: van nul af aan

Schone lei: geen oude alpaca-sprites of -modeltekeningen bekeken. Wel gelezen: `SPRITING.md`, de Dragonfly Cave-gids (Scratch Sprites, Shading, Textures, Outline Shading), `FAKEMON_DESIGN.md`, de referentie-README, FEEDBACK.md (ronde 7 en de conceptronde) en als niveau-maatstaf Cuyby ronde 3. Echte Gen 3 op pixelniveau bekeken: Mareep, Eevee, Skitty, Ponyta, Growlithe, Makuhita, Hitmonchan, Swablu, Teddiursa.

## Schetsen (`schetsen.png`, bron `bron/schetsen.txt`)
- **A** staand op vier poten, kop groot linksvoor, beide wolvuisten op de grond. **Gekozen**: het meest baby-achtig en het blijft een viervoeter.
- **B** zittend met de vuisten in dekking: bokserig, maar minder viervoeter en de vuisten verbergen het lijf.
- **C** één vuist geheven (jab): dynamisch, maar oogt ouder/stoerder dan een fase 1.

## Ontwerpkeuzes
- **Vormen:** een ronde kop (±half van de hoogte, oren meegerekend meer), een wolpompon met drie bulten en pony-lokken over het voorhoofd, een wolwolk als lijf, twee grote rode wolvuisten met een crèmekleurige wolmanchet, twee korte achterpootjes met hoefjes. Geen staart, geen andere details.
- **Kleuren (3 groepen):** crème wol, lichtbruin (gezicht, oren, poten) en rood-oranje vuisten; roze alleen in de oren en een wangvlekje. Elke groep: hooglicht, basis, schaduw en een eigen donkere omlijning. 16 kleuren, index 0 transparant.
- **Ogen:** grote kraalogen zoals Eevee, op de helft van het zichtbare gezicht. Het rechteroog is 4×6, het linker 3×6 (3/4-pose, dus verkort), allebei met een witte glans linksboven en een blauwgrijze reflectie rechtsonder. Mondje: een klein 'v'-tje links onder het midden. Geen neus.
- **Vuisten:** gladde bollen (Makuhita/Hitmonchan) met een sikkelvormig hooglicht linksboven, één glanspixel, schaduw rechtsonder en een duimvouw op de voorste vuist. De wolmanchet hangt met lokjes over de bovenrand, zodat de vuist uit de wol lijkt te groeien.
- **Fluffy:** bultige omtrek van pompon, borst en lijf, krulnaden waar de bulten elkaar raken, en een gekartelde schaduwgrens op het lijf.
- **Frame 2:** kop, pompon en oren 1 pixel omlaag (ademen/knikje).

## Werkwijze
Elk lichaamsdeel is met de hand als tekstraster getekend (`bron/delen.txt`, van achter naar voor). `bron/bouw.py` legt de delen alleen over elkaar en schrijft de png/het palet weg: geen vormfuncties, geen automatische schaduw of omlijning. `bron/raster_f1.txt` en `raster_f2.txt` zijn het samengevoegde eindresultaat. `bron/vergelijk.py` maakt `schetsen.png` en `compare.png`.

## Checklist SPRITING.md
- [x] Met de hand, per lichaamsdeel; geen ellipsen of scripts voor vormen of schaduw.
- [x] 3/4-pose naar links, licht linksboven; schaduw rechtsonder en onder de kin (slagschaduw volledig in de schaduwtint).
- [x] Geen gespiegelde delen: oren, ogen en vuisten zijn elk anders getekend.
- [x] Omlijning per kleurgroep: zwart aan de schaduwkant, de omlijningstint van de groep aan de lichte kant, de schaduwtint als lichte omlijning op de bovenste wolbulten. Zwart-aandeel van de rand: **0,53** (doel 0,35–0,6).
- [x] Anti-aliasing alleen binnen de lijn; 1 pixel brede omlijning.
- [x] Ogen met witte glans en gekleurde reflectie.
- [x] Vacht/wol: gekartelde schaduwgrens, niet overdreven.
- [x] 64×64, anim_front 64×128 met een subtiel tweede frame, 16 kleuren, index 0 transparant.
- [ ] **Oppervlak 1130 px**: boven het doel van ±750–900 (Mareep 893, Eevee 748, maar Growlithe 1088, Makuhita 1142). Dat komt door de grote kop met oren en pompon. Kleiner kan door het lijf 2–3 kolommen in te korten.
- [~] Curven: de grote vormen zijn rond, maar de wangen hebben lange rechte stukken (x14 en x34).

## Eigen oordeel
Leest op 1× als een schattige baby-alpaca met rode vuisten en past qua stijl en grootte tussen Mareep/Eevee/Torchic. Zwakke punten: de vuisten kunnen op 1× ook als rode laarsjes gelezen worden (de duimvouw helpt een beetje). Een geheven vuist (schets C) maakt het bokskenmerk duidelijker, maar oogt minder baby. Verder is de pompon wat breed, zodat hij iets van een mutsje heeft, en het lijf zou fluffier kunnen met diepere bulten onderaan.
