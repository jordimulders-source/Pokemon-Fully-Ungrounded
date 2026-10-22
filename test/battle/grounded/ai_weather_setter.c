#include "global.h"
#include "test/battle.h"
#include "battle_ai_util.h"

// Project Grounded: de AI brengt een weerzetter terug als het weer weg is en bewaart hem zolang het nog staat.

AI_SINGLE_BATTLE_TEST("AI weather setters: AI sends out its Drought mon after a KO when there is no sun and a teammate needs it")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_CHECK_VIABILITY | AI_FLAG_TRY_TO_FAINT | AI_FLAG_SMART_SWITCHING | AI_FLAG_SMART_MON_CHOICES | AI_FLAG_OMNISCIENT);
        PLAYER(SPECIES_SNORLAX) { Level(50); Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_WEEDLE) { Level(1); Moves(MOVE_STRING_SHOT); }
        OPPONENT(SPECIES_RATTATA) { Level(30); Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_NINETALES) { Level(30); Ability(ABILITY_DROUGHT); Moves(MOVE_EMBER); }
        OPPONENT(SPECIES_BULBASAUR) { Level(30); Moves(MOVE_SOLAR_BEAM); }
    } WHEN {
        TURN { MOVE(player, MOVE_TACKLE); EXPECT_SEND_OUT(opponent, 2); }
    }
}

AI_SINGLE_BATTLE_TEST("AI weather setters: AI keeps its second Drought mon in reserve while the sun is still up")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_CHECK_VIABILITY | AI_FLAG_TRY_TO_FAINT | AI_FLAG_SMART_SWITCHING | AI_FLAG_SMART_MON_CHOICES | AI_FLAG_OMNISCIENT);
        PLAYER(SPECIES_SNORLAX) { Level(50); Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_VULPIX) { Level(1); Ability(ABILITY_DROUGHT); Moves(MOVE_EMBER); }
        OPPONENT(SPECIES_TORKOAL) { Level(30); Ability(ABILITY_DROUGHT); Moves(MOVE_EMBER); }
        OPPONENT(SPECIES_BULBASAUR) { Level(30); Moves(MOVE_SOLAR_BEAM); }
    } WHEN {
        TURN { MOVE(player, MOVE_TACKLE); EXPECT_SEND_OUT(opponent, 2); }
    }
}

AI_SINGLE_BATTLE_TEST("AI weather setters: AI switches to its Drought mon mid-battle to bring the sun back")
{
    PASSES_RANDOMLY(50, 100, RNG_AI_SWITCH_WEATHER);
    GIVEN {
        AI_FLAGS(AI_FLAG_CHECK_BAD_MOVE | AI_FLAG_CHECK_VIABILITY | AI_FLAG_TRY_TO_FAINT | AI_FLAG_SMART_SWITCHING | AI_FLAG_SMART_MON_CHOICES | AI_FLAG_OMNISCIENT);
        PLAYER(SPECIES_SNORLAX) { Level(30); Moves(MOVE_CELEBRATE); }
        OPPONENT(SPECIES_CHARIZARD) { Level(30); Moves(MOVE_EMBER); }
        OPPONENT(SPECIES_NINETALES) { Level(30); Ability(ABILITY_DROUGHT); Moves(MOVE_EMBER); }
    } WHEN {
        TURN { MOVE(player, MOVE_CELEBRATE); EXPECT_SWITCH(opponent, 1); }
    }
}
