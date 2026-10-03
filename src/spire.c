// Project Grounded: The Spire, roguelike-faciliteit in de Battle Frontier (zie SPIRE_DESIGN.md).
// Prototype: Spire-modus in gevechten (HP-vermenigvuldigers, DEFEND met blok, intenties)
// en een testgevecht vanuit het debugmenu.
#include "global.h"
#include "battle.h"
#include "battle_ai_main.h"
#include "battle_scripts.h"
#include "battle_setup.h"
#include "battle_transition.h"
#include "battle_util.h"
#include "event_data.h"
#include "main.h"
#include "move.h"
#include "overworld.h"
#include "pokemon.h"
#include "random.h"
#include "script.h"
#include "spire.h"
#include "string_util.h"
#include "text.h"
#include "constants/abilities.h"
#include "constants/characters.h"
#include "constants/battle_move_effects.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "constants/songs.h"
#include "constants/species.h"
#include "constants/trainers.h"

#define SPIRE_FULL_BLOCK 0x8000

EWRAM_DATA bool8 gSpireBattle = FALSE;
EWRAM_DATA u8 gSpireAct = 0;
EWRAM_DATA u16 gSpireBlock[MAX_BATTLERS_COUNT] = {0};
EWRAM_DATA u16 gSpireBlockAbsorbed[MAX_BATTLERS_COUNT] = {0};
EWRAM_DATA u8 gSpireDefendTarget[MAX_BATTLERS_COUNT] = {0};
EWRAM_DATA u16 gSpireEnemyHp[PARTY_SIZE] = {0}; // HP-vermenigvuldiger per vijand (procent)

EWRAM_DATA u8 gSpirePattern[PARTY_SIZE][8] = {0};   // vaste patronen van de vijanden (moveslots 1-4)
EWRAM_DATA u8 gSpirePatternStep[PARTY_SIZE] = {0};

// act-factor van het blok (procenten), per act 1-3
static const u8 sActBlockFactor[] = {100, 100, 125, 150};

void Spire_ScaleMonHp(struct Pokemon *mon, u32 percent)
{
    u32 maxHp;

    if (GetMonData(mon, MON_DATA_SPECIES) == SPECIES_NONE)
        return;
    maxHp = GetMonData(mon, MON_DATA_MAX_HP) * (percent ? percent : 100) / 100;
    if (maxHp > 9999)
        maxHp = 9999;
    SetMonData(mon, MON_DATA_MAX_HP, &maxHp);
    SetMonData(mon, MON_DATA_HP, &maxHp);
}

// Na het aanmaken van de vijandelijke party: de eerste is de baas, de rest normaal.
void Spire_OnEnemyPartyCreated(void)
{
    u32 i;

    if (!gSpireBattle)
        return;
    Spire_ClearBlocks();
    for (i = 0; i < PARTY_SIZE; i++)
        Spire_ScaleMonHp(&gEnemyParty[i], gSpireEnemyHp[i]);
}

// Vast patroon (zoals de vijanden in Slay the Spire): de AI kiest niet zelf, maar volgt het patroon.
// De intentie toont dus precies wat er komt. Kan de move niet (geen PP, Taunt, Disable, ...), dan kiest de AI.
void Spire_ApplyPattern(u32 battler)
{
    u32 party, len, slot, target, i;
    s32 best;
    const u8 *pattern;

    if (!gSpireBattle || IsOnPlayerSide(battler))
        return;
    party = gBattlerPartyIndexes[battler];
    if (party >= PARTY_SIZE)
        return;
    pattern = gSpirePattern[party];
    for (len = 0; len < 8 && pattern[len] != 0; len++)
        ;
    if (len == 0)
        return;
    slot = pattern[gSpirePatternStep[party] % len] - 1;
    if (slot >= MAX_MON_MOVES || gBattleMons[battler].moves[slot] == MOVE_NONE
     || (gAiLogicData->moveLimitations[battler] & (1u << slot)))
        return;
    gAiBattleData->chosenMoveIndex[battler] = slot;
    // doel: de speler-Pokémon waarop de AI deze move het hoogst scoorde
    best = -10000;
    target = gAiBattleData->chosenTarget[battler];
    for (i = 0; i < gBattlersCount; i++)
    {
        if (!IsOnPlayerSide(i) || !IsBattlerAlive(i))
            continue;
        if (gAiBattleData->finalScore[battler][i][slot] > best || !IsOnPlayerSide(target) || !IsBattlerAlive(target))
        {
            best = gAiBattleData->finalScore[battler][i][slot];
            target = i;
        }
    }
    gAiBattleData->chosenTarget[battler] = target;
}

void Spire_EndTurn(void)
{
    u32 i;

    if (!gSpireBattle)
        return;
    Spire_ClearBlocks();
    for (i = 0; i < PARTY_SIZE; i++)
        gSpirePatternStep[i]++;
}

void Spire_ClearBlocks(void)
{
    u32 i;

    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        gSpireBlock[i] = 0;
        gSpireBlockAbsorbed[i] = 0;
    }
}

// Blok = 15% van max HP x (gemiddelde Def/SpD gedeeld door een base-80-stat op dit level) x act-factor.
u32 Spire_BlockAmount(u32 battler)
{
    u32 level = gBattleMons[battler].level;
    u32 def = (gBattleMons[battler].defense + gBattleMons[battler].spDefense) / 2;
    u32 ref = (2 * 80 + 31 + 21) * level / 100 + 5;
    u32 act = gSpireAct < ARRAY_COUNT(sActBlockFactor) ? gSpireAct : ARRAY_COUNT(sActBlockFactor) - 1;
    u32 amount = gBattleMons[battler].maxHP * SPIRE_BLOCK_PERCENT * def / (100 * ref);

    amount = amount * sActBlockFactor[act] / 100;
    if (Spire_HasRelic(SPIRE_RELIC_KINGS_ROCK))
        amount = amount * 13 / 10;
    return amount ? amount : 1;
}

u32 Spire_BlockPercent(u32 amount, u32 target)
{
    if (gBattleMons[target].maxHP == 0)
        return 0;
    return (amount * 100 + gBattleMons[target].maxHP / 2) / gBattleMons[target].maxHP;
}

// Uit Cmd_adjustdamage: het blok vangt directe schade van moves eerst op.
void Spire_AbsorbDamage(u32 battlerDef)
{
    s16 *dmg = &gBattleStruct->moveDamage[battlerDef];
    u32 absorbed;

    if (!gSpireBattle || gSpireBlock[battlerDef] == 0 || *dmg <= 0)
        return;
    absorbed = min((u32)*dmg, gSpireBlock[battlerDef]);
    if (absorbed == (u32)*dmg)
        absorbed |= SPIRE_FULL_BLOCK;
    *dmg -= absorbed & ~SPIRE_FULL_BLOCK;
    gSpireBlock[battlerDef] -= absorbed & ~SPIRE_FULL_BLOCK;
    gSpireBlockAbsorbed[battlerDef] = absorbed;
}

// Uit Cmd_resultmessage: meld hoeveel het blok heeft opgevangen.
bool32 Spire_TryPrintBlockAbsorbed(void)
{
    if (!gSpireBattle || gSpireBlockAbsorbed[gBattlerTarget] == 0)
        return FALSE;
    if (gSpireBlockAbsorbed[gBattlerTarget] & SPIRE_FULL_BLOCK)
        BattleScriptCall(BattleScript_SpireBlockAbsorbed);
    else
        BattleScriptCall(BattleScript_SpireBlockSoftened);
    gSpireBlockAbsorbed[gBattlerTarget] = 0;
    return TRUE;
}

void HandleAction_SpireDefend(void)
{
    u32 battler = gBattlerByTurnOrder[gCurrentTurnActionNumber];
    u32 partner = BATTLE_PARTNER(battler);
    u32 target = gSpireDefendTarget[battler];
    u32 amount = Spire_BlockAmount(battler);
    bool32 partnerAlive = IsDoubleBattle() && IsBattlerAlive(partner);

    gBattlerAttacker = battler;
    gBattle_BG0_X = 0;
    gBattle_BG0_Y = 0;
    if (target == SPIRE_DEFEND_BOTH && partnerAlive)
    {
        amount = amount * SPIRE_BLOCK_SPLIT / 100;
        gSpireBlock[battler] += amount;
        gSpireBlock[partner] += amount;
        gBattlerTarget = partner;
        gBattlescriptCurrInstr = BattleScript_SpireDefendBoth;
    }
    else if (target == partner && partnerAlive)
    {
        gSpireBlock[partner] += amount;
        gBattlerTarget = partner;
        gBattlescriptCurrInstr = BattleScript_SpireDefendAlly;
    }
    else
    {
        gSpireBlock[battler] += amount;
        gBattlerTarget = battler;
        gBattlescriptCurrInstr = BattleScript_SpireDefendSelf;
    }
    gCurrentActionFuncId = B_ACTION_EXEC_SCRIPT;
}

// ---------------------------------------------------------------------------
// Intenties: de AI heeft zijn keuze voor deze beurt al vastgelegd vóór de speler kiest
// (ComputeBattlerDecisions bij STATE_TURN_START_RECORD); die tonen we.

static const u8 sText_Both[] = _("both");

// Schade als percentage van de max HP van het doel (in doubles staan er geen HP-getallen bij je eigen Pokémon).
static u32 DamagePercent(u32 battler, u32 target, u32 moveIndex)
{
    u32 dmg = gAiLogicData->simulatedDmg[battler][target][moveIndex].median;
    u32 pct;

    if (gBattleMons[target].maxHP == 0)
        return 0;
    pct = (dmg * 100 + gBattleMons[target].maxHP / 2) / gBattleMons[target].maxHP;
    if (pct == 0 && dmg != 0)
        pct = 1;
    return pct;
}

static u8 *AppendPercent(u8 *dst, u32 pct)
{
    dst = ConvertIntToDecimalStringN(dst, pct, STR_CONV_MODE_LEFT_ALIGN, 3);
    *dst++ = CHAR_PERCENT;
    *dst = EOS;
    return dst;
}

// Achter de schade: "KO" als zelfs de laagste rol het doel uitschakelt, "KO?" als alleen de hoogste rol dat doet.
static u8 *AppendKoMark(u8 *dst, u32 battler, u32 target, u32 moveIndex)
{
    const struct SimulatedDamage *dmg = &gAiLogicData->simulatedDmg[battler][target][moveIndex];

    if (dmg->maximum >= gBattleMons[target].hp)
    {
        *dst++ = CHAR_K;
        *dst++ = CHAR_O;
        if (dmg->minimum < gBattleMons[target].hp)
            *dst++ = CHAR_QUESTION_MARK;
    }
    *dst = EOS;
    return dst;
}

static u8 *AppendDamage(u8 *dst, u32 battler, u32 target, u32 moveIndex)
{
    *dst++ = CHAR_SPACE;
    dst = AppendPercent(dst, DamagePercent(battler, target, moveIndex));
    if (gAiLogicData->simulatedDmg[battler][target][moveIndex].maximum >= gBattleMons[target].hp)
        *dst++ = CHAR_SPACE;
    return AppendKoMark(dst, battler, target, moveIndex);
}

// Spread: per doel het percentage, direct gevolgd door KO/KO? (bijv. "23%KO/15%").
static u8 *AppendSpreadPart(u8 *dst, u32 battler, u32 target, u32 moveIndex)
{
    dst = AppendPercent(dst, DamagePercent(battler, target, moveIndex));
    return AppendKoMark(dst, battler, target, moveIndex);
}

#define INTENT_MAX_WIDTH 98 // vak van 112 px min marge en het driehoekje

static u8 *AppendTargetLabel(u8 *dst, u32 battler, u32 target, u32 moveIndex, bool32 isSpread, bool32 shortForm)
{
    u32 left = GetBattlerAtPosition(B_POSITION_PLAYER_LEFT);
    u32 right = GetBattlerAtPosition(B_POSITION_PLAYER_RIGHT);

    *dst++ = CHAR_RIGHT_ARROW;
    if (isSpread)
    {
        if (!shortForm)
            dst = StringCopy(dst, sText_Both);
        *dst++ = CHAR_SPACE;
        if (IsBattlerAlive(left))
            dst = AppendSpreadPart(dst, battler, left, moveIndex);
        if (IsDoubleBattle() && IsBattlerAlive(right))
        {
            if (IsBattlerAlive(left))
                *dst++ = CHAR_SLASH;
            dst = AppendSpreadPart(dst, battler, right, moveIndex);
        }
    }
    else
    {
        if (shortForm)
        {
            // te lang: alleen kant (L/R) i.p.v. de naam
            *dst++ = (GetBattlerPosition(target) == B_POSITION_PLAYER_LEFT) ? CHAR_L : CHAR_R;
        }
        else
        {
            u8 nick[POKEMON_NAME_LENGTH + 1];

            GetMonData(GetBattlerMon(target), MON_DATA_NICKNAME, nick);
            dst = StringCopy(dst, nick);
        }
        dst = AppendDamage(dst, battler, target, moveIndex);
    }
    *dst = EOS;
    return dst;
}

// Schrijft bijv. "Rock Slide→both 12%/15%", "Crunch→Gardevoir 20%" of "Dragon Dance".
// Past het niet in het vak, dan "Rock Slide→ 12%/15%" of "Crunch→L 20%".
u8 *Spire_GetIntentText(u8 *dst, u32 battler)
{
    u32 moveIndex = gAiBattleData->chosenMoveIndex[battler];
    u32 target = gAiBattleData->chosenTarget[battler];
    u32 move, moveTarget;
    bool32 isSpread;
    u8 *start = dst, *afterMove;

    *dst = EOS;
    if (!IsBattlerAlive(battler) || moveIndex >= MAX_MON_MOVES)
        return dst;
    move = gBattleMons[battler].moves[moveIndex];
    if (move == MOVE_NONE)
        return dst;

    afterMove = StringCopy(dst, GetMoveName(move));
    if (IsBattleMoveStatus(move))
        return afterMove;

    moveTarget = GetBattlerMoveTargetType(battler, move);
    isSpread = (moveTarget == MOVE_TARGET_BOTH || moveTarget == MOVE_TARGET_FOES_AND_ALLY);
    if (target >= gBattlersCount || !IsOnPlayerSide(target) || !IsBattlerAlive(target))
        target = IsBattlerAlive(GetBattlerAtPosition(B_POSITION_PLAYER_LEFT)) ? GetBattlerAtPosition(B_POSITION_PLAYER_LEFT)
                                                                               : GetBattlerAtPosition(B_POSITION_PLAYER_RIGHT);
    dst = AppendTargetLabel(afterMove, battler, target, moveIndex, isSpread, FALSE);
    if (GetStringWidth(FONT_SMALL_NARROW, start, 0) > INTENT_MAX_WIDTH)
        dst = AppendTargetLabel(afterMove, battler, target, moveIndex, isSpread, TRUE);
    return dst;
}

// ---------------------------------------------------------------------------
// Hulpfuncties voor src/spire_run.c

void Spire_CreateMon(struct Pokemon *mon, u16 species, u8 level, u8 iv, u32 ev, const u16 *moves)
{
    u32 i;

    CreateMon(mon, species, level, iv, FALSE, 0, OT_ID_PLAYER_ID, 0);
    for (i = 0; i < NUM_STATS; i++)
        SetMonData(mon, MON_DATA_HP_EV + i, &ev);
    if (moves != NULL)
        for (i = 0; i < MAX_MON_MOVES; i++)
            SetMonMoveSlot(mon, moves[i], i);
    CalculateMonStats(mon);
}


