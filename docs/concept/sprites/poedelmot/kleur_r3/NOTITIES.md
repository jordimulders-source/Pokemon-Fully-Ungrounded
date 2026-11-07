# Poedelmot: kleur r3 (maker)

Jordi: "zo true to form als mogelijk" · "moet echt heel erg lijken op het model, anders is die niet goed" · "ga je werk heel kritisch keuren voordat je het als af bestempelt".
Ronde 2 is door beide keurders afgekeurd (`kleur_r2/poedelmot.png.keuring_gelijkenis.md`, `…keuring_stijl.md`). r3 is gebouwd vanaf r2; r2 is niet aangeraakt. De correctie van de coördinator: het verre oog volgt de bron (±4 px zwart, x16–19).

## Bestanden
- `raster.txt` (bron), `palet.py` → `poedelmot.png` (geïndexeerd, index 0 transparant) + `normal.pal` (JASC, 16, veelvouden van 8; 13–15 ongebruikt).
- `vel.py` → `vel.png`: r3 | r2 | bron op 8×, r3 op 1×/2× licht en donker, close-ups 12× (ogen/gezicht, sprieten, pootjes, vleugels) r3 naast de bron.
- `controle.py` → `controle_uitvoer.txt` (leest `spriet_zone.txt`, `klauw_rand.txt`).
- `stappen/`: `bouw.sh` met de lagen op r2 (`m_kleur` tinten, `k_kop3`, `k_vleugel3`, `k_onder3`, `k_spriet3`, opschonen, `k_fix3`, buitenlijn, `k_na`).

## Palet (helderheid)
Vacht: `A` wit warm 241 · `9` koel lila-grijs 212 · `8` koel diep 181 (stappen ±30, één koele schaduwgroep zoals Altaria/Swablu).
Vleugel/lijf warm: `7` crème 226 · `6` lichttan 190 · `5` tan 152. Lijnen: `1` zwart, `2` zwartbruin, `3` donkerbruin, `4` bruin (selout). `B` warm bruin (oogreflectie), `C` lichte crème (nerf).

## Wat er per keuringspunt is gedaan
1. **Volume in het wit**: `A`+`9` uit r2 zijn samengevoegd tot één wit. De schaduw is één koele groep, als sikkel rechtsonder per vorm: kop langs de vleugelvoetlijn, kraag rechtsonder, de verre vleugel onder de spriet, elke pluim rechtsonder. Slagschaduwen: van de kop op de vleugelvoet (`6` naast de lijn), onder de kin op de kraag (`9`, langs de glimlachboog) en van de sprietvoet op de kruin.
2. **Rechte lijnen**:
   - De zoom tussen de vleugels (was y36) is een golvende, geschulpte lijn met witte lobjes. De onderrand van de achtervleugel (was y46) ook.
   - De pootbovenkanten zijn ronde ovalen met slagschaduw in plaats van een donkere lijn.
   - Het achterlijf heeft twee korte gebogen ringen in plaats van verticale kolommen. De kraag hangt er met getande plukken overheen, dus er is geen rechte onderrand meer.
   - De mond is een glimlachboog (laagste punt x22–26, y43) die rechts oploopt naar de oogrand.
   - De wanglijnen x35 en x39–40 zijn vervangen door één schuine vleugelvoetlijn (37,30) → (41,47) met witte vacht ervoor. De band langs x59–61 is weg; daar staan nu lobboogjes per lob.
   - De rechte sprietbovenrand: zie punt 7.
3. **Ogen en kop**:
   - Ver oog: smal, staand ovaal, zwart x16–19, y33–39, glans 2 px op (17,34–35), reflectie warm bruin. Het streepje (10–12,36) is selout `4` geworden; de tanvlakjes ernaast zijn wit.
   - Nabij oog: tan ring rondom (ook onder en rechtsonder), ovale glans van 2×2 op (27–28,34–35), onderste helft warm bruin `B` in plaats van grijs.
   - Door het kleine verre oog en de schaduw rechts kijkt de kop nu driekwart naar links.
4. **Vacht**:
   - Kruin: witte plukjes met schaduwstreepjes tussen de sprietvoeten.
   - Kraag en linkerrand: korte plukstreepjes van 3 px; de kraag hangt getand over het achterlijf.
   - Verre vleugel: wit, de tan band (9–18,29–31) is weg.
   - Grens: het silhouet is bevroren, dus de buitenrand zelf kan niet getand worden. Het pluizige komt alleen van binnenuit.
5. **Pootjes**:
   - Zes pluimen als hangende ovalen met lichte top linksboven en een koele sikkel rechtsonder.
   - Een contour alleen rechtsonder waar de pluim over iets anders valt, dus geen donkere ring. De achterste pluim krijgt een slagschaduw waar de voorste ervoor hangt.
   - Klauwtjes klein en schuin, de verre hoger en donkerder. Achterlijf lichter (`7`/`6` met `5`-ringen).
6. **Vleugelpatroon**:
   - Geen letterkrullen meer.
   - Voorvleugel: twee grote gladde bogen rond de vleugelbasis en een witte buitenzone met lobboogjes.
   - Achtervleugel: twee schuine bogen, een tan basis en een witte bovenzoom met lobjes.
7. **Sprieten**:
   - Vlak zwart met een lichte nerf (`C`) als doorlopende curve.
   - Baarden als doorlopende schuine lichte streepjes om de 3 px (`6` bij de nerf, `5` verder weg), met een paar onderbrekingen.
   - Geen kammetjes boven de nerf: die gaven een dambordeffect.
   - De belichte bovenrand is donkerbruin `3` in plaats van zwart, de tips zijn bruin `4`.
   - Donker-aandeel (1+2) van de hele sprite: **0,207** (was 0,268).

## Controle (`python3 controle.py`)
- **Alpha-diff met silhouet: 0** (1782 = 1782).
- Open randen: 0 (uitzondering: 4 klauwpixels en de rechtersprietpunt (52,18–19) in `4`).
- Selout `4`: 11 reeksen, geen afwisseling met donker binnen één rand.
- Losse pixels: 0. Tintclusters < 3 px: 0 (vlaktinten 5–9 en A; sprietzone en oogglans uitgezonderd).

## Hoofdvraag (zelf getoetst op 8× en 1× naast de bron)
- **Leest het als Jordi's ontwerp?** Beter dan r2: het witte, ronde donslijf, de driekwart-kop met één groot glazig oog en een smal ver oog, de glimlach, de donkere geveerde sprieten en de hangende pluimpootjes komen nu overeen. Op 1× herkenbaar als dezelfde poedelmot. Maar niet "heel erg lijkend":
  - **Vleugels**: Jordi's vleugels hebben een duidelijke, fijne tan schubtekening en een gerafelde witte rand. Hier zijn het grote vlakke crèmevlakken met zwakke bogen. Dit is het grootste resterende verschil.
  - **Vacht**: niet echt pluizig. Het silhouet ligt vast, dus de randen kunnen niet gerafeld worden; de plukjes binnenin zijn een benadering.
  - **Sprieten**: de baarden staan op 45° en om de 3 px; in de bron zijn ze steiler en fijner. Op 8× zie je nog een regelmatig patroon.
  - **Koele schaduw**: de lila-grijze schaduw (zoals de stijlkeurder vroeg) maakt de vacht koeler dan Jordi's warme crème-wit. Dat is een bewuste keuze tussen de twee keuringen.
- **Leest het als een Game Freak-sprite?** Deels. Omlijning, selout, ogen en de 3/4-compositie kloppen. Het grote vlakke vleugelvlak en de regelmatige sprietbaarden lezen eerder als machinaal dan als met de hand gezet.
- **Werkwijze eerlijk**: de schaduwsikkels, vleugelbogen, pluimovalen, sprietbaarden en opschoning zijn met kleine scripts op mijn eigen ontwerp gezet (vormen, middelpunten en pixellijsten met de hand gekozen op de bron) en daarna nagewerkt.
