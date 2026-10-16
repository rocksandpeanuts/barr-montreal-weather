#!/usr/bin/env python3
"""Build the 1777-78 manuscript winter (Royal Society MA/206/8) from the eye readings in ms/."""
import csv, datetime as dt, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS = os.path.join(HERE, 'ms')
FILES = [('eye_nov1777.csv',1777,11),('eye_dec1777.csv',1777,12),('eye_jan1778.csv',1778,1),
         ('eye_feb1778.csv',1778,2),('eye_mar1778.csv',1778,3),('eye_apr1778.csv',1778,4)]
SRC = 'Royal Society MA/206/8 (manuscript, W. Barr), read from the RS IIIF images'
def C(f): return round((f-32)*5/9,1)
rows=[]
for fn,y,m in FILES:
    prev={'weather':'','rain':'','remarks':''}
    for r in csv.DictReader(open(os.path.join(MS,fn))):
        d=dt.date(y,m,int(r['day']))
        w=r['weather'].strip()
        wres = prev['weather'] if w=='do' else w
        prev['weather']=wres
        rain=r.get('rain','').strip()
        rainres = prev['rain'] if rain=='do' else rain
        prev['rain']=rainres
        mo,ev=int(r['morn_7am']),int(r['even_9pm'])
        rows.append({'date':d.isoformat(),'source':SRC,
            'morning_7am_F':mo,'morning_7am_C':C(mo),'evening_9pm_F':ev,'evening_9pm_C':C(ev),
            'snow_inches_or_word':r['snow_in'].strip(),'rain':'Rain' if rainres else '',
            'wind':r['wind'].strip(),'weather':wres,'weather_as_written':w,
            'remarks':r['remarks'].strip(),'notes':r['doubt'].strip()})
cols=list(rows[0])
with open(os.path.join(HERE,'barr_montreal_1777-78_manuscript.csv'),'w',newline='') as f:
    wr=csv.DictWriter(f,cols); wr.writeheader(); wr.writerows(rows)
# SEF: times must be UTC. Barr's hours are local (apparent/mean solar); offset = lon/15 h.
LON=-73.56; OFF=LON*24/360
def sef(slot,hour,label):
    p=os.path.join(HERE,f'Barr_Montreal_MS_ta_{hour:02d}00.tsv')
    with open(p,'w') as f:
        hdr=[('SEF','1.0.0'),('ID','Barr_Montreal_MS'),('Name','Montreal (William Barr, manuscript)'),('Lat','45.50'),('Lon',f'{LON:.2f}'),
             ('Alt','NA'),('Source','Royal Society MA/206/8 (William Barr, Montreal, Nov 1777 - Apr 1778)'),
             ('Link','https://github.com/rocksandpeanuts/barr-montreal-weather'),('Vbl','ta'),('Stat','point'),('Units','C'),
             ('Meta',f'Data policy=public domain source; transcription CC0|obs.time={label} local (stated in MS header); converted to UTC with offset lon/15 = {OFF:.2f} h|orig.units=F|exposure=post in a garden, exposed to NE, no shelter, no wall near (MS footer)')]
        for k,v in hdr: f.write(f'{k}\t{v}\n')
        f.write('Year\tMonth\tDay\tHour\tMinute\tPeriod\tValue\tMeta\n')
        for r in rows:
            d=dt.datetime.fromisoformat(r['date']).replace(hour=hour)
            u=d-dt.timedelta(hours=OFF)
            u=u.replace(second=0,microsecond=0)
            F=r[f'{slot}_F']
            f.write(f"{u.year}\t{u.month}\t{u.day}\t{u.hour}\t{u.minute}\t0\t{r[slot+'_C']}\torig={F}F|orig.time={label}|orig.date={r['date']}\n")
sef('morning_7am',7,'7 am'); sef('evening_9pm',21,'9 pm')
print(len(rows),'days')
