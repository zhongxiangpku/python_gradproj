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