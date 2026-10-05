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

static const struct GymLeaderRematch sGymLeaderRematches[] = {
    { REMATCH_ROXANNE,       FLAG_DAILY_REMATCH_ROXANNE },
    { REMATCH_BRAWLY,        FLAG_DAILY_REMATCH_BRAWLY },
    { REMATCH_WATTSON,       FLAG_DAILY_REMATCH_WATTSON },
    { REMATCH_FLANNERY,      FLAG_DAILY_REMATCH_FLANNERY },
    { REMATCH_NORMAN,        FLAG_DAILY_REMATCH_NORMAN },
    { REMATCH_WINONA,        FLAG_DAILY_REMATCH_WINONA },
    { REMATCH_TATE_AND_LIZA, FLAG_DAILY_REMATCH_TATE_AND_LIZA },
    { REMATCH_WALLACE,          FLAG_DAILY_REMATCH_WALLACE },
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
    // Wattson staat pas weer in zijn gym na de New Mauville-opdracht.
    if (rematchIdx == REMATCH_WATTSON && !FlagGet(FLAG_WATTSON_REMATCH_AVAILABLE))
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

static const u8 sText_RefuseRoxanne[] = _(
    "ROXANNE: Again? Today?\n"
    "My rocks need rest.\p"
    "So does my dignity. Call me\n"
    "tomorrow. Rock bottom has\l"
    "opening hours.$");
static const u8 sText_RefuseBrawly[] = _(
    "BRAWLY: Bro, I still see\n"
    "three of you. Two too many.\p"
    "Tomorrow. The ringing stops\n"
    "at midnight. Usually.$");
static const u8 sText_RefuseWattson[] = _(
    "WATTSON: Wahahahah! Again?\n"
    "My heart monitor says no.\p"
    "Loudly. Try tomorrow, if the\n"
    "pacemaker holds!$");
static const u8 sText_RefuseFlannery[] = _(
    "FLANNERY: I already lost to\n"
    "you today! I'm still on fire.\p"
    "Emotionally. And a little bit\n"
    "literally. Tomorrow!$");
static const u8 sText_RefuseNorman[] = _(
    "DAD: Not today, {PLAYER}.\n"
    "My back made a noise.\p"
    "A sad noise. Tomorrow.\n"
    "Tell your mother I'm fine.$");
static const u8 sText_RefuseWinona[] = _(
    "WINONA: My birds have\n"
    "unionized. One battle a day.\p"
    "It's in writing.\n"
    "Fly by tomorrow.$");
static const u8 sText_RefuseTateLiza[] = _(
    "TATE: We foresaw this call.\p"
    "LIZA: We also foresaw\n"
    "saying no. Tomorrow!$");
static const u8 sText_RefuseWallace[] = _(
    "WALLACE: Again? I'm two\n"
    "glasses into forgetting\l"
    "today's battle.\p"
    "Tomorrow, darling.\n"
    "Let us both breathe.$");

static const u8 *const sRefuseTexts[] = {
    sText_RefuseRoxanne,
    sText_RefuseBrawly,
    sText_RefuseWattson,
    sText_RefuseFlannery,
    sText_RefuseNorman,
    sText_RefuseWinona,
    sText_RefuseTateLiza,
    sText_RefuseWallace,
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
