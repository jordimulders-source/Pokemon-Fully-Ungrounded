// Project Grounded: Battle Stadium (Pokémon World Tournament, zie STADIUM_DESIGN.md).
// Toernooi van 32 (singles 4v4) of 16 duo's (doubles 3+3 als multi battle met een compagnon).
// Alles level 50; jouw team wordt per gevecht als kopie geschaald en na het toernooi teruggezet.
// NPC-wedstrijden worden gesimuleerd op sterkte (gem. BST, zie tools/grounded/stadium/pool.py).
#include "global.h"
#include "battle.h"
#include "battle_setup.h"
#include "battle_tower.h"
#include "battle_transition.h"
#include "data.h"
#include "event_data.h"
#include "field_screen_effect.h"
#include "load_save.h"
#include "main.h"
#include "overworld.h"
#include "party_menu.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "sound.h"
#include "stadium.h"
#include "string_util.h"
#include "task.h"
#include "constants/battle_frontier.h"
#include "constants/battle_partner.h"
#include "constants/trainers.h"
#include "constants/event_objects.h"

#define SAVE STADIUM_SAVE

#include "data/stadium_pool.h"
#include "data/stadium_announcer.h"

STATIC_ASSERT(sizeof(struct StadiumSave) <= STADIUM_SAVE_SIZE, StadiumSaveFits);
STATIC_ASSERT(ARRAY_COUNT(sStadiumPool) <= STADIUM_MAX_POOL, StadiumPoolFits);
STATIC_ASSERT(ARRAY_COUNT(sStadiumCompanions) <= STADIUM_MAX_COMPANIONS, StadiumCompanionsFit);

#define UNKNOWN_SLOT 0xFE
#define NO_POOL      0xFF

struct StadiumTournament
{
    u8 mode;
    u8 round;           // huidige ronde (0 = eerste)
    u8 rounds;          // 5 bij 32 deelnemers, 4 bij 16
    u8 entrants;
    u8 lost;
    u8 companion;
    u8 order[STADIUM_SINGLES_MONS];     // gekozen teamplekken (1-based, zoals gSelectedOrderFromParty)
    u8 pool[STADIUM_MAX_ENTRANTS][2];   // poolplekken per deelnemer (doubles: twee); deelnemer 0 = speler
    u8 bracket[6][STADIUM_MAX_ENTRANTS];// deelnemer per ronde en plek
    u8 newUnlocks[16];
    u8 newUnlockCount;
    u16 bp;
};

EWRAM_DATA bool8 gStadiumBattle = FALSE;
static EWRAM_DATA struct StadiumTournament sT = {0};

static const u8 sBpPerRound[] = {1, 1, 2, 3, 5};   // laatste rondes tellen het zwaarst (zie STADIUM_DESIGN.md)

// --- pool en compagnons -------------------------------------------------------------------------
u32 Stadium_PoolCount(void)
{
    return ARRAY_COUNT(sStadiumPool);
}

const struct StadiumEntrant *Stadium_GetEntrant(u32 i)
{
    return &sStadiumPool[i];
}

u32 Stadium_CompanionCount(void)
{
    return ARRAY_COUNT(sStadiumCompanions);
}

const struct StadiumCompanion *Stadium_GetCompanion(u32 i)
{
    return &sStadiumCompanions[i];
}

static s32 PoolIndexOfTrainer(u16 trainerId)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStadiumPool); i++)
        if (sStadiumPool[i].trainerId == trainerId)
            return i;
    return -1;
}

static bool32 GetBit(const u32 *bits, u32 i)
{
    return (bits[i / 32] >> (i % 32)) & 1;
}

static void SetBit(u32 *bits, u32 i)
{
    bits[i / 32] |= 1u << (i % 32);
}

// De rivaal van het andere geslacht dan de speler bestaat niet: niet tonen
bool32 Stadium_IsCompanionVisible(u32 i)
{
    u16 p = sStadiumCompanions[i].partnerId;

    if (p == PARTNER_STADIUM_BRENDAN)
        return gSaveBlock2Ptr->playerGender != MALE;
    if (p == PARTNER_STADIUM_MAY)
        return gSaveBlock2Ptr->playerGender == MALE;
    return TRUE;
}

bool32 Stadium_IsCompanionUnlocked(u32 i)
{
    const struct StadiumCompanion *c = &sStadiumCompanions[i];
    s32 p;

    switch (c->unlockType)
    {
    case STADIUM_UNLOCK_START:
        // Brendan of May: alleen het andere geslacht dan de speler
        if (c->partnerId == PARTNER_STADIUM_BRENDAN)
            return gSaveBlock2Ptr->playerGender != MALE;
        if (c->partnerId == PARTNER_STADIUM_MAY)
            return gSaveBlock2Ptr->playerGender == MALE;
        return TRUE;
    case STADIUM_UNLOCK_BEAT:
        p = PoolIndexOfTrainer(c->unlockValue);
        return p >= 0 && GetBit(SAVE.beaten, p);
    default:
        return SAVE.points >= c->unlockValue;
    }
}

// Na een gevecht: nieuwe compagnons verzamelen voor de melding (Vampire Survivors-stijl)
static void CollectNewUnlocks(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStadiumCompanions); i++)
    {
        if (Stadium_IsCompanionUnlocked(i) && !GetBit(SAVE.seen, i))
        {
            SetBit(SAVE.seen, i);
            if (sStadiumCompanions[i].unlockType != STADIUM_UNLOCK_START && sT.newUnlockCount < ARRAY_COUNT(sT.newUnlocks))
                sT.newUnlocks[sT.newUnlockCount++] = i;
        }
    }
}

void Stadium_HasNewUnlocks(void)
{
    gSpecialVar_Result = (sT.newUnlockCount != 0);
}

u8 Stadium_TakeNewUnlock(void)
{
    u32 i;
    u8 c;

    if (sT.newUnlockCount == 0)
        return 0xFF;
    c = sT.newUnlocks[0];
    for (i = 1; i < sT.newUnlockCount; i++)
        sT.newUnlocks[i - 1] = sT.newUnlocks[i];
    sT.newUnlockCount--;
    return c;
}

// --- bracket ------------------------------------------------------------------------------------
u8 Stadium_GetMode(void)          { return sT.mode; }
u8 Stadium_GetRound(void)         { return sT.round; }
u8 Stadium_GetRoundCount(void)    { return sT.rounds; }
u8 Stadium_GetCompanionIndex(void){ return sT.companion; }

void Stadium_SetCompanionIndex(u8 i)
{
    sT.companion = i;
    SAVE.lastCompanion = i;
}

u8 Stadium_GetBracketSlot(u32 round, u32 pos)
{
    return sT.bracket[round][pos];
}

// Trainer van deelnemer e (lid 0 of 1); de speler en zijn compagnon: TRAINER_NONE
u16 Stadium_EntrantTrainer(u8 e, u32 member)
{
    u8 p;

    if (e >= sT.entrants || e == 0)
        return TRAINER_NONE;
    p = sT.pool[e][member];
    return p == NO_POOL ? TRAINER_NONE : sStadiumPool[p].trainerId;
}

void Stadium_GetEntrantName(u8 e, u8 *dst)
{
    if (e == 0)
    {
        StringCopy(dst, gSaveBlock2Ptr->playerName);
        return;
    }
    dst = StringCopy(dst, GetTrainerNameFromId(Stadium_EntrantTrainer(e, 0)));
    if (sT.mode == STADIUM_DOUBLES)
    {
        dst = StringCopy(dst, COMPOUND_STRING(" & "));
        StringCopy(dst, GetTrainerNameFromId(Stadium_EntrantTrainer(e, 1)));
    }
}

u16 Stadium_EntrantPic(u8 e)
{
    if (e == 0)
        return gSaveBlock2Ptr->playerGender == MALE ? TRAINER_PIC_BRENDAN : TRAINER_PIC_MAY;
    return GetTrainerPicFromId(Stadium_EntrantTrainer(e, 0));
}

static u32 EntrantRating(u8 e)
{
    u32 r = sStadiumPool[sT.pool[e][0]].rating;

    if (sT.mode == STADIUM_DOUBLES)
        r = (r + sStadiumPool[sT.pool[e][1]].rating) / 2;
    return r;
}

// NPC tegen NPC: kans = 50% + 0,3% per BST-punt verschil (50 BST = 65%), begrensd op 10-90%
static u8 SimulateMatch(u8 a, u8 b)
{
    s32 chance = 500 + 3 * ((s32)EntrantRating(a) - (s32)EntrantRating(b));

    chance = max(100, min(900, chance));
    return (s32)(Random() % 1000) < chance ? a : b;
}

static u32 PlayerPos(u32 round)
{
    u32 p;

    for (p = 0; p < (sT.entrants >> round); p++)
        if (sT.bracket[round][p] == 0)
            return p;
    return 0;
}

// Alle wedstrijden van ronde r zonder de speler
static void SimulateRound(u32 r)
{
    u32 p, n = sT.entrants >> r;

    for (p = 0; p < n; p += 2)
    {
        u8 a = sT.bracket[r][p], b = sT.bracket[r][p + 1];

        if (a == 0 || b == 0)
            continue;
        sT.bracket[r + 1][p / 2] = SimulateMatch(a, b);
    }
}

static bool32 Eligible(u32 i, u16 excludeTrainer)
{
    u8 g = sStadiumPool[i].rivalFor;

    if (sStadiumPool[i].trainerId == excludeTrainer)
        return FALSE;
    return g == 0 || g == gSaveBlock2Ptr->playerGender + 1;
}

// --- specials -----------------------------------------------------------------------------------
// VAR_0x8004 = STADIUM_SINGLES/DOUBLES. Daarna: special ChooseHalfPartyForBattle (zonder restricties).
void Stadium_PrepareChooseParty(void)
{
    sT.mode = gSpecialVar_0x8004;
    VarSet(VAR_FRONTIER_FACILITY, FACILITY_STADIUM);
    gSpecialVar_0x8005 = (sT.mode == STADIUM_DOUBLES) ? STADIUM_DOUBLES_MONS : STADIUM_SINGLES_MONS;
}

void Stadium_StartTournament(void)
{
    u8 picks[STADIUM_MAX_POOL];
    u32 i, j, n = 0, need, members = (sT.mode == STADIUM_DOUBLES) ? 2 : 1;
    u16 exclude = TRAINER_NONE;

    for (i = 0; i < STADIUM_SINGLES_MONS; i++)
        sT.order[i] = gSelectedOrderFromParty[i];
    sT.round = 0;
    sT.lost = FALSE;
    sT.bp = 0;
    sT.newUnlockCount = 0;
    if (sT.mode == STADIUM_DOUBLES)
        exclude = sStadiumCompanions[sT.companion].trainerId;

    // geschikte deelnemers schudden
    for (i = 0; i < ARRAY_COUNT(sStadiumPool); i++)
        if (Eligible(i, exclude))
            picks[n++] = i;
    for (i = n - 1; i > 0; i--)
    {
        j = Random() % (i + 1);
        SWAP(picks[i], picks[j], need);
    }
    sT.entrants = (sT.mode == STADIUM_DOUBLES) ? 16 : 32;
    while (sT.entrants > 4 && (u32)(sT.entrants - 1) * members > n)
        sT.entrants /= 2;
    sT.rounds = 0;
    for (i = sT.entrants; i > 1; i /= 2)
        sT.rounds++;

    sT.pool[0][0] = sT.pool[0][1] = NO_POOL;
    for (i = 1; i < sT.entrants; i++)
    {
        sT.pool[i][0] = picks[(i - 1) * members];
        sT.pool[i][1] = (members == 2) ? picks[(i - 1) * members + 1] : NO_POOL;
    }
    // plekken in de bracket schudden
    for (i = 0; i < sT.entrants; i++)
        sT.bracket[0][i] = i;
    for (i = sT.entrants - 1; i > 0; i--)
    {
        j = Random() % (i + 1);
        SWAP(sT.bracket[0][i], sT.bracket[0][j], need);
    }
    for (i = 1; i < ARRAY_COUNT(sT.bracket); i++)
        memset(sT.bracket[i], UNKNOWN_SLOT, sizeof(sT.bracket[i]));
    SavePlayerParty();
}

// Kopie van een eigen Pokémon op level 50, volledig hersteld
static void ScaleMon(struct Pokemon *mon)
{
    u16 species = GetMonData(mon, MON_DATA_SPECIES);
    u32 exp = gExperienceTables[gSpeciesInfo[species].growthRate][STADIUM_LEVEL];

    SetMonData(mon, MON_DATA_EXP, &exp);
    CalculateMonStats(mon);
}

static void BuildPlayerParty(void)
{
    u32 i, n = (sT.mode == STADIUM_DOUBLES) ? STADIUM_DOUBLES_MONS : STADIUM_SINGLES_MONS;

    ZeroPlayerPartyMons();
    for (i = 0; i < n; i++)
    {
        if (sT.order[i] == 0)
            continue;
        gPlayerParty[i] = *GetSavedPlayerPartyMon(sT.order[i] - 1);
        ScaleMon(&gPlayerParty[i]);
    }
    CalculatePlayerPartyCount();
    HealPlayerParty();
}

static void CB2_EndStadiumBattle(void)
{
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void Task_StartStadiumBattle(u8 taskId)
{
    if (IsBattleTransitionDone() == TRUE)
    {
        gMain.savedCallback = CB2_EndStadiumBattle;
        SetMainCallback2(CB2_InitBattle);
        DestroyTask(taskId);
    }
}

static const u8 sText_StadiumDefeat[] = _("What a match!\nThe crowd is on its feet!");

// Eigen teksten per trainer (placeholders; Jordi herschrijft): nederlaag en winst. De intro staat in
// src/data/stadium_slides.h (trainer slide voor de eerste beurt). Ditto praat niet.
struct StadiumQuote
{
    u16 trainerId;
    const u8 *defeat;
    const u8 *win;
};

static const struct StadiumQuote sStadiumQuotes[] =
{
    {TRAINER_STADIUM_WARIO, COMPOUND_STRING("WAAAH! I demand a recount! And a refund! And garlic!"), COMPOUND_STRING("Wahaha! Pay up! Cash only. No coupons.")},
    {TRAINER_STADIUM_YOSHI, COMPOUND_STRING("Yoshi... sniff...\p(He cried. You did this.)"), COMPOUND_STRING("Yoshi! Yoshi!\p(Happy tears this time.)")},
    {TRAINER_STADIUM_GOLBAT, COMPOUND_STRING("skree...\p(It flaps back into the cave of your childhood.)"), COMPOUND_STRING("SKREEEEE!\p(It will be waiting in every cave. Forever.)")},
    {TRAINER_STADIUM_GRIMER, COMPOUND_STRING("Blorp... blorp.\p(It seeps away through the floor. The janitor sighs.)"), COMPOUND_STRING("BLORP!\p(The arena smells like this now.)")},
    {TRAINER_STADIUM_BOO, COMPOUND_STRING("You looked! You LOOKED! That's cheating!"), COMPOUND_STRING("Heh heh... You turned your back for one second.")},
    {TRAINER_STADIUM_MEW, COMPOUND_STRING("Mew...\p(It crawls back under the truck. See you in 1998.)"), COMPOUND_STRING("Mew! Mew!\p(It used TRANSFORM on your dignity.)")},
    {TRAINER_STADIUM_SHY_GUY_RED, COMPOUND_STRING("...!\p(He hides behind his own mask.)"), COMPOUND_STRING("...\p(A tiny victory dance. Very shy. Still a dance.)")},
    {TRAINER_STADIUM_SHY_GUY_GREEN, COMPOUND_STRING("(He has left the building. His POKéMON stayed to apologize.)"), COMPOUND_STRING("(He whispers gg. Then he hides under the bleachers.)")},
    {TRAINER_STADIUM_SHY_GUY_PINK, COMPOUND_STRING("Bzz... bzz...\p(Battery low.)"), COMPOUND_STRING("BZZZZZ!\p(A victory loop. The referee is not amused.)")},
    {TRAINER_STADIUM_SHY_GUY_BLACK, COMPOUND_STRING("This never happened. We never met. Nice mask, though."), COMPOUND_STRING("Pleasure doing business. Your wallet's in my pocket now.")},
    {TRAINER_STADIUM_BURGLAR, COMPOUND_STRING("Fine. I'll just steal the trophy later. When nobody's looking."), COMPOUND_STRING("Thanks for the win. And for your wallet.")},
    {TRAINER_STADIUM_DITTO, COMPOUND_STRING("... :)"), COMPOUND_STRING(":)")},
    {TRAINER_STADIUM_JOEY, COMPOUND_STRING("Ouch! A scrape!\pMy POOCHYENA is still top percentage, though."), COMPOUND_STRING("Told you. Top percentage. Maybe even top percent-percentage.")},
    {TRAINER_STADIUM_WINSTON, COMPOUND_STRING("Dolla Dolla Bill yo!\pI'll just buy the next tournament."), COMPOUND_STRING("Money can't buy happiness. But it bought this win.")},
    {TRAINER_STADIUM_DONALD, COMPOUND_STRING("I wish we'd never met... All six of them wish that too."), COMPOUND_STRING("Your own team, but purple. I call it DITTO MANIA.")},
    {TRAINER_STADIUM_IVAN, COMPOUND_STRING("Blupblup..."), COMPOUND_STRING("Very rare fishies. Told you. Blupblup!")},
    {TRAINER_STADIUM_JOHNSON, COMPOUND_STRING("Tik... tok...\pTime's up."), COMPOUND_STRING("Tik tok. The METRONOME has spoken.")},
    {TRAINER_STADIUM_N, COMPOUND_STRING("Your POKéMON... they actually like you.\pThat was not in my equations.\pI need a moment. Or a ferris wheel."), COMPOUND_STRING("I set your POKéMON free. They came back. They want a rematch.")},
    {TRAINER_STADIUM_GHETSIS, COMPOUND_STRING("Impossible! I am perfect! This bracket is rigged!\pI'll be in my castle. Sulking. Majestically."), COMPOUND_STRING("Bow before me! Or sit down. Sitting is also fine.")},
    {TRAINER_STADIUM_ZINZOLIN, COMPOUND_STRING("Defeated... and STILL cold.\pSomebody bring me a blanket. And a new career."), COMPOUND_STRING("Cold, isn't it? Welcome to my life.")},
    {TRAINER_STADIUM_ROOD, COMPOUND_STRING("A wonderful battle. Your POKéMON look happy.\pI'll still write you a strongly worded letter. Kindly."), COMPOUND_STRING("Everyone gets a WISH. Except your team. They get a nap.")},
    {TRAINER_STADIUM_SHADOW_TRIAD, COMPOUND_STRING("We vanish now.\p...The door is locked. We'll wait for the next round."), COMPOUND_STRING("You blinked. We won. That's the whole technique.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_M, COMPOUND_STRING("Lost again? My boss is going to yell at me.\pHe yells at everyone. It's his whole personality."), COMPOUND_STRING("Ha! Hand over your POKéMON! ...No? Okay. Worth a shot.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_F, COMPOUND_STRING("Fine. I'm unionizing the grunts.\pFirst demand: a dental plan."), COMPOUND_STRING("Grunt of the month! Again! There's no prize, but still.")},
    {TRAINER_STADIUM_LYLE, COMPOUND_STRING("Level 50 and still... Maybe I should start training their IVs... hmm."), COMPOUND_STRING("Told you! Indestructible! I'm calling my brother.")},
};

static const struct StadiumQuote *GetQuote(u32 trainerId)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStadiumQuotes); i++)
        if (sStadiumQuotes[i].trainerId == trainerId)
            return &sStadiumQuotes[i];
    return NULL;
}

static const u8 *GetDefeatText(u32 trainerId)
{
    const struct StadiumQuote *q = GetQuote(trainerId);

    return q ? q->defeat : sText_StadiumDefeat;
}

void Stadium_StartMatch(void)
{
    u32 pos = PlayerPos(sT.round);
    u8 opp = sT.bracket[sT.round][pos ^ 1];

    BuildPlayerParty();
    memset(&gTrainerBattleParameter, 0, sizeof(gTrainerBattleParameter));
    TRAINER_BATTLE_PARAM.opponentA = Stadium_EntrantTrainer(opp, 0);
    TRAINER_BATTLE_PARAM.defeatTextA = (u8 *)GetDefeatText(TRAINER_BATTLE_PARAM.opponentA);
    gBattleTypeFlags = BATTLE_TYPE_TRAINER;
    if (sT.mode == STADIUM_DOUBLES)
    {
        TRAINER_BATTLE_PARAM.opponentB = Stadium_EntrantTrainer(opp, 1);
        TRAINER_BATTLE_PARAM.defeatTextB = (u8 *)GetDefeatText(TRAINER_BATTLE_PARAM.opponentB);
        gBattleTypeFlags |= BATTLE_TYPE_DOUBLE | BATTLE_TYPE_TWO_OPPONENTS | BATTLE_TYPE_MULTI | BATTLE_TYPE_INGAME_PARTNER;
        gPartnerTrainerId = TRAINER_PARTNER(sStadiumCompanions[sT.companion].partnerId);
        FillPartnerParty(gPartnerTrainerId);
    }
    gStadiumBattle = TRUE;
    CreateTask(Task_StartStadiumBattle, 1);
    PlayMapChosenOrBattleBGM(0);
    BattleTransition_StartOnField(GetTrainerBattleTransition());
}

// VAR_RESULT: 0 = verloren, 1 = door naar de volgende ronde, 2 = kampioen
void Stadium_AfterMatch(void)
{
    u32 pos = PlayerPos(sT.round);
    u8 opp = sT.bracket[sT.round][pos ^ 1];
    u32 m;

    gStadiumBattle = FALSE;
    if (gBattleOutcome != B_OUTCOME_WON)
    {
        sT.lost = TRUE;
        gSpecialVar_Result = 0;
        return;
    }
    // gewonnen: BP, punten, verslagen trainers (compagnons)
    sT.bp += sBpPerRound[min(sT.round + (5 - sT.rounds), ARRAY_COUNT(sBpPerRound) - 1)];
    SAVE.points = min(0xFFFF, SAVE.points + STADIUM_POINTS_WIN);
    SAVE.matchesWon = min(0xFFFF, SAVE.matchesWon + 1);
    for (m = 0; m < 2; m++)
        if (sT.pool[opp][m] != NO_POOL)
            SetBit(SAVE.beaten, sT.pool[opp][m]);
    sT.bracket[sT.round + 1][pos / 2] = 0;
    SimulateRound(sT.round);
    sT.round++;
    if (sT.round >= sT.rounds)
    {
        SAVE.titles[sT.mode] = min(0xFFFF, SAVE.titles[sT.mode] + 1);
        SAVE.points = min(0xFFFF, SAVE.points + STADIUM_POINTS_TITLE);
        gSpecialVar_Result = 2;
    }
    else
    {
        gSpecialVar_Result = 1;
    }
    CollectNewUnlocks();
}

// Team terugzetten en BP uitbetalen. gStringVar1 = verdiende BP.
void Stadium_EndTournament(void)
{
    u32 bp = gSaveBlock2Ptr->frontier.battlePoints + sT.bp;

    LoadPlayerParty();
    gSaveBlock2Ptr->frontier.battlePoints = min(MAX_BATTLE_FRONTIER_POINTS, bp);
    SAVE.points = min(0xFFFF, SAVE.points + STADIUM_POINTS_TOURNAMENT);
    CollectNewUnlocks();
    ConvertIntToDecimalStringN(gStringVar1, sT.bp, STR_CONV_MODE_LEFT_ALIGN, 3);
    VarSet(VAR_FRONTIER_FACILITY, 0);
}

// --- gevechtshaakjes ------------------------------------------------------------------------------
// Team van een tegenstander: de keuze uit pool.py (singles 4 / doubles 3, synergie, ace altijd), level 50.
u8 Stadium_BuildTrainerParty(struct Pokemon *party, u16 trainerNum, bool8 firstTrainer)
{
    const struct Trainer *trainer = GetTrainerStructFromId(trainerNum);
    s32 p = PoolIndexOfTrainer(trainerNum);
    u8 mask = 0x3F;
    struct TrainerMon mons[PARTY_SIZE];
    struct Trainer temp;
    u32 i, n = 0;

    if (p >= 0)
        mask = (sT.mode == STADIUM_DOUBLES) ? sStadiumPool[p].doublesMask : sStadiumPool[p].singlesMask;
    for (i = 0; i < trainer->partySize && i < PARTY_SIZE; i++)
    {
        if (!(mask & (1 << i)))
            continue;
        mons[n] = trainer->party[i];
        mons[n].lvl = STADIUM_LEVEL;
        n++;
    }
    temp = *trainer;
    temp.party = mons;
    temp.partySize = n;
    temp.poolSize = 0;
    return CreateNPCTrainerPartyFromTrainer(party, &temp, firstTrainer, gBattleTypeFlags);
}

bool32 Stadium_PartnerUsesFrontPic(void)
{
    return gStadiumBattle && sT.mode == STADIUM_DOUBLES && sStadiumCompanions[sT.companion].frontPic;
}

// Wat een trainer zegt als hij van je wint (placeholders; Jordi herschrijft)
const u8 *Stadium_GetWinText(u32 opponent)
{
    static const u8 sWin1[] = _("That's how it's done in the Stadium!");
    static const u8 sWin2[] = _("Better luck next tournament.\nThe crowd still loves you. A bit.");
    static const u8 sWin3[] = _("The bracket has spoken.");
    const struct StadiumQuote *q = GetQuote(opponent);

    if (q != NULL)
        return q->win;
    switch (Random() % 3)
    {
    case 0:  return sWin1;
    case 1:  return sWin2;
    default: return sWin3;
    }
}

// Debug: alle compagnons vrij (alle deelnemers verslagen, veel punten); meldingen overslaan
void Stadium_DebugUnlockAll(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStadiumPool); i++)
        SetBit(SAVE.beaten, i);
    for (i = 0; i < ARRAY_COUNT(sStadiumCompanions); i++)
        SetBit(SAVE.seen, i);
    SAVE.points = 0xFFFF;
}

// Bord in de lobby: gStringVar1-3 = titels singles/doubles, gewonnen wedstrijden
void Stadium_GetRecord(void)
{
    ConvertIntToDecimalStringN(gStringVar1, SAVE.titles[STADIUM_SINGLES], STR_CONV_MODE_LEFT_ALIGN, 5);
    ConvertIntToDecimalStringN(gStringVar2, SAVE.titles[STADIUM_DOUBLES], STR_CONV_MODE_LEFT_ALIGN, 5);
    ConvertIntToDecimalStringN(gStringVar3, SAVE.matchesWon, STR_CONV_MODE_LEFT_ALIGN, 5);
}

// --- arena (Battle Dome-zaal met publiek) ---------------------------------------------------------
static u8 CurrentOpponent(void)
{
    return sT.bracket[sT.round][PlayerPos(sT.round) ^ 1];
}

static u16 EntrantGfx(u8 e, u32 member)
{
    s32 p = PoolIndexOfTrainer(Stadium_EntrantTrainer(e, member));

    return p >= 0 ? sStadiumPool[p].gfx : OBJ_EVENT_GFX_MAN_3;
}

// VAR_OBJ_GFX_ID_0/2 = tegenstanders, _1 = speler, _3 = compagnon; VAR_RESULT = singles/doubles
void Stadium_SetArenaGfx(void)
{
    u8 opp = CurrentOpponent();

    VarSet(VAR_OBJ_GFX_ID_0, EntrantGfx(opp, 0));
    VarSet(VAR_OBJ_GFX_ID_1, gSaveBlock2Ptr->playerGender == MALE ? OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL : OBJ_EVENT_GFX_RIVAL_MAY_NORMAL);
    if (sT.mode == STADIUM_DOUBLES)
    {
        VarSet(VAR_OBJ_GFX_ID_2, EntrantGfx(opp, 1));
        VarSet(VAR_OBJ_GFX_ID_3, sStadiumCompanions[sT.companion].gfx);
    }
    gSpecialVar_Result = sT.mode;
}

// gStringVar1 = speler (en compagnon), gStringVar2 = tegenstander(s), gStringVar3 = ronde
void Stadium_GetMatchNames(void)
{
    const u8 *const sRounds[] = {
        COMPOUND_STRING("first round"), COMPOUND_STRING("second round"), COMPOUND_STRING("quarterfinal"),
        COMPOUND_STRING("semifinal"), COMPOUND_STRING("FINAL") };
    u8 *p = StringCopy(gStringVar1, gSaveBlock2Ptr->playerName);

    if (sT.mode == STADIUM_DOUBLES)
    {
        p = StringCopy(p, COMPOUND_STRING(" & "));
        StringCopy(p, GetTrainerNameFromId(TRAINER_PARTNER(sStadiumCompanions[sT.companion].partnerId)));
    }
    Stadium_GetEntrantName(CurrentOpponent(), gStringVar2);
    StringCopy(gStringVar3, sRounds[min(sT.round + (5 - sT.rounds), 4)]);
}

// Omroeper in de arena: gStringVar4 = één zin over de tegenstander (doubles: één van de twee, willekeurig).
// Teksten in src/data/stadium_announcer.h (tools/grounded/stadium/announcer.py).
void Stadium_GetAnnouncerLine(void)
{
    u8 opp = CurrentOpponent();
    u16 trainerId = Stadium_EntrantTrainer(opp, 0);
    const u8 *text = sStadiumAnnouncerFallback;
    u32 i;

    if (sT.mode == STADIUM_DOUBLES && (Random() & 1) && Stadium_EntrantTrainer(opp, 1) != TRAINER_NONE)
        trainerId = Stadium_EntrantTrainer(opp, 1);
    for (i = 0; i < ARRAY_COUNT(sStadiumAnnouncerLines); i++)
    {
        if (sStadiumAnnouncerLines[i].trainerId == trainerId)
        {
            text = sStadiumAnnouncerLines[i].text;
            break;
        }
    }
    StringCopy(gStringVar4, text);
}

// gStringVar1 = verdiende BP (opnieuw, na de meldingsschermen)
void Stadium_GetBpText(void)
{
    ConvertIntToDecimalStringN(gStringVar1, sT.bp, STR_CONV_MODE_LEFT_ALIGN, 3);
}
