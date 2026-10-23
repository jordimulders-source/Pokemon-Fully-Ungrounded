#include "global.h"
#include "test/battle.h"
#include "battle_message.h"
#include "malloc.h"
#include "string_util.h"
#include "text.h"

// Project Grounded: signature moves Twin Tails (Ambipom), Life Buoy (Floatzel), Keystone Curse (Spiritomb),
// Frosty Tap Dance (Mr. Rime) en Rolling Thunder (Hitmonlee).
// Let op: Wobbuffet is in deze rom Psychic/Normal.

TEST("Project Grounded signature moves 910-914 have the agreed data")
{
    EXPECT_EQ(GetMoveType(MOVE_TWIN_TAILS), TYPE_NORMAL);
    EXPECT_EQ(GetMovePower(MOVE_TWIN_TAILS), 40);
    EXPECT_EQ(GetMoveStrikeCount(MOVE_TWIN_TAILS), 2);
    EXPECT(MoveMakesContact(MOVE_TWIN_TAILS));
    EXPECT_EQ(GetMoveEffect(MOVE_LIFE_BUOY), EFFECT_LIFE_BUOY);
    EXPECT_EQ(GetMovePower(MOVE_LIFE_BUOY), 80);
    EXPECT_EQ(GetMovePriority(MOVE_LIFE_BUOY), 0);
    EXPECT_EQ(GetMoveCategory(MOVE_KEYSTONE_CURSE), DAMAGE_CATEGORY_SPECIAL);
    EXPECT_EQ(GetMovePower(MOVE_KEYSTONE_CURSE), 60);
    EXPECT(IsDanceMove(MOVE_FROSTY_TAP_DANCE));
    EXPECT_EQ(GetMovePower(MOVE_FROSTY_TAP_DANCE), 70);
    EXPECT_EQ(GetMoveAccuracy(MOVE_ROLLING_THUNDER), 90);
    EXPECT_EQ(GetMovePower(MOVE_ROLLING_THUNDER), 100);
    EXPECT(MoveIgnoresProtect(MOVE_ROLLING_THUNDER));
}

// Twin Tails: steelt één stage van de hoogste boost, niet één per klap.
SINGLE_BATTLE_TEST("Twin Tails steals one stage of the target's highest boost")
{
    GIVEN {
        PLAYER(SPECIES_AMBIPOM) { Speed(1); Ability(ABILITY_PICKUP); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SWORDS_DANCE); MOVE(player, MOVE_TWIN_TAILS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SWORDS_DANCE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TWIN_TAILS, player);
        MESSAGE("Ambipom snatched the opposing Wobbuffet's Attack boost!");
    } THEN {
        EXPECT_EQ(opponent->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE + 1);
    }
}

SINGLE_BATTLE_TEST("Twin Tails does nothing extra without boosts")
{
    GIVEN {
        PLAYER(SPECIES_AMBIPOM) { Ability(ABILITY_PICKUP); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_TWIN_TAILS); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TWIN_TAILS, player);
        NONE_OF { MESSAGE("Ambipom snatched the opposing Wobbuffet's Attack boost!"); }
    } THEN {
        EXPECT_EQ(player->statStages[STAT_ATK], DEFAULT_STAT_STAGE);
    }
}

// Life Buoy: +1 prioriteit in regen.
SINGLE_BATTLE_TEST("Life Buoy goes first in rain")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_RAIN_DANCE); MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_LIFE_BUOY); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_RAIN_DANCE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LIFE_BUOY, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
    }
}

SINGLE_BATTLE_TEST("Life Buoy does not go first without rain")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SCRATCH); MOVE(player, MOVE_LIFE_BUOY); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_SCRATCH, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_LIFE_BUOY, player);
    }
}

// Life Buoy: na gebruik 1/4 max HP terug bij uitwisselen (ook via U-turn).
SINGLE_BATTLE_TEST("Life Buoy heals 1/4 max HP when the user switches out")
{
    u32 move, uturn;
    PARAMETRIZE { move = MOVE_SCRATCH; uturn = FALSE; }
    PARAMETRIZE { move = MOVE_LIFE_BUOY; uturn = FALSE; }
    PARAMETRIZE { move = MOVE_LIFE_BUOY; uturn = TRUE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { HP(100); MaxHP(400); }
        PLAYER(SPECIES_WYNAUT);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, move); MOVE(opponent, MOVE_CELEBRATE); }
        if (uturn)
            TURN { MOVE(player, MOVE_U_TURN); MOVE(opponent, MOVE_CELEBRATE); SEND_OUT(player, 1); }
        else
            TURN { SWITCH(player, 1); MOVE(opponent, MOVE_CELEBRATE); }
    } THEN {
        if (move == MOVE_LIFE_BUOY)
            EXPECT_EQ(GetMonData(&gPlayerParty[0], MON_DATA_HP), 200);
        else
            EXPECT_EQ(GetMonData(&gPlayerParty[0], MON_DATA_HP), 100);
    }
}

// Keystone Curse: +20 BP per flauwgevallen teamlid.
SINGLE_BATTLE_TEST("Keystone Curse gets stronger for each fainted party member", s16 damage)
{
    u32 fainted;
    PARAMETRIZE { fainted = 0; }
    PARAMETRIZE { fainted = 1; }
    PARAMETRIZE { fainted = 5; }
    GIVEN {
        PLAYER(SPECIES_SPIRITOMB);
        PLAYER(SPECIES_WYNAUT) { HP(fainted >= 1 ? 0 : 100); }
        PLAYER(SPECIES_WYNAUT) { HP(fainted >= 2 ? 0 : 100); }
        PLAYER(SPECIES_WYNAUT) { HP(fainted >= 3 ? 0 : 100); }
        PLAYER(SPECIES_WYNAUT) { HP(fainted >= 4 ? 0 : 100); }
        PLAYER(SPECIES_WYNAUT) { HP(fainted >= 5 ? 0 : 100); }
        OPPONENT(SPECIES_ALAKAZAM) { Ability(ABILITY_SYNCHRONIZE); HP(999); MaxHP(999); }
    } WHEN {
        TURN { MOVE(player, MOVE_KEYSTONE_CURSE, criticalHit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_KEYSTONE_CURSE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_GT(results[1].damage, results[0].damage);
        EXPECT_GT(results[2].damage, results[1].damage);
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(160.0 / 60.0), results[2].damage);
    }
}

// Frosty Tap Dance: altijd +1 Speed; in Snow ook +1 Sp. Atk.
SINGLE_BATTLE_TEST("Frosty Tap Dance raises Speed, and Sp. Atk in snow")
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_SNOWSCAPE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_FROSTY_TAP_DANCE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_FROSTY_TAP_DANCE, player);
    } THEN {
        EXPECT_EQ(player->statStages[STAT_SPEED], DEFAULT_STAT_STAGE + 1);
        EXPECT_EQ(player->statStages[STAT_SPATK], DEFAULT_STAT_STAGE + (move == MOVE_SNOWSCAPE ? 1 : 0));
    }
}

// Rolling Thunder: door Protect heen, en raakt dan altijd.
SINGLE_BATTLE_TEST("Rolling Thunder breaks through Protect and Detect")
{
    u32 move;
    PARAMETRIZE { move = MOVE_PROTECT; }
    PARAMETRIZE { move = MOVE_DETECT; }
    PARAMETRIZE { move = MOVE_SPIKY_SHIELD; }
    GIVEN {
        PLAYER(SPECIES_HITMONLEE);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_ROLLING_THUNDER); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ROLLING_THUNDER, player);
        HP_BAR(opponent);
        NOT HP_BAR(player);
    }
}

SINGLE_BATTLE_TEST("Rolling Thunder never misses a protecting target")
{
    GIVEN {
        PLAYER(SPECIES_HITMONLEE);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_PROTECT); MOVE(player, MOVE_ROLLING_THUNDER, hit: FALSE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PROTECT, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_ROLLING_THUNDER, player);
        HP_BAR(opponent);
    }
}

SINGLE_BATTLE_TEST("Rolling Thunder can miss a target that is not protecting")
{
    GIVEN {
        PLAYER(SPECIES_HITMONLEE);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_ROLLING_THUNDER, hit: FALSE); }
    } SCENE {
        NOT ANIMATION(ANIM_TYPE_MOVE, MOVE_ROLLING_THUNDER, player);
        MESSAGE("Hitmonlee's attack missed!");
    }
}

// Namen (gevechtsscherm, 64 px) en beschrijvingen passen. Frosty Tap Dance is 62 px: 3 px te breed
// voor het contestscherm (uitzondering in test/text.c).
TEST("Project Grounded moves 910-914 fit on screen")
{
    u32 move;
    for (move = MOVE_TWIN_TAILS; move <= MOVE_ROLLING_THUNDER; move++)
    {
        EXPECT_LE(GetStringWidth(FONT_NARROWER, GetMoveName(move), 0), 64);
        EXPECT_LE(GetStringWidth(FONT_NORMAL, GetMoveDescription(move), 0), 152);
    }
}

#define TT_STRING_BUFFER_SIZE 1000

TEST("Twin Tails message fits on the battle message window")
{
    u32 j, strWidth;
    u8 nickname[POKEMON_NAME_LENGTH + 1] = _("MMMMMMMMMMMM");
    u8 *battleString = Alloc(TT_STRING_BUFFER_SIZE);
    CreateMon(&gPlayerParty[0], SPECIES_WOBBUFFET, 100, 0, OTID_STRUCT_PRESET(0));
    CreateMon(&gEnemyParty[0], SPECIES_WOBBUFFET, 100, 0, OTID_STRUCT_PRESET(0));
    SetMonData(&gPlayerParty[0], MON_DATA_NICKNAME, nickname);
    SetMonData(&gEnemyParty[0], MON_DATA_NICKNAME, nickname);
    gBattlerPositions[0] = B_POSITION_PLAYER_LEFT;
    gBattlerPositions[1] = B_POSITION_OPPONENT_LEFT;
    gBattleTypeFlags |= BATTLE_TYPE_TRAINER;
    gBattlerPartyIndexes[0] = gBattlerPartyIndexes[1] = 0;
    gBattlerAttacker = gBattlerTarget = gEffectBattler = 1;
    gBattleMsgDataPtr = AllocZeroed(sizeof(struct BattleMsgData));
    StringCopy(gBattleTextBuff1, gStatNamesTable[STAT_EVASION]);
    BattleStringExpandPlaceholders(gBattleStringsTable[STRINGID_TWINTAILSSNATCH], battleString, TT_STRING_BUFFER_SIZE);
    for (j = 1;; j++)
    {
        strWidth = GetStringLineWidth(FONT_NORMAL, battleString, 0, j, TT_STRING_BUFFER_SIZE);
        if (strWidth == 0)
            break;
        EXPECT_LE(strWidth - 1, BATTLE_MSG_MAX_WIDTH);
    }
    Free(gBattleMsgDataPtr);
    Free(battleString);
}
