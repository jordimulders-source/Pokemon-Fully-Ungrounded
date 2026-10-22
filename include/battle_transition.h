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
    B_TRANSITION_REGIDRAGO, // Project Grounded
    B_TRANSITION_REGIELEKI, // Project Grounded
    B_TRANSITION_DEOXYS, // Project Grounded: ruimte + DNA-helix
    B_TRANSITION_ROUTE_WAVE, // Project Grounded: zee/surfen, golf van rechts naar links
    B_TRANSITION_ROUTE_BUBBLES, // Project Grounded: onder water, luchtbellen
    B_TRANSITION_PIKACHU, // Project Grounded: wilde Pikachu, geel scherm met wangen en "Pika!"
    B_TRANSITION_MAGIKARP, // Project Grounded: wilde Magikarp, scherm vol spartelende Magikarp
    B_TRANSITION_PSYDUCK, // Project Grounded: wilde Psyduck, enorm draaiend vraagteken
    B_TRANSITION_KOFFING, // Project Grounded: wilde Koffing/Weezing, schedel-en-botten-teken op paars
    B_TRANSITION_ZANGOOSE, // Project Grounded: wilde Zangoose, een reuzenklauw scheurt het scherm open
    B_TRANSITION_SEVIPER, // Project Grounded: wilde Seviper, een schermvullende Poison Fang
    B_TRANSITION_ZARUDE, // Project Grounded: Zarude, de jungle groeit dicht, lianen, drie klauwkrassen en een silhouet met rode ogen
    B_TRANSITION_REGIGIGAS, // Project Grounded: Regigigas, zes ogen (rood/blauw/wit) in het Regi-weefeffect
    B_TRANSITION_KECCLES, // Project Grounded: Keccles, lab vol schoolborden, de camouflage golft weg
    B_TRANSITION_VOLCANION, // Project Grounded: Volcanion, manometer in het rood, klinknagels schieten eruit, stoom
    B_TRANSITION_MEW, // Project Grounded: Mew, Guyana bij zonsopgang in parallax, een roze glinstering, Mews staart zwiept door beeld
    B_TRANSITION_LEGEND_ZYGARDE, // Project Grounded: Zygarde, een groene Z als Zorro en het beeld splijt
    B_TRANSITION_CLASS_INTRO, // Project Grounded (class_intros.h): lichte intro per trainerklasse
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

bool32 ClassIntro_HasIntro(u32 trainerClass); // Project Grounded (src/data/class_intros.h)

#endif // GUARD_BATTLE_TRANSITION_H
