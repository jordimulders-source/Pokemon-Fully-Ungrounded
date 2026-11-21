# Dundragoon (Dunsparce-evolutie, Dragon/Normal) frontsprite, ronde 1 (kandidaat)

Bestanden: `dundragoon_r1.png` (64×64, geïndexeerd, index 0 transparant, 12 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal 8× / close-ups 12× kop+oog+hoorns, vleugels, pootjes, boor naast het model / 1× op wit, crème, donker, zwart + model 1×), `bouw.py`.
Gereedschap (`../gereedschap/`, gekopieerd van Gloom en aangepast): `pitch.py` (rastermeting), `natief.py` (natief raster → `natief.png`), `klassen.py` (zwart/geel/blauw/vleugel per modelpixel), `gemeen.py` (schaal, palet, overlap), `vel.py`, `raster.py` (spriteraster over het model), `controle.py` (Gen 3-metingen), `zones.py` (afwijkingen per zone).
Bouwen: `cd dundragoon && python3 sprite_r1/bouw.py` (`kaal` als argument toont alleen de kale reductie).

## Metingen
- **Rasterpitch:** randsterkte per kolom/rij gaf één duidelijke kam op **10,24 px** (1024/100), x fase 9,25, y fase 9,20; visueel bevestigd op een uitvergroting van het oog (modelpixels ±10 px). Natief raster 99×99, figuur x5–90, y6–91 (**86×86**, 3568 px).
- **Schaal: 61/86 = 0,709** (1,41 natieve px per spritepixel). Figuur in de sprite **x1–61, y1–61 (61×61), 1791 px**. Niet gespiegeld (model kijkt al naar links), verhoudingen ongewijzigd.
- **Maatkeuze:** echte eindvormen: Dragonite 57×64 / 1997 px, Altaria 58×63 / 1778, Flygon 63×61 / 1836, Rayquaza 61×64 / 1839, Salamence 64×59 / 2446 (Dunsparce zelf 46×44 / 1008). Dundragoon 61×61 / 1791 px zit midden in die groep; verder vergroten kan niet (vak vol op de diagonaal), kleiner zou onder de grote draken vallen.

## Wat uit het model komt (kale reductie, `kaal.png`)
Oppervlakteweging per spritepixel over het natieve raster:
- achtergrond als < ½ pixel figuur;
- **zwart wint** vanaf 30 % oppervlak, daarna **olijflijn** (geel met L < 150: selout van de kop, overgang kop/kaak, boorlijnen) vanaf 30 %, daarna **blauw wint van vleugelwit** vanaf 30 % (aders en rand in de vleugels);
- anders de groep (geel/blauw/vleugel) met het grootste oppervlak, tint naar de gemiddelde modelhelderheid (geel: drempels 150/200/228 zonder de olijflijnpixels; blauw 98/128; vleugel 185/221).
Silhouet, beide hoorns, beide vleugels met hun vingers en aders, oog met ooglijn, blauwe kaak met de golvende onderrand, blauwe rugbanden, blauwe buik, vier pootjes (voorpoot links, twee onder de buik, achterpoot bij de staart) en de boor komen allemaal uit deze reductie.

## Pixels die afwijken van de kale reductie: 257 px (silhouet-diff 0)
Per zone (`zones.py`): **kop+oog+hoorns 76, vleugels+hoorn rechts 34, lijf 88, pootjes 5, boor 54.** Per stap:
- **buitenlijn (73 px):** geen open of lichte rand; schaduwkant (achtergrond rechts/onder) zwart, lichtkant gekleurde selout van de groep (olijf / donkerblauw / vleugeldonker). Zwart uit het model blijft zwart.
- **ontkorrelen (77 px):** tintvlekjes < 3 px (lichtste tint < 2) nemen de buurtint van dezelfde groep aan; lijntinten niet.
- **losse zwarte pixel (1 px).**
- **oog (37 px), naar het model:** de reductie maakte de ring een mengsel van drie blauwtinten met gaten. Opnieuw uit het model gemeten: elke spritepixel met ≥ 45 % blauwe modeldekking in het oogvak is ring, tint donker waar de gemiddelde modelhelderheid < 112 is (zoals het model: donkere buitenrand links/rechts en donkere binnenrand onder), anders middenblauw. Blauwe restjes binnen het oogvak → geel. Ring 2 px breed, buitenmaat 12×11; ooglijn (olijf + 3 zwart, 1 zwart, 1 zwart, schuin omlaag) is de kale reductie, niet aangeraakt.
- **boor (51 px), kleur, géén vorm** (Jordi: "de drill ... met kleurgebruik oplossen"):
  - de spiraallijnen komen uit het model: elk 8-samenhangend olijfcluster in de natieve boor (4 lijnen; de selout langs de buitenrand telt niet) wordt punt voor punt naar de sprite gemapt en als 1-px lijn gezet (hoekpixels weg zolang de lijn samenhangend blijft). De reductie had ze in losse stukjes gebroken. De overgangslijn lijf→boor is de kale reductie.
  - vultinten per dwarsdoorsnede van de kegel: onder/links schaduw (zoals het model), dan midden, een lichte band bovenop (35 px licht, o.a. (53–55,44–48) … (59–60,58–60)) en midden vlak vóór de zwarte rand. Daarna ontkorreld binnen de boor.
- **volume lijf (37 px), kleur, géén vorm:** het model is op het lijf één vlak middengeel. Een rechte lichte band van ±2–4 px evenwijdig aan de lijfas, alleen op middengeel en alleen in het dikste stuk tussen kop en boor: (30,26) → (42,37) (lijst: (29–31,27), (30–31,28), (31–34,29), (33–36,30), (34–37,31), (35–38,32), (37–39,33), (38–41,34), (39–42,35), (40–42,36), (42,37), (30,26)). Licht van boven; de schaduw achteraan blijft waar het model hem heeft.
- Geen andere pixels die niet uit het model komen.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (16,16,24) · geel 2 olijf lijn/selout (124,112,56) 3 schaduw (200,184,96) 4 midden (236,224,140) 5 licht (248,244,184) · blauw 6 donker (36,84,116) 7 midden (62,126,160) 8 licht (96,164,204) · vleugel 9 donker/selout (112,148,172) 10 midden (180,210,224) 11 licht (228,244,248).
Tinten = modeltonen (gemeten: geel 124,114,55 / 204,190,104 / 238,228,145 / 245,235,170; blauw 43,97,126 / 63,127,159 / 83,154,191; vleugel 144,176,190 / 184,213,225 / 224,242,244), donkerste tinten iets dieper voor contrast. 11 kleuren, dus 4 vrij.

## Controle (`controle.py`)
- 64×64, mode P, transparency 0, 12 kleuren incl. transparant; per groep ≤ 3 tinten + lijn/selout.
- Geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart 13,6 % van de figuur.
- Tintvlekjes < 3 px die over zijn: olijf (9×) en donkerblauw/middenblauw/vleugeldonker zijn lijnen (selout, ooglijnbegin, overgang kop/kaak, rugbandranden, vleugeladers: schuine 1-px lijnen tellen per 4-buur als losse stukjes); lichtblauw 4× (hoornvoet/kopband (18,8) (19,10), vleugelpunt (56,6), rugband (44,21)) en 1 middengeel (41,26) staan op modelplekken.

## Resterende twijfels (eerlijk)
- **Lijflichtband** is een eigen kleurtoevoeging (model is daar vlak); hij leest als volume maar is recht. Zonder band is het lijf vlak middengeel zoals het model.
- **Boor:** de spiraallijnen volgen het model, maar op 1,41× verkleining blijven ze trappig (schuine 1-px lijnen met een knik waar het model een boog heeft); de lichte band kruist de lijnen, waardoor elk segment drie tinten krijgt. Leest op 1× als spiraalboor, op 8× wat druk.
- **Oogring:** donkere binnenrand onder en donkere buitenrand links/rechts komen uit de meting, maar geven op 8× een wat onrustige ring (afwisselend donker/midden). Alternatief: ring helemaal middenblauw met alleen een donkere buitenrand.
- **Kaak:** de golvende onderrand (model: blauwe "tandjes" met zwarte rand) is op deze maat een rij zwarte en blauwe pixels; leest op 1× als rafelige kaakrand, zoals het model.
- Vleugeladers zijn 1-px schuine lijnen in middenblauw; op 1× lezen de vleugels als twee lichte vleugels met vingers, de aders zijn subtiel.
