import json,csv,re,sys
from collections import defaultdict
P=json.load(open('/home/claude.guest/lab/barr/data/pageread2.json'))
def norm68(s):
    s=s.replace('—','-').replace('–','-').replace('4-','+').replace('-{-','+').replace('-|-','+')
    if re.search(r'\bat\b',s): return 0.0
    m=re.search(r'([+-])\s*(\d{1,2})\s*(½|5\b)?',s)
    if not m: return None
    v=int(m.group(2))
    return (1 if m.group(1)=='+' else -1)*v
T68=defaultdict(dict)
for r in csv.DictReader(open('/home/claude.guest/lab/barr/truth68.csv')): T68[r['month']][int(r['day'])]=r
T70=defaultdict(dict)
for r in csv.DictReader(open('/home/claude.guest/lab/barr/truth.csv')): T70[r['month']][int(r['day'])]=r
out=[]
# PT68: rows in order; match to OLM by sequence of rows having any number
for mon in ['1776-12','1777-01','1777-02','1777-03']:
    rows=[r for r in P[mon] if norm68(r['m']) is not None or norm68(r['e']) is not None]
    days=sorted(T68[mon]); n=0; bad=0
    # greedy alignment: walk both
    i=0
    for d in days:
        t=T68[mon][d]; tm=float(t['morning']) if t['morning'] else None; te=float(t['evening']) if t['evening'] else None
        # find best row among next 3
        best=None
        for j in range(i,min(i+3,len(rows))):
            a,b=norm68(rows[j]['m']),norm68(rows[j]['e'])
            sc=(a is not None and tm is not None and abs(a-tm)<1)+(b is not None and te is not None and abs(b-te)<1)
            if best is None or sc>best[0]: best=(sc,j,a,b)
        if best and best[0]==2: i=best[1]+1; continue
        bad+=1; out.append(('PT68',mon,d,t['raw_m'],t['raw_e'],rows[best[1]]['m'] if best else '',rows[best[1]]['e'] if best else ''))
        if best and best[0]==1: i=best[1]+1
    print('PT68',mon,len(days),'rows',len(rows),'not both-agree',bad)
for mon in ['1778-12','1779-01','1779-02','1779-03','1779-04']:
    txt=[(r['day']+' '+r['m']+' '+r['e']) for r in P[mon]]
    flat=[re.sub(r'[^0-9ab]','',t.replace('O','0').replace('o','0').replace('°','0')) for t in txt]
    bad=0; i=0
    for d in sorted(T70[mon]):
        t=T70[mon][d]
        def tok(v):
            if v=='' : return r'\d{0,2}[ab]?0?'
            v=int(v); return str(abs(v))+('b' if v<0 else 'a')
        pat=re.compile(tok(t['morning'])+r'0?'+r'.{0,2}?'+tok(t['evening']))
        hit=None
        for j in range(max(0,i-1),min(i+3,len(flat))):
            if pat.search(flat[j]): hit=j; break
        if hit is not None: i=hit+1; continue
        bad+=1; out.append(('PT70',mon,d,t['morning'],t['evening'],txt[i] if i<len(txt) else ''))
    print('PT70',mon,len(T70[mon]),'not confirmed',bad)
for o in out: print(o)
