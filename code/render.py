import json,re,sys
import numpy as np
from PIL import Image
P=json.load(open('/home/claude.guest/lab/barr/data/pageread2.json'))
pages={'1776-12':('106332','0002'),'1777-01':('106332','0003'),'1777-02':('106332','0004'),'1777-03':('106332','0005'),
 '1778-12':('106379','0002'),'1779-01':('106379','0003'),'1779-02':('106379','0004'),'1779-03':('106379','0005'),'1779-04':('106379','0006')}
nd={'1776-12':31,'1777-01':31,'1777-02':28,'1777-03':31,'1778-12':31,'1779-01':31,'1779-02':28,'1779-03':31,'1779-04':15}
def fit(mon):
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
    q=pts[best[1]]; return np.polyfit(q[:,0],q[:,1],1)
mon=sys.argv[1]; d=int(sys.argv[2]); x0=int(sys.argv[3]); x1=int(sys.argv[4]); dy=int(sys.argv[5]) if len(sys.argv)>5 else 0
doc,pg=pages[mon]; k,b=fit(mon); y=int(k*d+b)+dy
im=np.array(Image.open(f'/home/claude.guest/lab/barr/img/{doc}/{doc}_{pg}.png').convert('L'),float)
reg=im[y-8:y+36,x0:x1]
print(mon,d,'y',y)
for r in range(0,reg.shape[0],2):
    print(''.join('#' if reg[r:r+2,c:c+2]. mean()<110 else ('+' if reg[r:r+2,c:c+2].mean()<170 else ' ') for c in range(0,reg.shape[1],2)))
