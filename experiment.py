a=int(input('a:'))
b=int(input('b:'))
import math
def format_significant_figures(x, n):
    if x == 0:
        return "0"
    else:
        return f"{x:.{n - int(math.floor(math.log10(abs(x)))) - 1}f}"

while 1:
    v2=int(input('v2:'))
    r=int(input('r:'))
    v_mid=(12*math.log(r/b))/math.log(a/b)
    v=format_significant_figures(v_mid,2)
    print(v)
    print('\n')
    w=(v2-v)/v
    print(w)
    print('\n')


