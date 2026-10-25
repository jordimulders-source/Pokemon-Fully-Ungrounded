# Olinguito v2: silhouet met de hand (B2, Linoone-perspectief)

Eén kleur, 64×64, met de hand getekend als tekstraster (`silhouet.txt`: `.` = transparant, `#` = lijf). Ik heb de onderlaag (`../silhouet_kolibriemethode/onderlaag_b2_256.png` / `_64.png`) gebruikt voor de pose, de volgorde van de onderdelen en de richting van de poten. De render is níet verkleind en overgenomen: de verhoudingen zijn die van een Pokémon (grotere kop, compacter lijf, kortere en dikkere poten, staart dichter op het lijf).

**Bestanden:** `silhouet.txt`, `silhouet_1x.png`, `vel.png`. Op het vel staan: de onderlaag, het silhouet op 4× en 1×, het silhouet half doorzichtig over de onderlaag (5 px naar rechts en 6 px omlaag geschoven, zodat de koppen samenvallen), de versie met de verre poten lichter, en Linoone, Zigzagoon, Poochyena, Growlithe en Sentret op 4× en 1× (op grijs en op wit).

## Maten
| | olinguito | ter vergelijking (Gen 3, 1 kleur) |
|---|---|---|
| pixels | **982** | Poochyena 989, Sentret 982, Zigzagoon 1127, Growlithe 1154, Linoone 1089 |
| box | 47 × 42 (x 1–47, y 10–51) | D4: ≤ 48 breed ✓ |
| kop (oppervlak) | ±34 % | ≤ 41 % ✓ |
| kop (hoogte, oor t/m kin) | 23/42 = 55 % | fase 1: 40–55 % (bovengrens) |
| samenhang | 1 geheel (4-buren), geen losse pixels; alleen klauwpunten en tenen hebben 1 buur | |

Het formaat ligt ±30 px boven de 950. Het zit op het niveau van Poochyena en Sentret (fase 1). Vorm gaat vóór het getal: verder krimpen zou de poten of de klauwen dunner maken.

## Per eis
- **Hoek B2:** de kop staat linksboven met de snuit naar links-onder, het lijf loopt schuin naar rechtsachter en de staart geeft rechtsboven tegenwicht. De kop staat hoger dan de rug (rug y 27–28, kruin y 16), dus licht gekanteld met de kop omhoog.
- **Kop als eigen onderdeel:**
  - boven: een wig tussen het achterhoofd en de rug (x 22–30, y 26–28);
  - onder: een inham onder de kin, tussen de kaak en de voorpoot (x 11–15, y 34–36);
  - de kop is een ronde schedel met een hoog, rond voorhoofd (de kruin verbreedt in stapjes van 2-1-1-0-1).
- **Oor:** een ronde bult van 7 × 5 bovenop de kruin, achteraan, met een inkeping links (x 17–18) en rechts eronder. Het verre oor is een nopje van 2 px links op de kruin.
- **Snuit:** een stomp stuk dat 5 px voorbij het voorhoofd uitsteekt (punt bij x 1, y 28–29), iets onder het midden van de kop. Daaronder een getrapte kin. Het oog komt er in kleur laag bij de snuit (rond x 9–11, y 25–27).
- **Vier poten** (op 1× tel ik er vier; zie de versie met de verre poten lichter op het vel):
  - nabije voorpoot (x 8–23): reikt diagonaal naar voren en omlaag; 8–10 px dik; elleboog als knik achteraan (y 38–40 → 41); poot y 45–46;
  - verre voorpoot (x 21–28): korter en rechter onder de borst, 5 px dik, poot y 44;
  - verre achterpoot (x 28–35): stapt naar voren (tenen naar links), 5 px dik, staat het hoogst (y 45);
  - nabije achterpoot: grote dij die doorloopt in de romp, knie naar voren (x 36, y 42–44), scheen naar achteren naar de hak (x 45), voet plat naar voren (x 35–44, y 48–49). Tussen knie en tenen zit een driehoek lucht, zodat het gewricht leest.
  - Tussen elk paar poten zit minstens 1 kolom lucht. Tussen de verre voorpoot en de verre achterpoot zit de buikboog (x 29–31, y 37–39).
- **Diagonaal, geen telgang:** de nabije voorpoot en de verre achterpoot staan vooruit, de verre voorpoot en de nabije achterpoot achteruit. Voethoogtes, van laag naar hoog: nabije voorpoot (klauwpunt y 51), nabije achterpoot (y 49), verre voorpoot (y 47), verre achterpoot (y 45).
- **Klauwen:**
  - nabije voorpoot: 2 klauwen, elk 5 rijen lang. Ze zijn aan de basis 3 px breed en lopen spits toe. Ze lopen eerst schuin naar voren en omlaag; de punt buigt terug (haakje zoals bij Linoone). Tussen de twee klauwen zit steeds 1–2 px lucht. Het oude "kussentje" ernaast is weggehaald, omdat het op 1× als een derde klauw las;
  - verre voorpoot: 2 kleinere klauwen van 3 rijen, met dezelfde buiging.
- **Staart:** begint boven op de romp, gaat 3 px dik omhoog dicht langs het lijf en krult bovenaan naar links in een haak (vraagteken) met lucht in de krul. Er zitten geen trapjes of losse pixels in; de dikte is overal 3.
- **Werkwijze:** ik heb 18 versies getekend als spans/tekstraster per rij, telkens bekeken op 1×, 4× en 8× naast Linoone, Zigzagoon en Poochyena, en daarna in het raster bijgewerkt. Het gebruikte script tekent alleen wat ik per rij heb ingetypt (geen ovalen, geen schaling).

## Gerepareerd na eigen keuring
1. Versie 1–3 waren te groot (1375 → 1064 px) en te blokkig: een tafel van een lijf met vier poten eronder. Ik heb het lijf verlaagd en versmald, de buik laten welven en de bil afgerond.
2. De kop las als een kegel (een recht 45°-voorhoofd). Nu is de kruin breder en ronder.
3. De kop ging naadloos over in de borst. Nu zitten er een kininham en een nekwig.
4. Er was een derde "klauw" (het kussentje) aan de nabije voorpoot; die is weg.
5. De klauwen van de verre voorpoot waren losse puntjes van 1 px en zijn nu klauwtjes van 3 rijen.
6. De verre achterpoot was een rechte paal en stapt nu schuin naar voren.

## Eerlijk: wat nog niet (goed) leest
- **Formaat:** 982 px, ±30 boven de 950.
- **Kop iets groot:** 55 % van de hoogte, precies op de bovengrens van fase 1.
- **De verre poten zijn eenvoudige zuiltjes** van 5 px zonder zichtbaar gewricht. Op 1× tellen ze als poten, maar ze hebben weinig vorm. In kleur moeten ze donker (schaduwtint) worden, anders lezen ze als een kam.
- **De spleten tussen de poten zijn 1 px breed.** Op 4× geeft dat een kam-indruk. Op 1× lezen ze als aparte poten.
- **De nabije voorpoot is vrij recht:** een brede diagonale band met maar een kleine elleboogknik.
- **"Olinguito" leest in silhouet nog niet specifiek.** Op 1× lees ik een klein, klimmend zoogdier (tussen kat en aapje) met een ronde kop, een rond oor, een krulstaart en klauwen. Het masker, de lage oogpositie en de donkerbruine vacht moeten het in de kleurfase tot olinguito maken.
- **Afwijkingen van de onderlaag (bewust):** de staart staat dichter bij het lijf, zodat de box onder de 48 blijft, en de poten zijn korter. Daardoor valt het silhouet over de onderlaag niet precies samen.

## Lessen
- **Een tekstraster per rij als spans** (x-van, x-tot) typen gaat sneller en met minder fouten dan 64-tekenregels. Het blijft handwerk, maar kopieer het daarna naar het echte raster en werk daar verder.
- **Een gedeelde scratchpad kan oude bestanden van andere agents bevatten** (bijv. `v2.png`). Werk in een eigen submap; een afgebroken render (BrokenPipe door `| head`) laat dan geen vreemd plaatje achter.
- **Kijk naar een 8×-uitsnede om hoeken te vinden:** rechte 45°-trappen op het voorhoofd lezen als een kegel. Een rond voorhoofd heeft stappen 2-1-1-0-1-0.
- **Een extra uitsteeksel naast twee klauwen** (een kussentje) leest op 1× als een derde klauw. Laat de poot erachter rond eindigen.
