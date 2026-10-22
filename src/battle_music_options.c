#include "global.h"
#include "battle_music_options.h"
#include "event_data.h"
#include "constants/flags.h"
#include "overworld.h"
#include "constants/game_stat.h"
#include "constants/songs.h"
#include "constants/vars.h"

// Project Grounded: keuzes voor gevechtsmuziek in het optiemenu. Fully Ungrounded: alleen vanilla-thema's
// (Emerald/FRLG/Crystal) en Keccles; de eigen Ungrounded-muziek is weg.
const struct BattleMusicOption gWildBattleMusicOptions[] =
{
    { COMPOUND_STRING("ROTATE"),       MUS_NONE }, // standaard: elk gevecht het volgende uit sWildRotation
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
    { COMPOUND_STRING("KECCLES"),      MUS_GROUNDED_VS_KECCLES },
};

const struct BattleMusicOption gTrainerBattleMusicOptions[] =
{
    { COMPOUND_STRING("ROTATE"),       MUS_NONE }, // standaard: elk gevecht het volgende uit sTrainerRotation
    { COMPOUND_STRING("HOENN"),        MUS_VS_TRAINER },
    { COMPOUND_STRING("KANTO"),        MUS_RG_VS_TRAINER },
    { COMPOUND_STRING("KANTO GYM"),    MUS_RG_VS_GYM_LEADER },
    { COMPOUND_STRING("KANTO CHAMP"),  MUS_RG_VS_CHAMPION },
    { COMPOUND_STRING("DEOXYS"),       MUS_RG_VS_DEOXYS },
    { COMPOUND_STRING("LEGEND DOGS"),  MUS_C_VS_LEGEND_BEAST },
    { COMPOUND_STRING("KECCLES"),      MUS_GROUNDED_VS_KECCLES },
};

// Project Grounded (Jordi: "3/4 wild pokemon/trainer battle themes rouleren, zodat muziek spannend blijft"):
// de keuze ROTATE draait per gevecht door deze lijsten, op de teller van wilde/trainergevechten (vast binnen één gevecht).
// Eerst alleen Hoenn; vanaf de 4e badge wisselen Hoenn en Kanto elkaar af.
static const u16 sWildRotation[] = { MUS_VS_WILD, MUS_RG_VS_WILD };
static const u16 sTrainerRotation[] = { MUS_VS_TRAINER, MUS_RG_VS_TRAINER };

const u8 gWildBattleMusicOptionsCount = ARRAY_COUNT(gWildBattleMusicOptions);
const u8 gTrainerBattleMusicOptionsCount = ARRAY_COUNT(gTrainerBattleMusicOptions);

u16 GetChosenWildBattleMusic(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_WILD);

    if (choice >= ARRAY_COUNT(gWildBattleMusicOptions))
        choice = 0;
    if (gWildBattleMusicOptions[choice].song == MUS_NONE)
    {
        if (!FlagGet(FLAG_BADGE04_GET))
            return MUS_VS_WILD;
        return sWildRotation[GetGameStat(GAME_STAT_WILD_BATTLES) % ARRAY_COUNT(sWildRotation)];
    }
    return gWildBattleMusicOptions[choice].song;
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

// Alle keuzes zijn vrij (het slot op de Mario-wereldmuziek is met die muziek verdwenen).
bool8 IsBattleMusicOptionUnlocked(const struct BattleMusicOption *option)
{
    return TRUE;
}
