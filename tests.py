import pandas
import csv


f = open('tests_per_country(until 22-4).csv')
csv_f = csv.reader(f)

list = []
country = []
code = []
date = []
tests = []

for row in csv_f:
    #print(row)
    for i in row:
        i = i.split(',')
        list.append(i)

s = ','
for x in list[4:]:
    date.append(s.join([x[2], x[3]]))
    country.append(x[0])
    code.append(x[1])
    tests.append(x[4])

#print(list)
#print(country)
#print(code)
#print(date)
#print(tests)

dictionary = {list[2][0]: date, "Country": country, list[1][0]: code, list[3][0]: tests}
#print(dictionary)

organized_data = pandas.DataFrame(data = dictionary)
#organized_data.rename(columns = {"Entity": "Country"})
print(organized_data)
