import json,csv,re
import numpy as np
from collections import defaultdict
P=json.load(open('/home/claude.guest/lab/barr/data/pageread2.json'))
T=defaultdict(dict)
for r in csv.DictReader(open('/home/claude.guest/lab/barr/truth.csv')): T[r['month']][int(r['day'])]=r
nd={'1778-12':31,'1779-01':31,'1779-02':28,'1779-03':31,'1779-04':15}
tot=ok=0; flags=[]
for mon in nd:
    pts=[]
    for r in P[mon]:
        m=re.fullmatch(r'\D*?(\d{1,2})\D*',r['day'])
        if m and 1<=int(m.group(1))<=nd[mon]: pts.append((int(m.group(1)),r['y']))
    pts=np.array(pts,float); best=None
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            if pts[j,0]==pts[i,0]: continue
            k=(pts[j,1]-pts[i,1])/(pts[j,0]-pts[i,0]); b=pts[i,1]-k*pts[i,0]
            inl=np.abs(pts[:,1]-(k*pts[:,0]+b))<8
            if best is None or inl.sum()>best[0]: best=(inl.sum(),inl)
    q=pts[best[1]]; k,b=np.polyfit(q[:,0],q[:,1],1)
    byday=defaultdict(str)
    for r in P[mon]:
        d=int(round((r['y']-b)/k))
        byday[d]+=' '+r['day']+' '+r['m']+' '+r['e']
    for d in sorted(T[mon]):
        t=T[mon][d]; s=byday.get(d,'')
        s=s.replace('O','0').replace('o','0').replace('°','0').replace('©','0').replace('I','1').replace('l','1').replace('|','1').replace('j','1').replace('[','1').replace(']','1').replace('{','1').replace('}','1')
        s=re.sub(r'\s+','',s)
        def pat(v):
            if v=='': return r''
            v=int(v); return r'(?<![0-9])1?'+str(abs(v))+('[b6]' if v<0 else '[a28@3]')
        tot+=1
        rx=pat(t['morning'])+r'.{0,4}?'+pat(t['evening'])
        # day prefix may glue: allow day digits immediately before
        s2=re.sub('^'+str(d),'',s)
        if re.search(rx,s) or re.search(rx,s2) or re.search(rx.replace('(?<![0-9])',''),s2): ok+=1
        else: flags.append((mon,d,t['morning'],t['evening'],s))
print('confirmed',ok,'/',tot)
for f in flags: print(f)
