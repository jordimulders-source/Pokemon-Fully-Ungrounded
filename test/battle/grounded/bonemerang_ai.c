#include "global.h"
#include "test/battle.h"

// Project Grounded: Bonemerang raakt Flying- en Levitate-Pokémon; de AI moet dat weten.
AI_SINGLE_BATTLE_TEST("AI uses Bonemerang against Flying and Levitate foes")
{
    u32 species;
    PARAMETRIZE { species = SPECIES_PIDGEY; }
    PARAMETRIZE { species = SPECIES_GASTLY; }

    GIVEN {
        AI_FLAGS(AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_CHECK_VIABILITY | AI_FLAG_TRY_TO_FAINT);
        PLAYER(species) { Speed(10); }
        OPPONENT(SPECIES_MAROWAK) { Moves(MOVE_BONEMERANG, MOVE_GROWL); Speed(100); }
    } WHEN {
        TURN { EXPECT_MOVE(opponent, MOVE_BONEMERANG); }
    }
}
