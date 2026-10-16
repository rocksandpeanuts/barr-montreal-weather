import subprocess,csv,io,re,json,sys
import numpy as np
from PIL import Image
sys.argv=[sys.argv[0]]
exec(open('/home/claude.guest/lab/barr/data/render.py').read().split("mon=sys.argv[1]")[0])
X={'106332':{'snow':(622,735),'wind':(735,845),'rem':(845,1500)},'106379':{'snow':(530,625),'rain':(625,738),'wind':(738,860),'rem':(860,1500)}}
first={'1776-12':14}
out={}
for mon,(doc,pg) in pages.items():
    S=2
    im=Image.open(f'/home/claude.guest/lab/barr/img/{doc}/{doc}_{pg}.png'); im=im.resize((im.size[0]*S,im.size[1]*S)); im.save('/tmp/p.png')
    p=subprocess.run('tesseract /tmp/p.png - --psm 6 tsv',shell=True,capture_output=True,text=True).stdout
    R=[r for r in csv.DictReader(io.StringIO(p),delimiter='\t') if r['text'] and r['text'].strip()]
    k,b=fit(mon)
    for r in R:
        xc=(int(r['left'])+int(r['width'])/2)/S; y=(int(r['top']))/S
        d=int(round((y-b)/k))
        if not (first.get(mon,1)<=d<=nd[mon]): continue
        for col,(a,c) in X[doc].items():
            if a<=xc<c: out.setdefault(f'{mon}-{d:02d}',{}).setdefault(col,[]).append(r['text'])
json.dump(out,open('/home/claude.guest/lab/barr/data/extra.json','w'),indent=0)
for kk in ['1776-12-15','1776-12-20','1778-12-01','1778-12-05','1778-12-08','1779-01-02']: print(kk,out.get(kk))
