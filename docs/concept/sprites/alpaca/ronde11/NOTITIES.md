# Alpaca fase 1, ronde 11: herstart from scratch

Jordi na ronde 10: "Het formaat is te groot en het is gewoon nog steeds geen alpaca, het gezicht klopt niet. Kijk goed naar een alpaca foto, alles is in 1 vacht kleur, waarom maak je het gezicht en de poten anders?" Ronde 11 begint daarom opnieuw vanaf de foto. Er zijn geen rasters of vormen uit eerdere rondes overgenomen. De enige uitzondering zijn de bokshandschoenen: die zijn op Jordi's verzoek als basisvorm hergebruikt, verkleind van 11 naar 9 px breed, en ze hebben een geweven manchet gekregen. Ronde 10 is alleen bekeken om te zien wat niet werkte: een bruin Eevee-gezicht, poten in een andere kleur, een kop die te groot was en een oppervlak van 1248 px.

## Wat een alpaca een alpaca maakt (foto `referentie_alpaca.webp`)
- **Eén vachtkleur overal.** Kop, nek, lijf en poten hebben dezelfde kleur; je ziet alleen schaduwtinten. Er is geen crème gezicht en er zijn geen andersgekleurde poten. Dat was de grootste fout van ronde 9–10.
- **Kop en nek:** een kleine kop op een lange, rechtopstaande nek. De nek is ongeveer even lang als de kop en dik van de wol. Het lijf is kort en tonvormig, de poten zijn dun en vrij lang.
- **Korte, stompe snuit.** Hij steekt iets naar voren en omlaag uit. Vooraan zitten een donkere neus en een gespleten bovenlip: een Y- of λ-vorm van de neusgaten naar de mond.
- **Ogen:** groot, vrijwel zwart, hoog en opzij op de kop, net onder de franje.
- **Oren:** lang en speervormig, in een V schuin omhoog en naar buiten.
- **Wolpompon** op de kruin. De franje hangt tot net boven de ogen, waardoor de kop bovenaan rond en hobbelig is.
- **Staart:** een kort pluimpje, iets omhoog gedragen.

## Silhouetschetsen (`schetsen.png`)
- **A rechtop (gekozen):** een verticale nek, de kop met pompon erop, een klein lijf en dunne poten. Bij de knijp-je-ogen-test leest deze schets het meest als alpaca.
- **B chibi:** de grote kop slokt de nek op. Dat is de valkuil van ronde 9 (schaap).
- **C nek vooruit:** leest als lama of geit.

## Keuzes
- **Kleuren:** één vachtkleur, warm crème (`w`), met 2 schaduwtinten (`v`, `u`), hooglicht `W` en een bruine omlijning `V`. Daarnaast alleen rood voor de handschoenen (4 tinten) en een weefband in Andeskleuren (magenta, geel, turquoise, met roze als hooglicht). Roze komt ook terug in het oor. De vacht verzint verder niets.
- **Manchet (verzoek van Jordi):** een gebreide band zoals bij een chullo of aguayo, met twee magenta strepen en daartussen een rij geel/turquoise-ruitjes. Op 1× lees je een bontgekleurde rand boven de handschoen. De verre manchet heeft één streep minder.
- **Pokémonificatie:** de kop en de ogen zijn iets groter dan echt, en de vorm is vereenvoudigd tot kop, nek, lijf en vier dunne poten. Er is geen kleur of onderdeel bijgekomen dat een alpaca niet heeft, behalve de handschoenen.
- **Pose 3/4 naar links-voor:** beide ogen zijn zichtbaar en het verre oog is smaller (2×4, met de wang ernaast). De snuit wijst linksvoor. De dichtbije voorpoot staat schuin naar voren, zoals bij een bokser in stelling. De voeten staan op verschillende hoogte voor diepte: dichtbije handschoen y52, verre handschoen y49, achterpoten y49 en y46. De achterpoten hebben een hak.
- **Frame 2:** kop, pompon en oren zakken 1 px (een knikje). De rest blijft staan.

## Cijfers
- **Oppervlak 869 px.** Ronde 10 had 1248. Ter vergelijking: Torchic 782, Mudkip 852, Mareep 893, Treecko 967. De eerste opzet was 1030 px en is ingekort met een smallere nek (9–10 px), een korter lijf, kortere achterpoten en een smallere kop.
- **Zwart-aandeel rand 0,49.** Het doel was 0,35–0,6.
- 16 kleuren, index 0 transparant. `anim_front.png` is 64×128.

## Checklist (§0)
1. **Lijf én blik diagonaal:** deels gelukt. De kop staat duidelijk 3/4 (twee ogen, snuit linksvoor). Het lijf toont de borst vooraan, en de voeten op verschillende hoogte en de verre poten die rechts uitsteken geven diepte. De romp zelf is nog vrij zijwaarts.
2. **Ledematen, oren en ogen geteld en verbonden:** 4 poten (2 handschoenen, 2 achterpoten), 2 oren, 2 ogen, neus en mond, en een staartje. Er zijn geen open randen; `bouw11.py` meldt niets.
3. **Geen rechte lijnen in een ronde omtrek:** de rechte stukken die overblijven zitten in de nek (7 px, een zuil), de schenen en de onderkanten van de handschoenen en voeten (die staan op de grond). De achterkant van de kop is rond gemaakt (segmenten 1-1-4-2-2-1-1).
4. **Ogen geïntegreerd, verre oog geen kopie:** het dichtbije oog is 3×4 met een glanspunt linksboven, een blauwe reflectie rechtsonder en een zachte hoek linksboven. Het verre oog is 2×4 en anders gevormd. De franjepunten zitten tussen de ogen en niet erboven, want erboven lazen ze als een boze wenkbrauw.
5. **Silhouet leest op 1× als de soort:** blinde check (zie hieronder).
6. **Formaat vergeleken met dezelfde fase:** zie Cijfers.
7. **Pose niet stijf:** de schuine voorpoot, de gespreide stand en de hakken helpen. Het blijft wel een vrij rustige houding.

## Blinde check (eigen oordeel)
Ik heb de sprite op 1× tussen Mareep, Ponyta, Torchic, Girafarig, Mudkip en Makuhita gezet, op een groene achtergrond. Zou iemand zonder context "alpaca" zeggen? **Ja, of "lama".** Wat dat oordeel draagt:
- de lange witte nek met een kleine kop;
- de V van de speeroren;
- de korte snuit;
- de crème kleur overal.

Hij oogt daar niet als een schaap of als een Eevee-kop. Zwakke punten:
- de pompon is op 1× meer een hobbelige kruin dan een duidelijke bol;
- de romp is nog vrij zijwaarts;
- crème op een lichte achtergrond heeft minder contrast dan de felle starters.

## Bestanden
- `anim_front.png`, `normal.pal`, `schetsen.png`
- `compare.png`: de foto, ronde 10, ronde 11 (frame 1 en 2), Torchic, Mudkip en Mudbray, op 1× en 3×
- `bron/delen.txt`: de handgetekende rijen per deel, van achter naar voor. De kop is één blok met een vaste x0.
- `bron/palet.txt` en `bron/bouw11.py`: samenvoegen en controleren (oppervlak, zwart-aandeel, open randen, rechte stukken). Gebruik `python3 bouw11.py docs/concept/sprites/alpaca/ronde11 [preview.png]`.
- `bron/schetsen.py`, `bron/vergelijk11.py` (met een optioneel blind-checkvel), `bron/raster_f1.txt` en `bron/raster_f2.txt`
