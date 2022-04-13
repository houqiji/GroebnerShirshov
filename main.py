import copy
s1 = [
    's1',
    [1, ['M2', 'n'], ['M1', 'n']],
    ['-q^2', ['M1', 'n'], ['M2', 'n']],
    [0, 0, 0]
    ]
s7 = [
    's7',
    [1, ['M1', 'n'], ['M1', 'm']],
    ['-v2(-1)n-m', ['M1', 'm'], ['M1', 'n']],
    [0, 0, 0]
    ]


# #生成合成多项式函数
def CombinationItem(item1, item2):
    global ConbinePoly
    if item1[1][2] == item2[1][1]:
        omega = [item1[1][1], item1[1][2], item2[1][1]]   # 计算Omega并将其展示
        print("Omega =", omega)
    else:
        return ("There's no conbination.")

    # 将item1 和 item2 乘以合成为一个多项式并将其传入展开函数

    ConbinePoly = [
                [item1[2][0],item1[2][1],item1[2][2],item2[1][2]],
                [item1[3][0],item1[3][1],item1[3][2],item2[1][2]],
                [item2[2][0],item1[1][1],item2[2][1],item2[2][2]],
                [item2[3][0],item1[1][1],item2[3][1],item2[3][2]]
                ]

    #去除空白项
    if ConbinePoly[1][0] == 0:
        del(ConbinePoly[1])
    if ConbinePoly[2][0] == 0:
        del (ConbinePoly[2])

    print("ConbinePoly=",ConbinePoly)
    eon = ExpansionPoly(ConbinePoly)
    while not eon:
        eon = ExpansionPoly(ConbinePoly)
    print('ConbinePoly=',ConbinePoly)



'''代码效率太低电脑跑不出来的方法
##合成展开
#合成展开函数(将[[B,A,C,D,E]+[a1,B,C,D,E]+...[an,B,C,D,E]]加入ConbinePoly)
def expansionPoly(ConbinePoly):
    i = 0
    while i <= len(ConbinePoly)-1:
        afterExpasion = expansionPolyn(ConbinePoly[i])
        for j in range(len(afterExpasion)):
            ConbinePoly.insert(afterExpasion[i])
        return (expansionPoly(ConbinePoly))


#合成展开函数分组处理函数 (将[[B,A,a1,...,an],C,D,E]->[[B,A,C,D,E]+[a1,C,D,E]+...[an,C,D,E]])
def expansionPolyn(ConbinePolyn):
    i = 1
    while i <= len(ConbinePolyn)-1:
        if JudgeOrder(ConbinePolyn[i],ConbinePolyn[i+1]):
            del ConbinePolyn[i]
            afterExchange = ExchangeEle(ConbinePolyn[i],ConbinePolyn[i+1])
            returnex = list(map(lambda x:ConbinePolyn.insert(i,x),afterExchange))
            return returnex
    return ConbinePolyn
#交换元素函数（返回n个项在expansionpoly内处理 [A,B]->[A,B,a1,...,an])
def ExchangeEle(ele1,ele2):
    return 0'''



#判断是否完全展开函数
def ExpansionPoly(Poly):
    global ConbinePoly
    for i in range(len(Poly)):
        for j in range(len(Poly[i])-2):
            if not JudgeOrder(Poly[i][j+1], Poly[i][j+2]):
                exfu = FindExchange(Poly[i][j+1],Poly[i][j+2])
                Poly = copy.deepcopy(Poly)

                for k in range(len(exfu)):
                    Poly[i][0] = Poly[i][0] + '*' + exfu[k][0]
                    del exfu[k][0]
                del Poly[i][j+1]
                del Poly[i][j+1]

                for l in range(len(exfu)):
                    exfu[l].reverse()
                    for m in range(len(exfu[l])):
                        Poly[i].insert(j+1, exfu[l][m])
                ConbinePoly = []
                for n in range(len(Poly)):
                    ConbinePoly.append(Poly[n])
                return False
    return True

# 寻找交换函数
def FindExchange(elef1,elef2):
    fe1 = elef1.copy()
    fe2 = elef2.copy()
    ExDict = {
        'M2nM1n':[['q^2',['M1','n'],['M2','n']]],
        'M1nM1m':[['v2(-1)n-m',['M1','m'],['M1','n']]],
        'M2nM1m': [['v2(-1)n-m', ['M1', 'm'], ['M2', 'n']]],
    }
    #print('plus=',fe1[0]+fe1[1]+fe2[0]+fe2[1])
    #print(ExDict.get(fe1[0]+fe1[1]+fe2[0]+fe2[1]))
    return ExDict.get(fe1[0]+fe1[1]+fe2[0]+fe2[1])
# 判断序关系函数(参数1是否大于参数2)
def JudgeOrder(ele1,ele2):

    """   给ele1 与ele2 赋权重便于比较 权重规则如下
       K-1/1 -> 1    M1   -> 10    n+1   -> 100
       K-1/2 -> 2    M2   -> 20    n     -> 200
       K/1   -> 3    M3   -> 30    m     -> 300
       K/2   -> 4    M4   -> 40  """

    judgerule = {"K-1/1": '1', 'K-1/2': '2', 'K/1': '3', 'K/2': '4',
            'M1': '10', 'M2': '20', 'M3': '30', 'M4': '40',
            'n+1': '100', 'n': '200', 'm': '300'
            }
    #做replace方法字典替换
    jr1 = ele1.copy()
    jr2 = ele2.copy()
    for i in judgerule.keys():
        jr1[0].replace(i, judgerule[i])
        jr1[1].replace(i, judgerule[i])
        jr2[0].replace(i, judgerule[i])
        jr2[1].replace(i, judgerule[i])

    #将ele内元素转为int型
    map(lambda x: int(x), jr1)
    map(lambda x: int(x), jr2)
    #print('jr1/jr2=',jr1,jr2)
    #比较ele1和ele2大小
    if jr1[0]+jr1[1] < jr2[0]+jr2[1]:
        return True
    else:
        return False



CombinationItem(s1,s7)

