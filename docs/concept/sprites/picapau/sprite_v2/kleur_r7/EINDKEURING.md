# Eindkeuring picapau sprite_v2 kleur r7 (verse keurder, 5 nov)

Gekeurd: `kleur_r7/picapau.png` (855 px, 15 kleuren + transparant), `normal.pal`, `raster.txt`. Niets aan de sprite veranderd. Jordi keurde vorm, ontwerp, snavel, kuif en kleurkeuze goed; die staan hier niet ter discussie. Deze keuring gaat over de afwerking (Dragonfly Cave, Gen 3) en over de vraag of de sprite het B1-model volgt.

## 1. Blinde indruk
Bekeken op 1×, 3× en 8×, op licht (235) en donker (40,40,48), naast Taillow, Pikachu, Starly, Trumbeak, Swablu en Pidgey (bovenste 64×64 van `anim_front.png`).
- **1×:** leest direct als een gele vogel met een rode wang, zwarte kuifpunten en een bruine vleugel en staart. Het formaat past tussen Taillow en Pikachu. De Pikachu-verwantschap is zichtbaar zonder dat het een kopie wordt.
- **3×/8×:** het palet en de omlijning zijn dezelfde familie als bij Pikachu: een goudbruine selout aan de lichte kant, zwart aan de schaduwkant en een gele bal met een schaduwsikkel rechts. De kop leest als een bal en het lijf is bol, met een slagschaduw van de kop op de borst (r29). De vleugel heeft een lichte schouder en stippen. De staart sluit nu aan: de rechterrand loopt door vanaf rij 47.
- **Wat minder als een echte Gen 3-sprite oogt (klein):**
  - Tenen en het nabije pootje hebben geen echte omlijning. Ze zijn tweetonig `g` boven en `G` onder. Taillow, Starly en Pidgey omlijnen hun tenen met zwart of donkerbruin. Op donker vallen het verre voetje (`G` 64,64,72) en de kuifpunten bijna weg, net als Pikachu's oorpunten in dezelfde kleur.
  - De kuifstelen zijn binnen de omlijning maar 1 px geel (rijen 7–8). Dat volgt het bevroren silhouet (3 px breed).
  - De rug en vleugelrand (rij 25–42) is een regelmatige 2-2-2-trap en leest daardoor als een rechte lijn. Het B1-model en het bevroren silhouet hebben hier ook een rechte, stijve spechtenrug.

## 2. Tegen het model (`model_vs_sprite.py` B1 ↔ r7)
| onderdeel | oordeel |
|---|---|
| kop | volgt het model: ronde kop, licht linksboven waar de toonkaart toon 4 heeft, schaduwsikkel rechts |
| kuif | twee kegels met zwarte punten, naad als binnenlijn `3` van (33,9) tot (30,12). De lichte kant van beide kegels (r7) staat waar de toonkaart toon 4 heeft. Achterkuif rechts ongewijzigd (r2, Jordi's zone). |
| oog | één oog (snavel opzij), glans `w` en reflectie `G`, ongewijzigd |
| wang | rond, `C` rechtsonder, ongewijzigd |
| snavel | ongewijzigd ("snavel is prima") |
| borst/buik | bol. Het hooglicht is een ovaal op x28–32, r30–35, en de losse vlek van r6 is weg: rij 38–44 bevat geen `1` meer. Slagschaduw onder de kop, onderrand in `3`. |
| vleugel | lichte schouder linksboven, `d` rechts en onder. De stippen zijn gelijk; de stip op (35–36,27–28) is nu `g` zoals de rest. |
| poten | ingeplant in het lijf. Het verre voetje ligt hoger en verder naar achteren, in schaduwtint, zoals in het model. |
| staart | stijve steunstaart, rechterrand x50 doorlopend zoals het silhouet. De inkeping op rij 51 is dicht. Licht `l` links van het midden, schaduw `b` rechts. |
| licht | overal linksboven |

## 3. Harde regels
| regel | oordeel | pixels / toelichting |
|---|---|---|
| ≤ 3 tinten per kleurgroep + omlijning | **PASS** | geel `1 2 3` + `4`; vleugel `l b d` + `k` (stippen `g`); staart `l r b` + `d`; snavel `h g G` + `k`; wang `c C`; poten `g G` |
| contrast | **PASS** | geel helderheid 230 / 202 / 165 (stappen 28 en 37, Taillow-bereik). De basis (202) is donkerder dan Pikachu's basis (218), zoals Jordi vroeg. |
| geen clusters < 3 px (behalve glans/1-px-lijnen) | **PASS** | De nieuwe clusters uit r7 zijn bedoeld: `3` op (33,9), (32,10), (31,11), (30,12) is één diagonale binnenlijn tussen de kegels (vorm over vorm), en `2` op (32,7)–(32,8) is de vulling van een steel van 1 px. Verder alleen bevroren oog- en snavelankers, de primaire lijn `b` (41–42,34)/(44,36), die diagonaal doorloopt in de vleugelpunt, en de teen (27–28,48). Geen losse pixels en geen pixels die alleen diagonaal vastzitten. |
| geen banding / pillow shading | **PASS** | Op de kop is de `2`-band geen vaste afstand tot de rand (5–8 px). Op de buik zit het licht linksboven met een sikkel rechtsonder, niet langs de hele omtrek. De drie tonen op de kegels volgen de kegelvorm. |
| licht linksboven | **PASS** | |
| zwart alleen aan de schaduwkant | **PASS** | Links is r7–41 helemaal `4`. Zwart staat rechts, onder (r42–46) en op de kuifpunten, zwart zoals Pikachu's oorpunten. De `k` op (17,17)/(18,16) zit in de bevroren snavel. |
| gekleurde selout aan de lichtkant | **PASS** | links `4`, staart links `d`, bovenkant van de achterkuifpunten `4` |
| nooit zwart en gekleurd om en om op één rand | **PASS** | De linkerrand gaat één keer over van `4` naar `k` (27,41)→(28,42). Rechts staan groepen `444`/`4 44` op de bovenkant van de achterkuifpunten, en `k` op hun onderkant: dat zijn per facet aparte groepen, geen om-en-om-patroon. |
| geen open randen | **PASS** | Rand rondom gesloten. Tenen en pootje zijn 1–2 px dun en hebben pseudo-omlijning (SPRITING §8: dunne delen alleen met kleur scheiden). |
| geen lichte kleur op de buitenrand | **PASS** | 0× `1 2 h w c l` op de rand. Alleen `g` (helderheid 142, middentoon) op de snavelrug (bevroren) en op pootje en tenen (pseudo-omlijning). |
| vloeiende curven | **PASS** | Voorkant links 2-5-2-2-2-1-1-1 en daarna onder 3-5-6, steeds geleidelijk. Voorhoofd 4-2-2-1-1. Staart links 4-1-2-1-2-1, taps naar de punt. Geen spijkertjes. |
| pootjes in perspectief | **PASS** | De verre voet (34–37, 46–47) ligt 2 rijen hoger dan de nabije (26–33, 48–49), schuift naar achteren en staat in schaduwtint `G`. Ze staan niet op één lijn. |

## 4. Oordeel: **GOED**
Geen reparaties nodig; er is geen pixeltabel. De vijf punten van Jordi over r6 zijn verwerkt (staartpunt, buikvlek, donkerder geel, vleugelstip, kuif). Elke r7-wijziging is terug te voeren op de render of de toonkaart. Buiten die zones is niets veranderd: zie `repareer.py` en de diff r6→r7 (rijen 10–14, 28–29, 41–43 en 52).

## 5. Voor Jordi (smaak, geen afkeur)
- **Pootjes/tenen** zijn grijs zonder harde omlijning en vallen op een donkere achtergrond wat weg. Echte vogels zoals Taillow en Starly omlijnen hun tenen. Als je ze steviger wilt, is de kleinste stap de nabije pootrand (31,45)–(31,47) en de teenbovenkant (27–28,48), (30–31,48) van `g` naar `G`. Dan verdwijnt wel de lichte kant van het pootje. Niet nodig volgens de norm.
- **Kuifstelen** zijn 1 px geel tussen de omlijning (rijen 7–8). Dat komt uit het bevroren silhouet. Op 1× lezen de zwarte punten daardoor als losse stokjes boven de kop. Wil je ze steviger, dan moet het silhouet daar 1 px breder; dat is jouw keuze.
