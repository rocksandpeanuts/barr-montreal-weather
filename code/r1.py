import sys
sys_argv=sys.argv[:]; sys.argv=[sys.argv[0]]
exec(open('/home/claude.guest/lab/barr/data/render.py').read().split("mon=sys.argv[1]")[0])
mon,d,x0,x1=sys_argv[1],int(sys_argv[2]),int(sys_argv[3]),int(sys_argv[4])
doc,pg=pages[mon]; k,b=fit(mon); y=int(k*d+b)
im=np.array(Image.open(f'/home/claude.guest/lab/barr/img/{doc}/{doc}_{pg}.png').convert('L'),float)
reg=im[y-2:y+30,x0:x1]
print(mon,d,x0,x1)
for r in range(reg.shape[0]):
    print(''.join('#' if v<110 else ('+' if v<170 else '.') for v in reg[r]))
