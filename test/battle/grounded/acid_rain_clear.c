#include "global.h"
#include "test/battle.h"

// Project Grounded: Tailwind blaast de zure regen weg, Purify neutraliseert hem.
SINGLE_BATTLE_TEST("Tailwind blows away Acid Rain")
{
    GIVEN {
        PLAYER(SPECIES_PIDGEOT);
        OPPONENT(SPECIES_WOBBUFFET);
    } WHEN {
        TURN { MOVE(opponent, MOVE_ACID_RAIN); MOVE(player, MOVE_TAILWIND); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_TAILWIND, player);
        MESSAGE("The acid clouds were blown away!");
    } THEN {
        EXPECT(!(gBattleWeather & B_WEATHER_ACID_RAIN));
    }
}

SINGLE_BATTLE_TEST("Purify neutralizes Acid Rain even without a status to cure")
{
    GIVEN {
        PLAYER(SPECIES_WOBBUFFET) { Speed(1); }
        OPPONENT(SPECIES_WOBBUFFET) { Speed(100); }
    } WHEN {
        TURN { MOVE(opponent, MOVE_ACID_RAIN); MOVE(player, MOVE_PURIFY); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_PURIFY, player);
        MESSAGE("The acid rain was neutralized!");
    } THEN {
        EXPECT(!(gBattleWeather & B_WEATHER_ACID_RAIN));
    }
}
