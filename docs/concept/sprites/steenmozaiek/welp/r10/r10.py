# Ronde 10: alleen de kop (zone x<=16, y<=22 in arraycoordinaten = x<=23, y<=40 in 64x64), per onderdeel naar het model.
# Basis welp_r9.npy. Varianten via argv: oog=E1|E2, ver=A|B|C, tand=1|2
import numpy as np, sys
CH='.KdSMLPQRgWCTGHU'; IX={c:i for i,c in enumerate(CH)}
r9=np.load('welp_r9.npy'); a=r9.copy()
opt=dict(oog='E9',ver='B',tand='1',tong='6',band='B3')
for s in sys.argv[1:]:
    k,v=s.split('='); opt[k]=v
def rij(y,s,x0=0):
    for i,c in enumerate(s):
        if c!='_': a[y,x0+i]=IX[c]
# --- band (y2-7): buitenstreep R, groef P (doorlopende 2:1-lijn), binnenstreep R, onderkant Q
#      x: 0123456789012345 6
opt.setdefault('band','B2')
if opt['band']=='B1':
    rij(2,'____dMMMMRRRRPRdd'); rij(3,'____dSSMRRRPPRMLL'); rij(4,'____dSRRRPPRRMLLL')
    rij(5,'____dSRRPRRLLLLLM'); rij(6,'____dRRPRRLLLLLMM'); rij(7,'___dLLQRQMMMMMMMM')
else:
    # B2: haarspeld-U zoals het model: buitenarm R, groef in vaste 2:1-trap (13 | 11-12 | 9-10 | 7-8 | 7), binnenarm R, onderbocht
    g='S' if opt['band'] in ('B3','B5') else 'P'
    rij(2,'____dMMMMRRRR'+g+'Rdd'); rij(3,'____dSSMRRR'+g+g+'RMLL'); rij(4,'____dSRRR'+g+g+'RRMLLL')
    rij(5,'____dSR'+g+g+'RRLLLLLM'); rij(6,'____dRR'+g+'RRLLLLLMM'); rij(7,'___dLLQRQMMMMMMMM')
    if opt['band'] in ('B4','B5'):  # donkerbruine rand langs de buitenkant van de band (zoals het model)
        for x,y in [(8,2),(7,3),(5,4),(13,4),(11,5),(10,6),(9,7),(5,7)]: a[y,x]=IX['S']

# --- oog dichtbij (x10-14, y8-11) en wang/snuit
rij(8, '___ddLLLLLdKKKKMM')
if opt['oog']=='E1':   # 5 breed, wit (C) achteraan zonder sluitlijn
    rij(9, '___dKMMMSSKWKGCMM'); rij(10,'___dKMLLSSKgKgCMM'); rij(11,'___dHHHLMMdgggdMM')
elif opt['oog']=='E2': # iris links van de pupil, wit + sluitlijn achteraan
    rij(9, '___dKMMMSSKWKCKMM'); rij(10,'___dKMLLSSKGKCKMM'); rij(11,'___dHHHLMMdgggdMM')
elif opt['oog']=='E4': # lichte iris, pupil 1 px, glans linksboven, wit achteraan
    rij(9, '___dKMMMSSKWGgWMM'); rij(10,'___dKMLLSSdgKgCMM'); rij(11,'___dHHHLMMdgggdMM')
elif opt['oog']=='E5': # als E4 maar pupil 2 hoog
    rij(9, '___dKMMMSSKWKgWMM'); rij(10,'___dKMLLSSdgKgCMM'); rij(11,'___dHHHLMMdgggdMM')
elif opt['oog']=='E6': # gemeten modelkleuren per pixel: lid x10-13, pupil x12 (2 hoog), glans (11,9), wit rechtsonder (13,11)
    rij(8, '___ddLLLLLKKKKMMM'); rij(9, '___dKMMMSSKWKGdMM'); rij(10,'___dKMLLSSdGKgGMM'); rij(11,'___dHHHLMMGggCMMM')
elif opt['oog']=='E7': # als E6, wit rechtsonder W en iris onder licht
    rij(8, '___ddLLLLLKKKKMMM'); rij(9, '___dKMMMSSKWKGdMM'); rij(10,'___dKMLLSSdGKggMM'); rij(11,'___dHHHLMMdggWMMM')
elif opt['oog']=='E8': # rond: lid 3 breed, glans + pupil + iris + wit, onderkant afgerond
    rij(8, '___ddLLLLLMKKKMMM'); rij(9, '___dKMMMSSKWKgWMM'); rij(10,'___dKMLLSSKgKgCMM'); rij(11,'___dHHHLMMdggddMM')
elif opt['oog']=='E9': # rond met onderlijn op y12 (5 hoog)
    rij(8, '___ddLLLLLdKKKdMM'); rij(9, '___dKMMMSSKWKgWMM'); rij(10,'___dKMLLSSKgKgCMM'); rij(11,'___dHHHLMMKgggdMM'); rij(12,'___dHHLMMLLdddMMM')
elif opt['oog']=='E10': # als E8 maar wit C en iris onder licht, lid 4 breed
    rij(8, '___ddLLLLLdKKKKMM'); rij(9, '___dKMMMSSKWKgCMM'); rij(10,'___dKMLLSSKgKgCMM'); rij(11,'___dHHHLMMdgggdMM')
elif opt['oog']=='E3': # 6 breed: iris aan beide kanten, wit en sluitlijn (d)
    rij(8, '___ddLLLLLdKKKKKM'); rij(9, '___dKMMMSSKWKGCdM'); rij(10,'___dKMLLSSKgKgCdM'); rij(11,'___dHHHLMMdgggdMM')
if opt['oog']!='E9': rij(12,'___dHHLMMLLLLLMMM')
# --- ver oog (op de kopcontour x3-4, y8-11)
if opt['ver']=='A':    # model: wit OP de contour, donker erachter
    a[8,3]=IX['d']; a[8,4]=IX['K']; a[9,3]=IX['W']; a[10,3]=IX['g']; a[9,4]=IX['K']; a[10,4]=IX['K']; a[11,3]=IX['d']
elif opt['ver']=='B':  # Growlithe: contour blijft, witte kolom + zwarte kolom binnen de contour
    a[8,4]=IX['K']; a[8,5]=IX['K']; a[9,4]=IX['W']; a[10,4]=IX['g']; a[9,5]=IX['K']; a[10,5]=IX['K']
elif opt['ver']=='A2': # model letterlijk: grijs op de contour, licht onderaan
    a[8,3]=IX['K']; a[8,4]=IX['d']; a[9,3]=IX['G']; a[10,3]=IX['G']; a[11,3]=IX['g']; a[9,4]=IX['K']; a[10,4]=IX['K']
elif opt['ver']=='C':  # Vulpix: contour donker, smal oog 1 breed: wit boven, zwart onder, lid erboven
    a[8,4]=IX['K']; a[9,4]=IX['W']; a[10,4]=IX['K']; a[9,5]=IX['S']
# --- neus, neusrug, mond
rij(13,'__ddddKMLLLMMMMMM')
rij(14,'__dSSKMLLLMMMMMMM')
rij(15,'__dMKMMMMMMKMSSSS')
rij(16,'__dMdMMMMMKKSSSSS')
rij(17,'___KWKKKWKSKSSSSS')
if opt['tand']=='2': rij(18,'____W'); 
if opt['tong']=='1':
    rij(18,'____dUTTWSSKSSSdd' if opt['tand']=='1' else '____WUTTWSSKSSSdd')
    rij(19,'____dTTTUSSKSddSS')
    rij(20,'____dTTUdWKddSSSS')
    rij(21,'___dTTUdMMMKdSSSS')
    rij(22,'___ddTdKKKK.ddLLL')
elif opt['tong']=='3':   # donkere mondholte (d), tong breed uit de bek, punt naar links over de poot
    rij(18,'____dUTTUddKSSSdd' if opt['tand']=='1' else '____WUTTUddKSSSdd')
    rij(19,'____dTTTUddKSddSS')
    rij(20,'____dTTUdWKddSSSS')
    rij(21,'___dTTUdMMMKdSSSS')
    rij(22,'___ddTdKKKK.ddLLL')
elif opt['tong'] in ('4','5'):   # per pixel naar de gemeten modelkleuren (rij 15-22)
    rij(13,'__dddddMLLLMMMMMM'); rij(14,'__dSSdSLLLMMMMMMM' if opt.get('neus','N2')=='N2' else '__dSdKMLLLMMMMMMM')
    rij(15,'__dSKSMMMMMdMSSSS' if opt.get('neus','N2')=='N2' else '__dMKMMMMMMdMSSSS'); rij(16,'__dMKMMMMMKKSSSSS')
    rij(17,'___KWKKKWKdKSSSSS')
    rij(18,'____W'+('.' if opt['tong']=='4' else 'd')+'UUWSSKSSSdd')
    rij(19,'_____TUTUWdMSKdSS'); a[19,4]=IX['.' if opt['tong']=='4' else 'd']
    rij(20,'____dTTUKWSSddSSS')
    rij(21,'____dTTUMMSdd')
    rij(22,'___ddTUKKKK.ddLLL')
elif opt['tong']=='6':   # als 4 (gemeten modelpixels), tong lichter met G = lichtroze glans (palet-index 13 was ongebruikt)
    rij(13,'__dddddMLLLMMMMMM'); rij(14,'__dSSdMLLLMMMMMMM')
    rij(15,'__dSKSMMMMMdMSSSS'); rij(16,'__dMKMMMMMKKSSSSS')
    rij(17,'___KWKKKWKdKSSSSS')
    rij(18,'____g.UTWSSKSSSdd')   # tanden met grijze schaduw zoals het model (9a9b9d / c9bfc0)
    rij(19,'____.TUTUWdMSKdSS')
    rij(20,'____dGTUKgSSddSSS')
    rij(21,'____dGTUMMSdd')
    rij(22,'___ddTUKKKK.ddLLL')
elif opt['tong']=='2':
    rij(18,'____dUTTWSSKSSSdd' if opt['tand']=='1' else '____WUTTWSSKSSSdd')
    rij(19,'____dTTUdSSKSddSS')
    rij(20,'____dTUTdWKddSSSS')
    rij(21,'___dTTUTdMMKdSSSS')
    rij(22,'___dTTTdKKK.ddLLL')
if opt.get('snuit')=='L':   # snuitrug als modelvlak: L i.p.v. H, neuspunt 1 px naar voren (model x1,4 op y14)
    rij(11,'____LLLL',0); rij(12,'____LLL',0)
if opt.get('punt')=='1':
    a[14,1]=IX['d']; a[14,2]=IX['S']
naam=sys.argv[0] if False else 'welp_r10'+''.join('_%s%s'%(k,v) for k,v in opt.items())
np.save(naam+'.npy',a)
z=np.zeros_like(a,bool); z[:23,:17]=True
print(naam,'diff r9 in zone:',int((a!=r9)[z].sum()),'buiten zone:',int((a!=r9)[~z].sum()))
