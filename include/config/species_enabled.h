#ifndef GUARD_CONFIG_SPECIES_ENABLED_H
#define GUARD_CONFIG_SPECIES_ENABLED_H

// Modifying the latest generation WILL change the saveblock due to Dex flags and will require a new save file.
// Generations of Pokémon are defined by the first member introduced,
// so Pikachu depends on the Gen 1 setting despite Pichu being the lowest member of the evolution tree.
// Eg: If P_GEN_2_POKEMON is set to FALSE, all members of the Sneasel Family will be disabled
// (Sneasel + Hisuian, Weavile and Sneasler).
#define P_GEN_1_POKEMON                  TRUE // Generation 1 Pokémon (RGBY)
#define P_GEN_2_POKEMON                  TRUE // Generation 2 Pokémon (GSC)
#define P_GEN_3_POKEMON                  TRUE // Generation 3 Pokémon (RSE, FRLG)
#define P_GEN_4_POKEMON                  TRUE // Generation 4 Pokémon (DPPt, HGSS)
#define P_GEN_5_POKEMON                  TRUE // Generation 5 Pokémon (BW, B2W2)
#define P_GEN_6_POKEMON                  TRUE // Generation 6 Pokémon (XY, ORAS)
#define P_GEN_7_POKEMON                  TRUE // Generation 7 Pokémon (SM, USUM, LGPE)
#define P_GEN_8_POKEMON                  TRUE // Generation 8 Pokémon (SwSh, BDSP, LA)
#define P_GEN_9_POKEMON                  TRUE // Generation 9 Pokémon (SV)

// Setting this to TRUE will add the new evolutions to the Regional Dex.
#define P_NEW_EVOS_IN_REGIONAL_DEX       TRUE

// Battle gimmick specific Forms.
#define P_MEGA_EVOLUTIONS                FALSE // Fully Ungrounded: uit (stond aan voor de Spire, die is weg)
#define P_PRIMAL_REVERSIONS              FALSE // Groudon and Kyogre only.
#define P_ULTRA_BURST_FORMS              FALSE // Ultra Necrozma only. Fully Ungrounded: uit
#define P_GIGANTAMAX_FORMS               FALSE // Fully Ungrounded: uit
#define P_TERA_FORMS                     FALSE // Fully Ungrounded: uit

#define P_GEN_9_MEGA_EVOLUTIONS          P_MEGA_EVOLUTIONS // Mega Evolutions introduced in Z-A and its DLC

// Fusion forms
#define P_FUSION_FORMS                   TRUE

// Regional Forms. Includes Regional Form evolutions, like Sirfetch'd.
#define P_REGIONAL_FORMS                 TRUE
#define P_ALOLAN_FORMS                   P_REGIONAL_FORMS
#define P_GALARIAN_FORMS                 P_REGIONAL_FORMS
#define P_HISUIAN_FORMS                  P_REGIONAL_FORMS
#define P_PALDEAN_FORMS                  P_REGIONAL_FORMS

// Big groups of forms that aren't always desired when choosing families.
#define P_PIKACHU_EXTRA_FORMS            FALSE // Fully Ungrounded: cosplay- en cap-Pikachu uit
#define P_COSPLAY_PIKACHU_FORMS          P_PIKACHU_EXTRA_FORMS
#define P_CAP_PIKACHU_FORMS              P_PIKACHU_EXTRA_FORMS

// Cross-generation evolutions. Includes pre-evolutions.
#define P_CROSS_GENERATION_EVOS          TRUE
#define P_GEN_2_CROSS_EVOS               P_CROSS_GENERATION_EVOS
#define P_GEN_3_CROSS_EVOS               P_CROSS_GENERATION_EVOS
#define P_GEN_4_CROSS_EVOS               P_CROSS_GENERATION_EVOS
//#define P_GEN_5_CROSS_EVOS             // Gen 5 didn't introduce any cross-gen evos.
#define P_GEN_6_CROSS_EVOS               P_CROSS_GENERATION_EVOS // Just Sylveon.
//#define P_GEN_7_CROSS_EVOS             // Alolan evolutions handled by P_ALOLAN_FORMS.
#define P_GEN_8_CROSS_EVOS               P_CROSS_GENERATION_EVOS // Regional evolutions handled by P_GALARIAN_FORMS and P_HISUIAN_FORMS.
#define P_GEN_9_CROSS_EVOS               P_CROSS_GENERATION_EVOS // Clodsire handled by P_PALDEAN_FORMS.

// To disable specific families, replace P_GEN_x_POKEMON with FALSE.
#define P_FAMILY_BULBASAUR               FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_CHARMANDER              FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_SQUIRTLE                FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_CATERPIE                P_GEN_1_POKEMON
#define P_FAMILY_WEEDLE                  FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_PIDGEY                  FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_RATTATA                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_SPEAROW                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_EKANS                   FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_PIKACHU                 P_GEN_1_POKEMON
#define P_FAMILY_SANDSHREW               P_GEN_1_POKEMON
#define P_FAMILY_NIDORAN                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_CLEFAIRY                P_GEN_1_POKEMON
#define P_FAMILY_VULPIX                  P_GEN_1_POKEMON
#define P_FAMILY_JIGGLYPUFF              FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_ZUBAT                   FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_ODDISH                  P_GEN_1_POKEMON
#define P_FAMILY_PARAS                   P_GEN_1_POKEMON
#define P_FAMILY_VENONAT                 P_GEN_1_POKEMON
#define P_FAMILY_DIGLETT                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_MEOWTH                  P_GEN_1_POKEMON
#define P_FAMILY_PSYDUCK                 P_GEN_1_POKEMON
#define P_FAMILY_MANKEY                  P_GEN_1_POKEMON
#define P_FAMILY_GROWLITHE               P_GEN_1_POKEMON
#define P_FAMILY_POLIWAG                 P_GEN_1_POKEMON
#define P_FAMILY_ABRA                    P_GEN_1_POKEMON
#define P_FAMILY_MACHOP                  P_GEN_1_POKEMON
#define P_FAMILY_BELLSPROUT              P_GEN_1_POKEMON
#define P_FAMILY_TENTACOOL               P_GEN_1_POKEMON
#define P_FAMILY_GEODUDE                 P_GEN_1_POKEMON
#define P_FAMILY_PONYTA                  P_GEN_1_POKEMON
#define P_FAMILY_SLOWPOKE                P_GEN_1_POKEMON
#define P_FAMILY_MAGNEMITE               P_GEN_1_POKEMON
#define P_FAMILY_FARFETCHD               FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_DODUO                   P_GEN_1_POKEMON
#define P_FAMILY_SEEL                    P_GEN_1_POKEMON
#define P_FAMILY_GRIMER                  P_GEN_1_POKEMON
#define P_FAMILY_SHELLDER                P_GEN_1_POKEMON
#define P_FAMILY_GASTLY                  P_GEN_1_POKEMON
#define P_FAMILY_ONIX                    FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_DROWZEE                 P_GEN_1_POKEMON
#define P_FAMILY_KRABBY                  P_GEN_1_POKEMON
#define P_FAMILY_VOLTORB                 P_GEN_1_POKEMON
#define P_FAMILY_EXEGGCUTE               P_GEN_1_POKEMON
#define P_FAMILY_CUBONE                  P_GEN_1_POKEMON
#define P_FAMILY_HITMONS                 P_GEN_1_POKEMON
#define P_FAMILY_LICKITUNG               FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_KOFFING                 P_GEN_1_POKEMON
#define P_FAMILY_RHYHORN                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_CHANSEY                 P_GEN_1_POKEMON
#define P_FAMILY_TANGELA                 P_GEN_1_POKEMON
#define P_FAMILY_KANGASKHAN              FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_HORSEA                  P_GEN_1_POKEMON
#define P_FAMILY_GOLDEEN                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_STARYU                  P_GEN_1_POKEMON
#define P_FAMILY_MR_MIME                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_SCYTHER                 P_GEN_1_POKEMON
#define P_FAMILY_JYNX                    FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_ELECTABUZZ              FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_MAGMAR                  FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_PINSIR                  P_GEN_1_POKEMON
#define P_FAMILY_TAUROS                  P_GEN_1_POKEMON
#define P_FAMILY_MAGIKARP                P_GEN_1_POKEMON
#define P_FAMILY_LAPRAS                  P_GEN_1_POKEMON
#define P_FAMILY_DITTO                   P_GEN_1_POKEMON
#define P_FAMILY_EEVEE                   P_GEN_1_POKEMON
#define P_FAMILY_PORYGON                 P_GEN_1_POKEMON
#define P_FAMILY_OMANYTE                 FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_KABUTO                  FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_AERODACTYL              FALSE // FU: niet in de dex (was P_GEN_1_POKEMON)
#define P_FAMILY_SNORLAX                 P_GEN_1_POKEMON
#define P_FAMILY_DRATINI                 P_GEN_1_POKEMON

#define P_FAMILY_CHIKORITA               FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_CYNDAQUIL               FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_TOTODILE                FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_SENTRET                 FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_HOOTHOOT                P_GEN_2_POKEMON
#define P_FAMILY_LEDYBA                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_SPINARAK                P_GEN_2_POKEMON
#define P_FAMILY_CHINCHOU                P_GEN_2_POKEMON
#define P_FAMILY_TOGEPI                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_NATU                    P_GEN_2_POKEMON
#define P_FAMILY_MAREEP                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_MARILL                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_SUDOWOODO               FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_HOPPIP                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_AIPOM                   P_GEN_2_POKEMON
#define P_FAMILY_SUNKERN                 FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_YANMA                   P_GEN_2_POKEMON
#define P_FAMILY_WOOPER                  P_GEN_2_POKEMON
#define P_FAMILY_MURKROW                 FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_MISDREAVUS              P_GEN_2_POKEMON
#define P_FAMILY_UNOWN                   P_GEN_2_POKEMON
#define P_FAMILY_WOBBUFFET               FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_GIRAFARIG               FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_PINECO                  P_GEN_2_POKEMON
#define P_FAMILY_DUNSPARCE               P_GEN_2_POKEMON
#define P_FAMILY_GLIGAR                  P_GEN_2_POKEMON
#define P_FAMILY_SNUBBULL                FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_QWILFISH                P_GEN_2_POKEMON
#define P_FAMILY_SHUCKLE                 FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_HERACROSS               P_GEN_2_POKEMON
#define P_FAMILY_SNEASEL                 P_GEN_2_POKEMON
#define P_FAMILY_TEDDIURSA               P_GEN_2_POKEMON
#define P_FAMILY_SLUGMA                  P_GEN_2_POKEMON
#define P_FAMILY_SWINUB                  P_GEN_2_POKEMON
#define P_FAMILY_CORSOLA                 P_GEN_2_POKEMON
#define P_FAMILY_REMORAID                P_GEN_2_POKEMON
#define P_FAMILY_DELIBIRD                FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_MANTINE                 P_GEN_2_POKEMON
#define P_FAMILY_SKARMORY                P_GEN_2_POKEMON
#define P_FAMILY_HOUNDOUR                P_GEN_2_POKEMON
#define P_FAMILY_PHANPY                  FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_STANTLER                FALSE // FU: niet in de dex (was P_GEN_2_POKEMON)
#define P_FAMILY_SMEARGLE                P_GEN_2_POKEMON
#define P_FAMILY_MILTANK                 P_GEN_2_POKEMON
#define P_FAMILY_LARVITAR                P_GEN_2_POKEMON

#define P_FAMILY_TREECKO                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_TORCHIC                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_MUDKIP                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_POOCHYENA               FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_ZIGZAGOON               FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_WURMPLE                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_LOTAD                   P_GEN_3_POKEMON
#define P_FAMILY_SEEDOT                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_TAILLOW                 P_GEN_3_POKEMON
#define P_FAMILY_WINGULL                 P_GEN_3_POKEMON
#define P_FAMILY_RALTS                   FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_SURSKIT                 P_GEN_3_POKEMON
#define P_FAMILY_SHROOMISH               P_GEN_3_POKEMON
#define P_FAMILY_SLAKOTH                 P_GEN_3_POKEMON
#define P_FAMILY_NINCADA                 P_GEN_3_POKEMON
#define P_FAMILY_WHISMUR                 P_GEN_3_POKEMON
#define P_FAMILY_MAKUHITA                FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_NOSEPASS                P_GEN_3_POKEMON
#define P_FAMILY_SKITTY                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_SABLEYE                 P_GEN_3_POKEMON
#define P_FAMILY_MAWILE                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_ARON                    P_GEN_3_POKEMON
#define P_FAMILY_MEDITITE                FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_ELECTRIKE               FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_PLUSLE                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_MINUN                   FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_VOLBEAT_ILLUMISE        P_GEN_3_POKEMON
#define P_FAMILY_ROSELIA                 P_GEN_3_POKEMON
#define P_FAMILY_GULPIN                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_CARVANHA                P_GEN_3_POKEMON
#define P_FAMILY_WAILMER                 P_GEN_3_POKEMON
#define P_FAMILY_NUMEL                   FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_TORKOAL                 P_GEN_3_POKEMON
#define P_FAMILY_SPOINK                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_SPINDA                  P_GEN_3_POKEMON
#define P_FAMILY_TRAPINCH                P_GEN_3_POKEMON
#define P_FAMILY_CACNEA                  P_GEN_3_POKEMON
#define P_FAMILY_SWABLU                  P_GEN_3_POKEMON
#define P_FAMILY_ZANGOOSE                P_GEN_3_POKEMON
#define P_FAMILY_SEVIPER                 P_GEN_3_POKEMON
#define P_FAMILY_LUNATONE                P_GEN_3_POKEMON
#define P_FAMILY_SOLROCK                 P_GEN_3_POKEMON
#define P_FAMILY_BARBOACH                P_GEN_3_POKEMON
#define P_FAMILY_CORPHISH                FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_BALTOY                  P_GEN_3_POKEMON
#define P_FAMILY_LILEEP                  FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_ANORITH                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_FEEBAS                  P_GEN_3_POKEMON
#define P_FAMILY_CASTFORM                P_GEN_3_POKEMON
#define P_FAMILY_KECLEON                 P_GEN_3_POKEMON
#define P_FAMILY_SHUPPET                 P_GEN_3_POKEMON
#define P_FAMILY_DUSKULL                 P_GEN_3_POKEMON
#define P_FAMILY_TROPIUS                 P_GEN_3_POKEMON
#define P_FAMILY_CHIMECHO                FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_ABSOL                   P_GEN_3_POKEMON
#define P_FAMILY_SNORUNT                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_SPHEAL                  P_GEN_3_POKEMON
#define P_FAMILY_CLAMPERL                FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_RELICANTH               FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_LUVDISC                 FALSE // FU: niet in de dex (was P_GEN_3_POKEMON)
#define P_FAMILY_BAGON                   P_GEN_3_POKEMON
#define P_FAMILY_BELDUM                  P_GEN_3_POKEMON

#define P_FAMILY_TURTWIG                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_CHIMCHAR                FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_PIPLUP                  FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_STARLY                  FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_BIDOOF                  P_GEN_4_POKEMON
#define P_FAMILY_KRICKETOT               P_GEN_4_POKEMON
#define P_FAMILY_SHINX                   FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_CRANIDOS                FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_SHIELDON                FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_BURMY                   FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_COMBEE                  P_GEN_4_POKEMON
#define P_FAMILY_PACHIRISU               FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_BUIZEL                  P_GEN_4_POKEMON
#define P_FAMILY_CHERUBI                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_SHELLOS                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_DRIFLOON                FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_BUNEARY                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_GLAMEOW                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_STUNKY                  P_GEN_4_POKEMON
#define P_FAMILY_BRONZOR                 P_GEN_4_POKEMON
#define P_FAMILY_CHATOT                  P_GEN_4_POKEMON
#define P_FAMILY_SPIRITOMB               P_GEN_4_POKEMON
#define P_FAMILY_GIBLE                   P_GEN_4_POKEMON
#define P_FAMILY_RIOLU                   FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_HIPPOPOTAS              P_GEN_4_POKEMON
#define P_FAMILY_SKORUPI                 P_GEN_4_POKEMON
#define P_FAMILY_CROAGUNK                P_GEN_4_POKEMON
#define P_FAMILY_CARNIVINE               FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_FINNEON                 FALSE // FU: niet in de dex (was P_GEN_4_POKEMON)
#define P_FAMILY_SNOVER                  P_GEN_4_POKEMON
#define P_FAMILY_ROTOM                   P_GEN_4_POKEMON

#define P_FAMILY_SNIVY                   FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_TEPIG                   FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_OSHAWOTT                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PATRAT                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_LILLIPUP                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PURRLOIN                P_GEN_5_POKEMON
#define P_FAMILY_PANSAGE                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PANSEAR                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PANPOUR                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_MUNNA                   FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PIDOVE                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_BLITZLE                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_ROGGENROLA              FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_WOOBAT                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_DRILBUR                 P_GEN_5_POKEMON
#define P_FAMILY_AUDINO                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_TIMBURR                 P_GEN_5_POKEMON
#define P_FAMILY_TYMPOLE                 P_GEN_5_POKEMON
#define P_FAMILY_THROH                   FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_SAWK                    FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_SEWADDLE                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_VENIPEDE                P_GEN_5_POKEMON
#define P_FAMILY_COTTONEE                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_PETILIL                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_BASCULIN                P_GEN_5_POKEMON
#define P_FAMILY_SANDILE                 P_GEN_5_POKEMON
#define P_FAMILY_DARUMAKA                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_MARACTUS                P_GEN_5_POKEMON
#define P_FAMILY_DWEBBLE                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_SCRAGGY                 P_GEN_5_POKEMON
#define P_FAMILY_SIGILYPH                P_GEN_5_POKEMON
#define P_FAMILY_YAMASK                  P_GEN_5_POKEMON
#define P_FAMILY_TIRTOUGA                FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_ARCHEN                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_TRUBBISH                P_GEN_5_POKEMON
#define P_FAMILY_ZORUA                   P_GEN_5_POKEMON
#define P_FAMILY_MINCCINO                P_GEN_5_POKEMON
#define P_FAMILY_GOTHITA                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_SOLOSIS                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_DUCKLETT                P_GEN_5_POKEMON
#define P_FAMILY_VANILLITE               FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_DEERLING                P_GEN_5_POKEMON
#define P_FAMILY_EMOLGA                  FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_KARRABLAST              FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_FOONGUS                 P_GEN_5_POKEMON
#define P_FAMILY_FRILLISH                P_GEN_5_POKEMON
#define P_FAMILY_ALOMOMOLA               FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_JOLTIK                  P_GEN_5_POKEMON
#define P_FAMILY_FERROSEED               P_GEN_5_POKEMON
#define P_FAMILY_KLINK                   FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_TYNAMO                  P_GEN_5_POKEMON
#define P_FAMILY_ELGYEM                  P_GEN_5_POKEMON
#define P_FAMILY_LITWICK                 P_GEN_5_POKEMON
#define P_FAMILY_AXEW                    FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_CUBCHOO                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_CRYOGONAL               P_GEN_5_POKEMON
#define P_FAMILY_SHELMET                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_STUNFISK                P_GEN_5_POKEMON
#define P_FAMILY_MIENFOO                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_DRUDDIGON               FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_GOLETT                  P_GEN_5_POKEMON
#define P_FAMILY_PAWNIARD                P_GEN_5_POKEMON
#define P_FAMILY_BOUFFALANT              P_GEN_5_POKEMON
#define P_FAMILY_RUFFLET                 P_GEN_5_POKEMON
#define P_FAMILY_VULLABY                 FALSE // FU: niet in de dex (was P_GEN_5_POKEMON)
#define P_FAMILY_HEATMOR                 P_GEN_5_POKEMON
#define P_FAMILY_DURANT                  P_GEN_5_POKEMON
#define P_FAMILY_DEINO                   P_GEN_5_POKEMON
#define P_FAMILY_LARVESTA                P_GEN_5_POKEMON

#define P_FAMILY_CHESPIN                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_FENNEKIN                FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_FROAKIE                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_BUNNELBY                FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_FLETCHLING              FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_SCATTERBUG              P_GEN_6_POKEMON
#define P_FAMILY_LITLEO                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_FLABEBE                 P_GEN_6_POKEMON
#define P_FAMILY_SKIDDO                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_PANCHAM                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_FURFROU                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_ESPURR                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_HONEDGE                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_SPRITZEE                FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_SWIRLIX                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_INKAY                   P_GEN_6_POKEMON
#define P_FAMILY_BINACLE                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_SKRELP                  P_GEN_6_POKEMON
#define P_FAMILY_CLAUNCHER               P_GEN_6_POKEMON
#define P_FAMILY_HELIOPTILE              FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_TYRUNT                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_AMAURA                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_HAWLUCHA                FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_DEDENNE                 FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_CARBINK                 P_GEN_6_POKEMON
#define P_FAMILY_GOOMY                   P_GEN_6_POKEMON
#define P_FAMILY_KLEFKI                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_PHANTUMP                P_GEN_6_POKEMON
#define P_FAMILY_PUMPKABOO               FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)
#define P_FAMILY_BERGMITE                P_GEN_6_POKEMON
#define P_FAMILY_NOIBAT                  FALSE // FU: niet in de dex (was P_GEN_6_POKEMON)

#define P_FAMILY_ROWLET                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_LITTEN                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_POPPLIO                 FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_PIKIPEK                 P_GEN_7_POKEMON
#define P_FAMILY_YUNGOOS                 FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_GRUBBIN                 P_GEN_7_POKEMON
#define P_FAMILY_CRABRAWLER              FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_ORICORIO                P_GEN_7_POKEMON
#define P_FAMILY_CUTIEFLY                FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_ROCKRUFF                FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_WISHIWASHI              FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_MAREANIE                P_GEN_7_POKEMON
#define P_FAMILY_MUDBRAY                 P_GEN_7_POKEMON
#define P_FAMILY_DEWPIDER                P_GEN_7_POKEMON
#define P_FAMILY_FOMANTIS                FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_MORELULL                P_GEN_7_POKEMON
#define P_FAMILY_SALANDIT                P_GEN_7_POKEMON
#define P_FAMILY_STUFFUL                 P_GEN_7_POKEMON
#define P_FAMILY_BOUNSWEET               FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_COMFEY                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_ORANGURU                FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_PASSIMIAN               FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_WIMPOD                  P_GEN_7_POKEMON
#define P_FAMILY_SANDYGAST               P_GEN_7_POKEMON
#define P_FAMILY_PYUKUMUKU               FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_MINIOR                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_KOMALA                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_TURTONATOR              P_GEN_7_POKEMON
#define P_FAMILY_TOGEDEMARU              FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_MIMIKYU                 P_GEN_7_POKEMON
#define P_FAMILY_BRUXISH                 FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_DRAMPA                  FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)
#define P_FAMILY_DHELMISE                P_GEN_7_POKEMON
#define P_FAMILY_JANGMO_O                FALSE // FU: niet in de dex (was P_GEN_7_POKEMON)

#define P_FAMILY_GROOKEY                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SCORBUNNY               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SOBBLE                  FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SKWOVET                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_ROOKIDEE                FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_BLIPBUG                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_NICKIT                  P_GEN_8_POKEMON
#define P_FAMILY_GOSSIFLEUR              FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_WOOLOO                  P_GEN_8_POKEMON
#define P_FAMILY_CHEWTLE                 P_GEN_8_POKEMON
#define P_FAMILY_YAMPER                  FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_ROLYCOLY                P_GEN_8_POKEMON
#define P_FAMILY_APPLIN                  FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SILICOBRA               P_GEN_8_POKEMON
#define P_FAMILY_CRAMORANT               P_GEN_8_POKEMON
#define P_FAMILY_ARROKUDA                P_GEN_8_POKEMON
#define P_FAMILY_TOXEL                   P_GEN_8_POKEMON
#define P_FAMILY_SIZZLIPEDE              P_GEN_8_POKEMON
#define P_FAMILY_CLOBBOPUS               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SINISTEA                FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_HATENNA                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_IMPIDIMP                P_GEN_8_POKEMON
#define P_FAMILY_MILCERY                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_FALINKS                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_PINCURCHIN              FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_SNOM                    P_GEN_8_POKEMON
#define P_FAMILY_STONJOURNER             FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_EISCUE                  P_GEN_8_POKEMON
#define P_FAMILY_INDEEDEE                FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_MORPEKO                 FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_CUFANT                  FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_DRACOZOLT               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_ARCTOZOLT               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_DRACOVISH               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_ARCTOVISH               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_DURALUDON               FALSE // FU: niet in de dex (was P_GEN_8_POKEMON)
#define P_FAMILY_DREEPY                  P_GEN_8_POKEMON

#define P_FAMILY_SPRIGATITO              FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_FUECOCO                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_QUAXLY                  P_GEN_9_POKEMON
#define P_FAMILY_LECHONK                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_TAROUNTULA              FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_NYMBLE                  FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_PAWMI                   FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_TANDEMAUS               FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_FIDOUGH                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_SMOLIV                  FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_SQUAWKABILLY            P_GEN_9_POKEMON
#define P_FAMILY_NACLI                   P_GEN_9_POKEMON
#define P_FAMILY_CHARCADET               P_GEN_9_POKEMON
#define P_FAMILY_TADBULB                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_WATTREL                 P_GEN_9_POKEMON
#define P_FAMILY_MASCHIFF                FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_SHROODLE                FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_BRAMBLIN                P_GEN_9_POKEMON
#define P_FAMILY_TOEDSCOOL               FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_KLAWF                   FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_CAPSAKID                P_GEN_9_POKEMON
#define P_FAMILY_RELLOR                  FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_FLITTLE                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_TINKATINK               P_GEN_9_POKEMON
#define P_FAMILY_WIGLETT                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_BOMBIRDIER              P_GEN_9_POKEMON
#define P_FAMILY_FINIZEN                 P_GEN_9_POKEMON
#define P_FAMILY_VAROOM                  FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_CYCLIZAR                FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_ORTHWORM                P_GEN_9_POKEMON
#define P_FAMILY_GLIMMET                 P_GEN_9_POKEMON
#define P_FAMILY_GREAVARD                FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_FLAMIGO                 P_GEN_9_POKEMON
#define P_FAMILY_CETODDLE                FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_VELUZA                  FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_DONDOZO                 FALSE // FU: niet in de dex (was P_GEN_9_POKEMON)
#define P_FAMILY_TATSUGIRI               P_GEN_9_POKEMON
#define P_FAMILY_FRIGIBAX                P_GEN_9_POKEMON
#define P_FAMILY_GIMMIGHOUL              P_GEN_9_POKEMON
#define P_FAMILY_POLTCHAGEIST            P_GEN_9_POKEMON
#define P_FAMILY_SINISTCHA               P_GEN_9_POKEMON

// =====================================================================
// Fully Ungrounded: losse soorten en vormen binnen een behouden familie.
// TRUE = in de ROM, FALSE = eruit. Bewaakt species_info, de vormtabellen,
// kleurvarianten en (waar de soort een eigen kreet heeft) de kreet; de sprites
// vallen dan vanzelf weg (pokemon.c met -fdata-sections). Zie DEX_IN_ROM.md.
// =====================================================================
#define FU_PARTNER_FORMS                 FALSE // Partner-Pikachu en Partner-Eevee (Let's Go)
#define FU_TOTEM_FORMS                   FALSE // Totem-vormen (Alola)
#define FU_PICHU_SPIKY_EARED             FALSE // Spiky-eared Pichu (eventvorm)
#define FU_FLOETTE_ETERNAL               FALSE // Eternal Floette (eventvorm)
#define FU_RAICHU_ALOLA                  FALSE // Alolan Raichu
#define FU_MEOWTH_KANTO                  FALSE // gewone Meowth en Persian (Galar-Meowth en Perrserker blijven; Galar-Meowth wordt de basisvorm)
#define FU_MEOWTH_ALOLA                  FALSE // Alolan Meowth en Persian
#define FU_GROWLITHE_HISUI               FALSE // Hisuian Growlithe en Arcanine
#define FU_GEODUDE_ALOLA                 FALSE // Alolan Geodude-lijn
#define FU_PONYTA_GALAR                  FALSE // Galarian Ponyta en Rapidash
#define FU_GRIMER_KANTO                  FALSE // gewone Grimer en Muk (Hoenn-Grimer blijft en wordt de basisvorm)
#define FU_GRIMER_ALOLA                  FALSE // Alolan Grimer en Muk
#define FU_VOLTORB_HISUI                 FALSE // Hisuian Voltorb en Electrode
#define FU_MAROWAK_ALOLA                 FALSE // Alolan Marowak
#define FU_TYROGUE_HITMONLEE_HITMONCHAN  FALSE // Tyrogue, Hitmonlee en Hitmonchan (alleen Hitmontop blijft)
#define FU_WEEZING_GALAR                 FALSE // Galarian Weezing
#define FU_TAUROS_PALDEA                 FALSE // Paldean Tauros (3 vormen)
#define FU_WOOPER_PALDEA                 FALSE // Paldean Wooper en Clodsire
#define FU_QWILFISH_HISUI                FALSE // Hisuian Qwilfish en Overqwil
#define FU_SNEASEL_HISUI                 FALSE // Hisuian Sneasel en Sneasler
#define FU_YAMASK_GALAR                  FALSE // Galarian Yamask en Runerigus
#define FU_ZORUA_HISUI                   FALSE // Hisuian Zorua en Zoroark
#define FU_STUNFISK_GALAR                FALSE // Galarian Stunfisk
#define FU_BRAVIARY_HISUI                FALSE // Hisuian Braviary
#define FU_GOOMY_HISUI                   FALSE // Hisuian Sliggoo en Goodra
#define FU_AVALUGG_HISUI                 FALSE // Hisuian Avalugg

// =====================================================================
// Fully Ungrounded: legendaries, mythicals, Ultra Beasts en paradoxen.
// Alleen Mew, Mewtwo en Zarude zitten in de game. Zet een regel op TRUE
// om een soort terug te halen: graphics, kreet, learnsets en dex-tekst
// komen dan vanzelf weer mee (de bronbestanden staan nog in de repo).
// Zie docs/concept/DEX_IN_ROM.md.
// =====================================================================
#define P_FAMILY_ARTICUNO                FALSE // gen 1
#define P_FAMILY_ZAPDOS                  FALSE // gen 1
#define P_FAMILY_MOLTRES                 FALSE // gen 1
#define P_FAMILY_MEWTWO                  TRUE  // gen 1
#define P_FAMILY_MEW                     TRUE  // gen 1
#define P_FAMILY_RAIKOU                  FALSE // gen 2
#define P_FAMILY_ENTEI                   FALSE // gen 2
#define P_FAMILY_SUICUNE                 FALSE // gen 2
#define P_FAMILY_LUGIA                   FALSE // gen 2
#define P_FAMILY_HO_OH                   FALSE // gen 2
#define P_FAMILY_CELEBI                  FALSE // gen 2
#define P_FAMILY_REGIROCK                FALSE // gen 3
#define P_FAMILY_REGICE                  FALSE // gen 3
#define P_FAMILY_REGISTEEL               FALSE // gen 3
#define P_FAMILY_LATIAS                  FALSE // gen 3
#define P_FAMILY_LATIOS                  FALSE // gen 3
#define P_FAMILY_KYOGRE                  FALSE // gen 3
#define P_FAMILY_GROUDON                 FALSE // gen 3
#define P_FAMILY_RAYQUAZA                FALSE // gen 3
#define P_FAMILY_JIRACHI                 FALSE // gen 3
#define P_FAMILY_DEOXYS                  FALSE // gen 3
#define P_FAMILY_UXIE                    FALSE // gen 4
#define P_FAMILY_MESPRIT                 FALSE // gen 4
#define P_FAMILY_AZELF                   FALSE // gen 4
#define P_FAMILY_DIALGA                  FALSE // gen 4
#define P_FAMILY_PALKIA                  FALSE // gen 4
#define P_FAMILY_HEATRAN                 FALSE // gen 4
#define P_FAMILY_REGIGIGAS               FALSE // gen 4
#define P_FAMILY_GIRATINA                FALSE // gen 4
#define P_FAMILY_CRESSELIA               FALSE // gen 4
#define P_FAMILY_MANAPHY                 FALSE // gen 4
#define P_FAMILY_DARKRAI                 FALSE // gen 4
#define P_FAMILY_SHAYMIN                 FALSE // gen 4
#define P_FAMILY_ARCEUS                  FALSE // gen 4
#define P_FAMILY_VICTINI                 FALSE // gen 5
#define P_FAMILY_COBALION                FALSE // gen 5
#define P_FAMILY_TERRAKION               FALSE // gen 5
#define P_FAMILY_VIRIZION                FALSE // gen 5
#define P_FAMILY_TORNADUS                FALSE // gen 5
#define P_FAMILY_THUNDURUS               FALSE // gen 5
#define P_FAMILY_RESHIRAM                FALSE // gen 5
#define P_FAMILY_ZEKROM                  FALSE // gen 5
#define P_FAMILY_LANDORUS                FALSE // gen 5
#define P_FAMILY_KYUREM                  FALSE // gen 5
#define P_FAMILY_KELDEO                  FALSE // gen 5
#define P_FAMILY_MELOETTA                FALSE // gen 5
#define P_FAMILY_GENESECT                FALSE // gen 5
#define P_FAMILY_XERNEAS                 FALSE // gen 6
#define P_FAMILY_YVELTAL                 FALSE // gen 6
#define P_FAMILY_ZYGARDE                 FALSE // gen 6
#define P_FAMILY_DIANCIE                 FALSE // gen 6
#define P_FAMILY_HOOPA                   FALSE // gen 6
#define P_FAMILY_VOLCANION               FALSE // gen 6
#define P_FAMILY_TYPE_NULL               FALSE // gen 7
#define P_FAMILY_TAPU_KOKO               FALSE // gen 7
#define P_FAMILY_TAPU_LELE               FALSE // gen 7
#define P_FAMILY_TAPU_BULU               FALSE // gen 7
#define P_FAMILY_TAPU_FINI               FALSE // gen 7
#define P_FAMILY_COSMOG                  FALSE // gen 7
#define P_FAMILY_NIHILEGO                FALSE // gen 7
#define P_FAMILY_BUZZWOLE                FALSE // gen 7
#define P_FAMILY_PHEROMOSA               FALSE // gen 7
#define P_FAMILY_XURKITREE               FALSE // gen 7
#define P_FAMILY_CELESTEELA              FALSE // gen 7
#define P_FAMILY_KARTANA                 FALSE // gen 7
#define P_FAMILY_GUZZLORD                FALSE // gen 7
#define P_FAMILY_NECROZMA                FALSE // gen 7
#define P_FAMILY_MAGEARNA                FALSE // gen 7
#define P_FAMILY_MARSHADOW               FALSE // gen 7
#define P_FAMILY_POIPOLE                 FALSE // gen 7
#define P_FAMILY_STAKATAKA               FALSE // gen 7
#define P_FAMILY_BLACEPHALON             FALSE // gen 7
#define P_FAMILY_ZERAORA                 FALSE // gen 7
#define P_FAMILY_MELTAN                  FALSE // gen 7
#define P_FAMILY_ZACIAN                  FALSE // gen 8
#define P_FAMILY_ZAMAZENTA               FALSE // gen 8
#define P_FAMILY_ETERNATUS               FALSE // gen 8
#define P_FAMILY_KUBFU                   FALSE // gen 8
#define P_FAMILY_ZARUDE                  TRUE  // gen 8
#define P_FAMILY_REGIELEKI               FALSE // gen 8
#define P_FAMILY_REGIDRAGO               FALSE // gen 8
#define P_FAMILY_GLASTRIER               FALSE // gen 8
#define P_FAMILY_SPECTRIER               FALSE // gen 8
#define P_FAMILY_CALYREX                 FALSE // gen 8
#define P_FAMILY_ENAMORUS                FALSE // gen 8
#define P_FAMILY_GREAT_TUSK              FALSE // gen 9
#define P_FAMILY_SCREAM_TAIL             FALSE // gen 9
#define P_FAMILY_BRUTE_BONNET            FALSE // gen 9
#define P_FAMILY_FLUTTER_MANE            FALSE // gen 9
#define P_FAMILY_SLITHER_WING            FALSE // gen 9
#define P_FAMILY_SANDY_SHOCKS            FALSE // gen 9
#define P_FAMILY_IRON_TREADS             FALSE // gen 9
#define P_FAMILY_IRON_BUNDLE             FALSE // gen 9
#define P_FAMILY_IRON_HANDS              FALSE // gen 9
#define P_FAMILY_IRON_JUGULIS            FALSE // gen 9
#define P_FAMILY_IRON_MOTH               FALSE // gen 9
#define P_FAMILY_IRON_THORNS             FALSE // gen 9
#define P_FAMILY_WO_CHIEN                FALSE // gen 9
#define P_FAMILY_CHIEN_PAO               FALSE // gen 9
#define P_FAMILY_TING_LU                 FALSE // gen 9
#define P_FAMILY_CHI_YU                  FALSE // gen 9
#define P_FAMILY_ROARING_MOON            FALSE // gen 9
#define P_FAMILY_IRON_VALIANT            FALSE // gen 9
#define P_FAMILY_KORAIDON                FALSE // gen 9
#define P_FAMILY_MIRAIDON                FALSE // gen 9
#define P_FAMILY_WALKING_WAKE            FALSE // gen 9
#define P_FAMILY_IRON_LEAVES             FALSE // gen 9
#define P_FAMILY_OKIDOGI                 FALSE // gen 9
#define P_FAMILY_MUNKIDORI               FALSE // gen 9
#define P_FAMILY_FEZANDIPITI             FALSE // gen 9
#define P_FAMILY_OGERPON                 FALSE // gen 9
#define P_FAMILY_GOUGING_FIRE            FALSE // gen 9
#define P_FAMILY_RAGING_BOLT             FALSE // gen 9
#define P_FAMILY_IRON_BOULDER            FALSE // gen 9
#define P_FAMILY_IRON_CROWN              FALSE // gen 9
#define P_FAMILY_TERAPAGOS               FALSE // gen 9
#define P_FAMILY_PECHARUNT               FALSE // gen 9

#endif // GUARD_CONFIG_SPECIES_ENABLED_H
