# stomp.py (exec vanuit bouw.py, STOMP = 'licht' of 'sterk'): elke achterpunt minder puntig, zoals de Gen 3 Starmie.
# Gen 3 Starmie (puntmaat.py): de punten eindigen in een stomp, plat eind; breedte 1 px van de tip 4,0-5,2 px
# (mediaan 4,6), 2 px van de tip 4,6-6,1 (mediaan 5,5), 3 px 5,0-6,8. Werkwijze: as = juweelmidden -> tip van de
# modelpunt (richting blijft); de punt wordt loodrecht op de as afgesneden op de plek waar hij voor het eerst
# minstens W px breed is (licht W=4, sterk W=5). Alleen weghalen: pixels voorbij de snede worden transparant.
# De voet en de richting blijven die van het model; facetkleuren blijven die van de reductie (de nieuwe rand krijgt
# daarna de gewone buitenlijn).
W={'licht':4.0,'sterk':5.0}[STOMP]; KERN=np.array([31.5,30.5]); STOMPWEG={}; STOMPINFO={}
for nm in ('linksboven','rechtsboven','linksonder','rechtsonder','onder'):
    m=(PNAAM==nm)&(o>0)
    ys,xs=np.where(m); p=np.stack([xs+0.5,ys+0.5],1)
    d=np.hypot(*(p-KERN).T); tip=p[np.argmax(d)]; ax=(tip-KERN)/np.linalg.norm(tip-KERN); pe=np.array([-ax[1],ax[0]])
    t=(p-KERN)@ax; s=(p-KERN)@pe; T=t.max(); cut=T
    for k in np.arange(0,12,0.5):
        sl=(t>T-k-1)&(t<=T-k)
        if sl.any() and s[sl].max()-s[sl].min()+1>=W: cut=T-k; break
    weg=[(int(x),int(y)) for (x,y),tt in zip(zip(xs,ys),t) if tt>cut]
    for x,y in weg: zet(x,y,0,'stomp weg'); PNAAM[y,x]=''
    STOMPWEG[nm]=len(weg); STOMPINFO[nm]=dict(richting=round(float(np.degrees(np.arctan2(-ax[1],ax[0]))),1),lengte_voor=round(float(T),1),lengte_na=round(float(cut),1))
BM=BM&(o>0)
print('stomp',STOMP,'W',W,'weg per punt',STOMPWEG); print('stomp info',STOMPINFO)
