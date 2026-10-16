# parse PT 68 (jstor 106332) Barr Montreal Dec 1776 - Mar 1777 into truth68.csv: month,day,morning,evening (int F, None if blank)
import re, csv
L=open('/home/claude.guest/lab/barr/pt/106332.md').read().split('\n')
mon=None; out=[]
MON={'DECEMBER, 1776':'1776-12','JANUARY, 1777':'1777-01','FEBRUARY, 1777':'1777-02','MARCH, 1777':'1777-03'}
def val(s):
    s=s.strip().replace('½','.5')
    if s.startswith('at 0') or s=='0': return 0.0
    m=re.fullmatch(r'([+-])\s*(\d+(?:\.5)?)',s)
    return (1 if m.group(1)=='+' else -1)*float(m.group(2)) if m else None
for l in L:
    for k,v in MON.items():
        if 'FOR '+k in l: mon=v
    m=re.match(r'\|\s*(\d+)\s*\|',l)
    if m and mon:
        c=[x.strip() for x in l.strip().strip('|').split('|')]
        out.append((mon,int(c[0]),val(c[1]),val(c[2]),c[1],c[2]))
w=csv.writer(open('/home/claude.guest/lab/barr/truth68.csv','w')); w.writerow(['month','day','morning','evening','raw_m','raw_e'])
for r in out: w.writerow(r)
from collections import Counter
print(Counter(r[0] for r in out))
bad=[r for r in out if r[2] is None or r[3] is None]
print('unparsed',len(bad),bad[:10])
for mo in MON.values():
    ds=[r[1] for r in out if r[0]==mo]; print(mo,ds[0],ds[-1],'gaps',[d for d in range(ds[0],ds[-1]+1) if d not in ds],'dups',[d for d in set(ds) if ds.count(d)>1])
