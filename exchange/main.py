import copy
s1 = [
    's1',
    [1, ['M2', 'n'], ['M1', 'n']],
    ['-1*q^2', ['M1', 'n'], ['M2', 'n']],
    [0, 0, 0]
]
s7 = [
    's7',
    [1, ['M1', 'n'], ['M1', 'm']],
    ['-1*v^2{(-1)^{n-m}}', ['M1', 'm'], ['M1', 'n']],
    [0, 0, 0]
]
s23 = [
    's23',
    [1,['M1','n'],['M1','n+1']],
    ['-1*v^{-2}',['M1','n+1'],['M1','n']],
    ['-1*/frac{1}{v^2-1}','','']
]

# #生成合成多项式函数
def CombinationItem(item1, item2):
    global circulateTime
    circulateTime = 0
    global ConbinePoly
    ConbinePoly = []
    if item1[1][2] == item2[1][1]:
        omega = [item1[1][1], item1[1][2], item2[1][2]]   # 计算Omega并将其展示
        print("Omega =", omega)
    else:
        return ("There's no conbination.")
    if not type(item2[2][0]) == int:
        item2[2][0] = item2[2][0] + '*' + '-1'
    else:
        item2[2][0] = item2[2][0]*(-1)
    if not type(item2[3][0]) == int:
        item2[3][0] = item2[3][0] + '*' + '-1'
    else:
        item2[3][0] = item2[3][0] * (-1)
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
        circulateTime = circulateTime + 1
    print('=',ConbinePoly)



#判断是否完全展开函数
def ExpansionPoly(Poly, exfu=None):
    global ConbinePoly
    # 删除空元素
    removeEmpty()
    # 遍历Poly内每一项 （即 AM1nM2nM3n+"bM2mM2nM3n")
    for i in range(len(Poly)-1):
        if type(Poly[i][0]) != str:
            Poly[i].insert(0, '1')
        for j in range(len(Poly[i])-2):
            # 如果只有一项就跳过该次循环(判断会溢出)
            if len(Poly) <= 2:
                continue
            # 判断相邻项目
            if not JudgeOrder(Poly[i][j+1], Poly[i][j+2]):
                # exfu:字典查找出的交换后的式 [M1n,M2n] = [M2n,M1n,a1,...,an]
                exfu = FindExchange(Poly[i][j+1],Poly[i][j+2])
                print('------ex------',Poly[i][j+1],Poly[i][j+2])
                # 对系数进行处理 删除第i项之后 将exfu逐项组合后插入末尾
                del ConbinePoly[i]
                for entr_y in exfu:
                    s = insertList(Poly[i], entr_y, j)
                    ConbinePoly.append(s)
                print('=',ConbinePoly)
                return False
    return True

# 寻找交换函数
def FindExchange(elef1,elef2,fe1 = None, fe2 = None):
    fe1 = elef1.copy()
    fe2 = elef2.copy()
    ExDict = {
        'M2nM1n': [
            ['q^2',['M1','n'],['M2','n']]
        ],
        'M3nM1n': [
            ['q',['M1','n'],['M3','n']],
            ['q+1',['M2','n']]
        ],
        'M4nM1n': [
            ['1',['M1','n'],['M4','n']],
            ['1',['M3','n']]
        ],
        'M3nM2n': [
            ['q^2',['M2','n'],['M3','n']]
        ],
        'M4nM2n': [
            ['q^2',['M2','n'],['M4','n']],
            ['/frac{q-1}{q^{-1}+1}',['M3','n'],['M3','n']]
        ],
        'M4nM3n': [
            ['q^2',['M3','n'],['M4','n']]
        ],


        'M1nM1m': [
            ['v^2{(-1)^{n-m}}', ['M1', 'm'], ['M1', 'n']]
        ],
        'M2nM1m': [
            ['v^2{(-1)^{n-m}}', ['M1', 'm'], ['M2', 'n']]
        ],
        'M3nM1m': [
            ['1', ['M1', 'm'], ['M3', 'n']]
        ],
        'M4nM1m': [
            ['v^2{(-1)^{n-m+1}}', ['M1', 'm'], ['M4', 'n']]
        ],
        'M1nM2m': [
            ['v^2{(-1)^{n-m}}', ['M2', 'm'], ['M1', 'n']]
        ],
        'M2nM2m': [
            ['v^4{(-1)^{n-m}}', ['M2', 'm'], ['M2', 'n']]
        ],
        'M3nM2m': [
            ['v^2{(-1)^{n-m}}', ['M2', 'm'], ['M3', 'n']]
        ],
        'M4nM2m': [
            ['1', ['M2', 'm'], ['M4', 'n']]
        ],
        'M1nM3m': [
            ['1', ['M3', 'm'], ['M1', 'n']]
        ],
        'M2nM3m': [
            ['v^2{(-1)^{n-m}}', ['M3', 'm'], ['M2', 'n']]
        ],
        'M3nM3m': [
            ['v^2{(-1)^{n-m}}', ['M3', 'm'], ['M3', 'n']]
        ],
        'M4nM3m': [
            ['v^2{(-1)^{n-m}}', ['M3', 'm'], ['M4', 'n']]
        ],
        'M1nM4m': [
            ['v^2{(-1)^{n-m+1}}', ['M4', 'm'], ['M1', 'n']]
        ],
        'M2nM4m': [
            ['1', ['M4', 'm'], ['M2', 'n']]
        ],
        'M3nM4m': [
            ['v^2{(-1)^{n-m+1}}', ['M4', 'm'], ['M3', 'n']]
        ],
        'M4nM4m': [
            ['v^4{(-1)^{n-m}}', ['M4', 'm'], ['M4', 'n']]
        ],



        'M1nM1n+1': [
            ['v^{-2}', ['M1', 'n+1'], ['M1', 'n']],
            ['/frac{1}{v^2-1}']
        ],
        'M2nM1n+1': [
            ['v^{-4}', ['M1', 'n+1'], ['M2', 'n']],
            ['v^{-2}',['M3','n']]
        ],
        'M3nM1n+1': [
            ['v^{-1}', ['M1', 'n+1'], ['M3', 'n']],
            ['v^{-1}(v^2+1)',['M3','n']]
        ],
        'M4nM1n+1': [
            ['v^{2}', ['M1', 'n+1'], ['M4', 'n']],
        ],
        'M1nM2n+1': [
            ['1', ['M2', 'n+1'], ['M1', 'n']]
        ],
        'M2nM2n+1': [
            ['v^{-4}', ['M2', 'n+1'], ['M2', 'n']],
            ['/frac{1}{v^4-1}']
        ],
        'M3nM2n+1': [
            ['v^{-2}', ['M2', 'n+1'], ['M3', 'n']],
            ['v^{-2}',['M1','n+1']]
        ],
        'M4nM2n+1': [
            ['1', ['M2', 'n+1'], ['M4', 'n']],
            ['/frac{v^2-1}{v^2+1}',['M1','n+1'],['M1','n+1']]
        ],
        'M1nM3n+1': [
            ['v^{2}', ['M3', 'n+1'], ['M1', 'n']]
        ],
        'M2nM3n+1': [
            ['1', ['M3', 'n+1'], ['M2', 'n']]
        ],
        'M3nM3n+1': [
            ['v^{-2}', ['M3', 'n+1'], ['M3', 'n']],
            ['/frac{1}{v^2-1}']
        ],
        'M4nM3n+1': [
            ['v^{-2}', ['M3', 'n+1'], ['M4', 'n']],
            ['v^{-2}', ['M1', 'n+1']]
        ],
        'M1nM4n+1': [
            ['v^{4}', ['M4', 'n+1'], ['M1', 'n']]
        ],
        'M2nM4n+1': [
            ['v^{4}', ['M4', 'n+1'], ['M2', 'n']]
        ],
        'M3nM4n+1': [
            ['1', ['M4', 'n+1'], ['M3', 'n']]
        ],
        'M4nM4n+1': [
            ['v^{-4}', ['M4', 'n+1'], ['M4', 'n']],
            ['/frac{1}{v^4-1}']
        ],




        'M1nM1n': ['1', ['M1', 'n'], ['M1', 'n']],
        'M2nM2n': ['1', ['M2', 'n'], ['M2', 'n']],
        'M3nM3n': ['1', ['M3', 'n'], ['M3', 'n']],
        'M4nM4n': ['1', ['M4', 'n'], ['M4', 'n']],
        'M1mM1m': ['1', ['M1', 'm'], ['M1', 'm']],
        'M2mM2m': ['1', ['M2', 'm'], ['M2', 'm']],
        'M3mM3m': ['1', ['M3', 'm'], ['M3', 'm']],
        'M4mM4m': ['1', ['M4', 'm'], ['M4', 'm']],
        'M1n+1M1n+1': ['1', ['M1', 'n+1'], ['M1', 'n+1']],
        'M2n+1M2n+1': ['1', ['M2', 'n+1'], ['M2', 'n+1']],
        'M3n+1M3n+1': ['1', ['M3', 'n+1'], ['M3', 'n+1']],
        'M4n+1M4n+1': ['1', ['M4', 'n+1'], ['M4', 'n+1']],






    }

    return ExDict.get(fe1[0]+fe1[1]+fe2[0]+fe2[1])
# 判断序关系函数(参数1是否大于参数2)
def JudgeOrder(jr1,jr2):

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

    jr10 = judgerule[jr1[0]]
    jr11 = judgerule[jr1[1]]
    jr20 = judgerule[jr2[0]]
    jr21 = judgerule[jr2[1]]

    #将ele内元素转为int型
    map(lambda x: int(x), jr1)
    map(lambda x: int(x), jr2)
    #print('jr1/jr2=',jr1,jr2)
    #比较ele1和ele2大小
    if jr10+jr11 <= jr20+jr21:
        del jr10
        del jr11
        del jr20
        del jr21
        return True
    else:
        del jr10
        del jr11
        del jr20
        del jr21
        return False


def insertList(List_, entry_, j):
    List = copy.deepcopy(List_)
    if type(List[0]) != str:
        List.insert(0,'1')
    entry = copy.deepcopy(entry_)
    List[0] = List[0] + '*' + entry[0]
    del entry[0]

    del List[j]
    del List[j]
    # 倒序保证插入顺序正确
    entry.reverse()
    for m in range(len(entry)):
        List.insert(j, entry[m])
    return List

def removeEmpty():
    global ConbinePoly
    for empt in ConbinePoly:
        while '' in empt:
            empt.remove('')
def toLatex():
    return 0

CombinationItem(s1,s7)
#CombinationItem(s1,s23)

