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
                    htmlline="<option value=\""
                    htmlline+=countrycode
                    htmlline+="\">"+countryname+"</option>"
                    wantedlist.append([htmlline,countryname])
                    break
    return wantedlist


countrycodes=f()
countrycodes.sort(key= lambda x: x[1])


countrycodes.append([])
countrycodes.append([])

for i in range(len(countrycodes)-1,1,-1):
    countrycodes[i]=countrycodes[i-2]

countrycodes[0]=["<option value=\"world\">World</option>",0]
countrycodes[1]=["<option value=\"without China\">World without China</option>",0]

# example line <option value="Zimbabwe">Zimbabwe</option>

with open("countrycodes.txt",'w') as f2:
    for i in countrycodes:
        temp=i[0]
        f2.write(temp)
        f2.write("\n")

