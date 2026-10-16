# parse Barr PT 70 print (pt/106379.md) into truth.csv: month,day,morning,evening (F; b = below 0 -> negative)
import re,csv,sys
L=open(sys.argv[1]).read().split('\n')
starts={'1778-12':26,'1779-01':64,'1779-02':106,'1779-03':139,'1779-04':179}
order=sorted(starts.items(),key=lambda x:x[1])
def val(s):
    s=s.strip()
    m=re.match(r'^(\d+)\s*([ab])?',s)
    if not m: return ''
    v=int(m.group(1)); return -v if m.group(2)=='b' else v
out=[]
for i,(mon,st) in enumerate(order):
    end=order[i+1][1] if i+1<len(order) else len(L)+1
    for line in L[st-1:end-1]:
        c=[x.strip() for x in line.split('|')]
        if len(c)<4: continue
        d=re.sub(r'[^0-9]','',c[1])
        if not d: continue
        out.append((mon,int(d),val(c[2]),val(c[3])))
w=csv.writer(open('truth.csv','w')); w.writerow(['month','day','morning','evening']); w.writerows(out)
from collections import Counter
print(Counter(o[0] for o in out)); print(out[:3], out[-3:])
