#include "global.h"
#include "battle_music_options.h"
#include "event_data.h"
#include "overworld.h"
#include "constants/game_stat.h"
#include "constants/songs.h"
#include "constants/vars.h"

// Project Grounded: keuzes voor gevechtsmuziek in het optiemenu.
const struct BattleMusicOption gWildBattleMusicOptions[] =
{
    { COMPOUND_STRING("ROTATE"),       MUS_NONE }, // Project Grounded (Jordi): standaard: elk gevecht het volgende uit sWildRotation
    { COMPOUND_STRING("HOENN"),        MUS_VS_WILD },
    { COMPOUND_STRING("KANTO"),        MUS_RG_VS_WILD },
    { COMPOUND_STRING("GROUDON"),      MUS_VS_KYOGRE_GROUDON },
    { COMPOUND_STRING("REGI"),         MUS_VS_REGI },
    { COMPOUND_STRING("RAYQUAZA"),     MUS_VS_RAYQUAZA },
    { COMPOUND_STRING("MEW"),          MUS_VS_MEW },
    { COMPOUND_STRING("KANTO BIRDS"),  MUS_RG_VS_LEGEND },
    { COMPOUND_STRING("MEWTWO"),       MUS_RG_VS_MEWTWO },
    { COMPOUND_STRING("DEOXYS"),       MUS_RG_VS_DEOXYS },
    { COMPOUND_STRING("LEGEND DOGS"),  MUS_C_VS_LEGEND_BEAST },
    { COMPOUND_STRING("GIRATINA"),     MUS_GROUNDED_VS_GIRATINA },
    { COMPOUND_STRING("DARK CAVE"), MUS_GROUNDED_VS_DARK_CAVE },
    { COMPOUND_STRING("YOSHI CASTLE"),MUS_GROUNDED_VS_YOSHI_CASTLE },
    { COMPOUND_STRING("BROKEN PIER"),MUS_GROUNDED_VS_BROKEN_PIER },
    { COMPOUND_STRING("SUNSET WILDS"),MUS_GROUNDED_VS_SUNSET_WILDS },
    { COMPOUND_STRING("LANDFILL"),MUS_GROUNDED_WL4_TOXIC_LANDFILL }, // Wario Land 4 (Jordi: "een goed ander battle theme")
};

const struct BattleMusicOption gTrainerBattleMusicOptions[] =
{
    { COMPOUND_STRING("ROTATE"),       MUS_NONE }, // Project Grounded (Jordi): standaard: elk gevecht het volgende uit sTrainerRotation
    { COMPOUND_STRING("HOENN"),        MUS_VS_TRAINER },
    { COMPOUND_STRING("KANTO"),        MUS_RG_VS_TRAINER },
    { COMPOUND_STRING("KANTO GYM"),    MUS_RG_VS_GYM_LEADER },
    { COMPOUND_STRING("KANTO CHAMP"),  MUS_RG_VS_CHAMPION },
    { COMPOUND_STRING("COLRESS"),      MUS_GROUNDED_VS_COLRESS },
    { COMPOUND_STRING("SINNOH CHAMP"), MUS_GROUNDED_VS_DPPT_CHAMPION },
    { COMPOUND_STRING("CYRUS"),        MUS_GROUNDED_VS_CYRUS },
    { COMPOUND_STRING("GHETSIS"),      MUS_GROUNDED_VS_GHETSIS },
    { COMPOUND_STRING("NEO PLASMA"),   MUS_GROUNDED_VS_NEO_PLASMA },
    { COMPOUND_STRING("DEOXYS"),       MUS_RG_VS_DEOXYS },
    { COMPOUND_STRING("LEGEND DOGS"),  MUS_C_VS_LEGEND_BEAST },
    { COMPOUND_STRING("LANDFILL"),MUS_GROUNDED_WL4_TOXIC_LANDFILL }, // Wario Land 4
};

// Project Grounded (Jordi: "3/4 wild pokemon/trainer battle themes rouleren, zodat muziek spannend blijft"):
// de keuze ROTATE draait per gevecht door deze lijsten, op de teller van wilde/trainergevechten (vast binnen één gevecht).
// Jordi: "die wild themes moeten echt in theme": alleen Pokémon-gevechtsthema's (geen Mario/Wario)
static const u16 sWildRotation[] = { MUS_VS_WILD, MUS_RG_VS_WILD, MUS_GROUNDED_VS_DARK_CAVE };
static const u16 sTrainerRotation[] = { MUS_VS_TRAINER, MUS_RG_VS_TRAINER };

const u8 gWildBattleMusicOptionsCount = ARRAY_COUNT(gWildBattleMusicOptions);
const u8 gTrainerBattleMusicOptionsCount = ARRAY_COUNT(gTrainerBattleMusicOptions);

u16 GetChosenWildBattleMusic(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_WILD);

    if (choice >= ARRAY_COUNT(gWildBattleMusicOptions))
        choice = 0;
    if (gWildBattleMusicOptions[choice].song == MUS_NONE)
        return sWildRotation[GetGameStat(GAME_STAT_WILD_BATTLES) % ARRAY_COUNT(sWildRotation)];
    return gWildBattleMusicOptions[choice].song;
}

// Project Grounded: staat de wildmuziek op de standaard (ROTATE of HOENN)? Dan krijgen vulkaan, woestijn, water en
// onderwater hun regionale remix van het Hoenn-wildthema (GetBattleBGM, tools/grounded/regio_theme.py).
bool8 IsDefaultWildBattleMusicChoice(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_WILD);

    if (choice >= ARRAY_COUNT(gWildBattleMusicOptions))
        choice = 0;
    return gWildBattleMusicOptions[choice].song == MUS_NONE || gWildBattleMusicOptions[choice].song == MUS_VS_WILD;
}

u16 GetChosenTrainerBattleMusic(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_TRAINER);

    if (choice >= ARRAY_COUNT(gTrainerBattleMusicOptions))
        choice = 0;
    if (gTrainerBattleMusicOptions[choice].song == MUS_NONE)
        return sTrainerRotation[GetGameStat(GAME_STAT_TRAINER_BATTLES) % ARRAY_COUNT(sTrainerRotation)];
    return gTrainerBattleMusicOptions[choice].song;
}

// Project Grounded: de trainerklasse-remixes van MUS_VS_TRAINER (tools/grounded/trclass_theme.py) spelen alleen als de
// speler HOENN of ROTATE koos; een gekozen specifiek trainerthema (KANTO, COLRESS, ...) blijft gerespecteerd.
bool32 TrainerClassRemixAllowed(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_TRAINER);

    if (choice >= ARRAY_COUNT(gTrainerBattleMusicOptions))
        choice = 0;
    return gTrainerBattleMusicOptions[choice].song == MUS_NONE
        || gTrainerBattleMusicOptions[choice].song == MUS_VS_TRAINER;
}
