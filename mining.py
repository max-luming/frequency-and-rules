import pandas as pd
import math

def createC1(dataSet):  
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:

def loadDataSet():
    clean_data = pd.DataFrame(pd.read_csv("./result.csv"))
    new_data = []
    # 关联规则挖掘数据处理
    for v in range(1, len(clean_data)):
        item = []
        item.append("category_id" + '='+ str(clean_data.loc[v,'category_id']))
        item.append("comments_disabled" + '='+ str(clean_data.loc[v,'comments_disabled']))
        item.append("ratings_disabled" + '='+ str(clean_data.loc[v,'ratings_disabled']))
        item.append("video_error_or_removed" + '='+ str(clean_data.loc[v,'video_error_or_removed']))
        #print(item)
        new_data.append(item)
    print(len(new_data))
    return new_data 

                C1.append([item])

    C1.sort()
    return map(frozenset, C1) 


def scanD(D, ck, minSupport): 

    ssCnt = {}
    # temp_D = list(D)
    numItem = float(len(D))
    temp_ck = list(ck)
    for tid in D:
        for can in temp_ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1

    retList = []
    supportData = {}
    for key in ssCnt:
        if numItem == 0:
            continue
        support = ssCnt[key] / numItem
        if support >= minSupport:
            retList.insert(0, key)
            supportData[key] = support
    return retList, supportData  


def aprioriGen(Lk, k):  
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()  
            if L1 == L2:  
                retList.append(Lk[i] | Lk[j])  
    return retList 


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet) # 
    D = dataSet
    L1, supportData = scanD(D, C1, minSupport) 
    L = [L1]  

    k = 2
    while (len(L[k - 2]) > 0):  
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK) 
        L.append(Lk)  
        k += 1
    return L, supportData  


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    lift = []
    file = open("generate_rules.txt","a",encoding = "utf-8")
    for conseq in H:  
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            file.write(str(freqSet - conseq)+"-->"+str(conseq)+" support:"+str(supportData[freqSet])+" conf:"+str(conf)+'\n')
            brl.append((freqSet - conseq, conseq, supportData[freqSet], conf))  
            prunedH.append(conseq) 
    file.close()
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])  
    if (len(freqSet) > m + 1):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []  # 存储规则
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def lift_eval(rules, suppData): 
    lift = []
    for rule in rules:
        freqSet_conseq = rule[0]
        conseq = rule[1]
        lift_val = float(rule[3]) / float(suppData[rule[1]])
        lift.append([freqSet_conseq,conseq,lift_val])
    return lift
dataSet = loadDataSet()
L, suppData = apriori(dataSet)
print(L)
rules = generateRules(L, suppData, minConf=0.5)
print(rules)
lifts = lift_eval(rules, suppData)
print(lifts)