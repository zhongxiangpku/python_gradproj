import os

print os.getcwd()

mymap = {}
s= []
s.append(1)
s.append(2)
mymap['url'] = s
mymap['url'].append(3)
if 'url' in mymap.keys():
    print mymap['url']
print mymap

lst = [1,2,3,4,5]
for i in range(0,len(lst)):
    for j in range(i+1,len(lst)):
        print lst[i], lst[j]