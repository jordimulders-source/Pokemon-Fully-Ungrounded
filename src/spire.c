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
EWRAM_DATA u8 gSpireHiddenIntent = 0;
EWRAM_DATA static u8 sRelicEndureUsed = 0;    // Resist Feather: bit per partyplek van de speler
EWRAM_DATA static u16 sOpeningTaken[MAX_BATTLERS_COUNT] = {0}; // openingsbescherming: schade deze beurt

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

// Vormwissel in een gevecht (Schooling, Zen Mode, Disguise, ...): CalculateMonStats rekent de max HP opnieuw uit
// zonder de Spire-vermenigvuldiger (Totem Wishiwashi had na het scholen 220 i.p.v. 440 HP). Zet hem terug en houd
// het verschil in HP zoals CalculateMonStats dat doet.
void Spire_RescaleAfterRecalc(u32 battler, struct Pokemon *mon, u32 hpBefore, u32 oldMaxHp)
{
    u32 party = gBattlerPartyIndexes[battler];
    u32 percent, maxHp;
    s32 hp;

    if (!gSpireBattle || party >= PARTY_SIZE)
        return;
    percent = IsOnPlayerSide(battler) ? Spire_PlayerHpPercent(party) : gSpireEnemyHp[party];
    if (percent == 0 || percent == 100)
        return;
    maxHp = min(9999, GetMonData(mon, MON_DATA_MAX_HP) * percent / 100);
    hp = (hpBefore == 0) ? 0 : (s32)hpBefore + (s32)maxHp - (s32)oldMaxHp;
    hp = max(hpBefore ? 1 : 0, min((s32)maxHp, hp));
    SetMonData(mon, MON_DATA_MAX_HP, &maxHp);
    SetMonData(mon, MON_DATA_HP, &hp);
}

// Na het aanmaken van de vijandelijke party: de eerste is de baas, de rest normaal.
void Spire_OnEnemyPartyCreated(void)
{
    u32 i;

    if (!gSpireBattle)
        return;
    Spire_ClearBlocks();
    sRelicEndureUsed = 0;
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

// Upgrades ("+", Porygon2 op de rustplek): opgeslagen als PP Up 3 op die slot.
bool32 Spire_IsMoveUpgraded(u32 battler, u32 move)
{
    u32 i;

    if (!gSpireBattle || !IsOnPlayerSide(battler))
        return FALSE;
    for (i = 0; i < MAX_MON_MOVES; i++)
        if (gBattleMons[battler].moves[i] == move)
            return ((gBattleMons[battler].ppBonuses >> (i * 2)) & 3) == 3;
    return FALSE;
}

uq4_12_t Spire_UpgradeDamageModifier(u32 battlerAtk, u32 move)
{
    return Spire_IsMoveUpgraded(battlerAtk, move) ? UQ_4_12(1.3) : UQ_4_12(1.0);
}

static bool32 IsAlone(u32 battler)
{
    return !IsBattlerAlive(BATTLE_PARTNER(battler));
}

// Relics in de schadeberekening (GetOtherModifiers in battle_util.c; ook in de schatting van de intenties).
// Speler valt aan: meer schade; speler wordt geraakt: minder (of meer, Meteorite).
uq4_12_t Spire_RelicDamageModifier(u32 battlerAtk, u32 battlerDef, bool32 isCrit, uq4_12_t typeEffectiveness)
{
    uq4_12_t mod = UQ_4_12(1.0);

    if (!gSpireBattle)
        return mod;
    if (IsOnPlayerSide(battlerAtk) && !IsOnPlayerSide(battlerDef))
    {
        if (Spire_HasRelic(SPIRE_RELIC_MUSCLE_BAND))
            mod = uq4_12_multiply(mod, UQ_4_12(1.1));
        if (Spire_HasRelic(SPIRE_RELIC_ADRENALINE_ORB) && gBattleResults.battleTurnCounter == 0)
            mod = uq4_12_multiply(mod, UQ_4_12(1.3));
        if (Spire_HasRelic(SPIRE_RELIC_BERSERK_GENE) && gBattleMons[battlerAtk].hp * 2 < gBattleMons[battlerAtk].maxHP)
            mod = uq4_12_multiply(mod, UQ_4_12(1.25));
        if (Spire_HasRelic(SPIRE_RELIC_REAPER_CLOTH) && (gBattleMons[battlerDef].status1 & STATUS1_ANY))
            mod = uq4_12_multiply(mod, UQ_4_12(1.25));
        if (Spire_HasRelic(SPIRE_RELIC_RAZOR_CLAW) && isCrit)
            mod = uq4_12_multiply(mod, UQ_4_12(1.3333)); // 1,5x -> 2x
        if (Spire_HasRelic(SPIRE_RELIC_SCANNER) && typeEffectiveness > UQ_4_12(1.0))
            mod = uq4_12_multiply(mod, UQ_4_12(1.25));
        if (Spire_HasRelic(SPIRE_RELIC_FOCUS_BAND) && IsAlone(battlerAtk))
            mod = uq4_12_multiply(mod, UQ_4_12(1.3));
        if (Spire_HasRelic(SPIRE_RELIC_AWAKENING))
            mod = uq4_12_multiply(mod, UQ_4_12(1.2));
        if (Spire_HasRelic(SPIRE_RELIC_METEORITE))
            mod = uq4_12_multiply(mod, UQ_4_12(1.35));
    }
    else if (IsOnPlayerSide(battlerDef) && !IsOnPlayerSide(battlerAtk))
    {
        if (Spire_HasRelic(SPIRE_RELIC_LAVA_COOKIE) && typeEffectiveness > UQ_4_12(1.0))
            mod = uq4_12_multiply(mod, UQ_4_12(0.8));
        if (Spire_HasRelic(SPIRE_RELIC_FOCUS_BAND) && IsAlone(battlerDef))
            mod = uq4_12_multiply(mod, UQ_4_12(0.8));
        if (Spire_HasRelic(SPIRE_RELIC_DUBIOUS_DISC))
            mod = uq4_12_multiply(mod, UQ_4_12(0.8));
        if (Spire_HasRelic(SPIRE_RELIC_METEORITE))
            mod = uq4_12_multiply(mod, UQ_4_12(1.15));
    }
    return mod;
}

// Resist Feather (relic): één keer per gevecht overleeft elke Pokémon van de speler een KO-klap met 1 HP.
bool32 Spire_TryRelicEndure(u32 battlerDef)
{
    u32 bit;

    if (!gSpireBattle || !IsOnPlayerSide(battlerDef) || !Spire_HasRelic(SPIRE_RELIC_RESIST_FEATHER))
        return FALSE;
    bit = 1u << gBattlerPartyIndexes[battlerDef];
    if (sRelicEndureUsed & bit)
        return FALSE;
    sRelicEndureUsed |= bit;
    return TRUE;
}

// Eén keer per beurt (battle_main.c, na de effecten aan het eind van de beurt).
void Spire_EndTurn(void)
{
    u32 i;

    if (!gSpireBattle)
        return;
    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        // Shed Shell (relic): de helft van het blok van je eigen Pokémon blijft staan
        gSpireBlock[i] = (Spire_HasRelic(SPIRE_RELIC_SHED_SHELL) && IsOnPlayerSide(i)) ? gSpireBlock[i] / 2 : 0;
        gSpireBlockAbsorbed[i] = 0;
        sOpeningTaken[i] = 0;
    }
    for (i = 0; i < PARTY_SIZE; i++)
        gSpirePatternStep[i]++;
}

// Iron Plate (relic): de eerste beurt begint met blok op beide, alsof ze allebei DEFEND kozen.
void Spire_OnFirstTurn(void)
{
    u32 i;

    if (!gSpireBattle || !Spire_HasRelic(SPIRE_RELIC_IRON_PLATE))
        return;
    for (i = 0; i < gBattlersCount; i++)
        if (IsOnPlayerSide(i) && IsBattlerAlive(i))
            gSpireBlock[i] += Spire_BlockAmount(i) * Spire_BlockSplit() / 100;
}

// DEFEND op beide: elk dit percentage van het blok (Rusted Shield: 85 i.p.v. 60).
u32 Spire_BlockSplit(void)
{
    return Spire_HasRelic(SPIRE_RELIC_RUSTED_SHIELD) ? 85 : SPIRE_BLOCK_SPLIT;
}

void Spire_ClearBlocks(void)
{
    u32 i;

    for (i = 0; i < MAX_BATTLERS_COUNT; i++)
    {
        gSpireBlock[i] = 0;
        gSpireBlockAbsorbed[i] = 0;
        sOpeningTaken[i] = 0;
    }
}

// Openingsbescherming: hoeveel schade een vijand deze beurt nog mag doen bij een Pokémon van de speler
// (0xFFFF = geen grens). Zie SPIRE_OPENING_CAP in spire.h.
u32 Spire_OpeningCapLeft(u32 battlerAtk, u32 battlerDef)
{
    u32 cap;

    if (!gSpireBattle || !IsOnPlayerSide(battlerDef) || IsOnPlayerSide(battlerAtk)
     || gBattleResults.battleTurnCounter >= SPIRE_OPENING_TURNS)
        return 0xFFFF;
    cap = gBattleMons[battlerDef].maxHP * SPIRE_OPENING_CAP / 100;
    return cap > sOpeningTaken[battlerDef] ? cap - sOpeningTaken[battlerDef] : 0;
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
    if (Spire_HasRelic(SPIRE_RELIC_GUARD_SPEC))
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

    if (!gSpireBattle || *dmg <= 0)
        return;
    // Iron Ball (relic): elke klap op je team 2% van de max HP minder (minstens 1 schade)
    if (IsOnPlayerSide(battlerDef) && Spire_HasRelic(SPIRE_RELIC_IRON_BALL))
        *dmg = max(1, *dmg - (s32)(gBattleMons[battlerDef].maxHP * 2 / 100));
    if (gSpireBlock[battlerDef] != 0)
    {
        absorbed = min((u32)*dmg, gSpireBlock[battlerDef]);
        if (absorbed == (u32)*dmg)
            absorbed |= SPIRE_FULL_BLOCK;
        *dmg -= absorbed & ~SPIRE_FULL_BLOCK;
        gSpireBlock[battlerDef] -= absorbed & ~SPIRE_FULL_BLOCK;
        gSpireBlockAbsorbed[battlerDef] = absorbed;
    }
    // openingsbescherming (beurt 1-3): na het blok, alle klappen van deze beurt samen
    if (*dmg > 0)
    {
        u32 left = Spire_OpeningCapLeft(gBattlerAttacker, battlerDef);

        if (left != 0xFFFF)
        {
            *dmg = max(1, min((s32)*dmg, (s32)left));
            sOpeningTaken[battlerDef] += *dmg;
        }
    }
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
        amount = amount * Spire_BlockSplit() / 100;
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
static u32 CappedDamage(u32 battler, u32 target, u32 dmg)
{
    return min(dmg, Spire_OpeningCapLeft(battler, target));
}

static u32 DamagePercent(u32 battler, u32 target, u32 moveIndex)
{
    u32 dmg = CappedDamage(battler, target, gAiLogicData->simulatedDmg[battler][target][moveIndex].median);
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

    if (CappedDamage(battler, target, dmg->maximum) >= gBattleMons[target].hp)
    {
        *dst++ = CHAR_K;
        *dst++ = CHAR_O;
        if (CappedDamage(battler, target, dmg->minimum) < gBattleMons[target].hp)
            *dst++ = CHAR_QUESTION_MARK;
    }
    *dst = EOS;
    return dst;
}

static u8 *AppendDamage(u8 *dst, u32 battler, u32 target, u32 moveIndex)
{
    *dst++ = CHAR_SPACE;
    dst = AppendPercent(dst, DamagePercent(battler, target, moveIndex));
    if (CappedDamage(battler, target, gAiLogicData->simulatedDmg[battler][target][moveIndex].maximum) >= gBattleMons[target].hp)
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
    if (gSpireHiddenIntent & (1u << gBattlerPartyIndexes[battler]))
        return StringCopy(dst, COMPOUND_STRING("??? (unreadable)"));

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


