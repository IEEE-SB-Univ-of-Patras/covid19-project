from itertools import *
ctrsdictionary=dict()
def f():
    lines=[]
    with open("htmlcode.txt", encoding="utf8") as f:
        lines=f.readlines()
    wantedlist=[]
    for i in lines:
        if "country/" in i:
            
            for x in range(len(i)-9):
                if str(i[x:x+8])=="country/":
                    countrycode=""
                    for y in range(x+8,1000):
                        if i[y]=="/":break
                        countrycode+=i[y]
                    if countrycode in ctrsdictionary : break
                    y+=3
                    countryname=""
                    for j in range(y,1000):
                        if i[j]=="<":break
                        countryname+=i[j]
                    ctrsdictionary[countrycode]=countryname
                    wantedlist.append([countryname,countrycode])
                    break
    return wantedlist


countrycodes=sorted(f())


with open("countrycodes.txt",'w') as f2:
    for i in countrycodes:
        temp=i[0]+" "+i[1]
        f2.write(temp)
        f2.write("\n")

