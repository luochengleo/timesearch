import re
from collections import defaultdict
def sort_by_value(d):
    items = d.items()
    backitems = [[v[1] , v[0]] for v in items]
    backitems.sort(reverse=True)
    return [backitems[i][1] for i in range(0,len(backitems))]
p = re.compile(r'result:(.*?),')
fout = open('stat.csv','w')
for l in open('result.csv'):
    count = defaultdict(lambda:0) 
    for q in p.findall(l):
        count[q.strip()] +=1
        qlist = sort_by_value(count)
    fout.write(','.join([ item +'('+str(count[item])+')' for item in qlist])+'\n')
fout.close()
