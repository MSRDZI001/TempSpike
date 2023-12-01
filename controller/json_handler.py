#Program to assist in getting somewhat resonable data from tempspike

import json
# Opening JSON file

with open('data.txt') as f:
    data = f.read()
    tmp = data.split('\n')
f.close()

if(tmp[0] != '{"data":'):
    f = open('data.txt','w')
    
    iter = 0
    for line in tmp:
        if("epoch" in line):
            iter+=1
        if iter != 1:    
            f.write(line.replace('"epoch', ',"epoc' ))
    
    f.write('{"data":\n{' + data + '}\n}')
    f.close() 
    
f = open('data.txt','r')

data = json.load(f)

for i in data:
    print[i]