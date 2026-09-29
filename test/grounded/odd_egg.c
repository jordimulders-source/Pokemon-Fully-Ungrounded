#include "global.h"
#include "test/overworld_script.h"
#include "test/test.h"

TEST("(Project Grounded) SetLastPartyMonShiny makes the newest party mon shiny")
{
    ZeroPlayerPartyMons();
    RUN_OVERWORLD_SCRIPT(
        givemon SPECIES_PIKACHU, 10;
        giveegg SPECIES_TOXEL;
        special SetLastPartyMonShiny;
    );
    EXPECT_EQ(GetMonData(&gPlayerParty[1], MON_DATA_SPECIES), SPECIES_TOXEL);
    EXPECT(GetMonData(&gPlayerParty[1], MON_DATA_IS_EGG));
    EXPECT(GetMonData(&gPlayerParty[1], MON_DATA_IS_SHINY));
}
