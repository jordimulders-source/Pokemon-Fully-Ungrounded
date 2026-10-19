#include "global.h"
#include "test/battle.h"

// Project Grounded: ijking van de OU-simulator (tools/grounded/balance/ousim.py) tegen de echte engine.
// De verwachte waarden (hoogste rol) komen uit ousim.Battle.damage met dezelfde stats; zie BALANS_OU.md.

SINGLE_BATTLE_TEST("Balance sim: Galvanize Exploud gets STAB and 1.2x on Boomburst", s16 damage)
{
    enum Ability ability;
    s16 expected;
    PARAMETRIZE { ability = ABILITY_SOUNDPROOF; expected = 178; }
    PARAMETRIZE { ability = ABILITY_GALVANIZE;  expected = 319; }
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_EXPLOUD, 0) == TYPE_STEEL);
        ASSUME(GetSpeciesType(SPECIES_EXPLOUD, 1) == TYPE_ELECTRIC);
        PLAYER(SPECIES_EXPLOUD) { Ability(ability); SpAttack(300); Moves(MOVE_BOOMBURST); }
        OPPONENT(SPECIES_WOBBUFFET) { SpDefense(200); HP(1000); MaxHP(1000); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_BOOMBURST, WITH_RNG(RNG_DAMAGE_MODIFIER, 0)); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &results[i].damage);
    } THEN {
        EXPECT_GE(results[i].damage, expected - 2);
        EXPECT_LE(results[i].damage, expected + 2);
    }
}

SINGLE_BATTLE_TEST("Balance sim: Pollen Season Ribombee's Bug Buzz in Pollen Haze")
{
    s16 damage;
    GIVEN {
        PLAYER(SPECIES_RIBOMBEE) { Ability(ABILITY_POLLEN_SEASON); SpAttack(250); Moves(MOVE_BUG_BUZZ); }
        OPPONENT(SPECIES_WOBBUFFET) { SpDefense(200); HP(1000); MaxHP(1000); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_BUG_BUZZ, WITH_RNG(RNG_DAMAGE_MODIFIER, 0)); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &damage);
    } THEN {
        EXPECT_GE(damage, 432 - 2);
        EXPECT_LE(damage, 432 + 2);
    }
}

SINGLE_BATTLE_TEST("Balance sim: Air Pollution Weezing's Sludge Bomb in Acid Rain")
{
    s16 damage;
    GIVEN {
        PLAYER(SPECIES_WEEZING) { Ability(ABILITY_AIR_POLLUTION); SpAttack(200); Moves(MOVE_SLUDGE_BOMB); }
        OPPONENT(SPECIES_WOBBUFFET) { SpDefense(200); HP(1000); MaxHP(1000); Moves(MOVE_CELEBRATE); }
    } WHEN {
        TURN { MOVE(player, MOVE_SLUDGE_BOMB, WITH_RNG(RNG_DAMAGE_MODIFIER, 0)); }
    } SCENE {
        HP_BAR(opponent, captureDamage: &damage);
    } THEN {
        EXPECT_GE(damage, 173 - 2);
        EXPECT_LE(damage, 173 + 2);
    }
}
