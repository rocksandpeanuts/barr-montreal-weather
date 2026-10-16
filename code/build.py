import json,csv,re
from collections import defaultdict
E=json.load(open('/home/claude.guest/lab/barr/data/extra.json'))
def olm(path,starts=None):
    rows={}
    L=open(path).read().split('\n'); mon=None
    MON={'DECEMBER, 1776':'1776-12','JANUARY, 1777':'1777-01','FEBRUARY, 1777':'1777-02','MARCH, 1777':'1777-03',
         'DECEMBER, 1778':'1778-12','JANUARY, 1779':'1779-01','FEBRUARY, 1779':'1779-02','MARCH, 1779':'1779-03','APRIL, 1779':'1779-04'}
    for i,l in enumerate(L):
        for k,v in MON.items():
            if k in l.upper(): mon=v
        if starts:
            for v,st in starts.items():
                if i+1==st: mon=v
        m=re.match(r'\|\s*(\d+)\s*\|',l)
        if m and mon:
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            rows[f'{mon}-{int(c[0]):02d}']=c
    return rows
O=olm('/home/claude.guest/lab/barr/pt/106332.md'); O.update(olm('/home/claude.guest/lab/barr/pt/106379.md',{'1778-12':26,'1779-01':64,'1779-02':106,'1779-03':139,'1779-04':179}))
WIND=re.compile(r'^(N|S|E|W|NE|NW|SE|SW|NNE|NNW|ENE|ESE|SSE|SSW|WSW|WNW|Calm|calm)$')
dis=[]; snow=[]
for k in sorted(O):
    c=O[k]; e=E.get(k,{})
    ow=[x for x in c if WIND.match(x.rstrip('.'))]
    tw=re.sub(r'[^A-Za-z]','',' '.join(e.get('wind',[]))).replace('EE','E')
    if (ow[0] if ow else '')!=tw: dis.append((k,ow,e.get('wind')))
    if e.get('snow') or e.get('rain'): snow.append((k,e.get('snow'),e.get('rain')))
print(len(O),'days; wind disagreements',len(dis))
for d in dis: print('W',d)
for s in snow: print('S',s)

from difflib import SequenceMatcher
def remt(c): return c[-1] if c else ''
def tw_of(k):
    return re.sub(r'[^A-Za-z ]','',' '.join(E.get(k,{}).get('wind',[]))).replace('EE','E').strip()
def tr_of(k): return re.sub(r'[|{}\[\]j;/]','',' '.join(E.get(k,{}).get('rem',[]))).replace('f','s').lower().strip()
print()
months=sorted(set(k[:7] for k in O))
SHIFT={}
for mon in months:
    ks=sorted(k for k in O if k.startswith(mon))
    res=[]
    for sh in (-1,0,1):
        sc=0
        for k in ks:
            d=int(k[-2:])+sh; k2=f'{mon}-{d:02d}'
            if k2 not in E: continue
            a=remt(O[k]).replace('f','s').lower(); b=tr_of(k2)
            sc+=SequenceMatcher(None,a,b).ratio()
        res.append((round(sc/len(ks),2),sh))
    SHIFT[mon]=max(res)[1]; print(mon,res)
