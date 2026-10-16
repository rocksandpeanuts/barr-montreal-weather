import json,csv,re
from difflib import SequenceMatcher
exec(open('/home/claude.guest/lab/barr/data/build.py').read().split("WIND=re.compile")[0])
WIND=re.compile(r'^(N|S|E|W|NE|NW|SE|SW|NNE|NNW|ENE|ESE|SSE|SSW|WSW|WNW|Calm\.?|[NSEW] by [NSEW])$')
T={}
for f,src in (('truth68.csv','PT68'),('truth.csv','PT70')):
    for r in csv.DictReader(open('/home/claude.guest/lab/barr/'+f)): T[f"{r['month']}-{int(r['day']):02d}"]=(r,src)
CORR={('1776-12-18','morning'):(29,'print shows +29 (open-bowled 9 with ball terminal); OLMoCR and ABBYY read +20; ~75% confident'),
      ('1777-03-11','evening'):(36,'print shows +36; OLMoCR read +30; ~90% confident')}
NOTE={('1778-12-14','evening'):'printed as a lone "o" with no figure; read as 0',('1779-01-27','morning'):'printed as a lone "o" with no figure; read as 0',
      ('1778-12-07','morning'):'blank in print'}
def clean_t(k): 
    s=' '.join(E.get(k,{}).get('rem',[])); s=re.sub(r'[|{}\[\]\\;]','',s).strip(); return re.sub(r'\s+',' ',s)
def olm_wr(c):
    w=[x for x in c[3:] if WIND.match(x)]; return (w[0] if w else ''), c[-1]
PREV={}
USED=set()
out=[]; stats={'olm0':0,'olmshift':0,'tess':0}
for k in sorted(T):
    r,src=T[k]; mon=k[:7]; d=int(k[-2:])
    tr=clean_t(k).replace('f','s').lower()
    tw=re.sub(r'[^A-Za-z ]','',' '.join(E.get(k,{}).get('wind',[]))).replace('EE','E').strip()
    cands=[]
    for sh in (0,-1,1):
        k2=f'{mon}-{d+sh:02d}'
        if k2 in O:
            w,rem=olm_wr(O[k2]); sc=SequenceMatcher(None,rem.lower(),tr).ratio()+(0.5 if (w and w==tw) else 0)
            cands.append((sc,sh,(w,rem)))
    cands.sort(key=lambda c:-c[0])
    best=cands[0]
    for c in cands:
        if c[1]==PREV.get(mon,0) and c[0]>=best[0]-0.02: best=c; break
    best=(best[0]-(0.5 if best[2][0]==tw and tw else 0),best[1],best[2])
    if best[0]>=0.6:
        PREV[mon]=best[1]
        wind,rem=best[2]; rsrc='OLMoCR' if best[1]==0 else f'OLMoCR row {d+best[1]} (row shift corrected)'
        stats['olm0' if best[1]==0 else 'olmshift']+=1
    else:
        wind,rem=tw,clean_t(k); rsrc='tesseract (raw, long s as f)'; stats['tess']+=1
    wind_olm=wind; rem_olm=rem if rsrc.startswith('OLMoCR') and 'already' not in rsrc else ''
    used=(mon,d+(best[1] or 0)) if rsrc.startswith('OLMoCR') else None
    if used and used in USED: rem=clean_t(k); rsrc='tesseract (raw, long s as f); OLMoCR row already used'
    elif used: USED.add(used)
    if not wind or not WIND.match(wind):
        wind2=tw if WIND.match(tw) else ''
        wind=wind2; 
    snow=' '.join(E.get(k,{}).get('snow',[])); snow=re.sub(r'[|{}()\[\]:;_.©—-]','',snow).replace('falittle','a little').replace('alittle','a little').replace('fome','some').strip()
    rain='Rain' if 'Rain' in ' '.join(E.get(k,{}).get('rain',[])) else ''
    row={'date':k,'source':'Phil. Trans. 68 (1778) 559-563, doi:10.1098/rstl.1778.0022' if src=='PT68' else 'Phil. Trans. 70 (1780) 272-277, doi:10.1098/rstl.1780.0015'}
    notes=[]
    for slot in ('morning','evening'):
        v=r[slot]; v=float(v) if v!='' else None
        if (k,slot) in CORR: v,n=CORR[(k,slot)]; notes.append(f'{slot}: {n}')
        if (k,slot) in NOTE: notes.append(f'{slot}: {NOTE[(k,slot)]}')
        row[f'{slot}_F']='' if v is None else (int(v) if float(v).is_integer() else v)
        row[f'{slot}_C']='' if v is None else round((float(v)-32)*5/9,1)
    row['snow_inches_or_word']=snow if re.search(r'\d|little|some|ditto',snow) else ''
    tw2=tw if WIND.match(tw) else ''
    rt=clean_t(k)
    agree_w = (wind_olm==tw2 and tw2!='')
    agree_r = rem_olm!='' and SequenceMatcher(None,rem_olm.lower(),rt.replace('f','s').lower()).ratio()>=0.8
    row['rain']=rain
    row['wind_olmocr']=wind_olm if WIND.match(wind_olm or '') else ''
    row['wind_tesseract']=tw2
    row['remarks_olmocr']=rem_olm
    row['remarks_tesseract']=rt
    row['wind_remarks_check']='both agree' if (agree_w and agree_r) else ('wind agrees' if agree_w else ('remarks agree' if agree_r else 'disputed'))
    row['notes']='; '.join(notes)
    out.append(row)
w=csv.DictWriter(open('/home/claude.guest/lab/barr/data/barr_montreal_daily.csv','w'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out),stats)
for r in out[:3]+out[150:156]: print(r)
