#include "global.h"
#include "mail.h"
#include "constants/items.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "text.h"
#include "international_string_util.h"

void ClearAllMail(void)
{
    // Doet niets, want er is geen mail
}

void ClearMail(struct Mail *mail)
{
    // Doet niets
}

bool8 MonHasMail(struct Pokemon *mon)
{
    return FALSE; // Een Pokemon kan nooit mail hebben als de teller op 0 staat
}

u8 GiveMailToMonByItemId(struct Pokemon *mon, enum Item itemId)
{
    return MAIL_NONE;
}

u16 SpeciesToMailSpecies(enum Species species, u32 personality)
{
    return species;
}

enum Species MailSpeciesToSpecies(u16 mailSpecies, u16 *buffer)
{
    return mailSpecies;
}

u8 GiveMailToMon(struct Pokemon *mon, struct Mail *mail)
{
    return MAIL_NONE;
}

void TakeMailFromMon(struct Pokemon *mon)
{
    u8 mailId = MAIL_NONE;
    u16 heldItem = ITEM_NONE;
    
    // Zorg alleen dat de data op de Pokemon zelf wordt gewist
    SetMonData(mon, MON_DATA_MAIL, &mailId);
    if (ItemIsMail(GetMonData(mon, MON_DATA_HELD_ITEM)))
        SetMonData(mon, MON_DATA_HELD_ITEM, &heldItem);
}

u8 SaveMailToPC(struct Mail *mail)
{
    // Doet niets
    return MAIL_NONE;
}

u8 TakeMailFromMonAndSave(struct Pokemon *mon)
{
    return MAIL_NONE;
}

bool8 ItemIsMail(enum Item itemId)
{
    // We houden dit op FALSE zodat de game mail-items als gewone items behandelt (of negeert)
    return FALSE; 
}