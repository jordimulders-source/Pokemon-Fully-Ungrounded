#ifndef GUARD_BATTLE_MUSIC_OPTIONS_H
#define GUARD_BATTLE_MUSIC_OPTIONS_H

// Project Grounded: keuzes voor gevechtsmuziek in het optiemenu.
// Opgeslagen in VAR_BATTLE_MUSIC_WILD en VAR_BATTLE_MUSIC_TRAINER (0 = Hoenn, de standaard).

struct BattleMusicOption
{
    const u8 *name;
    u16 song;
};

extern const struct BattleMusicOption gWildBattleMusicOptions[];
extern const struct BattleMusicOption gTrainerBattleMusicOptions[];
extern const u8 gWildBattleMusicOptionsCount;
extern const u8 gTrainerBattleMusicOptionsCount;

u16 GetChosenWildBattleMusic(void);
u16 GetChosenTrainerBattleMusic(void);
bool8 IsDefaultWildBattleMusicChoice(void);

#endif // GUARD_BATTLE_MUSIC_OPTIONS_H
