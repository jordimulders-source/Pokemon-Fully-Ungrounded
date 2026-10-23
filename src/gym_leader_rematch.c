#include "global.h"
#include "event_data.h"
#include "battle_setup.h"
#include "gym_leader_rematch.h"
#include "constants/flags.h"

// Project Grounded: gymleider-rematches zonder toeval.
// Na de Hall of Fame staat elke gymleider klaar voor een rematch in zijn gym
// (Wattson pas als hij na New Mauville terug in zijn gym staat). Na een gewonnen
// rematch zet het spel een dagelijkse flag; de volgende RTC-dag (ClearDailyFlags)
// staat dezelfde leider weer klaar, met het team van de volgende ronde (max. 5).

struct GymLeaderRematch
{
    u16 rematchIdx;
    u16 dailyFlag;
};

// Fully Ungrounded: de Hoenn-gymleiders zijn weg. Plaatshouder (één regel als voorbeeld) tot de nieuwe regio
// gymleiders heeft; gRematchTable is leeg, dus deze leider staat nooit klaar.
static const struct GymLeaderRematch sGymLeaderRematches[] = {
    { REMATCH_ROXANNE,       FLAG_DAILY_REMATCH_ROXANNE },
};

static s32 GetGymLeaderEntry(u32 rematchIdx)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sGymLeaderRematches); i++)
    {
        if (sGymLeaderRematches[i].rematchIdx == rematchIdx)
            return i;
    }
    return -1;
}

static bool32 IsGymLeaderInGym(u32 rematchIdx)
{
    if (!FlagGet(FLAG_SYS_GAME_CLEAR))
        return FALSE;
    return HasTrainerBeenFought(gRematchTable[rematchIdx].trainerIds[0]);
}

#if FREE_MATCH_CALL == FALSE
// Index van de eerstvolgende rematchronde (1..REMATCHES_COUNT), zoals SetRematchIdForTrainer.
static u8 GetNextRematchRound(u32 rematchIdx)
{
    u32 i;
    for (i = 1; i < REMATCHES_COUNT; i++)
    {
        u16 trainerId = gRematchTable[rematchIdx].trainerIds[i];
        if (trainerId == 0 || !HasTrainerBeenFought(trainerId))
            break;
    }
    return i;
}
#endif //FREE_MATCH_CALL

// Zet trainerRematches[] gelijk aan de regels hierboven. Veilig om vaak aan te roepen.
void UpdateGymLeaderRematch(void)
{
#if FREE_MATCH_CALL == FALSE
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sGymLeaderRematches); i++)
    {
        u32 idx = sGymLeaderRematches[i].rematchIdx;

        if (IsGymLeaderInGym(idx) && !FlagGet(sGymLeaderRematches[i].dailyFlag))
        {
            if (gSaveBlock1Ptr->trainerRematches[idx] == 0)
                gSaveBlock1Ptr->trainerRematches[idx] = GetNextRematchRound(idx);
        }
        else
        {
            gSaveBlock1Ptr->trainerRematches[idx] = 0;
        }
    }
#endif //FREE_MATCH_CALL
}

// Na een gewonnen rematch (HandleRematchVarsOnBattleEnd): vandaag niet meer.
void GymLeaderRematch_OnRematchWon(u16 trainerId)
{
    s32 tableId = TrainerIdToRematchTableId(gRematchTable, trainerId);
    s32 entry;

    if (tableId < 0)
        return;
    entry = GetGymLeaderEntry(tableId);
    if (entry >= 0)
        FlagSet(sGymLeaderRematches[entry].dailyFlag);
}

static const u8 sText_RefusePlaceholder[] = _(
    "Again? Today?\n"
    "Call me tomorrow.$");

static const u8 *const sRefuseTexts[] = {
    sText_RefusePlaceholder,
};

// Match Call: de speler belt een gymleider en vraagt om een rematch.
// Geeft een weigering terug als die leider vandaag al verslagen is; anders
// zet hij de leider klaar en geeft NULL (dan volgt de gewone "gym is klaar"-tekst).
const u8 *GymLeaderRematch_TryRequestByCall(u32 rematchIdx)
{
    s32 entry = GetGymLeaderEntry(rematchIdx);

    if (entry < 0 || !IsGymLeaderInGym(rematchIdx))
        return NULL;
    if (FlagGet(sGymLeaderRematches[entry].dailyFlag))
        return sRefuseTexts[entry];
    UpdateGymLeaderRematch();
    return NULL;
}

// Upstream 1.17 (pokeemerald-expansion): rematch-niveau van de gymleiders na de Hall of Fame.
s32 GetCurrentGymLeaderRematchLevel(void)
{
    u32 i, j;
    u32 maxLevel = REMATCHES_COUNT;
    if (!FlagGet(FLAG_SYS_GAME_CLEAR))
        return 0;
    for (i = REMATCH_SPECIAL_TRAINER_START; i < REMATCH_ELITE_FOUR_ENTRIES; i++)
    {
        for (j = 0; j < REMATCHES_COUNT; j++)
        {
            if (!HasTrainerBeenFought(gRematchTable[i].trainerIds[j]))
                break;
        }
        if (maxLevel > j)
            j = maxLevel;
    }
    return maxLevel;
}
