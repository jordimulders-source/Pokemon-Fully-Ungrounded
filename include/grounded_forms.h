#ifndef GUARD_GROUNDED_FORMS_H
#define GUARD_GROUNDED_FORMS_H

// Project Grounded: vormen die van toeval of de echte datum afhangen.
u32 GetRandomPatternForm(u32 species);   // Scatterbug/Spewpa/Vivillon: willekeurig patroon
u32 GetSeasonalForm(u32 species);        // Deerling/Sawsbuck: seizoen van de RTC-maand
u32 GetWildEncounterForm(u32 species);   // beide toegepast op een wilde ontmoeting
void SeasonalFormUpdateParty(void);      // Deerling/Sawsbuck in het team volgen het seizoen (Gen 5)

#endif // GUARD_GROUNDED_FORMS_H
