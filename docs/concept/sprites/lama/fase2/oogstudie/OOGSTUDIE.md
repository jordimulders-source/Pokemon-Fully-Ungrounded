# Oogstudie: een droog lama-oog (3 nov)

Jordi: "ik wil een beter oog, geen zwart rondje met een wit puntje erin. Kijk welke andere pokemon nog meer een droog zwart oog hebben, maar wat er toch goed uitkomt."

Alleen analyse; er is niets aan de lama getekend.

## Bestanden
- `oogstudie.png`:
  - rij 1–2: per voorbeeld de hele sprite op 2× (rood kader = uitsnede) en het oog op 10× met een pixelraster. Daarnaast de twee huidige lama-ogen op 10×.
  - rij 3: recept A en B op 10×, 3× en 1×, in het lamapalet.
- `vel.py`: bouwt het vel. Draai het vanuit de repo-root.

Bron: `graphics/pokemon/<naam>/anim_front.png` (frame 1) met `normal.pal`. Coördinaten zijn (x,y) op het 64×64-frame.

## Bekeken
Ongeveer 60 soorten uit nr. 1–386: de 36 uit de opdracht, plus Tropius, Lapras, Doduo/Dodrio, Drowzee/Hypno, Slowking, Seel/Dewgong, Kangaskhan, Rhyhorn, Houndoom, Mightyena, Linoone/Zigzagoon, Manectric, Absol, de legendarische honden, Ninetales, Arcanine, Cubone/Marowak, Dunsparce, Farfetch'd, Psyduck, Phanpy/Donphan, Houndour en Furret.

Afgevallen:
- **Gesloten of streepogen** (Snorlax, Torkoal, Wobbuffet, Wynaut, Drowzee, Slakoth): geen donker oog.
- **Kraal- of stipogen** (Quagsire, Wooper, Whiscash, Barboach, Spoink): precies het "zwarte rondje".
- **Boze of felle ogen** (Tauros, Zangoose, Houndoom, Absol, Mightyena).
- **Te druk** (Slaking, Spinda): ogen met wallen of spiralen.
- **Ponyta:** 3×3 zwart met een wit middenpuntje. Dat is precies wat we níet willen.

Belangrijkste vondst: in Gen 3 is een oog bij een 3/4-viervoeter maar **3–5 px breed**. "Droog" zit dan niet in details, maar in drie dingen:
1. de **bovenrand is recht** (een lid), niet rond;
2. de **pupil zit tegen dat lid aan**;
3. het **lichte deel zit onder of vóór de pupil**, niet als sterretje bovenin.

## De 8 voorbeelden

### 1. Camerupt: zwaar lid, wit onder (beste voorbeeld)
Uitsnede (13,35)–(24,44). Een viervoeter met een lange snuit in 3/4, één oog in beeld: dezelfde situatie als de lama.
- **Bovenlid:** een dik vlak in donkerrood `702838` (de donkerste huidkleur, géén zwart), 2 rijen hoog op (15–17,38–39) en (20,38). Het lid hangt als een zware huidplooi over het oog en is aan de voorkant dikker.
- **Pupil:** 3 px zwart `181818` op (19,39), (18–19,40), direct onder het lid. Er zit geen oogwit boven de pupil, dus hij is half geloken.
- **Wit:**
  - één glanspixel vóór-boven (18,39), half onder het lid;
  - verder een rij oogwit **ónder** de pupil: (20,40) en (18–20,41), met een staartje op (19,42).
  - De randen van het wit zijn grijs (`b8b0b8`/`909090`), dus zacht.
- **Onderrand:** grijsbruin `685850` (17,42), (20,42), geen zwarte lijn.
- **Wimpers:** geen.
- **Waarom het droog leest:** het wit onder de pupil geeft de blik van iemand die onder zware oogleden voor zich uit kijkt, zonder focus en zonder emotie. Toch leeft het oog: er is één echte glanspixel en het wit is fris.

### 2. Farfetch'd: plat zwart lid, donkerbruin lidvlak (beste voorbeeld)
Uitsnede (21,20)–(31,29). Het smalende, half geloken kijken.
- **Bovenlid:** een **rechte zwarte lijn** `101010` van 3 px op (27–29,23). Naar achteren loopt hij 1 px per rij omhoog door naar (30,22) en (31,21). Die doorloop werkt als een wimper of plooi naar de slaap.
- **Lidvlak:** het bovenste deel van het oog is donkerbruin `5a3900`: (26,21–22), (27,22), (26–27,24). Dat is het ooglid dat over de iris valt.
- **Pupil:** zwart op (28,24) en (26,25), dus net onder het lid.
- **Wit:** alleen **vóór-onder**, als een sikkel van 4 px: (25,25), (25–26,26), (25,27).
- **Glans:** geen aparte; het wit is de glans.
- **Onderrand en voorkant:** een donkerbruine lijn (x23), met lichtbruin `b49452`/`d8b870` ernaast. Er zit geen zwarte rand rondom.
- **Waarom het droog leest:** de rechte zwarte lidlijn en het bruine lidvlak maken het oog half dicht. Het wit laag vóór zegt dat het dier wel kijkt, maar zonder moeite. Dit is het "ik zie de wereld aan me voorbij gaan" in 6×5 px.

### 3. Numel: bruin oog, glans als streepje
Uitsnede (20,22)–(30,32). Een dommige, rustige viervoeter.
- **Oog:** een staande ovaal in **middenbruin** `706050`, niet zwart, ±3 breed en 6–8 hoog op x24–27. Alleen de voorrand (x24) is zwart `181818`.
- **Glans:** een **verticale streep** wit `f8f8f8` van 3 px op (25,26–28), die onderaan 2 px breed wordt (24–25,28). Eronder volgt lichtgrijs `d0c8d8` op (25,29).
- **Bovenlid en wimpers:** geen apart lid; de bovenkant van het bruine vlak gaat zacht over in de kop.
- **Waarom het droog leest:** door de bruine iris in plaats van zwart is het contrast laag; het oog is mat, niet glimmend. De glans ligt laag en is een streepje, geen sterretje, en leest als vocht op een loom oog. Het oog blijft leesbaar door de zwarte voorrand.

### 4. Slowpoke: lege blik met een minipupil
Uitsnede (20,27)–(31,38). Hét Pokémon-voorbeeld van "de wereld gaat aan me voorbij".
- **Bovenlid:** een **rechte lijn** van 4 px in donkerroze `de627b` op (23–26,29). Dat is de schaduwkleur van de huid, geen zwart.
- **Oog:** een groot wit ovaal `ffffff` van ±6×6 op x22–28, y30–36, met grijze randpixels `d5cdcd` op de hoeken.
- **Pupil:** **één pixel zwart** op (25,32), net boven het midden en zonder glans.
- **Onderrand:** huidbruin `dea462`/`eec58b`, geen lijn.
- **Waarom het droog leest:** de pupil is zo klein dat er geen focus is; Slowpoke kijkt nergens naar.
- **Bruikbaar voor de lama:** het principe "geen gerichte pupil, geen glans" en de lidlijn in een huidkleur. Het witte oog zelf past niet bij een lama.

### 5. Lapras: lange hals, bruine pupil laag in het oog
Uitsnede (14,10)–(24,19). Lange hals, kop in 3/4, één oog: lijkt qua bouw op de lama.
- **Bovenlid en voorkant:** een **schuine zwarte lijn** `000000` van (19–20,12) naar (16–17,16): het lid loopt van achter-boven naar voor-onder. Erboven ligt lichtblauw `73c5f6` als glimmende wenkbrauwboog (16–18,12–13).
- **Oog:** gebroken wit `f6eee6` op (19–20,13), (18,14), (20,14).
- **Pupil:** **donkerbruin** `5a4a41` op (19,14) en (18,15), met maar 1 px zwart op (19,15). De pupil zit **laag**, tegen de onderrand.
- **Onderrand:** grijs `a49494` (20,15), daaronder de kop. Geen zwarte onderlijn.
- **Waarom het droog leest:** door de bruine, laag liggende pupil kijkt Lapras rustig en een beetje weemoedig omlaag, zonder sterretje. Het licht zit in de wenkbrauw boven het oog, niet in het oog zelf.

### 6. Tropius: lange hals, blad als zwaar lid
Uitsnede (6,6)–(16,15). Een grazer met een lange hals.
- **Bovenlid:** het **blad** (donkergroen `206020`) hangt direct over het oog. Het oog heeft daardoor een rechte, zware bovenkant: y9–10.
- **Oog:** een zwart blok `101010` van ±2–3 px op (11–12,10), (12,11), (13,12), met een donkerbruine oogkas `503830`/`785848` eromheen.
- **Glans:** 2 losse witte pixels `f8f8f8` op (13,10) en (11,11), allebei half tegen de rand.
- **Waarom het droog leest:** de schaduw van wat erboven hangt (het blad, of bij de lama de vacht van de kuif of het voorhoofd) maakt elk oog zwaar en loom. De oogkas in donkerbruin zorgt dat het geen los kraaltje is.

### 7. Girafarig: smal oog met een lidhoek naar de slaap
Uitsnede (15,10)–(25,19). Een viervoeter met een lange hals, kop in 3/4 op een witte snuit.
- **Bovenlid:** een donkerbruine lijn `483838` die **schuin naar achter-boven** loopt: (20–21,12), (21–22,13). Achteraan wordt hij een puntje, als een wimper of ooghoek.
- **Oog:** een smal zwart vlak `101010`, ±2 breed, dat van (19,14) naar (18–19,17) naar voor-onder zakt. Er zit één pixel donkerblauw `404870` in als iris (20,14).
- **Wit:** het witte gezicht zelf aan de voorkant (19,15) en achter (21,14–16). Er is geen aparte glans.
- **Waarom het droog leest:** het oog is smal en schuin, met een lidpunt naar achteren. Het kijkt dromerig en onbewogen. Het lid zakt naar áchteren, niet naar de snuit; daardoor is het niet boos.

### 8. Rapidash: bruine lidlijn, minioog
Uitsnede (8,13)–(18,22). Paard in 3/4, lange snuit.
- **Bovenlid:** in **bruin** `8b5231`, niet zwart, schuin op (14,16), (13,17), (13,18).
- **Oog:**
  - pupil: 1 px zwart (12,18);
  - wit: 1 px `ffffff` (14,18), áchter de pupil;
  - lichtgrijs `c5c5c5` (14,17).
- **Onderrand en onderwimpers:** 2 px rood `de1010` op (12–13,19), in de kleur van de manen.
- **Waarom het droog leest:** de bruine lidlijn is zachter dan zwart en het oog is amandelvormig, rustig en voornaam. Het is een kleiner oog dan de lama nodig heeft. Wel bruikbaar: een **gekleurde onderwimper** in plaats van een zwarte lijn.

## De huidige lama-ogen (waarom ze niet werken)
- **kleur/ronde3** (17–19,13–16):
  - een zwart blok van 3×3–4 `2a161a`;
  - een witte pixel `faf6ec` **bovenin het midden** (18,14);
  - een blauwe reflex `4c5ca8` onderaan achter (19,16);
  - donkerbruin `6c3a20` eromheen.

  Het oog is rond, de pupil vult alles en het witte puntje zit waar een "sterretje" hoort. Zo kijkt een knuffel: wakker, glanzend, vriendelijk.
- **silhouet/variant_jonger2** (15–19,14–18):
  - zwart van 4×4;
  - wit (16,16) in het midden;
  - blauw (19,17);
  - een rij donkerbruin `6c3a20` (16–18,14) **boven** het zwart.

  Die bruine rij ligt bóven het oog en leest als een wenkbrauw, niet als een lid over de iris. Het zwart is nog steeds rond en vol.
- Bij beide is het **boven- en onderkant even rond**, staat de **glans in het midden of bovenin** en is de **iris puur zwart**. Dat zijn alle drie de dingen die de voorbeelden hierboven anders doen.

## Recept: een droog lama-oog
Voor een 3/4-kop met één oog in beeld, snuit naar **links** en licht van linksboven. Oog ±5 px breed (lid) en 3 rijen hoog (lid plus 2 rijen iris), met een wimper erboven.

### De regels
1. **Rechte bovenkant.** Het bovenlid is een **rechte horizontale lijn** van 5 px in `1` (de omlijningskleur). Hij hangt niet naar de snuit, want dat leest boos. Hij mag hooguit achteraan 1 px doorlopen of omhoog als plooi of wimper (Farfetch'd, Girafarig).
2. **Pupil tegen het lid.** Direct onder het lid begint de iris. Er zit geen glans, wit of ruimte tussen lid en pupil. Daardoor is het oog half dicht (Camerupt, Farfetch'd).
3. **Iris in donkerbruin of grijsbruin, niet alles zwart.** Gebruik `2` (6c3a20) of `a` (4a3c40), met hooguit 2 px `1` als pupil. Het oog wordt dan mat in plaats van glimmend (Numel, Lapras). Een lama heeft een liggende, ovale pupil; 2 px naast elkaar is daar een knipoog naar.
4. **Licht laag en vóór, klein en niet stralend.** Hooguit 1 px, onderaan aan de snuitkant (Farfetch'd, Camerupt). Gebruik crème `6` in plaats van wit `f` (variant A), of helemaal geen wit, alleen een warme reflex `4` (variant B).
5. **Geen zwarte onderrand.** De onderkant gaat over in vachtschaduw `3` (Camerupt, Slowpoke, Lapras). Een zwarte ring rondom maakt er weer een kraal van.
6. **Zwaarte van boven.** Een rij vachtschaduw `4` boven het lid (oogkas of voorhoofd) maakt het oog zwaar, zoals het blad bij Tropius en de rode wenkbrauw bij Camerupt.
7. **Wimpers.** 1–2 px in `1`, vanaf het **achterste** eind van het lid schuin omhoog naar achter. Niet aan de voorkant (dat wordt "make-up") en niet meer dan 2 px.

### Variant A: "zwaar lid" (Camerupt + Farfetch'd)
```
     0 1 2 3 4 5 6
r0   5 5 5 5 5 5 1     wimperpunt
r1   5 4 4 4 4 1 5     oogkas-schaduw 4, wimperaanzet 1
r2   5 1 1 1 1 1 5     bovenlid: rechte lijn van 5 px
r3   5 2 a 1 1 2 4     iris direct onder het lid, liggende pupil van 2 px
r4   5 6 a a 2 4 5     crème lichtje vóór-onder, iris loopt naar achter in bruin uit
r5   5 5 3 3 4 5 5     onderrand: vachtschaduw, geen lijn
```
Het oog is donker en groot, maar half dicht, en het lichtje zit laag. De lama kijkt traag en net niet geïnteresseerd langs je heen. Dit is de veiligste keus: het leeft nog duidelijk.

### Variant B: "leeg bruin" (Numel + Lapras + Slowpoke)
```
     0 1 2 3 4 5 6
r0   5 5 5 5 5 1 5     wimper
r1   5 1 1 1 1 1 2     bovenlid van 5 px, achteraan doorgetrokken in 2 (lidplooi naar de slaap)
r2   5 2 2 1 1 2 4     bruine iris, liggende pupil van 2 px tegen het lid
r3   5 4 2 2 2 3 5     warme reflex 4 vóór-onder (geen wit), iris, overgang 3
r4   5 5 3 3 3 5 5     onderrand: vachtschaduw
r5   5 5 5 5 5 5 5
```
Er zit nergens wit in. Het oog is mat bruin onder een zwart lid en daardoor het droogst. Het risico is dat het op 1× dof of "dood" leest. De terugvaloptie is dan 1 px `6` op r3 kolom 1, in plaats van de `4`.

Legenda (palet van `kleur/ronde3/normal.pal`):

| Teken | Kleur | Betekenis |
|---|---|---|
| `1` | 2a161a | omlijning, lid, pupil |
| `2` | 6c3a20 | donkerbruin, iris |
| `a` | 4a3c40 | grijsbruine iris |
| `3` | a8683a | vachtschaduw |
| `4` | d69a52 | vacht midden |
| `5` | efc27a | vacht licht |
| `6` | f8e2a8 | crème lichtje |

Op het vel staan beide recepten in rij 3.

### Waar het recept op let
- **Niet slaperig:** het lid bedekt maximaal de helft. Er blijven 2 rijen iris zichtbaar, het oog is breder dan hoog (5×3) en heeft geen gesloten streep zoals Snorlax of Torkoal. De lidlijn blijft recht; een boog naar beneden leest als dommelen.
- **Niet ziek:**
  - geen roze, rood of paars rond het oog;
  - geen donkere wallen onder het oog (daarom is de onderrand vachtschaduw `3`, niet `2` of `1`);
  - geen doffe grijze iris over het hele oog.
- **Niet boos:**
  - het lid zakt niet naar de snuit toe;
  - er staat geen wenkbrauwpixel boven de voorhoek;
  - de pupil zit niet in de voorhoek geperst.

  Als het lid ergens zakt, dan naar áchteren (Girafarig), en hooguit 1 px.
- **Geen "zwart rondje met wit puntje":**
  - de bovenkant is recht, niet rond;
  - het licht zit laag vóór, nooit in het midden of bovenin;
  - de iris is (deels) bruin;
  - er zit geen zwarte ring rondom.
- **Controle:** bekijk het oog op 1× en 3× naast Camerupt en Farfetch'd uit `oogstudie.png`. Het moet op 1× nog als oog lezen; anders kies je A en niet B.

## Aanvulling: Slakoth-lijn (Jordi, 3 nov: "slakoth lijn heeft ook luie ogen")
Vel: `aanvulling_slakoth.png` (Slakoth en Vigoroth komen van upstream pokeemerald-expansion, ze staan niet meer in onze repo).
- **Slakoth:** klein donker oog met een wit lichtje onderin, in een grote donkerbruine **oogvlek die naar achteren-onder afhangt**. De luie blik komt niet van het oog zelf, maar van die hangende vlek (wallen) en het lid dat erop drukt.
- **Slaking:** het oog is bijna een lijn (lid helemaal neer), met een **wal-lijn** eronder in de schaduwtint van de vacht.
- **Voor de lama (recept C, "lui" = A + Slakoth):** recept A (rechte lidlijn, iris tegen het lid, licht laag vóór), maar de lidlijn **loopt achteraan 1 px omlaag** (hangt af), en onder het oog ligt een **zachte wal** van 1 rij in de schaduwtint van de vacht, die naar achteren uitloopt. Geen zwarte vlek (een lama heeft geen masker); het hangen moet uit de vorm komen, niet uit een donkere kleur.
