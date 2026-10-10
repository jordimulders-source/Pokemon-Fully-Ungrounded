#include "global.h"
#include "battle_music_options.h"
#include "event_data.h"
#include "constants/songs.h"
#include "constants/vars.h"

// Project Grounded: keuzes voor gevechtsmuziek in het optiemenu.
const struct BattleMusicOption gWildBattleMusicOptions[] =
{
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

const u8 gWildBattleMusicOptionsCount = ARRAY_COUNT(gWildBattleMusicOptions);
const u8 gTrainerBattleMusicOptionsCount = ARRAY_COUNT(gTrainerBattleMusicOptions);

u16 GetChosenWildBattleMusic(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_WILD);

    if (choice >= ARRAY_COUNT(gWildBattleMusicOptions))
        choice = 0;
    return gWildBattleMusicOptions[choice].song;
}

u16 GetChosenTrainerBattleMusic(void)
{
    u16 choice = VarGet(VAR_BATTLE_MUSIC_TRAINER);

    if (choice >= ARRAY_COUNT(gTrainerBattleMusicOptions))
        choice = 0;
    return gTrainerBattleMusicOptions[choice].song;
}
