# Alpaca fase 1, ronde 12: zwarte ogen, Pokémon-shading, wolvuisten

Jordi na ronde 11: "Echt veel beter." Vorm, silhouet, formaat en de handschoenen met gebreide manchet blijven. Te doen waren: echt zwarte ogen, shading en kleuren meer zoals Gen 3, contrast op een lichte achtergrond en een ronder pompon. Daarna kwam er nog een verzoek bij: "maak het ook nog iets meer een Pokémon in plaats van een alpaca met bokshandschoenen."

Alles is opnieuw met de hand als tekstrijen getekend (`bron/delen.txt`). Er zijn geen vormfuncties en geen automatische schaduw of omlijning gebruikt.

## Referentiekleuren (gemeten uit de repo-sprites, frame 1; luma = 0,3R+0,59G+0,11B)
| Sprite | Hooglicht | Basis | Schaduw | Diepe schaduw / omlijningsbasis | Wat het leert |
|---|---|---|---|---|---|
| Altaria (wolk) | 248,248,248 | 200,200,224 | 152,152,192 | 112,112,152 · 72,96,144 | Wit is alleen hooglicht. De basis is al lavendel en de omlijning paarsblauw, zwart alleen onderaan. |
| Swablu | 248,248,248 | 200,200,224 | 152,152,192 | 128,128,144 · 88,88,112 | Hetzelfde recept in klein formaat. |
| Zangoose | 255,255,255 | 205,222,246 | 172,180,205 | 139,156,205 · 90,98,98 | Witte vacht met een koelblauwe basis en een grijze omlijning in plaats van zwart. |
| Absol | 255,255,255 | 213,222,238 | 180,180,213 | 139,139,172 · 98,98,131 | Wit dat via lila naar grijspaars loopt, met 4 duidelijke stappen. |
| Togetic | 255,255,255 | 213,238,238 | 172,197,189 | 115,123,131 | Koel groengrijs. |
| Mareep (wol) | 255,255,189 | 238,205,115 | 205,156,82 | 156,98,32 | Warm: crème verschuift naar oker en bruin en wordt verzadigder. |
| Ampharos | 255,255,255 | 230,230,230 | 172,172,172 | 90,90,90 | Neutraal grijs, het enige "alleen donkerder"-voorbeeld. |
| Ponyta | 255,238,205 | 230,205,139 | 197,156,106 | 139,82,49 | Warm crème naar karamel. |
| Whismur | 240,200,240 | 232,168,224 | 208,128,200 | 168,80,160 · 128,64,104 | Roze naar paars. |
| Smoochum (crème) | 248,248,248 | 240,224,168 | 216,192,128 | 136,128,72 | Crème naar olijf. |
| Cuyby-evolutie r2 (wit) | 255,255,246 | 246,238,214 | 214,198,166 | 106,98,115 · 49,41,57 | Jordi's favoriet: een warme witte vacht met een **koele paarsgrijze** omlijning. Het stro (255,238,168, 238,204,108, 208,154,72, 182,108,40, 140,84,26) verschuift naar roest. |

**Conclusie:**
- Bij een witte of crème vacht wordt de schaduw nooit gewoon "donkerder beige". De tint verschuift: koel naar lavendel of blauw (Altaria, Zangoose, Absol) of warm naar een verzadigder tint (Mareep, Ponyta).
- Er zijn 4 stappen met een luma-afstand van ongeveer 40–50 per stap.
- De omlijning zit in de donkerste tint van de groep. Zwart komt alleen aan de schaduwkant.

Ronde 11 deed precies wat niet hoort: 243,233,212, dan 214,190,156, dan 172,142,112, dan 132,104,86. Dat is één bruintint die alleen donkerder wordt.

## Palet ronde 12
- **Vacht:** hooglicht W 255,250,236 (luma 251), basis w 242,224,192 (225), schaduw v **210,166,166 oudroze** (182), diepe schaduw u **152,108,136 mauve** (130), omlijning V **100,66,98 pruim** (82) en zwart K 40,22,40.
  - De tint schuift van crème via oudroze naar mauve en pruim, zoals de koele schaduw van de Cuyby-evolutie en Altaria.
  - Het roze sluit aan bij het oor, de magenta weefband en de rode vuisten, dus het palet is één geheel.
- **Vuist:** R 255,140,120, r 226,58,64, s 162,30,62 (schuift naar magenta) en S 96,22,50.
- **Weefband:** M, Y en T zoals in ronde 11. Daarnaast roze P en oogreflectie B 104,92,150.
- 16 kleuren, index 0 transparant.

## Keuzes
1. **Ogen echt zwart.**
   - Het nabije oog is 4×5 in zwart K, met een witte glanspixel linksboven en een paarsblauwe reflectie rechtsonder.
   - Het lid is het zwaarst aan de binnenkant bovenaan en geeft een vastberaden blik. Een buitenhoekpixel in V maakt het af.
   - Er staat een oudroze randje onder het oog, zodat het niet in de vacht opgaat.
   - Het verre oog is 3×4 zonder reflectie: smaller en geen kopie.
   - Op 1× staan het zwart en de glans meteen.
2. **Shading.**
   - Het licht komt van linksboven. De borst, de linkerkant van de nek, de kruin en de pompon krijgen veel hooglicht (R/S-stijl).
   - De rechterkant van de kop, de nek en de flank vallen in v, de buik en de achterkant in u. De vlakken zijn helder, zonder dithering.
   - Onder de kin valt een slagschaduw op de nek (u). De pompon werpt een schaduw op de kruin rechts.
   - De omlijning is pruim (V) aan de belichte kant en zwart (K) alleen rechts en onderaan. Het zwart-aandeel is 0,49.
3. **Contrast op licht.** De pruimkleurige omlijning en de mauve schaduwtinten zijn donker genoeg om de figuur op wit en op de zandkleurige gevechtsgrond af te tekenen (zie `compare.png`). Ronde 11 ging daar op in.
4. **Pompon.** De pompon is een eigen wolbol (13×8) met een eigen omlijning en een u-onderrand op de kruin, plus één lok tussen de ogen. Hij leest nu als een bol en tegelijk als een kuif.
5. **Meer Pokémon, minder "alpaca met handschoenen":**
   - **Babystarter-verhoudingen:** de kop is groter ten opzichte van het lijf (kop ±25×19, lijf korter) en de nek is 1 rij korter. Zo lijkt hij meer op Torchic of Chimchar, maar de rechtopstaande nek en de V-oren houden hem alpaca.
   - **De vuisten groeien uit het wezen.** De nabije voorpoot komt uit een **wolpluim** op de borst (dezelfde vacht, geen naad). Dan volgt de gebreide band (magenta, geel en turquoise), en daarna een matte wolbol zonder plastic glans, met een vouwlijn als duim of knokkel. De verre voorpoot loopt via een wolverdikking in de band en de vuist uit. De vuist hoort zo bij het lijf, zoals bij Makuhita en Pancham, en is geen aangetrokken handschoen.
   - **Fighting zit ook in de houding:** de nabije vuist is geheven, als dekking voor de borst. Hij staat op drie poten met het gewicht naar voren en heeft een vastberaden blik. De pompon leest als een kuif.
   - **Vereenvoudigd:** een stompe snuit van 1 px met een neus en een Y-mond, korte poten met een hak en een eenvoudig pluimstaartje.
6. **Pose.** De 3/4-houding van ronde 11 is gebleven. De borst staat als een voorvlak naar de kijker (een v-vouw scheidt borst en flank) en de flank wijkt naar rechts. Er is één bewuste wijziging: de nabije voorpoot is geheven in plaats van neergezet, op verzoek van de coördinator ("dichtbije vuist geheven"). Als Jordi de oude stand wil, kan de vuist terug naar de grond. De vorm van de wolvuist blijft dan hetzelfde.
7. **Frame 2:** kop, pompon en oren zakken 1 px (een knikje), zoals in ronde 11.

## Cijfers
- **Oppervlak 1013 px** (frame 2: 1002). Ronde 11 had 869. Ter vergelijking:
  - Treecko 967, Makuhita 1142, Mankey 872, Torchic 782, Chimchar 764.
- De groei komt van de grotere kop en de geheven vuist die vóór het lijf uitsteekt. In hoogte is hij kleiner dan ronde 11 (y4–y51).
- **Zwart-aandeel rand 0,49.**
- 16 kleuren. `anim_front.png` is 64×128.

## Checklist (§0)
1. **Lijf én blik diagonaal:** ok.
   - Beide ogen zijn zichtbaar en het verre oog is smaller. De snuit wijst linksvoor.
   - De borst vormt een voorvlak en de flank wijkt naar achteren.
   - De voeten staan op verschillende hoogte: verre achtervoet y47, verre vuist y50, nabije achtervoet y51.
2. **Ledematen, oren en ogen geteld en verbonden:** ok.
   - Er zijn 4 poten: de nabije vuist geheven, de verre vuist op de grond en 2 achterpoten.
   - Verder 2 oren, 2 ogen, neus en mond, pompon en staart.
   - `bouw12.py` meldt geen open randen.
3. **Geen rechte lijnen in een ronde omtrek:** grotendeels ok. Wat overblijft zijn stukken van 5–8 px:
   - de voorkant van de nek (een zuil);
   - de schenen;
   - de onderkant van de voeten, die op de grond staan;
   - de bovenrand van de rug (6 px).
4. **Ogen geïntegreerd, verre oog geen kopie:** ok. De ogen zijn zwart met glans en reflectie, hebben een lid met karakter en een roze rand eronder.
5. **Silhouet leest op 1× als de soort:** ok volgens de knijp-je-ogen-test naast Altaria, Zangoose, Mareep en Makuhita. Wat het draagt:
   - de lange rechte nek met de kleine snuit;
   - de V-oren met de wolbol ertussen;
   - de crème vacht.

   Hij leest als een jonge alpaca of lama die boksend in de verdediging staat.
6. **Formaat vergeleken met dezelfde fase:** zie Cijfers. Hij is iets groter dan Treecko en ronde 11. Als Jordi het kleiner wil, zijn een kolom flank en de geheven vuist 2 px dichter op de borst de eerste kandidaten.
7. **Pose niet stijf:** ok. De geheven vuist, de stand op drie poten, de hakken in de achterpoten en het knikje in frame 2 zorgen daarvoor.

## Bestanden
- `anim_front.png` en `normal.pal`.
- `compare.png`: ronde 11, ronde 12 (frame 1 en 2), Altaria, Zangoose, Mareep en Makuhita, op wit, op de gevechtsgrond en op donker, telkens op 1× en 3×.
- `bron/delen.txt` bevat de tekenrijen per deel. `@ dx dy` verschuift de hele figuur.
- `bron/palet.txt`, `bron/bouw12.py` en `bron/vergelijk12.py`. Gebruik:
  - `python3 docs/concept/sprites/alpaca/ronde12/bron/bouw12.py docs/concept/sprites/alpaca/ronde12 [preview.png]`
  - `python3 docs/concept/sprites/alpaca/ronde12/bron/vergelijk12.py`
