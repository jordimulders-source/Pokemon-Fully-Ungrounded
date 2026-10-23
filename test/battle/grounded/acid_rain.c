#include "global.h"
#include "test/battle.h"

// Project Grounded: Acid Rain - zure regen. Poison herstelt 1/16, de rest (behalve Steel) verliest 1/16,
// Poison Def x1.5, Poison-moves x1.5, Fire en Water x0.5, gifkansen verdubbeld, Venoshock altijd sterk.
ASSUMPTIONS
{
    ASSUME(GetMoveEffect(MOVE_ACID_RAIN) == EFFECT_WEATHER);
    ASSUME(GetMoveWeatherType(MOVE_ACID_RAIN) == BATTLE_WEATHER_ACID_RAIN);
}

SINGLE_BATTLE_TEST("Acid Rain hurts non-Poison, non-Steel Pokémon and heals Poison types")
{
    GIVEN {
        PLAYER(SPECIES_GRIMER) { HP(100); MaxHP(200); Moves(MOVE_ACID_RAIN); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_ACID_RAIN); }
    } SCENE {
        MESSAGE("Acid rain started to fall!");
        MESSAGE("Grimer soaks up\nthe acid rain. Delicious!");
        MESSAGE("The opposing Wobbuffet is corroded\nby the acid rain!");
    } THEN {
        EXPECT_EQ(player->hp, 100 + 200 / 16);
    }
}

SINGLE_BATTLE_TEST("Acid Rain does not hurt Steel types")
{
    GIVEN {
        PLAYER(SPECIES_GRIMER) { Moves(MOVE_ACID_RAIN); }
        OPPONENT(SPECIES_STEELIX) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_ACID_RAIN); }
    } SCENE {
        NOT MESSAGE("The opposing Steelix is corroded\nby the acid rain!");
    }
}

SINGLE_BATTLE_TEST("Acid Rain weakens Fire and Water moves and boosts Poison moves", s16 damage)
{
    u32 move, weatherMove;
    PARAMETRIZE { move = MOVE_EMBER; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_EMBER; weatherMove = MOVE_ACID_RAIN; }
    PARAMETRIZE { move = MOVE_WATER_GUN; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_WATER_GUN; weatherMove = MOVE_ACID_RAIN; }
    PARAMETRIZE { move = MOVE_ACID; weatherMove = MOVE_CELEBRATE; }
    PARAMETRIZE { move = MOVE_ACID; weatherMove = MOVE_ACID_RAIN; }
    GIVEN {
        ASSUME(GetMoveType(MOVE_ACID) == TYPE_POISON);
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_EMBER, MOVE_WATER_GUN, MOVE_ACID, MOVE_CELEBRATE); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_ACID_RAIN, MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(opponent, weatherMove); MOVE(player, MOVE_CELEBRATE); }
        TURN { MOVE(player, move); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, move, player);
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } FINALLY {
        EXPECT_MUL_EQ(results[0].damage, Q_4_12(0.5), results[1].damage);
        EXPECT_MUL_EQ(results[2].damage, Q_4_12(0.5), results[3].damage);
        EXPECT_MUL_EQ(results[4].damage, Q_4_12(1.5), results[5].damage);
    }
}

SINGLE_BATTLE_TEST("Acid Rain makes Thunder never miss")
{
    PASSES_RANDOMLY(100, 100, RNG_ACCURACY);
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_ACID_RAIN, MOVE_THUNDER); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_ACID_RAIN); }
        TURN { MOVE(player, MOVE_THUNDER); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_THUNDER, player);
    }
}

SINGLE_BATTLE_TEST("Acid Rain makes Heal Bell fail")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Status1(STATUS1_POISON); Moves(MOVE_ACID_RAIN, MOVE_HEAL_BELL); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_ACID_RAIN); }
        TURN { MOVE(player, MOVE_HEAL_BELL); }
    } SCENE {
        MESSAGE("The acid rain keeps\npoisoning everything!");
    } THEN {
        EXPECT(player->status1 & STATUS1_POISON);
    }
}

SINGLE_BATTLE_TEST("Air Pollution summons Acid Rain on switch-in")
{
    GIVEN {
        PLAYER(SPECIES_KOFFING) { Ability(ABILITY_AIR_POLLUTION); }
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { }
    } SCENE {
        ABILITY_POPUP(player, ABILITY_AIR_POLLUTION);
        MESSAGE("Koffing's Air Pollution\nmade acid rain fall!");
    }
}

SINGLE_BATTLE_TEST("Defog blows Acid Rain away")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(20); Moves(MOVE_ACID_RAIN, MOVE_DEFOG); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(10); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_ACID_RAIN); }
        TURN { MOVE(player, MOVE_DEFOG); }
    } SCENE {
        MESSAGE("The acid clouds were\nblown away!");
    }
}

SINGLE_BATTLE_TEST("Forecast makes Castform immune to Acid Rain and Sandstorm damage")
{
    u32 move;
    PARAMETRIZE { move = MOVE_ACID_RAIN; }
    PARAMETRIZE { move = MOVE_SANDSTORM; }
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_ACID_RAIN, MOVE_SANDSTORM); }
        OPPONENT(SPECIES_CASTFORM) { Ability(ABILITY_FORECAST); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, move); }
    } SCENE {
        NOT HP_BAR(opponent);
    }
}
