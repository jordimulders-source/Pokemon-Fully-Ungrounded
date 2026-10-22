#include "global.h"
#include "test/battle.h"

// Project Grounded: Stealth Rock van Stone Axe op een Fire/Electric-Volbeat hoort 25% te doen (2x).
SINGLE_BATTLE_TEST("Stone Axe rocks deal 25% to Fire/Electric Volbeat")
{
    s16 dmg;
    GIVEN {
        ASSUME(GetSpeciesType(SPECIES_VOLBEAT, 0) == TYPE_FIRE);
        ASSUME(GetSpeciesType(SPECIES_VOLBEAT, 1) == TYPE_ELECTRIC);
        PLAYER(SPECIES_SANDSLASH);
        OPPONENT(SPECIES_WOBBUFFET);
        OPPONENT(SPECIES_VOLBEAT) { HP(400); MaxHP(400); }
    } WHEN {
        TURN { MOVE(player, MOVE_STONE_AXE); }
        TURN { SWITCH(opponent, 1); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_STONE_AXE, player);
        HP_BAR(opponent, captureDamage: &dmg);
    } THEN {
        EXPECT_EQ(opponent->hp, 300);
    }
}
