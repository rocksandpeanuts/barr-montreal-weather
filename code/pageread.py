import subprocess,csv,io,sys,re,json
from PIL import Image
cfg={'106332':{'pages':{'0002':'1776-12','0003':'1777-01','0004':'1777-02','0005':'1777-03'},'day':(150,305),'m':(305,467),'e':(467,625)},
     '106379':{'pages':{'0002':'1778-12','0003':'1779-01','0004':'1779-02','0005':'1779-03','0006':'1779-04'},'day':(150,258),'m':(258,396),'e':(396,537)}}
S=int(sys.argv[1]) if len(sys.argv)>1 else 2
res={}
for doc,c in cfg.items():
    for pg,mon in c['pages'].items():
        im=Image.open(f'/home/claude.guest/lab/barr/img/{doc}/{doc}_{pg}.png')
        im=im.resize((im.size[0]*S,im.size[1]*S)); im.save('/tmp/p.png')
        p=subprocess.run('tesseract /tmp/p.png - --psm 6 tsv',shell=True,capture_output=True,text=True).stdout
        R=[r for r in csv.DictReader(io.StringIO(p),delimiter='\t') if r['text'] and r['text'].strip()]
        L={}
        for r in R:
            L.setdefault((r['block_num'],r['par_num'],r['line_num']),[]).append(r)
        rows=[]
        for k,ws in L.items():
            y=sum(int(w['top']) for w in ws)/len(ws)/S
            if y<560: continue
            row={'y':round(y),'day':[],'m':[],'e':[]}
            for w in ws:
                xc=(int(w['left'])+int(w['width'])/2)/S
                for col in ('day','m','e'):
                    a,b=c[col]
                    if a<=xc<b: row[col].append(w['text'])
            rows.append({k:(' '.join(v) if isinstance(v,list) else v) for k,v in row.items()})
        res[mon]=rows
        print(doc,mon,len(rows))
json.dump(res,open('/home/claude.guest/lab/barr/data/pageread%d.json'%S,'w'),indent=0)
