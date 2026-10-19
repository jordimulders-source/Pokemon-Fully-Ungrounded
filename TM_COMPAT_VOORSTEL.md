# Voorstel: extra TM-compatibiliteit (nog NIET doorgevoerd)

Soorten die in déze rom (herziene types uit `src/data/pokemon/species_info/`, lichaamsbouw, signature-thema) logisch een
bestaande-move-TM zouden kunnen leren, maar dat nu niet kunnen. Jordi keurt eerst; daarna in
`GROUNDED_EXTRA_TM_SPECIES` (`tools/learnset_helpers/make_teachables.py`) zetten en het script opnieuw draaien.

Gevonden met: soorten met het type van de move (en bij fysieke/speciale moves de passende Attack/Sp. Atk), die de move
nergens kunnen leren; daarna met de hand gefilterd.

| TM | Move | Voorgestelde soorten | Waarom |
|---|---|---|---|
| TM50 | Flare Blitz | Groudon, Sizzlipede | Groudon is Fire/Ground (fysiek); Sizzlipede is de Centiskorch-lijn (die kan het wel). |
| TM60 | Rock Tomb | Nacli, Naclstack | Rock-types, Garganacl kan het al: lijn gelijktrekken. |
| TM61 | Snarl | Gyarados, Huntail, Noctowl, Hypno, Cacturne, Banette, Dusknoir, Inkay, Malamar, Greninja, Grimmsnarl, Impidimp, Morgrem, Overqwil | Allemaal Dark in deze rom; grommen/sissen past bij elk. |
| TM62 | Roost | Clefable, Pinsir, Torchic, Combee, Delibird, Celesteela, Tornadus, Thundurus, Landorus, Rayquaza, ArticunoGalar, ZapdosGalar, MoltresGalar | Flying in deze rom (Clefable, Pinsir, Torchic) of vogels/vliegers die nu niet kunnen rusten. |
| TM63 | Bulk Up | Lopunny, Spinda, Farfetchd, FarfetchdGalar, Sirfetchd, Pawmo, LilligantHisui, Cobalion, Terrakion, Virizion | Fighting in deze rom (Lopunny, Spinda, Farfetch'd) of fysieke vechters zonder spierwerk-TM. |
| TM64 | Charge Beam | Loudred, Exploud, Nosepass, Probopass, Starmie, Yamper, Boltund, Toxel, Stunfisk, Zeraora, TapuKoko | Electric in deze rom (Loudred/Exploud, Nosepass, Starmie) of elektrische soorten zonder straal. |
| TM65 | Thunder Wave | Loudred, Exploud, Toxel, Oricorio | Electric in deze rom / Pom-Pom-vorm; Thunder Wave is de basis-Electric-TM. |
| TM66 | Icy Wind | DarumakaGalar, DarmanitanGalar | Ice-types die nu geen enkele ijswind hebben. |
| TM67 | Poison Jab | Muk, Grimer, Crobat, Golbat, Zubat, Weedle, Kakuna | Grimer/Muk (Poison/Ground, fysiek), Zubat-lijn (giftanden), Weedle (gifangel). |
| TM68 | Will-O-Wisp | Volbeat, Parasect, Golett, Golurk, Honedge, Doublade, Aegislash, Sandygast, Palossand, Annihilape, Dreepy, Decidueye | Volbeat is Fire, Parasect Ghost in deze rom; de rest zijn Ghost-types zonder dwaallicht. |
| TM69 | Tailwind | Clefable, Pinsir, Torchic, Rowlet, Ninjask, Celesteela, Thundurus, Landorus | Flying in deze rom; vleugels of windgoden. |
| TM70 | X-Scissor | Heracross, Pheromosa, Buzzwole, Wimpod, Flygon, Vibrava, Trapinch, Shelmet | Fysieke Bugs met scharen/kaken; Trapinch-lijn heeft kaken als scharen. |
| TM72 | Wild Charge | Loudred, Nosepass, Tynamo, Porygon | Electric-types die nu niet kunnen aanstormen (Loudred-lijn is Electric/Steel). |
| TM74 | Heavy Slam | Loudred, Mawile, Scizor, Kingambit, Bisharp, Excadrill, Durant, SandslashAlola, Klinklang | Zware Steel-types (Loudred is Electric/Steel in deze rom). |
| TM75 | Energy Ball | Applin, Rotom | Grass-types (Applin-lijn kan het verder wel; Rotom heeft Grass in deze rom). |
| TM76 | Bug Buzz | Crustle, Shuckle, Kricketot, Paras | Bug-types; Kricketot zoemt al, Kricketune kan het wel. |
| TM77 | Hex | Parasect, Honedge, Doublade, Aegislash, Annihilape, Oricorio, Dreepy | Ghost in deze rom (Parasect) of Ghost-types zonder Hex. |
| TM80 | Focus Blast | Spinda, Farfetchd, Tyrogue | Fighting in deze rom. |
| TM81 | Knock Off | Gyarados, Huntail, Sharpedo, Carvanha, Mightyena, Poochyena, Honchkrow, Murkrow, Kingambit, Deino, Zweilous, Sandile, Spiritomb | Dark-types (Gyarados/Huntail zijn Dark in deze rom) met fysieke aanvallen. |
| TM84 | Stone Edge | Sableye, Anorith | Sableye is Rock/Ghost/Dark in deze rom (fysiek); Anorith-lijn (Armaldo kan het al). |
| TM85 | High Horsepower | Dodrio, Doduo, Muk, Grimer, Golurk, Golett, Cubone, Marowak, Marshtomp, Seismitoad, Trapinch, Garchomp, Gible, Gabite, Larvitar, TingLu, Dunsparce, Dudunsparce | Ground in deze rom (Doduo-lijn, Grimer-lijn, Dunsparce) of zware stampers. |
| TM86 | Dragon Dance | Druddigon, Gible, Gabite, Garchomp, Deino, Zweilous, Dracozolt, Dracovish, Frigibax, Arctibax, Koraidon, Giratina, Guzzlord | Fysieke Dragon-types zonder setup-move. |
| TM87 | Close Combat | Throh, Tyrogue, Pancham, Pawmo, Stufful, Spinda | Fighting-types (Spinda in deze rom); de eindvormen kunnen het al. |
| TM93 | Power Gem | Kabuto, Amaura, Aurorus, Golem, Shuckle | Fossielen/stenen; Aurorus heeft kristallen aan zijn lijf. |
| TM94 | Wood Hammer | Grovyle, Sceptile, Treecko, Leavanny, Tsareena, Gogoat, Sawsbuck, Ferrothorn, Victreebel, Cacturne, Kecleon | Fysieke Grass-types met een stevig lijf of stam (Kecleon is Grass in deze rom). |
| TM95 | Dragon Rush | Applin | Dragon-type; Flapple kan het al. |
| TM98 | Fake Out | Blaziken, Combusken, Emboar, Breloom, Heracross, Gallade, Poliwrath, Chesnaught, Quaquaval, Okidogi, Clobbopus, Grapploct | Fighting-types met handen die nu geen Fake Out hebben. |
| TM100 | Super Splash | Wailord, Gyarados, Milotic | Leren Splash niet via level-up (dus nu uitgesloten), maar hun voorvorm wel: lijn gelijktrekken. |

Niet voorgesteld: Substitute, Baton Pass en Swords Dance (vrijwel iedereen die het logisch kan, kan het al), Earth Power en
Shell Smash (geen logische ontbrekers).
