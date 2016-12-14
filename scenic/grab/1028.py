#!/usr/bin/python

class Birth:
    def __init__(self,name,date):
        self.name = name
        self.date = date

num = input()
ldate = 1814 * 10000 + 9 * 100 + 6
cdate = 2014 * 10000 + 9 * 100 + 6
li = []
for i in range(0,num):
    line = raw_input()
    sp = line.split(" ")
    date = sp[1].split("/")
    year = int(date[0])
    mon  = int(date[1])
    day = int(date[2])
    idate = year * 10000 + mon * 100 + day
    if idate >= ldate and idate <= cdate:
        bir = Birth(sp[0],idate)
        li.append(bir)
max = li[0]
min = li[0]
for i in range(1,len(li)):
    if li[i].date > max.date:
        max = li[i]
    if li[i].date < min.date:
        min = li[i]
print len(li),min.name,max.name
    
