#include "global.h"
#include "test/battle.h"

// Project Grounded: Eelevate (Eelektross), Aura Guard (Lucario), Spicy Spray (Scovillain).

SINGLE_BATTLE_TEST("Eelevate makes the user immune to Ground-type moves")
{
    GIVEN {
        ASSUME(GetMoveType(MOVE_EARTHQUAKE) == TYPE_GROUND);
        PLAYER(SPECIES_EELEKTROSS) { Ability(ABILITY_EELEVATE); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_EARTHQUAKE); }
    } SCENE {
        NOT HP_BAR(player);
    } THEN {
        EXPECT_EQ(player->hp, player->maxHP);
    }
}

SINGLE_BATTLE_TEST("Eelevate makes the user immune to Spikes")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        PLAYER(SPECIES_EELEKTROSS) { Ability(ABILITY_EELEVATE); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_SPIKES); }
        TURN { SWITCH(player, 1); }
    } SCENE {
        NOT HP_BAR(player);
    } THEN {
        EXPECT_EQ(player->hp, player->maxHP);
    }
}

SINGLE_BATTLE_TEST("Eelevate boosts the user's highest stat when it knocks out a target")
{
    u8 stats[] = {1, 1, 1, 1, 1};
    PARAMETRIZE { stats[0] = 255; }
    PARAMETRIZE { stats[2] = 255; }
    PARAMETRIZE { stats[4] = 255; }
    GIVEN {
        PLAYER(SPECIES_EELEKTROSS) { Ability(ABILITY_EELEVATE); Attack(stats[0]); Defense(stats[1]); SpAttack(stats[2]); SpDefense(stats[3]); Speed(stats[4]); }
        OPPONENT(SPECIES_WOBBUFFET) { HP(1); Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(1); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); SEND_OUT(opponent, 1); }
    } SCENE {
        ABILITY_POPUP(player, ABILITY_EELEVATE);
        ANIMATION(ANIM_TYPE_GENERAL, B_ANIM_STATS_CHANGE, player);
    } THEN {
        u32 expectedStat = STAT_ATK;
        if (i == 1)
            expectedStat = STAT_SPATK;
        else if (i == 2)
            expectedStat = STAT_SPEED;
        EXPECT_EQ(player->statStages[expectedStat], DEFAULT_STAT_STAGE + 1);
    }
}

SINGLE_BATTLE_TEST("Aura Guard halves damage from contact moves", s16 damage)
{
    enum Ability ability;
    PARAMETRIZE { ability = ABILITY_STEADFAST; }
    PARAMETRIZE { ability = ABILITY_AURA_GUARD; }
    GIVEN {
        ASSUME(MoveMakesContact(MOVE_SCRATCH));
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_LUCARIO) { Ability(ability); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, UQ_4_12(0.5), results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Aura Guard does not reduce damage from non-contact moves", s16 damage)
{
    enum Ability ability;
    PARAMETRIZE { ability = ABILITY_STEADFAST; }
    PARAMETRIZE { ability = ABILITY_AURA_GUARD; }
    GIVEN {
        ASSUME(!MoveMakesContact(MOVE_SWIFT));
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_LUCARIO) { Ability(ability); }
    } WHEN {
        TURN { MOVE(player, MOVE_SWIFT); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray burns the attacker after any damaging hit")
{
    u32 move;
    PARAMETRIZE { move = MOVE_SCRATCH; }
    PARAMETRIZE { move = MOVE_SWIFT; }
    GIVEN {
        ASSUME(MoveMakesContact(MOVE_SCRATCH));
        ASSUME(!MoveMakesContact(MOVE_SWIFT));
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); }
    } WHEN {
        TURN { MOVE(player, move); }
    } SCENE {
        ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
        ANIMATION(ANIM_TYPE_STATUS, B_ANIM_STATUS_BRN, player);
        STATUS_ICON(player, burn: TRUE);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray does not burn Fire-type attackers")
{
    GIVEN {
        PLAYER(SPECIES_CHARMANDER);
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        NONE_OF {
            ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
            STATUS_ICON(player, burn: TRUE);
        }
    } THEN {
        EXPECT_EQ(player->status1, 0);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray does not trigger on status moves")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); }
    } WHEN {
        TURN { MOVE(player, MOVE_GROWL); }
    } SCENE {
        NOT ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
    } THEN {
        EXPECT_EQ(player->status1, 0);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray burns the attacker even if the user faints")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); HP(1); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); SEND_OUT(opponent, 1); }
    } SCENE {
        ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
        STATUS_ICON(player, burn: TRUE);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray does not trigger when the user's Substitute takes the hit")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_SUBSTITUTE); MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        NOT ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
    } THEN {
        EXPECT_EQ(player->status1, 0);
    }
}

SINGLE_BATTLE_TEST("Aura Guard does not reduce damage from a Long Reach attacker", s16 damage)
{
    enum Ability ability;
    PARAMETRIZE { ability = ABILITY_STEADFAST; }
    PARAMETRIZE { ability = ABILITY_AURA_GUARD; }
    GIVEN {
        PLAYER(SPECIES_DECIDUEYE) { Ability(ABILITY_LONG_REACH); }
        OPPONENT(SPECIES_LUCARIO) { Ability(ability); }
    } WHEN {
        TURN { MOVE(player, MOVE_SCRATCH); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Spicy Spray triggers on every hit of a multi-hit move")
{
    GIVEN {
        ASSUME(GetMoveStrikeCount(MOVE_DOUBLE_KICK) == 2);
        PLAYER(SPECIES_WOBBUFFET) { Item(ITEM_LUM_BERRY); }
        OPPONENT(SPECIES_SCOVILLAIN) { Ability(ABILITY_SPICY_SPRAY); }
    } WHEN {
        TURN { MOVE(player, MOVE_DOUBLE_KICK); }
    } SCENE {
        ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
        STATUS_ICON(player, burn: TRUE);
        ABILITY_POPUP(opponent, ABILITY_SPICY_SPRAY);
        STATUS_ICON(player, burn: TRUE);
    } THEN {
        EXPECT(player->status1 & STATUS1_BURN);
    }
}
