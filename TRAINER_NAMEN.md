# Trainernamen: welke constante hoort bij welk personage

Sinds v0.9.84 heten de constanten naar het personage dat je in de game ziet (niet meer naar de vanilla-trainer
wiens plek hij inneemt). Alleen de **namen** zijn veranderd: nummers, tabelvolgorde, flagnummers en de save-indeling
zijn gelijk gebleven (de ROM was byte voor byte identiek), dus oude saves werken gewoon.

Handig om te weten:
- **Verslagen-flag** van een trainer = `TRAINER_FLAGS_START` (0x500) + het trainernummer. Er is geen aparte
  `FLAG_DEFEATED_<NAAM>`; scripts gebruiken `goto_if_defeated TRAINER_X` / `call_if_defeated TRAINER_X`.
- **Match Call-registratie** = `FLAG_REGISTERED_<NAAM>` = `TRAINER_REGISTERED_FLAGS_START` (0x15C) + rematch-index.
- **Labels in de kaartscripts:** `*_EventScript_*`-labels zijn mee hernoemd; de **tekstlabels** (`*_Text_*`) niet,
  omdat de Dialoogstudio daarop sleutelt (bijv. `SootopolisCity_Gym_1F_Text_JuanIntro` is gewoon Wallace' tekst,
  `Route111_Text_WiltonIntro` die van Charles).
- Hernoemd in v0.9.84; in `CHANGELOG.md` staan van vóór die versie nog de oude namen.

## Gymleider 8 en de kampioen

In deze romhack is **Wallace gymleider 8** (Sootopolis) en **Steven de kampioen**. Juan bestaat nog als losse
trainer op Route 129.

| Personage | Constante(n) | Oude naam | Nummer | Verslagen-flag | Waar |
|---|---|---|---|---|---|
| Wallace (gymleider 8) | `TRAINER_WALLACE_1` | (zelfde) | 272 | 0x610 | Sootopolis Gym (`SootopolisCity_Gym_1F/scripts.inc`) |
| Wallace (gym-rematches) | `TRAINER_WALLACE_2` … `TRAINER_WALLACE_5` | `TRAINER_JUAN_2` … `_5` | 798–801 | 0x81E–0x821 | rematch-tabel (`src/battle_setup.c`); `WALLACE_5` in het Stadium (`WALLACE`). Sinds v0.9.85 ook `Name: WALLACE` / `Pic: Champion Wallace` |
| Steven (kampioen) | `TRAINER_CHAMPION_STEVEN` | (zelfde) | 855 | 0x857 | `EverGrandeCity_ChampionsRoom` |
| Steven (post-game) | `TRAINER_STEVEN` | (zelfde) | 804 | 0x824 + `FLAG_DEFEATED_METEOR_FALLS_STEVEN` | Meteor Falls, Steven's Cave; Stadium |
| (vrijgemaakt) | `TRAINER_RIVAL_POSTGAME_TREECKO` | `TRAINER_WALLACE_OLD_CHAMPION` (vanilla `TRAINER_WALLACE`) | 335 | 0x64F | sinds de post-game rivaal (zie "Rivaal na de Hall of Fame"); de rematch-rij `REMATCH_OLD_CHAMPION` is nu leeg (`TRAINER_NONE`) |
| Juan | `TRAINER_JUAN` | `TRAINER_REED` | 675 | 0x7A3 | Route 129 (`Route129_EventScript_Juan`), FRLG-gymleidermuziek; Stadium (`JUAN`, op de oude poolplek van het vanilla-kampioenteam) |

Bijbehorende constanten van gym 8 (Wallace):

| Wat | Nieuwe naam | Oude naam | Waarde |
|---|---|---|---|
| Rematch-index | `REMATCH_WALLACE` | `REMATCH_JUAN` | 72 |
| Match Call geregistreerd | `FLAG_REGISTERED_WALLACE` | `FLAG_REGISTERED_JUAN` | 0x15C + 72 = 0x1A4 |
| Match Call aan (na de badge) | `FLAG_ENABLE_WALLACE_MATCH_CALL` | `FLAG_ENABLE_JUAN_MATCH_CALL` | 0x1D9 |
| Rematch vandaag al gewonnen | `FLAG_DAILY_REMATCH_WALLACE` | `FLAG_DAILY_REMATCH_JUAN` | `DAILY_FLAGS_START` + 0x1C |
| Match Call-contact | `MC_HEADER_WALLACE`, `sWallaceMatchCallHeader`, `sWallaceTextScripts` | `MC_HEADER_JUAN`, `sJuan…` | `src/pokenav_match_call_data.c` |
| Match Call-teksten | `MatchCall_Text_Wallace1` … `4` | `MatchCall_Text_Juan1` … `4` | `data/text/match_call.inc` |
| Match Call-profiel | `MCFLAVOR(DandyCharm_Wallace)` | `DandyCharm_Juan` | `src/data/text/match_call_messages.h` |
| Weigertekst rematch | `sText_RefuseWallace` | `sText_RefuseJuan` | `src/gym_leader_rematch.c` |
| Gymscript | `SootopolisCity_Gym_1F_EventScript_Wallace(Defeated/Rematch)` | `…_EventScript_Juan…` | |
| Gevechtsmuziek | `MUS_GROUNDED_VS_WALLACE` voor `TRAINER_WALLACE_1` … `_5` | | `GetTrainerBattleBGM` in `src/pokemon.c` |
| Badge/gym verslagen | `FLAG_BADGE08_GET`, `FLAG_DEFEATED_SOOTOPOLIS_GYM` | (zelfde) | |

Het oude kampioen-slot (vanilla: Wallace als kampioen):

| Wat | Nieuwe naam | Oude naam | Waarde |
|---|---|---|---|
| Rematch-index (Ever Grande) | `REMATCH_OLD_CHAMPION` | `REMATCH_WALLACE` | 77 |
| Match Call geregistreerd | `FLAG_REGISTERED_OLD_CHAMPION` | `FLAG_REGISTERED_WALLACE` | 0x1A9 |
| Match Call-contact | `MC_HEADER_OLD_CHAMPION`, `sOldChampion…`, `MatchCall_Text_OldChampion`, `MCFLAVOR(OldChampion_Wallace)` | `MC_HEADER_WALLACE`, `sWallace…`, `MatchCall_Text_Wallace`, `Champion_Wallace` | lege plek: `MatchCall_GetEnabled` geeft altijd FALSE (Steven staat al als `MC_HEADER_STEVEN` in de lijst) |
| Steven in de kampioenszaal | `LOCALID_CHAMPIONS_ROOM_STEVEN` | `LOCALID_CHAMPIONS_ROOM_WALLACE` | object 1 |
| Kampioenszaal-scripts | `EverGrandeCity_ChampionsRoom_EventScript_Steven`, `_Movement_PlayerApproachSteven`, `_Movement_StevenExit(Start)` | `…Wallace…` | tekstlabels `_Text_WallaceComeWithMe`/`_Text_WallaceWaitOutside` niet hernoemd (Steven-teksten) |
| Steven in de Hall of Fame | `LOCALID_HALL_OF_FAME_STEVEN` (sprite `OBJ_EVENT_GFX_STEVEN`) | `LOCALID_HALL_OF_FAME_WALLACE` | object 1 |

Battle Stadium (`tools/grounded/stadium/pool.py`): `WALLACE` = gymleider Wallace (`TRAINER_WALLACE_5`, partner
`PARTNER_STADIUM_WALLACE`), `JUAN` = Juan van Route 129 (`TRAINER_JUAN`, `PARTNER_STADIUM_JUAN`), `STEVEN` = Steven
(post-game-team `TRAINER_STEVEN`). Het oude kampioenteam van Wallace zit er niet meer in.

**Let op, `REMATCH_WALLACE` en `FLAG_REGISTERED_WALLACE` betekenen nu gymleider Wallace**, niet meer het
kampioen-slot zoals in vanilla Emerald (en in oudere uitleg op internet).

## Charles (Route 111, met Match Call en rematches)

| Wat | Nieuwe naam | Oude naam | Waarde |
|---|---|---|---|
| Trainer | `TRAINER_CHARLES_1` … `TRAINER_CHARLES_5` | `TRAINER_WILTON_1` … `_5` | 78, 84–87 (flags 0x54E, 0x554–0x557) |
| Rematch-index | `REMATCH_CHARLES` | `REMATCH_WILTON` | 8 |
| Match Call geregistreerd | `FLAG_REGISTERED_CHARLES` | `FLAG_REGISTERED_WILTON` | 0x164 |
| Match Call-profiel | `MCFLAVOR(Cooltrainer_Charles)` | `Cooltrainer_Wilton` | |
| Scripts | `Route111_EventScript_Charles`, `_RegisterCharles`, `_RematchCharles` | `…Wilton` | |

## Overige trainers met een eigen naam

| Naam in de game | Constante | Oude naam | Nummer | Verslagen-flag | Waar |
|---|---|---|---|---|---|
| Gi-Hun | `TRAINER_GI_HUN` | `TRAINER_RANDALL` | 71 | 0x547 | Cooltrainer, Petalburg Gym |
| Jonas | `TRAINER_JONAS_PETALBURG` | `TRAINER_PARKER` | 72 | 0x548 | Cooltrainer, Petalburg Gym (`TRAINER_JONAS` = Ninja Boy op Route 123) |
| Harvey | `TRAINER_HARVEY` | `TRAINER_GEORGE` | 73 | 0x549 | Cooltrainer, Petalburg Gym |
| Horatio | `TRAINER_HORATIO` | `TRAINER_BERKE` | 74 | 0x54A | Cooltrainer, Petalburg Gym |
| Daenarys | `TRAINER_DAENARYS` | `TRAINER_MARY` | 89 | 0x559 | Cooltrainer, Petalburg Gym |
| Michonne | `TRAINER_MICHONNE` | `TRAINER_ALEXIA` | 90 | 0x55A | Cooltrainer, Petalburg Gym |
| Eleven | `TRAINER_ELEVEN` | `TRAINER_JODY` | 91 | 0x55B | Cooltrainer, Petalburg Gym |
| Tito | `TRAINER_TITO` | `TRAINER_TAKAO` | 179 | 0x5B3 | Black Belt, Dewford Gym |
| Romero | `TRAINER_ROMERO` | `TRAINER_JOCELYN` | 425 | 0x6A9 | Black Belt, Dewford Gym |
| McGregor | `TRAINER_MCGREGOR` | `TRAINER_LAURA` | 426 | 0x6AA | Black Belt, Dewford Gym |
| Bas Rutten | `TRAINER_BAS_RUTTEN` | `TRAINER_BRENDEN` | 572 | 0x73C | Sailor, Dewford Gym |
| Rogan | `TRAINER_ROGAN` | `TRAINER_LILITH` | 573 | 0x73D | Black Belt, Dewford Gym |
| Chael (was Cristian) | `TRAINER_CHAEL` | `TRAINER_CRISTIAN` | 574 | 0x73E | Black Belt, Dewford Gym |
| Dio | `TRAINER_DIO` | `TRAINER_MARC` | 571 | 0x73B | Dragon Tamer, Rustboro Gym |
| Uri | `TRAINER_URI` | `TRAINER_PRESTON` | 233 | 0x5E9 | Psychic, Mossdeep Gym |
| Blackmore | `TRAINER_BLACKMORE` | `TRAINER_MARCOS` | 702 | 0x7BE | Guitarist, Route 103 |
| Armstrong | `TRAINER_ARMSTRONG` | `TRAINER_ANTHONY` | 352 | 0x660 | Triathlete, Route 110 |
| Violet | `TRAINER_VIOLET_COOLTRAINER` | `TRAINER_JAZMYN` | 503 | 0x6F7 | Cooltrainer, Route 123 (`TRAINER_VIOLET` = Aroma Lady op dezelfde route) |
| Scarlet | `TRAINER_SCARLET` | `TRAINER_WENDY` | 92 | 0x55C | Cooltrainer, Route 123 |
| Dave | `TRAINER_DAVE` | `TRAINER_ALBERT` | 80 | 0x550 | Cooltrainer, Victory Road 1F (zijn 4e gevecht) + Stadium (`PARTNER_STADIUM_DAVE`); post-game praat hij op een ligstoel in het Paradiso Resort |
| Mitch | `TRAINER_MITCH` | `TRAINER_SAMUEL` | 81 | 0x551 | Cooltrainer, Victory Road B1F + Stadium (`PARTNER_STADIUM_MITCH`) |
| SickBlik | `TRAINER_SICKBLIK` | `TRAINER_OWEN` | 83 | 0x553 | Cooltrainer, Victory Road B2F + Stadium (`PARTNER_STADIUM_SICKBLIK`) |
| Dave | `TRAINER_DAVE_PARADISO` | (nieuw) | 1089 | 0x941 | post-game comeback op zijn ligstoel in het Paradiso Resort (18, 34), lv 100, eenmalig |
| SickBlik | `TRAINER_SICKBLIK_DEV` | (nieuw) | 1185 | 0x9A1 | post-game 'developer', per dag in Mauville (3, 9) / Fortree (5, 9) / Lilycove (10, 26) / Pacifidlog (1, 14) (`Grounded_SickBlikSpot`, objectflag `FLAG_HIDE_SICKBLIK_DEV`), lv 100, eenmalig; script `data/scripts/sickblik_dev.inc` |
| Kapitein Grimsby | `TRAINER_GRIMSBY` | (nieuw) | 1054 | 0x91E | Sailor, spookschip S.S. AGAVE (`GhostShip_CaptainsOffice`, 's nachts via Shipwreck Shoals) + Stadium (`PARTNER_STADIUM_GRIMSBY`) |
| Spookzeelieden Silas, Morgan, Ned, Percy | `TRAINER_GHOST_SAILOR_SILAS` … `_PERCY` | (nieuw) | 1050–1053 | 0x91A–0x91D | spookschip (dek, gang, hutten) |
| Garrett | `TRAINER_HOLLOW_GERRIT` | (nieuw; heette in de game Gerrit, constante en tekstlabels `*_Gerrit*` bewust niet hernoemd) | 991 | 0x8DF | Hiker, Toadstool Hollow (via Petalburg Woods) |

De scriptlabels volgen dezelfde namen (bijv. `PetalburgCity_Gym_EventScript_GiHun`,
`DewfordTown_Gym_EventScript_CheckRomero`, `VictoryRoad_B2F_EventScript_SickBlik`); de tekstlabels niet (zie boven).

Niet hernoemd, omdat de naam een rol beschrijft en niet misleidt: `TRAINER_LOCAL_CELEBRITY` (Brad),
`TRAINER_DRACONID_ELDER` (Selene), `TRAINER_DOJO_*`, `TRAINER_BURGLAR_*` / `TRAINER_STADIUM_BURGLAR` (Simon),
`TRAINER_STADIUM_SHY_GUY_*`, de duo's (`TRAINER_X_AND_Y`) en de generieke grunts/admins.

## Extra gevechten in de wereld (`tools/grounded/maptools/extra_fights.py`)

Zelfde personage, eerder in de game, met dezelfde muziek, mugshot en transitie als hun bestaande gevecht. Objecten heten
`LOCALID_EF_<CONSTANTE>`, scripts `<Kaart>_EventScript_EF_<Naam>`, teksten `<Kaart>_Text_EF_<Naam>Intro/Defeat/PostBattle`.
Verslagen-flag = 0x500 + nummer (Wally's objecten gebruiken die ook als verberg-flag).

| Personage | Constante | Nummer | Waar (x, y) | Levels |
|---|---|---|---|---|
| Wally | `TRAINER_WALLY_MT_PYRE` | 1134 | Mt. Pyre 1F (9, 4); verdwijnt na zijn nederlaag; thema Wally 3 | 42, Gallade 44 |
| Wally | `TRAINER_WALLY_MOSSDEEP` | 1135 | Mossdeep, voor het Space Center (68, 17); verdwijnt na zijn nederlaag; thema Wally 4 | 47, Gallade 49 |
| Zinnia | `TRAINER_ZINNIA_ROUTE_114` | 1136 | Route 114, bij de ingang van Meteor Falls (22, 34) | 25, Bagon 27 |
| Zinnia | `TRAINER_ZINNIA_ROUTE_119` | 1137 | Route 119, noordkant richting Fortree (33, 10) | 36, Shelgon 38 |
| Dave | `TRAINER_DAVE_ROUTE_111` | 1138 | Route 111 zuid, naast het pad vanaf Mauville (26, 117); vóór Wattson; verdwijnt na zijn nederlaag | 22, Pawniard 23 |
| Dave | `TRAINER_DAVE_PETALBURG` | 1139 | Petalburg, voor de gymdeur (15, 9); na badge 4 tot je wint (objectflag `FLAG_TEMP_9`, gezet in `PetalburgCity_OnTransition`) | 31, Pawniard 32 |
| Mitch | `TRAINER_MITCH_ROUTE_110` | 1140 | Route 110, plein boven Slateport (20, 54) | 23, Marshtomp 24 |
| Mitch | `TRAINER_MITCH_ROUTE_121` | 1141 | Route 121 (50, 13) | 39, Swampert 40 |
| SickBlik | `TRAINER_SICKBLIK_ROUTE_104` | 1142 | Route 104 noord, bij de uitgang van Petalburg Woods (14, 26) | 12, Remoraid 13 |
| SickBlik | `TRAINER_SICKBLIK_ROUTE_113` | 1143 | Route 113, oostkant (70, 13) | 26, Octillery 27 |
| SickBlik | `TRAINER_SICKBLIK_MOTEL` | 1184 | Cove Lily Motel 1F (Lilycove), aan tafel (1, 4); ja/nee-gevecht | 56, Galar-Slowbro 57 |
| SickBlik | `TRAINER_SICKBLIK_BEACH` | 854 (was `TRAINER_MAY_PLACEHOLDER`) | Route 104 zuid, strand (25, 76; buiten de looproute van Billy) | 16, Toedscool 17 |
| Shy Guy (rood) | `TRAINER_SHY_GUY_DESERT` | 1144 | Route 111, woestijn: ingegraven achter het rotsblok aan de oostrand (37, 69) | 28, Mr. Mime 29 |
| Dave | `TRAINER_DAVE_SOOTOPOLIS` | 1145 | Sootopolis (32, 35), rechts van de speler aan het begin van de Keccles-scène na Rayquaza (`FLAG_TEMP_9`) | 48, Kingambit 49 |

Wally's thema's (`GetTrainerBattleBGM`): 1 Mauville, 2 Meteor Falls, 3 Mt. Pyre, 4 Mossdeep, 5 Victory Road (+ rematches).
Burglar: `TRAINER_BURGLAR_1` … `_8` = 1–8 badges (979–983, 1146–1148), `_9` = na de Hall of Fame (1149).

**Ghetsis:** `TRAINER_TAO_GHETSIS` (1065) is de verhaalversie (post-league superboss in Frost Hollow op het Tao-eiland,
lv 82–84, geeft de DNA Splicers); `TRAINER_STADIUM_GHETSIS` (978) is de Stadium-versie (lv 50, met Kyurem-Black).
**Tao-eiland** (was Dragonspine Isle, `tools/grounded/maptools/tao_island.py`): `TRAINER_TAO_VERNON`, `_SAELA`, `_OSRIC`,
`_MIRA`, `_TALON` (1060–1064, waren `TRAINER_DRAGONSPINE_*` 1180–1184), `_JUN` (1066), `_YING` (1067). Drakenwachter
Gerald (`TRAINER_GERALD_WARDEN`, 1185) is geschrapt, ook uit het Stadium; 1180–1185 zijn vrij.

**Keccles:** `TRAINER_KECCLES_1` (859, strand Route 115), `_2` (860, onzichtbaar voor de Fortree Gym), `_3` (871,
Route 136; ook in het Stadium) en `TRAINER_KECCLES_FRONTIER` (853, was `TRAINER_BRENDAN_PLACEHOLDER`): post-game op het
Battle Frontier-eiland (oost, (57, 58), onzichtbaar op het pad naar de Sudowoodo, Devon Scope), lv 92–95, ace Salazzle 95.
Vlak voor dat gevecht springt Marshadow (lv 88) uit de schaduw van de speler en komt in je team
(`FLAG_RECEIVED_MARSHADOW`); Keccles verdwijnt na het gevecht (`FLAG_HIDE_FRONTIER_KECCLES`). Alle vier: salsa-thema
en de Keccles-transitie.

## Hall of Origin (`tools/grounded/maptools/hall_of_origin.py`)

De emissaries van Arceus (lv 100, teams van legendaries) gebruiken ongebruikte vanilla-constanten; alleen de naam en
de partij zijn veranderd, het nummer niet (verslagen-flag = 0x500 + nummer).

| Personage | Constante | Oude naam | Nummer | Waar | Thema |
|---|---|---|---|---|---|
| Stratos | `TRAINER_HOO_STRATOS` | `TRAINER_CINDY_2` | 117 | Hall of Origin, trap (onderste trede) | lucht |
| Thalassa | `TRAINER_HOO_THALASSA` | `TRAINER_DUDLEY` | 173 | Hall of Origin, trap (middelste trede) | zee |
| Bedrock | `TRAINER_HOO_BEDROCK` | `TRAINER_KAYLEE` | 462 | Hall of Origin, trap (bovenste trede) | land |
| Nous | `TRAINER_HOO_NOUS` | `TRAINER_AMY_AND_LIV_3` | 485 | Hall of Origin, atrium | geest |
| Somnia | `TRAINER_HOO_SOMNIA` | `TRAINER_GINA_AND_MIA_2` | 486 | Hall of Origin, atrium | dromen |
| Gladius | `TRAINER_HOO_GLADIUS` | `TRAINER_GRUNT_UNUSED` | 568 | Hall of Origin, atrium | rechtvaardigheid |
| Hephaest | `TRAINER_HOO_HEPHAEST` | `TRAINER_TERRY` | 581 | Hall of Origin, atrium | vuur/smidse |
| Ordo | `TRAINER_HOO_ORDO` | `TRAINER_LUCAS_2` | 633 | Hall of Origin, top | orde (de Regi's) |
| Kairos | `TRAINER_HOO_KAIROS` | `TRAINER_MIKE_1` | 634 | Hall of Origin, top | tijd en ruimte |

Arceus (top) vecht pas als alle negen verslagen zijn.

## Rivaal na de Hall of Fame (`src/rival_postgame.c`, `src/data/rival_postgame.party`)

De trainer-id's waren op, dus de post-game rivaal heeft er maar **drie**, een per starter van de speler (zelfde
benaming als de andere rivaalgevechten: de naam is de starter van de speler, de rivaal heeft de starter die daarvan wint).
`GetTrainerStructFromId` (`include/data.h`) stuurt deze drie naar `GetRivalPostgameTrainer`, dat uit twaalf teams kiest:
BRENDAN of MAY (geslacht van de speler) × fase 1 (Pacifidlog) of fase 2 (Battle Tower + dagelijks Paradiso, na
`FLAG_RIVAL_PG_PACIFIDLOG_DONE`). De blokken in `trainers.party` (Brendan, fase 1) zijn er alleen voor de tools en de
testrunner (onder `TESTING` staat de omleiding uit). Verslagen-flag wordt gedeeld door alle fasen; scripts gebruiken hem niet.

| Constante | Oude naam | Nummer | Verslagen-flag | Waar |
|---|---|---|---|---|
| `TRAINER_RIVAL_POSTGAME_TREECKO` | `TRAINER_WALLACE_OLD_CHAMPION` | 335 | 0x64F | Pacifidlog (18, 14), Battle Tower (OutsideEast 18, 16), Paradiso Resort (27, 9) |
| `TRAINER_RIVAL_POSTGAME_TORCHIC` | `TRAINER_RED` (alleen de testrunner) | 851 | 0x853 | idem |
| `TRAINER_RIVAL_POSTGAME_MUDKIP` | `TRAINER_LEAF` (alleen de testrunner) | 852 | 0x854 | idem |
| Psychic Dua (zweeft op het water, zingt Levitating) | `TRAINER_DUA` | `TRAINER_SPENCER` | 159 | 0x59F | Route 124 (`Route124/scripts.inc`) |

Flags: `FLAG_RIVAL_PG_PACIFIDLOG_DONE` (gevecht 7), `FLAG_RIVAL_PG_RETIRED` (gevecht 8, verhuisd naar Paradiso),
`FLAG_RIVAL_PG_RESORT_MET` (Guinness-verhaal gehoord), `FLAG_DAILY_REMATCH_RIVAL` (vandaag al verslagen). Levels: fase 1
86 (ace 88), fase 2 92 (ace 94).

## Nieuwe trainer of hernoeming

Hernoem met een script over alle bestanden (behalve `CHANGELOG.md`), draai daarna
`tools/grounded/stadium/pool.py` en `announcer.py`, en vergelijk de ROM vóór en na met `cmp`: die moet identiek zijn.
