# Great potoo (Ghost/Normal, losse soort): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Stand: **opnieuw beginnen** (Jordi, 5 nov: "begin maar helemaal opnieuw"). Het 3D-werk in `model3d/`, `model3d_v2/` en `model3d_v3/` is afgekeurd; geen Blender/3D meer voor de potoo (Jordi, 5 nov).

## Besloten (Jordi, 5 nov)
- Basissoort: **great potoo** (*Nyctibius grandis*): "ik wil sowieso een great potoo".
- **Eén stage** (single stage, zoals Sableye): "laten we 1 stage doen en gelijk met ontwerp gaan beginnen".
- Type **Ghost/Normal**: "Ik vind Ghost/Normal een leuke type, helemaal omdat we al een Ghost/Flying hebben en ik echt ontzettend veel ideeën heb voor vogels". (In de repo zijn alleen Zorua/Zoroark-Hisui Normal/Ghost.)
- **Geen tak of stomp in beeld:** "er is eigenlijk geen enkele pokemon sprite met een tak of iets anders in beeld, dus die camouflage kunnen we niet zo goed overbrengen". De vermomming zit in de sprite-frames (stilstaan ↔ bek open), in het lijf (schorsachtig verenpatroon) en in de data (ability, dex-tekst).

## Kenmerken (uit Jordi's foto's)
- Grote ronde kop, enorme zwarte kraalogen (great potoo: donkere iris, leest als zwart).
- Klein snaveltje, maar een gigantische roze muil als de bek opengaat.
- Licht grijswit met bruingrijs gespikkeld/geschubd verenpatroon (schors/korstmos).
- Rechtop zittend, peervormig lijf, lange vleugels en staart naar beneden.

## Achtergrond
- Guaraní-legende van de urutau: Ñeambiú verliest haar geliefde, verstomt van verdriet en wordt een urutau; de nachtelijke roep is haar klaagzang.
- Leefwijze: zit overdag stil als een afgebroken tak, vaak wekenlang op dezelfde plek; vliegt 's nachts korte stukjes vanaf die plek om grote insecten te vangen en keert terug. Vliegt dus weinig (past bij Ghost/Normal zonder Flying).

## Onderdelen
| onderdeel | bron / referentie | Jordi's woorden | status |
|---|---|---|---|
| pose | driekwart, licht vooruit hangend, **bek open**; kop/muil uit het drieluik (boven + linksonder); skelet: `jordi_great_potoo_tak_bek_open_volledig.png` (hele vogel, bek open, 3/4), voorover hangen uit `jordi_great_potoo_vooroverhangend_bek_open.webp` | "Ik wil de bek juist open, want dat is de sprite die men het meest gaat zien. het wordt uiteraard een driekwart pose met de vogel die licht vooruit hangt" | besloten |
| klauwen | nauwelijks zichtbaar op de foto's | "De klauwen zijn nauwelijks zichtbaar lijkt wel, wel lachen. Dat betekent dat we die prima in een sprite ook kunnen verbergen" | besloten: verborgen |
| neerzetten | optie 1: op een onzichtbare tak, zoals Swellow/Noctowl/Taillow (`vogels_neerzetten.png`) | "ja, optie 1, ga maar naar het silhouet" | besloten |
| frames | frame 1 = bek open (hoofdsprite); frame 2 nog open | idem | deels |

## Silhouet
- v1: omtrek van de takfoto, 10° voorover, gespiegeld: las als augurk (muil onzichtbaar).
- v2: muil-inkeping: te klein op 64.
- v3: onderkaak hangt verder open (drieluik), kop 15% groter (Pokémon-verhouding). 1023 px (Xatu 1033). Model = de foto zelf langs dezelfde omtrek (`silhouet/model_v3.png`).

## Ontwerp (Jordi, 5 nov)
| onderdeel | Jordi's woorden | status |
|---|---|---|
| vacht | "misschien dat we de vacht heel licht maken als mooi contrast"; "C zie ik zitten qua vachtkleur" | besloten: heel licht (C) |
| ogen | "grote ogen"; "de ogen worden echt pikzwart, kijk naar andere pokemon die dat ook hebben"; "drifloon heeft ook puur zwarte ogen, dat gaan wij ook doen" | besloten: **puur zwart zonder glans (Drifloon)**, bewuste uitzondering op de regel "geen volledig zwarte ogen zonder glans" |
| mond | "grote mond"; "De mond maken we dan geestblauw/paars achtig"; "de muil moet wel echt een snavel zijn he" | besloten: echte snavel zoals de bron: bovensnavel = voorkant van het gezicht met klein haakje, onderkaak = brede schep, wijd open; binnenkant geestblauw/paars. Afgekeurd: losse grijze eendensnavel ("de snavel is nog helemaal niet goed", "kijk eens naar het bronmateriaal, je bent aan het speculeren") |
| geest | "dus hij mag nog wat geestachtiger"; "Het geestachtige zit alleen in de kleuren en de muil" | besloten: geen vervagend onderlijf |
| patroon | "We kunnen wel het hisui zorua idee doen dat ze goed passen in sneeuwgebied, dus dat er wat schorsachtige vlekken in komen" | besloten: lichte vacht (sneeuwcamouflage) + enkele schorsachtige vlekken |
| vorm | "de vorm mag redelijk vergelijkbaar met het origineel" (5 nov, tweede gesprek) | besloten: 3D-model blijft dicht bij de echte great potoo; Pokémon-aanpassingen klein en benoemd |
| sfeer | "hij moet schattig maar uncanny tegelijkertijd zijn zoals in het echt" (5 nov, tweede gesprek) | besloten: ronde zachte kop + kraalogen (schattig), te wijde muil tot achter de ogen en starende blik (uncanny) |
| bronnen | "de bronnen die ik net gestuurd heb", "die 5 fotos die ik aan het begin stuur"; over de platte-kopfoto: "die moet juist niet"; over oortjes/kop: "nu ben je weer net een soort vleermuis aan het bouwen" (5 nov, tweede gesprek) | besloten: **alleen** `jordi_great_potoo_bek_open_drieluik.webp`, `jordi_great_potoo_bek_open_duo.webp`, `jordi_great_potoo_kop_closeup_bek_open.webp`, `jordi_great_potoo_illustratie_rug_staart.png`, `jordi_great_potoo_nacht_stam_volledig.webp`. Geen andere foto's, geen oortjes, geen platte kop/snavel |
| kop-leidraad | "dit mag als leidraad voor het hoofd, dit linkse stuk" (linkerhelft van `jordi_great_potoo_bek_open_duo.webp`) | besloten: kopvorm, oog, snavel en muil op die foto meten |
| bek groot | "met die lekker overdreven grote bek", "dat is grappig" (5 nov, tweede gesprek) | besloten: de muil mag overdreven groot (Pokémon-stap B) |
| ogen hoger | "en de ogen moeten hoger" (5 nov, tweede gesprek, bij de 3D-overlay) | besloten: oogmidden hoger op de koepel |
| snavel = kern | "de snavel is de main selling point, die moet gewoon goed zijn", "maak nu een poppetje zoals bij de lama, doe het desnoods alleen vanuit sprite vorm. Er zijn pokemon die ook hun snavel open hebben die je als inspiratie kan gebruiken", "ik accepteer het niet als de bron niet goed nagemaakt is want dat kan gewoon niet moeilijk zijn" (5 nov) | besloten: poppetje in lama-stijl (mag alleen in de spritehoek); bron (close-up/leidraad) getrouw nagemaakt; open snavels in echte sprites: `referenties/open_snavels_sprites.png` |
| poppetje r3 | "elke keer dezelfde fouten he. Het is geen bol hoofd, de kaak gaat niet voldoende naar voren, ogen net te laag op de bek. De bovenkant van de snavel sluit niet goed aan en is te puntig", "en de mond is nog teveel pacman ook", "maar het was wel de beste tot nu toe" (5 nov) | harde eisen: kop BOL (Claude las dit eerst omgekeerd en maakte de kop in ronde 4 platter; Jordi: "maak het hoofd nu gewoon eens bol en laat een keurder kijken"); onderkaak verder naar voren; ogen iets hoger boven de mondrand; bovensnavel sluit vloeiend aan op het gezicht en is niet puntig |
| snavelpunt | "de punt is echt onderdeel van de snavel he, niet een decoratie"; bij ronde 5: "die punt bovenop de snavel is geen losse punt, die is onderdeel van de snavel"; "allereerst mijn oordeel, je leest niet", "echt al 4x gezeggd" (5 nov) | besloten: echte bovensnavel (hoornvorm, snavelrug tussen de veertjes) die in één vorm in het haakje eindigt; Jordi's oordeel gaat vóór de keurder |
| onderkaak r5 | "de onderkant lijkt meer op een pelikaan omdat die die te ver uitsteekt van het lichaam en niet ver genoeg open gaat, plus de vorm is gewoon nog steeds anders dan de foto" (5 nov) | besloten: kaak wijder open, dicht bij het lijf, omtrek = de overgetrokken mondrand van leidraad en close-up |
| vorm kop+muil | "maar waarom ben je al uren bezig met een fucking snavel nabouwen"; daarna stuurde Jordi de overtrek van de maker terug (`referenties/overtrek_ronde5_AFGEKEURD_niet_nauwkeurig.png`): "dit is helemaal niet overgetrokken", "en eerder ging je overtrekken en toen kregen we allemaal rare pixels eromheen" (5 nov) | besloten: kop + snavel + muil in de spritehoek als 2D-tekening; eerst nauwkeurig met de hand overtrekken (veel punten, gladde curven, < 2 px van de rand), alleen eigen vectorvormen, geen fotopixels/segmentatie; lijf van het poppetje blijft |
| oog zonder rand | "en waarom heeft het oog opeens een half wit stuk eronder" (5 nov, bij ronde 3–5) | besloten: geen licht ooglid/sikkel; puur zwarte kraal (keurderadvies ronde 2 verworpen) |
| lichaamsvorm | "kijk dit is de vorm van het lichaam" (5 nov) bij `referenties/jordi_great_potoo_illustratie_LICHAAMSVORM.png` | besloten: lijf volgt deze illustratie: rechtop, lang; brede schouders direct onder de kop waar de vleugels beginnen, smal taps lijf, zeer lange staart (±de helft van de vogel) met de lange vleugelpunten ertegenaan |
| kop blijft staan | "als de mond open gaat schuift het hoofd niet opeens een stuk naar voren" (5 nov) | besloten: kop op dezelfde plek als met dichte bek (illustratie lichaamsvorm); alleen de onderkaak klapt open voor de borst |
| proces | "ik wil niks meer zien totdat het echt lijkt op de bronfotos" (5 nov) | besloten: geen tussenresultaten naar Jordi; pas na eigen vergelijking met de foto's + keurder PASS |
| blinde test | "ik denk dat een onafhankelijke agent niet eens kan zien dat dit een vogel is" (5 nov) | besloten: elke ronde een blinde test (agent zonder context ziet alleen het plaatje en zegt wat het is); pas verder naar keurder/Jordi als hij een (potoo-achtige) vogel met open snavel ziet |
| hoek + sprite | "driekwart, als je een sprite wil bouwen al meteen mag het ook, maar het moet goed zijn" (6 nov) | besloten: driekwart blijft; direct naar de 64×64-sprite mag, met poppetje ronde 14 als bron voor massa/pose; snavel/muil in de pixelstap naar de close-up en echte open-snavelsprites |
| stand 6 nov | "Lichaam is oké, de rest niet. We gaan morgen verder en dan zal ik een nieuw idee opperen voor hoofd en snavel" (6 nov) | lijf bevroren (poppetje ronde 14 / sprite ronde 3: rechtop, brede schouders, gevouwen vleugel met pennen, brede platte staart, schorspatroon); kop en snavel opnieuw met Jordi's nieuwe idee |
| schets kop/bek | Jordi's schets (`referenties/jordi_schets_kop_bek_7nov.webp`, over de driekwart-tekenbasis): "allereerst de bekvorm wat meer zoals in de bron. Wat hem anders maakt dan andere vogels is dat de kop wat meer voorover geleund is en de nek er echt achterop zit en helemaal doorloopt. Alsof die echt voorover hangt om zijn bek open te trekken, plus de positie van het oog heb ik iets anders gedaan. Kijk of je deze feedback begrijpt met een sprite schets, dat de afwerking niet goed is, is niet erg, we gaan de vorm goed krijgen. Weet dat mijn schets niet 1 op 1 klopt maar ik hoop daarmee het concept toe te lichten" (7 nov) | Claude leest: (1) bek = brede ronde U met punt onderaan zoals de bron, van snavelpunt tot onder het oog; (2) kop hangt voorover, achterkop/nek loopt in één doorgaande bocht van kruin naar rug, geen knik; (3) oog verder naar voren, iets liggend ovaal. Eerst een vormschets als sprite. Aanvulling: "ja in de schets kan ik dat niet uittekenen maar de kop hangt wat meer voorover" |
| kern | "De snavel en ogen zijn het kernpunt van het design, zoals je kan zien zitten er kleine veren allemaal ook tussen de ogen duidelijk, dat mag je ook uitbeelden" (5 nov, tweede gesprek) | besloten: snavel + ogen krijgen de meeste aandacht; korte veertjes tussen en rond de ogen (borstelveertjes/wenkbrauwkuif) uitbeelden |
| werkwijze | "Voordat je een silhouet bouwt, bouw je eerst een 3d model" | 3D-poppetje vóór het silhouet |

## Afgekeurd (niet herhalen)
- **Poppetje (bollen-renderer, `poppetje/`) ronde 1–3, maker-agent:** twee keurders FAIL. Ronde 2: "witte gladde helm met paars grijnsvlak"; ronde 3: "paars schild/slabbetje met grijs kader", bovensnavel als vizier, kruin als pet, staart als stokje. Keurder: de bollen-renderer maakt van snavel en kaak losse geometrische stukken; niet verder repareren.
- **3D v3 (snavel uit onderdelen, `model3d_v3/`) en Blender/3D als geheel:** "haha je gaat nu precies hetzelfde weer fout doen", "deze aanpak werkt niet", "stop met blender"; eerder: "hij hoeft echt niet geometrisch perfect te zijn he maar er gaan zulke simpele dingen bij het model eerder fout, oog in de mond enzo".
- **3D v2 (gespleten koepel + schep, `model3d_v2/`):** "ik vind het eerlijk gezegd nog totaal niet lijken, de bek is geen snavel, lijkt net een soort pacman zeehond, de bolling bovenop is niet goed", "de onderkaak moet meer pronounced", "en de snavel is geen pacman mond". Bek niet als opengeknipte kop bouwen.
- Paars rond de mond (voxelkop): "geen idee wat dit was maar doe dit nooit meer, met al dat paars om die mond heen". Mondkleur alleen binnen de mondrand.
- Zichtbare roep / geestslierten uit de muil: "een zichtbare roep doen we niet, dat is niet pokemon".
- **Silhouet v1–v4 (de foto overgetrokken):** "we gaan niet een potoo namaken", "we maken een pokemon". Eerst een Pokémon-ontwerp (stap 1), dan pas een silhouet. Gewenst: "geestachtiger", "grote ogen, grote mond".
- Tweede stage die met een tak/stomp versmelt (`concept_schets_2stages_afgekeurd.png`): tak in beeld past niet bij Pokémon-sprites.

## Referenties
- `referenties/jordi_great_potoo_bek_open_drieluik.webp`: bek open (3/4 en zij), voederen.
- `referenties/jordi_great_potoo_stomp_voor.png`: rechtop op stomp, bijna van voren.
- `referenties/jordi_great_potoo_wit_zijaanzicht.png`: lichte vogel, zijaanzicht, kop van dichtbij.
- `referenties/jordi_grijze_potoo_takhouding_nacht.webp`: andere soort (gele iris), takhouding.
- `referenties/jordi_great_potoo_tak_bek_open_volledig.png`: hele vogel op tak, bek open, 3/4 (skelet).
- `referenties/jordi_great_potoo_vooroverhangend_bek_open.webp`: voorover hangend, zijaanzicht, bek open, staart zichtbaar.
- `referenties/jordi_great_potoo_nacht_voor_volledig.webp`: hele vogel van voren, 's nachts (verenpatroon, kop).
- `referenties/jordi_great_potoo_illustratie_rug_staart.png`: illustratie rug/vleugel/lange staart.
