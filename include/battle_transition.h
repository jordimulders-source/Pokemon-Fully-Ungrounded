#ifndef GUARD_BATTLE_TRANSITION_H
#define GUARD_BATTLE_TRANSITION_H

void BattleTransition_StartOnField(u8 transitionId);
void BattleTransition_Start(u8 transitionId);
bool8 IsBattleTransitionDone(void);
bool8 FldEff_PokeballTrail(void);
void Task_BattleTransition_Intro(u8 taskId);
void GetBg0TilesDst(u16 **tilemap, u16 **tileset);

extern const struct SpritePalette gSpritePalette_Pokeball;

enum MugshotColor
{
    MUGSHOT_COLOR_NONE,
    MUGSHOT_COLOR_PURPLE,
    MUGSHOT_COLOR_GREEN,
    MUGSHOT_COLOR_PINK,
    MUGSHOT_COLOR_BLUE,
    MUGSHOT_COLOR_YELLOW,
    MUGSHOT_COLOR_COUNT
};

enum BattleTransition
{
    B_TRANSITION_BLUR,
    B_TRANSITION_SWIRL,
    B_TRANSITION_SHUFFLE,
    B_TRANSITION_BIG_POKEBALL,
    B_TRANSITION_POKEBALLS_TRAIL,
    B_TRANSITION_CLOCKWISE_WIPE,
    B_TRANSITION_RIPPLE,
    B_TRANSITION_WAVE,
    B_TRANSITION_SLICE,
    B_TRANSITION_WHITE_BARS_FADE,
    B_TRANSITION_GRID_SQUARES,
    B_TRANSITION_ANGLED_WIPES,
    B_TRANSITION_MUGSHOT,
    B_TRANSITION_AQUA, // Here below added in Emerald
    B_TRANSITION_MAGMA,
    B_TRANSITION_REGICE,
    B_TRANSITION_REGISTEEL,
    B_TRANSITION_REGIROCK,
    B_TRANSITION_KYOGRE,
    B_TRANSITION_GROUDON,
    B_TRANSITION_RAYQUAZA,
    B_TRANSITION_SHRED_SPLIT,
    B_TRANSITION_BLACKHOLE,
    B_TRANSITION_BLACKHOLE_PULSATE,
    B_TRANSITION_RECTANGULAR_SPIRAL,
    B_TRANSITION_FRONTIER_LOGO_WIGGLE,
    B_TRANSITION_FRONTIER_LOGO_WAVE,
    B_TRANSITION_FRONTIER_SQUARES,
    B_TRANSITION_FRONTIER_SQUARES_SCROLL,
    B_TRANSITION_FRONTIER_SQUARES_SPIRAL,
    B_TRANSITION_FRONTIER_CIRCLES_MEET,
    B_TRANSITION_FRONTIER_CIRCLES_CROSS,
    B_TRANSITION_FRONTIER_CIRCLES_ASYMMETRIC_SPIRAL,
    B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL,
    B_TRANSITION_FRONTIER_CIRCLES_MEET_IN_SEQ,
    B_TRANSITION_FRONTIER_CIRCLES_CROSS_IN_SEQ,
    B_TRANSITION_FRONTIER_CIRCLES_ASYMMETRIC_SPIRAL_IN_SEQ,
    B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL_IN_SEQ,
    B_TRANSITION_AURORA, // Project Grounded: noorderlicht (Suicune)
    B_TRANSITION_REGIDRAGO, // Project Grounded
    B_TRANSITION_REGIELEKI, // Project Grounded
    B_TRANSITION_DEOXYS, // Project Grounded: ruimte + DNA-helix
    B_TRANSITION_BIRCH, // Project Grounded: poep-thema
    B_TRANSITION_AQUA_MAGMA, // Project Grounded: Archie + Maxie samen
    B_TRANSITION_RAIKOU, // Project Grounded: bliksems
    B_TRANSITION_ENTEI, // Project Grounded: steekvlam die het scherm overneemt
    B_TRANSITION_ROUTE_WAVE, // Project Grounded: zee/surfen, golf van rechts naar links
    B_TRANSITION_ROUTE_BEACH, // Project Grounded: strand van een zeeroute, golf uit de verte
    B_TRANSITION_ROUTE_BUBBLES, // Project Grounded: onder water, luchtbellen
    B_TRANSITION_ROUTE_SNOW, // Project Grounded: Route 135/136, sneeuwt dicht
    B_TRANSITION_ROUTE_ASH, // Project Grounded: Route 113, as waait door het beeld
    B_TRANSITION_ROUTE_SAND, // Project Grounded: woestijn, zandstorm
    B_TRANSITION_ROUTE_HEAT, // Project Grounded: Fiery Path / Mt. Chimney, hittegolf
    B_TRANSITION_ROUTE_CYCLING, // Project Grounded: Cycling Road, POV op de fiets
    B_TRANSITION_ROUTE_PYRE, // Project Grounded: Mt. Pyre, spookachtige vloek
    B_TRANSITION_ROUTE_SKY, // Project Grounded: Sky Pillar, razendsnel de lucht in
    B_TRANSITION_ROUTE_SHORT, // Project Grounded: New Mauville, kortsluiting
    B_TRANSITION_ROUTE_PAINT, // Project Grounded: Artisan Cave, wordt volgeschilderd
    B_TRANSITION_ROUTE_SAFARI, // Project Grounded: Safari Zone, tussen de bomen door
    B_TRANSITION_ROUTE_METEOR, // Project Grounded: Meteor Falls, tussen stalactieten en stalagmieten
    B_TRANSITION_ROUTE_JAGGED, // Project Grounded: Jagged Pass, tussen de rotsen naar beneden
    B_TRANSITION_ROUTE_RAINFOREST, // Project Grounded: Route 119/120 en Fortree, door het regenwoud
    B_TRANSITION_PIKACHU, // Project Grounded: wilde Pikachu, geel scherm met wangen en "Pika!"
    B_TRANSITION_MAGIKARP, // Project Grounded: wilde Magikarp, scherm vol spartelende Magikarp
    B_TRANSITION_PSYDUCK, // Project Grounded: wilde Psyduck, enorm draaiend vraagteken
    B_TRANSITION_KOFFING, // Project Grounded: wilde Koffing/Weezing, schedel-en-botten-teken op paars
    B_TRANSITION_GABBY_TY, // Project Grounded: Gabby & Ty, camerazoeker met REC
    B_TRANSITION_POOCHYENA, // Project Grounded: Joey, Poochyena springt op je af
    B_TRANSITION_BEACHBALL, // Project Grounded: strand van Route 109, strandbal in je gezicht
    B_TRANSITION_COLRESS, // Project Grounded: Colress, mugshot en dan twee tandwielen die op je af komen
    B_TRANSITION_ZANGOOSE, // Project Grounded: wilde Zangoose, een reuzenklauw scheurt het scherm open
    B_TRANSITION_SEVIPER, // Project Grounded: wilde Seviper, een schermvullende Poison Fang
    B_TRANSITION_HEATRAN, // Project Grounded: Heatran, lavapluimen en een uitbarsting
    B_TRANSITION_SHAYMIN, // Project Grounded: Shaymin, een wervelwind van bloemen in alle kleuren en een bloementapijt
    B_TRANSITION_GENESECT, // Project Grounded: Genesect, scanlijnen, rood vizier en Techno Blast
    B_TRANSITION_MEWTWO, // Project Grounded: Mewtwo, kweektank in het Cinnabar-lab, dagboek, glas spat uiteen
    B_TRANSITION_GIRATINA, // Project Grounded: Giratina, het scherm scheurt, klapt om en de schaduwvleugels sluiten het af
    B_TRANSITION_VICTINI, // Project Grounded: Victini, een grote V in vuur (V-create)
    B_TRANSITION_JIRACHI, // Project Grounded: Jirachi, een wensster tuimelt fladderend over het beeld
    B_TRANSITION_DARKRAI, // Project Grounded: Darkrai, nachtmerrierook sluit het beeld en een blauw oog gaat open
    B_TRANSITION_NEO_PLASMA, // Project Grounded: Neo Team Plasma (BW2): blauwe P, lichtstreep-Z, flits, schild, bliksems
    B_TRANSITION_ROCKET, // Project Grounded: Team Rocket, zwarte balken met rode strepen en een stempelende rode R
    B_TRANSITION_ZARUDE, // Project Grounded: Zarude, de jungle groeit dicht, lianen, drie klauwkrassen en een silhouet met rode ogen
    B_TRANSITION_POISON_CHAIN, // Project Grounded: Loyal Three (Okidogi, Munkidori, Fezandipiti), paarse gloeiende Poison Chain
    B_TRANSITION_REGIGIGAS, // Project Grounded: Regigigas, zes ogen (rood/blauw/wit) in het Regi-weefeffect
    B_TRANSITION_DAVE, // Project Grounded: Dave (Freed From Desire), een penalty strak in de winkelhaak, dan GOAL!
    B_TRANSITION_SICKBLIK, // Project Grounded: SickBlik (Jordi), mugshot, aan tafel bij een hotpot, die van bovenaf een Poké Ball wordt
    B_TRANSITION_STEVEN, // Project Grounded: Steven, verzamelkast, gloeiende steen met de badges in de facetten, spat uiteen
    B_TRANSITION_WALLY_VHS, // Project Grounded: Wally (Victory Road), VHS-band van zijn groei, bevriest op zijn gezicht
    B_TRANSITION_RAYQUAZA_PILLAR, // Project Grounded: Rayquaza, groene ring rond de Sky Pillar, Rayquaza breekt eruit
    B_TRANSITION_KYOGRE_MURAL, // Project Grounded: Kyogre, oude muurschildering barst, water stroomt erdoor, Primal-markeringen
    B_TRANSITION_GROUDON_MURAL, // Project Grounded: Groudon, dezelfde schildering, lava stroomt door de barsten
    B_TRANSITION_OGERPON, // Project Grounded: Ogerpon, maskerkraam op een nachtfestival, het Teal-masker kijkt terug
    B_TRANSITION_WEATHER_SERVICE, // Project Grounded: Archie + Maxie (werkstraf), koffievlek Groudon/Kyogre, rooster scheurt
    B_TRANSITION_MIMI, // Project Grounded: Mimi, poppenkast in een donkere kinderkamer, het nekje van de Pikachu-pop knakt
    B_TRANSITION_KECCLES, // Project Grounded: Keccles, lab vol schoolborden, de camouflage golft weg
    B_TRANSITION_BURGLAR, // Project Grounded: Burglar, bewakingscamera, de Gen 1-Burglar kijkt in de lens, alarm
    B_TRANSITION_GYM_ROXANNE, // Project Grounded: Roxanne, concert: aanstekers, spotlight, rotsblok-versterkers, powerchord
    B_TRANSITION_GYM_BRAWLY, // Project Grounded: Brawly, UFC-walkout, octagon, omroeperbalk, vuist tegen het kooigaas
    B_TRANSITION_GYM_WATTSON, // Project Grounded: Wattson, serverfarm, pop-ups, WATTCOIN crasht, SCAM-stempel, Wahahahah!
    B_TRANSITION_GYM_FLANNERY, // Project Grounded: Flannery, camping, Mt. Chimney ontploft, een lavasteen raakt de camera
    B_TRANSITION_TAPU_KOKO, // Project Grounded: Tapu's, gesloten schild op het motief van het schild, opent op de drumslag
    B_TRANSITION_TAPU_LELE,
    B_TRANSITION_TAPU_BULU,
    B_TRANSITION_TAPU_FINI,
    B_TRANSITION_GYM_NORMAN, // Project Grounded: Norman, NORMFLIX: Are you still watching?, het beeld krimpt in de tv, Slaking op de bank
    B_TRANSITION_GYM_WINONA, // Project Grounded: Winona, WINAIR: vertrekbord DELAYED -> BOARDING, Altaria vliegt over, het koffertje springt open
    B_TRANSITION_GYM_TATE_LIZA, // Project Grounded: Tate & Liza, ouijabord spelt RIP, drie tarotkaarten, psychic overload in lowercase
    B_TRANSITION_GYM_WALLACE, // Project Grounded: Wallace, Crater Pub: een wijnglas schenkt vol, de wijn wordt Hoenn-blauw, een golf over de pub, Santé!
    B_TRANSITION_COUNT
};

// IDs for GetSpecialBattleTransition
enum BattleTransitionGroup
{
    B_TRANSITION_GROUP_B_TOWER,
    B_TRANSITION_GROUP_B_DOME = 3,
    B_TRANSITION_GROUP_B_PALACE,
    B_TRANSITION_GROUP_B_ARENA,
    B_TRANSITION_GROUP_B_FACTORY,
    B_TRANSITION_GROUP_B_PIKE,
    B_TRANSITION_GROUP_B_PYRAMID = 10,
    B_TRANSITION_GROUP_TRAINER_HILL,
    B_TRANSITION_GROUP_SECRET_BASE,
    B_TRANSITION_GROUP_E_READER,
};

#endif // GUARD_BATTLE_TRANSITION_H
