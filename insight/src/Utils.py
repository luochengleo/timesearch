#coding=utf8
__author__ = 'luocheng'
from collections import defaultdict
import sqlite3
from numpy import mean
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')
def loadValidUsers():
    u2config = dict()
    for l in open('../data/validusers.txt').readlines():

        u,config = l.strip().split(' ')
        u2config[u] = config
    return u2config.keys(),u2config

def extractConfig():
    config  = defaultdict(lambda:defaultdict(lambda:('','')))
    for l in open('../data/settings.csv').readlines()[1:]:
        _,configid,taskid, sat,temporal,_ = l.strip().split('\t')
        config[configid][taskid] = (sat,temporal)
    return config

def dwelltimeextraction():
    validusers, u2config= loadValidUsers()

    dwelltime = defaultdict(lambda:defaultdict(lambda:[9433658019765,1,9433658019765]))
    cx = sqlite3.connect("../../db.sqlite3")
    cu = cx.cursor()
    cu.execute('select * from anno_log')
    while True:
        logitem  = cu.fetchone()
        if logitem == None:
            break
        studentid = logitem[1]
        taskid = logitem[2]
        action = logitem[3]
        content = logitem[5]
        time=int(content.split('\t')[0].split('=')[1])
        print time
        if studentid in validusers and  action =='BEGIN_SEARCH':
            if time < dwelltime[studentid][taskid][0]:
                dwelltime[studentid][taskid][0] = time
        if studentid in validusers:
            if time < dwelltime[studentid][taskid][2]:
                dwelltime[studentid][taskid][2] = time

        if studentid in validusers and action =='SEARCH_END':
            if  time > dwelltime[studentid][taskid][1]:
                dwelltime[studentid][taskid][1] = time
    fout = open('../data/dwelltime.txt','w')
    print len(validusers)
    for u in dwelltime.keys():
        print u, len(dwelltime[u].keys())
        for t in dwelltime[u].keys():
            fout.write('\t'.join([str(item) for item in [u,t,dwelltime[u][t][0],dwelltime[u][t][1],dwelltime[u][t][1]-dwelltime[u][t][0],dwelltime[u][t][1]-dwelltime[u][t][2]]]))
            fout.write('\n')
    fout.close()


def satisfactionextraction():
    validusers, u2config= loadValidUsers()
    satisfaction = defaultdict(lambda:defaultdict(lambda:-1))
    cx = sqlite3.connect('../../db.sqlite3')
    cu = cx.execute('select * from anno_querysatisfaction')
    while True:
        logsat = cu.fetchone()
        if logsat == None:
            break
        studentid = logsat[1]
        taskid = logsat[2]
        sat = logsat[4]
        if studentid in validusers:
            satisfaction[studentid][taskid]=sat
    fout = open('../data/querysat.txt','w')
    for s in satisfaction.keys():
        for t in satisfaction[s].keys():
            fout.write('\t'.join([str(s),str(t),str(satisfaction[s][t])]))
            fout.write('\n')
    fout.close()

def numofClicksExtraction():
    validusers, u2config= loadValidUsers()
    numofclicks = defaultdict(lambda:defaultdict(lambda:0))
    cx = sqlite3.connect('../../db.sqlite3')
    cu = cx.execute('select * from anno_log')
    while True:
        logitem = cu.fetchone()
        if logitem == None:
            break
        studentid = logitem[1]
        taskid = logitem[2]
        action = logitem[3]
        if action == 'CLICK' and studentid in validusers:
            numofclicks[studentid][taskid]+=1

    fout = open('../data/numofclicks.txt','w')
    for s in numofclicks.keys():
        for t in numofclicks[s].keys():
            fout.write('\t'.join([str(s),str(t),str(numofclicks[s][t])]))
            fout.write('\n')
    fout.close()


def estimateTimeExtraction():
    validusers, u2config= loadValidUsers()
    timeestimation = defaultdict(lambda:defaultdict(lambda:0))
    cx = sqlite3.connect('../../db.sqlite3')
    cu = cx.execute('select * from anno_timeestimation')
    while True:
        logitem = cu.fetchone()
        if logitem == None:
            break
        studentid = logitem[1]
        taskid = logitem[2]
        time = logitem[3]
        segs = time.split('分')
        minute = int(segs[0])
        second = int(segs[1].replace('秒',''))
        print studentid, taskid ,minute,second
        if studentid in validusers:
            timeestimation[studentid][taskid] = 60*minute+second
    fout = open('../data/timeestimation.csv','w')
    for s in timeestimation.keys():
        for t in timeestimation[s].keys():
            fout.write(','.join([str(item) for item in [s,t,timeestimation[s][t]]]))
            fout.write('\n')
    fout.close()




def loadConfig():
    config = defaultdict(lambda:defaultdict(lambda:[]))
    for l in open('../data/settings.csv').readlines()[1:]:
        _,configid,taskid,option,temporal,_ = l.strip().split('\t')
        if option != 'HIDDEN':
            config[configid][taskid] = [option,temporal]
    return config


def analysisDwellTime():
    bysat = defaultdict(lambda:defaultdict(lambda:[]))
    bytemporal = defaultdict(lambda:defaultdict(lambda:[]))
    byjoin = defaultdict(lambda:defaultdict(lambda:[]))
    config = loadConfig()
    validusers, u2config= loadValidUsers()



    for l in open('../data/dwelltime.txt').readlines():
        studentid,taskid,_,_,_,dtime = l.strip().split('\t')
        configid = u2config[studentid]
        cg = (config[configid][taskid][0],config[configid][taskid][1])
        byjoin[taskid][cg].append(int(dtime))

        cg = (config[configid][taskid][1])
        bytemporal[taskid][cg].append(int(dtime))

        cg = (config[configid][taskid][0])
        bysat[taskid][cg].append(int(dtime))

    fout = open('../data/dwelltime/dwelltime_bysat.csv','w')
    fout.write('taskid,SAT,MIDSAT,UNSAT\n')
    for t in bysat.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bysat[t][('SAT')],bysat[t]['MIDSAT'],bysat[t]['UNSAT']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/dwelltime/dwelltime_bytemporal.csv','w')
    fout.write('taskid,HIGH,LOW\n')
    for t in bytemporal.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bytemporal[t][('HIGH')],bytemporal[t]['LOW']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/dwelltime/dwelltime_byjoin.csv','w')

    cfgs = list(byjoin['1'].keys())

    fout.write('taskid')
    for _c in cfgs:
        print _c
        fout.write(','+_c[0]+'+'+_c[1])
    fout.write('\n')
    for t in bytemporal.keys():
        fout.write(t)
        for _c in cfgs:
            fout.write(','+str(mean( byjoin[t][_c])))
        fout.write('\n')
    fout.close()

def analysisSatisfaction():
    bysat = defaultdict(lambda:defaultdict(lambda:[]))
    bytemporal = defaultdict(lambda:defaultdict(lambda:[]))
    byjoin = defaultdict(lambda:defaultdict(lambda:[]))
    config = loadConfig()
    validusers, u2config= loadValidUsers()


    for l in open('../data/querysat.txt').readlines():
        studentid,taskid,satis = l.strip().split('\t')
        configid = u2config[studentid]
        cg = (config[configid][taskid][0],config[configid][taskid][1])
        byjoin[taskid][cg].append(int(satis))

        cg = (config[configid][taskid][1])
        bytemporal[taskid][cg].append(int(satis))

        cg = (config[configid][taskid][0])
        bysat[taskid][cg].append(int(satis))

    fout = open('../data/satisfaction_raw/satisfaction_bysat.csv','w')
    fout.write('taskid,SAT,MIDSAT,UNSAT\n')
    for t in bysat.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bysat[t][('SAT')],bysat[t]['MIDSAT'],bysat[t]['UNSAT']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/satisfaction_raw/satisfaction_bytemporal.csv','w')
    fout.write('taskid,HIGH,LOW\n')
    for t in bytemporal.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bytemporal[t][('HIGH')],bytemporal[t]['LOW']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/satisfaction_raw/satisfaction_byjoin.csv','w')

    cfgs = list(byjoin['1'].keys())

    fout.write('taskid')
    for _c in cfgs:
        print _c
        fout.write(','+_c[0]+'+'+_c[1])
    fout.write('\n')
    for t in bytemporal.keys():
        fout.write(t)
        for _c in cfgs:
            fout.write(','+str(mean( byjoin[t][_c])))
        fout.write('\n')
    fout.close()


def analysisNumOfClicks():
    bysat = defaultdict(lambda:defaultdict(lambda:[]))
    bytemporal = defaultdict(lambda:defaultdict(lambda:[]))
    byjoin = defaultdict(lambda:defaultdict(lambda:[]))
    config = loadConfig()
    validusers, u2config= loadValidUsers()


    for l in open('../data/numofclicks.txt').readlines():
        studentid,taskid,satis = l.strip().split('\t')
        configid = u2config[studentid]
        cg = (config[configid][taskid][0],config[configid][taskid][1])
        byjoin[taskid][cg].append(int(satis))

        cg = (config[configid][taskid][1])
        bytemporal[taskid][cg].append(int(satis))

        cg = (config[configid][taskid][0])
        bysat[taskid][cg].append(int(satis))

    fout = open('../data/numofclicks/numofclicks_bysat.csv','w')
    fout.write('taskid,SAT,MIDSAT,UNSAT\n')
    for t in bysat.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bysat[t][('SAT')],bysat[t]['MIDSAT'],bysat[t]['UNSAT']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/numofclicks/numofclicks_bytemporal.csv','w')
    fout.write('taskid,HIGH,LOW\n')
    for t in bytemporal.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bytemporal[t][('HIGH')],bytemporal[t]['LOW']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/numofclicks/numofclicks_byjoin.csv','w')

    cfgs = list(byjoin['1'].keys())

    fout.write('taskid')
    for _c in cfgs:
        print _c
        fout.write(','+_c[0]+'+'+_c[1])
    fout.write('\n')
    for t in bytemporal.keys():
        fout.write(t)
        for _c in cfgs:
            fout.write(','+str(mean( byjoin[t][_c])))
        fout.write('\n')
    fout.close()



def analysisTimeEstimation():
    bysat = defaultdict(lambda:defaultdict(lambda:[]))

    bytemporal = defaultdict(lambda:defaultdict(lambda:[]))
    byjoin = defaultdict(lambda:defaultdict(lambda:[]))

    estbysat = defaultdict(lambda:defaultdict(lambda:[]))

    estbytemporal = defaultdict(lambda:defaultdict(lambda:[]))
    estbyjoin = defaultdict(lambda:defaultdict(lambda:[]))


    config = loadConfig()
    validusers, u2config= loadValidUsers()


    for l in open('../data/dwelltime.txt').readlines():
        studentid,taskid,_,_,_,dtime = l.strip().split('\t')
        configid = u2config[studentid]
        cg = (config[configid][taskid][0],config[configid][taskid][1])
        byjoin[taskid][cg].append(int(dtime))

        cg = (config[configid][taskid][1])
        bytemporal[taskid][cg].append(int(dtime))

        cg = (config[configid][taskid][0])
        bysat[taskid][cg].append(int(dtime))

    for l in open('../data/timeestimation.csv').readlines():
        studentid, taskid,etime = l.strip().split(',')
        configid = u2config[studentid]
        cg = (config[configid][taskid][0],config[configid][taskid][1])
        estbyjoin[taskid][cg].append(int(etime)*1000)

        cg = (config[configid][taskid][1])
        estbytemporal[taskid][cg].append(int(etime)*1000)

        cg = (config[configid][taskid][0])
        estbysat[taskid][cg].append(int(etime)*1000)


    fout = open('../data/EtimeDtime/Etime_Dtime_bysat.csv','w')
    fout.write('taskid,SAT-Dtime,SAT-Etime,MIDSAT-Dtime,MIDSAT-Etime,UNSAT-Dtime,UNSAT-Etime\n')
    for t in bysat.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bysat[t][('SAT')],estbysat[t][('SAT')],bysat[t]['MIDSAT'],estbysat[t][('MIDSAT')],bysat[t]['UNSAT'],estbysat[t][('UNSAT')]]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/EtimeDtime/Etime_Dtime_bytemporal.csv','w')
    fout.write('taskid,HIGH-Dtime,HIGH-Etime,LOW-Dtime,LOW-Etime\n')
    for t in bytemporal.keys():
        fout.write(t+',')
        fout.write(','.join([str(mean(item)) for item in [bytemporal[t][('HIGH')],estbytemporal[t][('HIGH')],bytemporal[t]['LOW'],estbytemporal[t]['LOW']]]))
        fout.write('\n')
    fout.close()

    fout = open('../data/EtimeDtime/Etime_Dtime_byjoin.csv','w')

    cfgs = list(byjoin['1'].keys())

    fout.write('taskid')
    for _c in cfgs:

        fout.write(','+_c[0]+'+'+_c[1]+'-'+'Dtime')
        fout.write(','+_c[0]+'+'+_c[1]+'-'+'Etime')
    fout.write('\n')
    sum = 0
    for t in bytemporal.keys():
        fout.write(t)
        for _c in cfgs:
            sum +=len(byjoin[t][_c])
            fout.write(','+str(mean( byjoin[t][_c]))+','+str(mean(estbyjoin[t][_c])))
        fout.write('\n')
    print sum
    fout.close()

def checkUserExsitance():
    validusers, u2config= loadValidUsers()

    exsit  = defaultdict(lambda:'no')
    cx = sqlite3.connect("../../db.sqlite3")
    cu = cx.cursor()
    cu.execute('select * from anno_log')
    while True:
        logitem  = cu.fetchone()
        if logitem == None:
            break
        studentid = logitem[1]
        taskid = logitem[2]
        action = logitem[3]
        content = logitem[5]
        exsit[studentid] = 'yes'
    fout = open('../data/validusers2.txt','w')
    for u in validusers:
        fout.write(u+' '+u2config[u]+' '+exsit[u]+'\n')
    fout.close()
'''
dwelltimeextraction()
satisfactionextraction()
numofClicksExtraction()
estimateTimeExtraction()
#
analysisDwellTime()
analysisSatisfaction()
analysisNumOfClicks()
analysisTimeEstimation()
'''
def outcomeExtaction():
    validusers, u2config= loadValidUsers()

    outcome = defaultdict(lambda:defaultdict(lambda:''))
    cx = sqlite3.connect("../../db.sqlite3")
    cu = cx.cursor()
    cu.execute('select * from anno_outcome')
    fout = open('../data/outcome.txt','w')
    while True:
        logitem = cu.fetchone()
        if logitem == None:
            break
        else:
            studentid = logitem[1]
            taskid = logitem[2]
            content= logitem[3]
            if studentid in validusers:
                fout.write('\t'.join([str(item) for item in [studentid,taskid,content]])+'\n')
    fout.close()
def individualHabit():
    validusers, u2config= loadValidUsers()
    estimatime = defaultdict(lambda:defaultdict(lambda:0))
    for l in open('../data/timeestimation.csv'):
        sid,tid,time = l.strip().split(',')
        estimatime[sid][tid] = int(time)*1000
    actualtime = defaultdict(lambda:defaultdict(lambda:0))
    for l in open('../data/dwelltime.txt'):

        sid,tid,_,_,_,time = l.strip().split('\t')
        actualtime[sid][tid] = int(time)
    userhabit = defaultdict(lambda:[0,0])
    for s in validusers:
        for t in estimatime[s].keys():
            print estimatime[s][t] , actualtime[s][t]
            if estimatime[s][t] > actualtime[s][t]:
                userhabit[s][0]+=1
            else:
                userhabit[s][1]+=1
    fout = open('../data/userhabit.csv','w')
    fout.write('user,config,Estimate Time > Actual Time, Actual Time > Estimate Time\n')
    for s in validusers:
        fout.write(','.join([str(item) for item in [s,u2config[s],userhabit[s][0],userhabit[s][1]]]))
        fout.write('\n')

# outcomeExtaction()
# individualHabit()
