# audiocheck.py a.wav ...: piekmomenten, constante tonen (>=90% van de seconden sterk) en RMS per 5 s. Draai dit vóór je een muziekpreview stuurt.
import wave,sys,numpy as np
for p in sys.argv[1:]:
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(float)
    m=a.mean(1); R=32768
    pk=np.where(abs(a).max(1)>=30000)[0]
    print(p.split('/')[-1],'peaks at s:',np.unique((pk/R).round(2))[:8])
    # constante toon: per seconde spectrum, frequenties die in >=90% van de seconden sterk zijn
    S=[]
    for i in range(1,int(len(m)/R)):
        x=m[i*R:(i+1)*R]; S.append(np.abs(np.fft.rfft(x*np.hanning(R))))
    S=np.array(S); med=np.median(S,axis=1,keepdims=True)
    strong=(S>40*med).mean(0)
    f=np.where(strong>=0.9)[0]
    print('  constant tones (Hz):',f[:15], ' rms per 5s:',[int(np.sqrt((m[i:i+5*R]**2).mean())) for i in range(0,len(m)-5*R,5*R)])
