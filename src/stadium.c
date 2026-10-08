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
#include "battle_main.h"
#include "pokemon_storage_system.h"
#include "money.h"
#include "malloc.h"
#include "overworld.h"
#include "party_menu.h"
#include "pokedex.h"
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
#include "constants/characters.h"

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
        dst = StringCopy(dst, gSaveBlock2Ptr->playerName);
        if (sT.mode == STADIUM_DOUBLES)
        {
            dst = StringCopy(dst, COMPOUND_STRING(" & "));
            StringCopy(dst, GetTrainerNameFromId(TRAINER_PARTNER(sStadiumCompanions[sT.companion].partnerId)));
        }
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
    return Stadium_EntrantMemberPic(e, 0);
}

// Trainerfoto van lid 0 of 1 (doubles); deelnemer 0 lid 1 = de compagnon
u16 Stadium_EntrantMemberPic(u8 e, u32 member)
{
    if (e == 0 && member == 0)
        return gSaveBlock2Ptr->playerGender == MALE ? TRAINER_PIC_BRENDAN : TRAINER_PIC_MAY;
    if (e == 0)
        return GetTrainerPicFromId(TRAINER_PARTNER(sStadiumCompanions[sT.companion].partnerId));
    return GetTrainerPicFromId(Stadium_EntrantTrainer(e, member));
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
    if (SAVE.tournaments < 0xFF)
        SAVE.tournaments++;
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
    {TRAINER_STADIUM_WARIO, COMPOUND_STRING("WAAAH! I demand a recount! And a\nrefund! And garlic!"), COMPOUND_STRING("Wahaha! Pay up! Cash only. No coupons.")},
    {TRAINER_STADIUM_YOSHI, COMPOUND_STRING("Yoshi... sniff...\p(He cried. You did this.)"), COMPOUND_STRING("Yoshi! Yoshi!\p(Happy tears this time.)")},
    {TRAINER_STADIUM_GOLBAT, COMPOUND_STRING("skree...\p(It flaps back into the cave of your\nchildhood.)"), COMPOUND_STRING("SKREEEEE!\p(It will be waiting in every cave.\nForever.)")},
    {TRAINER_STADIUM_GRIMER, COMPOUND_STRING("Blorp... blorp.\p(It seeps away through the floor. The\njanitor sighs.)"), COMPOUND_STRING("BLORP!\p(The arena smells like this now.)")},
    {TRAINER_STADIUM_BOO, COMPOUND_STRING("You looked! You LOOKED! That's\ncheating!"), COMPOUND_STRING("Heh heh... You turned your back for\none second.")},
    {TRAINER_STADIUM_MEW, COMPOUND_STRING("Mew...\p(It crawls back under the truck. See\nyou in 1998.)"), COMPOUND_STRING("Mew! Mew!\p(It used TRANSFORM on your dignity.)")},
    {TRAINER_STADIUM_SHY_GUY_RED, COMPOUND_STRING("...!\p(He hides behind his own mask.)"), COMPOUND_STRING("...\p(A tiny victory dance. Very shy. Still a\ndance.)")},
    {TRAINER_STADIUM_SHY_GUY_GREEN, COMPOUND_STRING("(He has left the building. His POKéMON\nstayed to apologize.)"), COMPOUND_STRING("(He whispers gg. Then he hides under\nthe bleachers.)")},
    {TRAINER_STADIUM_SHY_GUY_PINK, COMPOUND_STRING("Bzz... bzz...\p(Battery low.)"), COMPOUND_STRING("BZZZZZ!\p(A victory loop. The referee is not\namused.)")},
    {TRAINER_STADIUM_SHY_GUY_BLACK, COMPOUND_STRING("This never happened. We never met.\nNice mask, though."), COMPOUND_STRING("Pleasure doing business. Your wallet's\nin my pocket now.")},
    {TRAINER_STADIUM_BURGLAR, COMPOUND_STRING("Fine. I'll just steal the trophy later.\nWhen nobody's looking."), COMPOUND_STRING("Thanks for the win. And for your\nwallet.")},
    {TRAINER_STADIUM_DITTO, COMPOUND_STRING("... :)"), COMPOUND_STRING(":)")},
    {TRAINER_STADIUM_JOEY, COMPOUND_STRING("Ouch! A scrape!\pMy POOCHYENA is still top percentage,\nthough."), COMPOUND_STRING("Told you. Top percentage. Maybe even\ntop percent-percentage.")},
    {TRAINER_STADIUM_WINSTON, COMPOUND_STRING("Dolla Dolla Bill yo!\pI'll just buy the next tournament."), COMPOUND_STRING("Money can't buy happiness. But it\nbought this win.")},
    {TRAINER_STADIUM_DONALD, COMPOUND_STRING("I wish we'd never met... All six of them\nwish that too."), COMPOUND_STRING("Your own team, but purple. I call it\nDITTO MANIA.")},
    {TRAINER_STADIUM_IVAN, COMPOUND_STRING("Blupblup..."), COMPOUND_STRING("Very rare fishies. Told you. Blupblup!")},
    {TRAINER_STADIUM_JOHNSON, COMPOUND_STRING("Tik... tok...\pTime's up."), COMPOUND_STRING("Tik tok. The METRONOME has spoken.")},
    {TRAINER_STADIUM_N, COMPOUND_STRING("Your POKéMON... they actually like you.\pThat was not in my equations.\pI need a moment. Or a ferris wheel."), COMPOUND_STRING("I set your POKéMON free. They came\nback. They want a rematch.")},
    {TRAINER_STADIUM_GHETSIS, COMPOUND_STRING("Impossible! I am perfect! This\nbracket is rigged!\pI'll be in my castle. Sulking.\nMajestically."), COMPOUND_STRING("Bow before me! Or sit down. Sitting is\nalso fine.")},
    {TRAINER_STADIUM_ZINZOLIN, COMPOUND_STRING("Defeated... and STILL cold.\pSomebody bring me a blanket. And a new\ncareer."), COMPOUND_STRING("Cold, isn't it? Welcome to my life.")},
    {TRAINER_STADIUM_ROOD, COMPOUND_STRING("A wonderful battle. Your POKéMON look\nhappy.\pI'll still write you a strongly worded\nletter. Kindly."), COMPOUND_STRING("Everyone gets a WISH. Except your\nteam. They get a nap.")},
    {TRAINER_STADIUM_SHADOW_TRIAD, COMPOUND_STRING("We vanish now.\p...The door is locked. We'll wait for the\nnext round."), COMPOUND_STRING("You blinked. We won. That's the whole\ntechnique.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_M, COMPOUND_STRING("Lost again? My boss is going to yell at\nme.\pHe yells at everyone. It's his whole\npersonality."), COMPOUND_STRING("Ha! Hand over your POKéMON! ...No?\nOkay. Worth a shot.")},
    {TRAINER_STADIUM_PLASMA_GRUNT_F, COMPOUND_STRING("Fine. I'm unionizing the grunts.\pFirst demand: a dental plan."), COMPOUND_STRING("Grunt of the month! Again! There's no\nprize, but still.")},
    {TRAINER_STADIUM_PETREL, COMPOUND_STRING("Unmasked by a child. Again.\pI'll tell the boss it was someone else.\pI'm very good at being someone else."), COMPOUND_STRING("You fought a MIMIKYU, a ZOROARK and\nyourself. Only one of them was real.")},
    {TRAINER_PLASMA_NIGEL, COMPOUND_STRING("Returned to sender. Again.\pI'll file a complaint. With myself. I'm\nalso Complaints."), COMPOUND_STRING("Delivered on time! First time ever!\nSomebody take a picture!")},
    {TRAINER_STADIUM_LYLE, COMPOUND_STRING("Level 50 and still... Maybe I should\nstart training their IVs... hmm."), COMPOUND_STRING("Told you! Indestructible! I'm calling\nmy brother.")},
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
    u32 i, pos = PlayerPos(sT.round);
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
        for (i = MULTI_PARTY_SIZE; i < PARTY_SIZE; i++)    // compagnon = tegenstanderversie (IV's/EV's per ronde)
        {
            if (GetMonData(&gPlayerParty[i], MON_DATA_SPECIES) == SPECIES_NONE)
                continue;
            Stadium_ScaleCompanionMon(&gPlayerParty[i]);
            CalculateMonStats(&gPlayerParty[i]);
        }
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
// Balans (Jordi verloor zonder EV-training bijna alles): de tegenstanders bouwen hun EV's per wedstrijd op.
// Eerste wedstrijd zonder EV's, dan 1/3, 2/3, vanaf de vierde alles (singles: halve finale; doubles: finale).
static const u8 sStadiumEvPercent[] = {0, 33, 67, 100};
// Jordi (8 okt): nog eerlijker; ook de IV's lopen op (max per stat), zodat de eerste rondes geen Showdown-teams zijn
static const u8 sStadiumIvCap[] = {20, 24, 28, 31};

// IV's (gepakt, 5 bits per stat) begrensd op het plafond van deze ronde
u32 Stadium_CapIvs(u32 ivs)
{
    u32 s, cap = sStadiumIvCap[min(sT.round, ARRAY_COUNT(sStadiumIvCap) - 1)], iv = 0;

    for (s = 0; s < NUM_STATS; s++)
        iv |= min((ivs >> (5 * s)) & MAX_IV_MASK, cap) << (5 * s);
    return iv;
}

// Jordi (8 okt): compagnon = zijn tegenstanderversie, ook in IV's/EV's. Dezelfde opbouw per ronde als de
// tegenstanders (Stadium_StartMatch na FillPartnerParty; daarna CalculateMonStats).
void Stadium_ScaleCompanionMon(struct Pokemon *mon)
{
    u32 s, evPercent = sStadiumEvPercent[min(sT.round, ARRAY_COUNT(sStadiumEvPercent) - 1)];

    for (s = 0; s < NUM_STATS; s++)
    {
        u32 iv = min(GetMonData(mon, MON_DATA_HP_IV + s), sStadiumIvCap[min(sT.round, ARRAY_COUNT(sStadiumIvCap) - 1)]);
        u32 ev = GetMonData(mon, MON_DATA_HP_EV + s) * evPercent / 100;
        SetMonData(mon, MON_DATA_HP_IV + s, &iv);
        SetMonData(mon, MON_DATA_HP_EV + s, &ev);
    }
}

// Bron-trainer van de gekozen compagnon (TRAINER_NONE bij trio's): de compagnon krijgt diens AI
u16 Stadium_CompanionSourceTrainer(void)
{
    return sStadiumCompanions[sT.companion].trainerId;
}

// Team van een tegenstander: de keuze uit pool.py (singles 4 / doubles 3, synergie, ace altijd), level 50.
u8 Stadium_BuildTrainerParty(struct Pokemon *party, u16 trainerNum, bool8 firstTrainer)
{
    const struct Trainer *trainer = GetTrainerStructFromId(trainerNum);
    s32 p = PoolIndexOfTrainer(trainerNum);
    u8 mask = 0x3F;
    struct TrainerMon mons[PARTY_SIZE];
    u8 evs[PARTY_SIZE][NUM_STATS];
    struct Trainer temp;
    u32 i, s, n = 0, evPercent = sStadiumEvPercent[min(sT.round, ARRAY_COUNT(sStadiumEvPercent) - 1)];

    if (p >= 0)
        mask = (sT.mode == STADIUM_DOUBLES) ? sStadiumPool[p].doublesMask : sStadiumPool[p].singlesMask;
    for (i = 0; i < trainer->partySize && i < PARTY_SIZE; i++)
    {
        if (!(mask & (1 << i)))
            continue;
        mons[n] = trainer->party[i];
        mons[n].lvl = STADIUM_LEVEL;
        mons[n].iv = Stadium_CapIvs(mons[n].iv);
        if (mons[n].ev != NULL && evPercent < 100)
        {
            for (s = 0; s < NUM_STATS; s++)
                evs[n][s] = mons[n].ev[s] * evPercent / 100;
            mons[n].ev = evs[n];
        }
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

// --- omroeper -------------------------------------------------------------------------------------
// Teksten in src/data/stadium_announcer.h (tools/grounded/stadium/announcer.py).
static const u8 *AnnouncerLineFor(u16 trainerId)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStadiumAnnouncerLines); i++)
        if (sStadiumAnnouncerLines[i].trainerId == trainerId)
            return sStadiumAnnouncerLines[i].text;
    return sStadiumAnnouncerFallback;
}

// Legendaries die de speler gevangen kan hebben (voor de spelerszin)
static const u16 sAnnouncerLegends[] =
{
    SPECIES_RAYQUAZA, SPECIES_GROUDON, SPECIES_KYOGRE, SPECIES_MEWTWO, SPECIES_GIRATINA, SPECIES_DARKRAI,
    SPECIES_JIRACHI, SPECIES_DEOXYS, SPECIES_REGIGIGAS, SPECIES_HEATRAN, SPECIES_GENESECT, SPECIES_VICTINI,
    SPECIES_SHAYMIN, SPECIES_LATIAS, SPECIES_LATIOS, SPECIES_RAIKOU, SPECIES_ENTEI, SPECIES_SUICUNE,
    SPECIES_REGIROCK, SPECIES_REGICE, SPECIES_REGISTEEL, SPECIES_REGIELEKI, SPECIES_REGIDRAGO, SPECIES_ZARUDE,
};

static bool32 Caught(u16 species)
{
    return GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_CAUGHT);
}

static const u16 sAnnouncerBirchFights[] =
{
    TRAINER_BIRCH, TRAINER_BIRCH_2, TRAINER_BIRCH_VERDANTURF, TRAINER_BIRCH_MOSSDEEP, TRAINER_BIRCH_UNDERWATER, TRAINER_BIRCH_RESORT,
};
static const u16 sAnnouncerDaveFights[] =
{
    TRAINER_DAVE_ROUTE_111, TRAINER_DAVE_PETALBURG, TRAINER_DAVE_SOOTOPOLIS, TRAINER_DAVE,
};
static const u16 sAnnouncerServiceFights[] =
{
    TRAINER_ARCHIE_SERVICE_1, TRAINER_ARCHIE_SERVICE_2, TRAINER_ARCHIE_SERVICE_3, TRAINER_ARCHIE_SERVICE_4,
    TRAINER_MAXIE_SERVICE_1, TRAINER_MAXIE_SERVICE_2, TRAINER_MAXIE_SERVICE_3, TRAINER_MAXIE_SERVICE_4,
};

static u32 CountFought(const u16 *trainers, u32 count)
{
    u32 i, n = 0;

    for (i = 0; i < count; i++)
        n += HasTrainerBeenFought(trainers[i]) ? 1 : 0;
    return n;
}

// Team + pc: de soort die de speler het vaakst heeft (fan van X) en het aantal shiny's
static void CountOwnedMons(u16 *fanSpecies, u32 *fanCount, u32 *shinies)
{
    u8 *counts = AllocZeroed(NUM_SPECIES);
    u32 box, pos, i, species;

    *fanSpecies = SPECIES_NONE;
    *fanCount = 0;
    *shinies = 0;
    if (counts == NULL)
        return;
    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon = GetSavedPlayerPartyMon(i);
        species = GetMonData(mon, MON_DATA_SPECIES_OR_EGG);
        if (species == SPECIES_NONE || species >= NUM_SPECIES)
            continue;
        if (counts[species] < 255)
            counts[species]++;
        *shinies += GetMonData(mon, MON_DATA_IS_SHINY) ? 1 : 0;
    }
    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
    {
        for (pos = 0; pos < IN_BOX_COUNT; pos++)
        {
            struct BoxPokemon *mon = GetBoxedMonPtr(box, pos);
            species = GetBoxMonData(mon, MON_DATA_SPECIES_OR_EGG);
            if (species == SPECIES_NONE || species >= NUM_SPECIES)
                continue;
            if (counts[species] < 255)
                counts[species]++;
            *shinies += GetBoxMonData(mon, MON_DATA_IS_SHINY) ? 1 : 0;
        }
    }
    for (i = 1; i < NUM_SPECIES; i++)
    {
        if (counts[i] > *fanCount)
        {
            *fanCount = counts[i];
            *fanSpecies = i;
        }
    }
    Free(counts);
}

// Het gekozen Stadium-team: een MAGIKARP erin? Deelt iedereen een type (TYPE_NONE = nee)?
static void CheckStadiumTeam(bool32 *magikarp, u32 *monoType)
{
    u32 i, j, t, n = 0, size = (sT.mode == STADIUM_DOUBLES) ? STADIUM_DOUBLES_MONS : STADIUM_SINGLES_MONS;
    u16 species[STADIUM_SINGLES_MONS];

    *magikarp = FALSE;
    *monoType = TYPE_NONE;
    for (i = 0; i < size; i++)
    {
        if (sT.order[i] == 0)
            continue;
        species[n] = GetMonData(GetSavedPlayerPartyMon(sT.order[i] - 1), MON_DATA_SPECIES);
        if (species[n] == SPECIES_MAGIKARP)
            *magikarp = TRUE;
        n++;
    }
    if (n < 3)
        return;
    for (t = 0; t < 2; t++)
    {
        u32 type = gSpeciesInfo[species[0]].types[t];
        for (j = 1; j < n; j++)
            if (gSpeciesInfo[species[j]].types[0] != type && gSpeciesInfo[species[j]].types[1] != type)
                break;
        if (j == n)
        {
            *monoType = type;
            return;
        }
    }
}

// Zin over de speler op basis van wat het spel van hem weet (Jordi: "Grey Fox in MGS"). Alle zinnen waarvan de
// voorwaarde klopt doen mee, gewogen (sStadiumAnnouncerPlayerWeight: specifiek 6, opvallend 3, algemeen 1); geen = de
// vanilla-zin. Zet gStringVar1 (soort/type) en gStringVar2 (getal) voor de gekozen zin.
static const u8 *AnnouncePlayer(void)
{
    u8 options[ANNOUNCE_PLAYER_COUNT];
    u32 num[ANNOUNCE_PLAYER_COUNT];
    const u8 *name[ANNOUNCE_PLAYER_COUNT];
    u16 legends[ARRAY_COUNT(sAnnouncerLegends)];
    u32 n = 0, nLegends = 0, i, total = 0, r, fanCount, shinies, monoType, money;
    u16 fanSpecies;
    bool32 magikarp;

#define ADD(id, value, str) do { options[n++] = (id); num[id] = (value); name[id] = (str); total += sStadiumAnnouncerPlayerWeight[id]; } while (0)
#define STAT_AT_LEAST(id, stat, min) do { u32 v_ = GetGameStat(stat); if (v_ >= (min)) ADD(id, v_, NULL); } while (0)

    // Jordi's voorbeelden. White-outs: een gewone run van deze pittige game heeft er ±5-10; 15+ is bovengemiddeld.
    STAT_AT_LEAST(ANNOUNCE_PLAYER_WHITE_OUTS, GAME_STAT_WHITE_OUTS, 15);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_LEAGUE_BULLY, GAME_STAT_ENTERED_HOF, 10);
    CountOwnedMons(&fanSpecies, &fanCount, &shinies);
    if (fanCount >= 5)
        ADD(ANNOUNCE_PLAYER_FAN, fanCount, GetSpeciesName(fanSpecies));
    // het Stadium-team
    CheckStadiumTeam(&magikarp, &monoType);
    if (magikarp)
        ADD(ANNOUNCE_PLAYER_MAGIKARP, 0, NULL);
    if (monoType != TYPE_NONE)
        ADD(ANNOUNCE_PLAYER_MONOTYPE, 0, gTypesInfo[monoType].name);
    // 'we weten wat je deed'
    if (FlagGet(FLAG_USED_IMPLOSION))
        ADD(ANNOUNCE_PLAYER_IMPLOSION, 0, NULL);
    if (FlagGet(FLAG_CAUGHT_SHIP_SPIRITOMB))
        ADD(ANNOUNCE_PLAYER_TRASH_SPIRITOMB, 0, NULL);
    if (FlagGet(FLAG_HOOPA_WISH_SNACK))
        ADD(ANNOUNCE_PLAYER_HOOPA_SNACK, 0, NULL);
    if (FlagGet(FLAG_HOOPA_WISH_FAME))
        ADD(ANNOUNCE_PLAYER_HOOPA_FAME, 0, NULL);
    if (FlagGet(FLAG_HOOPA_WISH_RICHES))
        ADD(ANNOUNCE_PLAYER_HOOPA_RICHES, 0, NULL);
    if (FlagGet(FLAG_HOOPA_WISH_POWER))
        ADD(ANNOUNCE_PLAYER_HOOPA_POWER, 0, NULL);
    if (VarGet(VAR_BURGLAR_DEFEATS) >= 5)
        ADD(ANNOUNCE_PLAYER_BURGLAR, VarGet(VAR_BURGLAR_DEFEATS), NULL);
    if (CountFought(sAnnouncerBirchFights, ARRAY_COUNT(sAnnouncerBirchFights)) >= 5)
        ADD(ANNOUNCE_PLAYER_BIRCH, 0, NULL);
    if (CountFought(sAnnouncerDaveFights, ARRAY_COUNT(sAnnouncerDaveFights)) == ARRAY_COUNT(sAnnouncerDaveFights))
        ADD(ANNOUNCE_PLAYER_DAVE, 0, NULL);
    if (CountFought(sAnnouncerServiceFights, ARRAY_COUNT(sAnnouncerServiceFights)) > 0)
        ADD(ANNOUNCE_PLAYER_COMMUNITY_SERVICE, 0, NULL);
    if (FlagGet(FLAG_CAUGHT_SHINY_RAYQUAZA))
        ADD(ANNOUNCE_PLAYER_SHINY_RAYQUAZA, 0, NULL);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_RELEASED, GAME_STAT_RELEASED_MONS, 30);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_FAINTED, GAME_STAT_OWN_MONS_FAINTED, 200);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_FLED, GAME_STAT_FLED_BATTLES, 50);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_SPLASH, GAME_STAT_USED_SPLASH, 10);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_STRUGGLE, GAME_STAT_USED_STRUGGLE, 10);
    // opvallende statistieken
    STAT_AT_LEAST(ANNOUNCE_PLAYER_STEPS, GAME_STAT_STEPS, 100000);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_EGGS, GAME_STAT_HATCHED_EGGS, 50);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_FISHING, GAME_STAT_FISHING_ENCOUNTERS, 200);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_SAVES, GAME_STAT_SAVED_GAME, 500);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_POKECENTER, GAME_STAT_USED_POKECENTER, 300);
    if (shinies >= 3)
        ADD(ANNOUNCE_PLAYER_SHINIES, shinies, NULL);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_LEDGES, GAME_STAT_JUMPED_DOWN_LEDGES, 300);
    STAT_AT_LEAST(ANNOUNCE_PLAYER_JACKPOT, GAME_STAT_SLOT_JACKPOTS, 1);
    money = GetMoney(&gSaveBlock1Ptr->money);
    if (money >= 500000)
        ADD(ANNOUNCE_PLAYER_RICH, 0, NULL);
    else if (money < 1000 && FlagGet(FLAG_BADGE01_GET))
        ADD(ANNOUNCE_PLAYER_BROKE, 0, NULL);
    for (i = 0; i < ARRAY_COUNT(sAnnouncerLegends); i++)
        if (Caught(sAnnouncerLegends[i]))
            legends[nLegends++] = sAnnouncerLegends[i];
    if (nLegends > 0)
        ADD(ANNOUNCE_PLAYER_LEGENDARY, 0, GetSpeciesName(legends[Random() % nLegends]));
    if (GetNationalPokedexCount(FLAG_GET_CAUGHT) >= 200)
        ADD(ANNOUNCE_PLAYER_BIG_DEX, 0, NULL);
    if (gSaveBlock2Ptr->playTimeHours >= 100)
        ADD(ANNOUNCE_PLAYER_PLAYTIME, 0, NULL);
    // algemeen
    if (SAVE.titles[STADIUM_SINGLES] + SAVE.titles[STADIUM_DOUBLES] > 0)
        ADD(ANNOUNCE_PLAYER_TITLES, 0, NULL);
    else if (SAVE.tournaments >= 2)
        ADD(ANNOUNCE_PLAYER_RETURNING, 0, NULL);
    if (SAVE.matchesWon >= 20)
        ADD(ANNOUNCE_PLAYER_VETERAN, 0, NULL);
    if (SAVE.matchesWon == 0 && SAVE.tournaments <= 1)
        ADD(ANNOUNCE_PLAYER_NEWCOMER, 0, NULL);
    if (FlagGet(FLAG_SYS_GAME_CLEAR))
        ADD(ANNOUNCE_PLAYER_HALL_OF_FAME, 0, NULL);
    else if (FlagGet(FLAG_BADGE08_GET))
        ADD(ANNOUNCE_PLAYER_EIGHT_BADGES, 0, NULL);
    if (FlagGet(FLAG_SYS_POKEMON_GET) && VarGet(VAR_STARTER_MON) <= 2)
        ADD(ANNOUNCE_PLAYER_TREECKO + VarGet(VAR_STARTER_MON), 0, NULL);
#undef ADD
#undef STAT_AT_LEAST

    if (n == 0)
        return sStadiumAnnouncerVanilla;
    r = Random() % total;
    for (i = 0; i < n - 1; i++)
    {
        if (r < sStadiumAnnouncerPlayerWeight[options[i]])
            break;
        r -= sStadiumAnnouncerPlayerWeight[options[i]];
    }
    if (name[options[i]] != NULL)
        StringCopy(gStringVar1, name[options[i]]);
    ConvertIntToDecimalStringN(gStringVar2, num[options[i]], STR_CONV_MODE_LEFT_ALIGN, 8);
    return sStadiumAnnouncerPlayer[options[i]];
}

// De compagnon (Jordi: "de compagnon moet hun typische tekst krijgen"): eigen compagnonzin, anders zijn omroepzin als
// tegenstander, pas daarna een algemene zin. Zet gStringVar1 = naam van de compagnon.
static const u8 *AnnounceCompanion(void)
{
    const struct StadiumCompanion *c = &sStadiumCompanions[sT.companion];
    const u8 *line;
    u32 i;

    StringCopy(gStringVar1, GetTrainerNameFromId(TRAINER_PARTNER(c->partnerId)));
    for (i = 0; i < ARRAY_COUNT(sStadiumAnnouncerCompanion); i++)
        if (sStadiumAnnouncerCompanion[i].partnerId == c->partnerId)
            return sStadiumAnnouncerCompanion[i].text;
    if (c->trainerId != TRAINER_NONE)
    {
        line = AnnouncerLineFor(c->trainerId);
        if (line != sStadiumAnnouncerFallback)
            return line;
    }
    return sStadiumAnnouncerPartner[Random() % ARRAY_COUNT(sStadiumAnnouncerPartner)];
}

// Voegt een tekstvak toe aan gStringVar4 ({PLAYER}/{STR_VAR_1} ingevuld), met \p ervoor als er al tekst staat
static u8 *AddAnnouncement(u8 *dst, const u8 *text)
{
    if (dst != gStringVar4)
    {
        *dst++ = CHAR_PROMPT_CLEAR;
        *dst = EOS;
    }
    return StringExpandPlaceholders(dst, text);
}

// Omroeper in de arena: gStringVar4 = alle tekstvakken voor deze wedstrijd, om beurten.
// Eerste gevecht: welkom, ronde, speler, (compagnon), tegenstander(s). Daarna: ronde, tegenstander(s).
void Stadium_GetAnnouncerLine(void)
{
    u8 opp = CurrentOpponent();
    u8 *p = gStringVar4;
    u32 roundName = min(sT.round + (5 - sT.rounds), ARRAY_COUNT(sStadiumAnnouncerRounds) - 1);

    gStringVar4[0] = EOS;
    if (sT.round == 0)
        p = AddAnnouncement(p, sStadiumAnnouncerWelcome[sT.mode == STADIUM_DOUBLES]);
    p = AddAnnouncement(p, sStadiumAnnouncerRounds[roundName]);
    if (sT.round == 0)
    {
        p = AddAnnouncement(p, AnnouncePlayer());
        if (sT.mode == STADIUM_DOUBLES)
            p = AddAnnouncement(p, AnnounceCompanion());
    }
    p = AddAnnouncement(p, AnnouncerLineFor(Stadium_EntrantTrainer(opp, 0)));
    if (sT.mode == STADIUM_DOUBLES && Stadium_EntrantTrainer(opp, 1) != TRAINER_NONE)
        p = AddAnnouncement(p, AnnouncerLineFor(Stadium_EntrantTrainer(opp, 1)));
}

// gStringVar1 = verdiende BP (opnieuw, na de meldingsschermen)
void Stadium_GetBpText(void)
{
    ConvertIntToDecimalStringN(gStringVar1, sT.bp, STR_CONV_MODE_LEFT_ALIGN, 3);
}
