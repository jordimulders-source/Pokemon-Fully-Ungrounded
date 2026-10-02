#include "global.h"
#include "test/battle.h"

// Project Grounded: Pollen Haze - Bug-weer. Bug: Speed x2, negeert stat boosts, Bug- en Grass-moves x1.5,
// Grass herstelt 1/16, Fire x0.5, poedermoves +20 acc, windmoves blazen het weg.
ASSUMPTIONS
{
    ASSUME(GetMoveEffect(MOVE_POLLEN_HAZE) == EFFECT_POLLEN_HAZE);
}

SINGLE_BATTLE_TEST("Pollen Haze heals Grass types")
{
    GIVEN {
        PLAYER(SPECIES_ODDISH) { HP(50); MaxHP(160); Moves(MOVE_POLLEN_HAZE); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_POLLEN_HAZE); }
    } SCENE {
        MESSAGE("Pollen filled the air!");
        MESSAGE("Oddish soaked up\nthe pollen!");
    } THEN {
        EXPECT_EQ(player->hp, 50 + 160 / 16);
    }
}

SINGLE_BATTLE_TEST("Pollen Haze doubles the Speed of Bug types")
{
    GIVEN {
        PLAYER(SPECIES_BEEDRILL) { Speed(60); Moves(MOVE_POLLEN_HAZE, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_POLLEN_HAZE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_POLLEN_HAZE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, player);
        ANIMATION(ANIM_TYPE_MOVE, MOVE_CELEBRATE, opponent);
    }
}

SINGLE_BATTLE_TEST("Pollen Haze boosts Bug and Grass moves and weakens Fire moves", s16 damage)
{
    u32 move, weatherMove;
    PARAMETRIZE { move = MOVE_BUG_BITE; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_BUG_BITE; weatherMove = MOVE_POLLEN_HAZE; }
    PARAMETRIZE { move = MOVE_VINE_WHIP; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_VINE_WHIP; weatherMove = MOVE_POLLEN_HAZE; }
    PARAMETRIZE { move = MOVE_EMBER; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_EMBER; weatherMove = MOVE_POLLEN_HAZE; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_BUG_BITE, MOVE_VINE_WHIP, MOVE_EMBER, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_POLLEN_HAZE, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(opponent, weatherMove); MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, move); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(1.5), results[1].damage);
        EXPECT_MUL_EQ(results[2].damage, Q_4_12(1.5), results[3].damage);
        EXPECT_MUL_EQ(results[4].damage, Q_4_12(0.5), results[5].damage);
    }
}

SINGLE_BATTLE_TEST("Bug types ignore the target's Defense boosts in Pollen Haze", s16 damage)
{
    u32 move;
    PARAMETRIZE { move = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_IRON_DEFENSE; }
    GIVEN {
        PLAYER(SPECIES_BEEDRILL) { Speed(5); Moves(MOVE_POLLEN_HAZE, MOVE_TACKLE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_CELEBRATE, MOVE_IRON_DEFENSE); }
    } WHEN {
        TURN { MOVE(opponent, move); MOVE(player, MOVE_POLLEN_HAZE); }
        TURN { MOVE(opponent, MOVE_CELEBRATE); MOVE(player, MOVE_TACKLE); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TACKLE, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_EQ(results[0].damage, results[1].damage);
    }
}

SINGLE_BATTLE_TEST("Wind moves blow Pollen Haze away")
{
    GIVEN {
        ASSUME(IsWindMove(MOVE_GUST));
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_POLLEN_HAZE, MOVE_GUST); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_POLLEN_HAZE); }
        TURN { MOVE(player, MOVE_GUST); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_GUST, player);
        MESSAGE("The wind blew the pollen away!\nAhchoo!");
    }
}

SINGLE_BATTLE_TEST("Pollen Season summons Pollen Haze on switch-in")
{
    GIVEN {
        PLAYER(SPECIES_RIBOMBEE) { Ability(ABILITY_POLLEN_SEASON); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { }
    } SCENE {
        ABILITY_POPUP(player, ABILITY_POLLEN_SEASON);
        MESSAGE("Ribombee's Pollen Season\nfilled the air with pollen!");
    }
}

SINGLE_BATTLE_TEST("Silver Powder extends Pollen Haze to 8 turns")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Item(ITEM_SILVER_POWDER); Moves(MOVE_POLLEN_HAZE, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_POLLEN_HAZE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, MOVE_CELEBRATE); }
    } SCENE {
        MESSAGE("Pollen filled the air!");
        NOT MESSAGE("The pollen settled.");
    }
}
