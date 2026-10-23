import sys;sys.path.insert(0,'.')
from lib import *
from PIL import ImageDraw
G2={
'01_viervoeter_klein':'poochyena zigzagoon cyndaquil growlithe eevee vulpix rhyhorn meowth skitty houndour snubbull ponyta mareep electrike shinx lillipup purrloin fennekin rockruff yamper nickit fidough zorua skwovet larvitar phanpy swinub stufful',
'02_viervoeter_groot':'mightyena arcanine ninetales rapidash persian houndoom manectric absol entei raikou suicune luxray stoutland liepard lycanroc boltund thievul mabosstiff sawsbuck tauros girafarig stantler camerupt mudsdale zebstrika leafeon umbreon espeon glaceon sylveon solgaleo zacian',
'03_tweevoet_klein':'teddiursa pikachu charmander squirtle totodile torchic chimchar piplup oshawott froakie chespin popplio grookey scorbunny sobble quaxly fuecoco aipom sentret riolu buneary pancham makuhita spinda munchlax smoochum elekid magby timburr mankey',
'04_tweevoet_groot':'machamp hitmonlee hitmonchan blaziken lucario infernape emboar conkeldurr hawlucha primeape medicham breloom sceptile gallade mienshao pangoro passimian rillaboom cinderace urshifu kangaskhan ursaring zangoose weavile gardevoir alakazam hypno gengar zoroark incineroar decidueye',
'05_vogels':'pidgey pidgeotto pidgeot spearow fearow farfetchd doduo natu xatu hoothoot noctowl murkrow honchkrow taillow swellow wingull pelipper swablu altaria starly staraptor pidove unfezant rufflet braviary fletchling talonflame rowlet pikipek toucannon rookidee corviknight wattrel flamigo skarmory',
'06_slang_vis':'ekans arbok dratini dragonair onix steelix seviper milotic gyarados magikarp goldeen seaking feebas carvanha sharpedo wailmer barboach whiscash relicanth luvdisc finneon lumineon basculin arrokuda barraskewda sandaconda silicobra dunsparce wiglett finizen palafin',
'07_bol_blob':'jigglypuff wigglytuff voltorb electrode koffing weezing ditto grimer muk shuppet duskull gastly drifloon swablu clefairy togepi azurill marill whismur loudred chimecho castform spheal munna solosis duosion reuniclus snom pyukumuku jellicent tandemaus',
'08_insecten':'caterpie metapod butterfree weedle beedrill paras venonat venomoth scyther pinsir ledyba ledian spinarak ariados yanma wurmple beautifly dustox surskit masquerain nincada ninjask volbeat kricketot kricketune combee vespiquen sewaddle leavanny karrablast escavalier joltik galvantula grubbin vikavolt blipbug nymble',
'09_starters_1':'bulbasaur charmander squirtle chikorita cyndaquil totodile treecko torchic mudkip turtwig chimchar piplup snivy tepig oshawott chespin fennekin froakie rowlet litten popplio grookey scorbunny sobble sprigatito fuecoco quaxly',
'10_starters_2':'ivysaur charmeleon wartortle bayleef quilava croconaw grovyle combusken marshtomp grotle monferno prinplup servine pignite dewott quilladin braixen frogadier dartrix torracat brionne thwackey raboot drizzile floragato crocalor quaxwell',
'11_starters_3':'venusaur charizard blastoise meganium typhlosion feraligatr sceptile blaziken swampert torterra infernape empoleon serperior emboar samurott chesnaught delphox greninja decidueye incineroar primarina rillaboom cinderace inteleon meowscarada skeledirge quaquaval',
'12_apen':'mankey primeape aipom ambipom chimchar monferno infernape pansage simisage pansear simisear panpour simipour oranguru passimian grookey thwackey rillaboom slakoth vigoroth slaking',
'13_langnek_hoefdier':'ponyta rapidash girafarig farigiraf mudbray mudsdale wooloo dubwool mareep flaaffy deerling sawsbuck stantler blitzle zebstrika skiddo gogoat tauros miltank bouffalant lechonk oinkologne',
'14_marter_knaagdier':'sentret furret zigzagoon linoone buizel floatzel patrat watchog minccino cinccino skwovet greedent rattata raticate pikachu pachirisu emolga dedenne togedemaru morpeko pawmi bidoof bibarel bunnelby diggersby yungoos gumshoos sandshrew zangoose',
'15_psychic_dark_ghost':'abra kadabra alakazam drowzee hypno mrmime jynx espeon umbreon natu xatu ralts kirlia gardevoir meditite medicham sneasel weavile absol murkrow sableye banette dusclops chimecho spoink grumpig gothita gothitelle inkay malamar hatenna hatterene impidimp grimmsnarl',
'16_nachtdieren_klein':'hoothoot sentret aipom teddiursa slakoth spinda shuppet mimikyu morelull cutiefly comfey dedenne togedemaru pichu cleffa igglybuff smoochum azurill wynaut happiny munchlax budew bonsly mimejr chingling riolu',
}
def make(name,lst,scale=2):
    names=lst.split()
    cw,ch=64*scale+4,64*scale+12
    cols=8; rows=(len(names)+cols-1)//cols
    sh=Image.new('RGB',(cols*cw,rows*ch),(232,236,232)); dr=ImageDraw.Draw(sh)
    for i,n in enumerate(names):
        d_=dex(); gba=True
        im=load(n,True)
        if im is None: dr.text(((i%cols)*cw+2,(i//cols)*ch+2),n+'?',fill=(200,0,0)); continue
        m=metrics(im)
        x,y=(i%cols)*cw,(i//cols)*ch
        dr.rectangle([x+1,y+1,x+cw-2,y+64*scale],outline=(205,210,205))
        sh.paste(im.resize((64*scale,64*scale),Image.NEAREST),(x+2,y+1),im.resize((64*scale,64*scale),Image.NEAREST))
        dr.text((x+3,y+64*scale+1),(f"{n[:11]} {m['A']}" if scale>1 else n[:10]),fill=(20,20,20))
    sh.save(f'sheets/{name}_{scale}x.png')
import os; os.makedirs('sheets',exist_ok=True)
for k,v in G2.items():
    make(k,v,2); make(k,v,1)
print('ok')
