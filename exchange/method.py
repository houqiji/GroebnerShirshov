import copy
import os
import yaml

global CombinePoly
global circulateTime

# 从yaml中导入预设
fd = open(os.getcwd() + r'\exchange\rule\ExDict.yaml')
fj = open(os.getcwd() + r'\exchange\rule\judge_rule.yaml')
fc = open(os.getcwd() + r'\exchange\rule\config.yaml')
ExDict = yaml.safe_load(fd)
judge_rule = yaml.safe_load(fj)
y = yaml.safe_load_all(fc)
for data in y:
    exec(data[0] + '=' + str(data))


# #生成合成多项式函数
def combination_item(item1o, item2o):
    item1 = copy.deepcopy(item1o)
    item2 = copy.deepcopy(item2o)
    circulate_time = 0
    global CombinePoly
    CombinePoly = None
    if item1[1][2] == item2[1][1]:
        print(item1[0] + '与' + item2[0] + '的交叉合成')
        omega = [item1[1][1], item1[1][2], item2[1][2]]  # 计算Omega并将其展示
        omega_l = to_latex([omega])
        print("$$\omega =", omega_l, '\n')
    else:
        # print(item1[0] + '和' + item2[0] + '之间没有合成')
        return 0
    if not type(item2[2][0]) == int and item2[2][0] != '':
        item2[2][0] = item2[2][0] + '*' + '-1'
    if not type(item2[3][0]) == int and item2[3][0] != '':
        item2[3][0] = item2[3][0] + '*' + '-1'
    # 将item1 和 item2 乘以合成为一个多项式并将其传入展开函数
    CombinePoly = [
        [item1[2][0], item1[2][1], item1[2][2], item2[1][2]],
        [item1[3][0], item1[3][1], item1[3][2], item2[1][2]],
        [item2[2][0], item1[1][1], item2[2][1], item2[2][2]],
        [item2[3][0], item1[1][1], item2[3][1], item2[3][2]]
    ]
    # 去除0元素
    if CombinePoly[1][0] == '':
        del (CombinePoly[1])
    if CombinePoly[2][0] == '':
        del (CombinePoly[2])
    remove_empty()
    poly_o = to_latex(CombinePoly)
    print('$$(', item1[0], ',', item2[0], r')_{\omega} \equiv', poly_o, '\n')
    eon = expansion_poly()
    while not eon:
        eon = expansion_poly()
        circulate_time = circulate_time + 1
    poly = to_latex(CombinePoly)
    print(r'$$\equiv', poly)
    return 1


# 判断展开函数
def expansion_poly():
    global CombinePoly
    poly = copy.deepcopy(CombinePoly)
    # 删除空元素
    remove_empty()
    # 遍历Poly内每一项（即 AM1nM2nM3n+"bM2mM2nM3n")
    for i1 in range(len(poly)):
        if type(poly[i1][0]) != str:
            poly[i1].insert(0, '1')
        for j1 in range(len(poly[i1]) - 2):
            # 如果只有一项就跳过该次循环(判断会溢出)
            if len(poly[i1]) <= 2:
                continue
            # 判断相邻项目
            if not judge_order(poly[i1][j1 + 1], poly[i1][j1 + 2]):
                # exfu:字典查找出的交换后的式 [M1n, M2n] = [M2n, M1n, a1, ..., an]
                exfu = find_exchange(poly[i1][j1 + 1], poly[i1][j1 + 2])

                # 输出交换元素
                '''if len(exfu) == 2:
                    print('------ex------', poly[i1][j1 + 1], poly[i1][j1 + 2], '=', exfu[0], '+', exfu[1], '\n')
                elif len(exfu) == 1:
                    print('------ex------', poly[i1][j1 + 1], poly[i1][j1 + 2], '=', exfu[0], '\n')'''

                # 对系数进行处理 删除第i项之后 将exfu逐项组合后插入末尾
                del CombinePoly[i1]
                for entry_y in exfu:
                    s = insert_list(poly[i1], entry_y, j1)
                    CombinePoly.insert(0, s)
                # 输出过程
                poly_i = to_latex(CombinePoly)
                print(r'$$\equiv', poly_i, '\n')

                return False
            else:
                continue
    return True


# 寻找交换函数
def find_exchange(elef1, elef2):
    fe1 = elef1.copy()
    fe2 = elef2.copy()
    return ExDict.get(fe1[0] + fe1[1] + fe2[0] + fe2[1])


# 判断序关系函数(参数1是否大于参数2)
def judge_order(jr1, jr2):
    # 做replace方法字典替换

    jr10 = int(judge_rule[jr1[0]])
    jr11 = int(judge_rule[jr1[1]])
    jr20 = int(judge_rule[jr2[0]])
    jr21 = int(judge_rule[jr2[1]])

    # 比较ele1和ele2大小
    if jr10 + jr11 <= jr20 + jr21:
        del jr10
        del jr11
        del jr20
        del jr21
        return True
    else:
        return False


# 将exfu的项（entry）与多项式拆括号
def insert_list(list_, entry_, j1):
    List = copy.deepcopy(list_)
    if type(List[0]) != str:
        List.insert(0, '1')
    entry = copy.deepcopy(entry_)
    List[0] = List[0] + '*' + entry[0]
    del entry[0]

    del List[j1 + 1]
    del List[j1 + 1]
    # 倒序保证插入顺序正确
    entry.reverse()
    for m in range(len(entry)):
        List.insert(j1 + 1, entry[m])
    return List


# 清除CombinePoly中所有的''元素
def remove_empty():
    global CombinePoly
    for empty in CombinePoly:
        while '' in empty:
            empty.remove('')


def to_latex(Poly):
    poly = copy.deepcopy(Poly)
    for k in range(len(poly)):
        for m in range(len(poly[k])):
            if poly[k][m] == ['M1', 'n']:
                poly[k][m] = 'M_1 [n]'
            elif poly[k][m] == ['M2', 'n']:
                poly[k][m] = 'M_2 [n]'
            elif poly[k][m] == ['M3', 'n']:
                poly[k][m] = 'M_3 [n]'
            elif poly[k][m] == ['M4', 'n']:
                poly[k][m] = 'M_4 [n]'
            elif poly[k][m] == ['M1', 'm']:
                poly[k][m] = 'M_1 [m]'
            elif poly[k][m] == ['M2', 'm']:
                poly[k][m] = 'M_2 [m]'
            elif poly[k][m] == ['M3', 'm']:
                poly[k][m] = 'M_3 [m]'
            elif poly[k][m] == ['M4', 'm']:
                poly[k][m] = 'M_4 [m]'
            elif poly[k][m] == ['M1', 'n+1']:
                poly[k][m] = 'M_1 [n+1]'
            elif poly[k][m] == ['M2', 'n+1']:
                poly[k][m] = 'M_2 [n+1]'
            elif poly[k][m] == ['M3', 'n+1']:
                poly[k][m] = 'M_3 [n+1]'
            elif poly[k][m] == ['M4', 'n+1']:
                poly[k][m] = 'M_4 [n+1]'
            elif poly[k][m] == ['K_1', 'n']:
                poly[k][m] = 'K_1'
            elif poly[k][m] == ['K_2', 'n']:
                poly[k][m] = 'K_2'
        poly[k] = ' '.join('%s' % a_temp for a_temp in poly[k])
    poly = ' + '.join('%s' % a_temp for a_temp in poly)
    # poly = poly.replace('*', ' ')
    return poly + '$$'


def start_combine():
    # s_set = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22,
    # s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38]
    s1_set = [s1, s2, s3, s4, s5, s6]
    s2_set = [s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22]
    s3_set = [t1, t2, t3, t4, t5, t6, t7, t8]
    s4_set = [s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38]

    s1_s1 = 0
    s1_s2 = 0
    s1_s3 = 0
    s1_s4 = 0

    # s1与自身的合成
    for i in range(len(s1_set)):
        for j in range(len(s1_set)):
            a = combination_item(s1_set[i], s1_set[j])
            if a != 0:
                print(to_latex(s1_set[i]), to_latex(s1_set[j]))
                s1_s1 += 1
    print('\n', '------------------------------------------------------------------', s1_s1,
          '------------------------------------------------------------------', '\n')

    # s1与s2的合成
    for i in range(len(s1_set)):
        for j in range(len(s2_set)):
            a = combination_item(s1_set[i], s2_set[j])
            if a != 0:
                print(to_latex(s1_set[i]), to_latex(s2_set[j]))
                s1_s2 += 1
            a = combination_item(s2_set[j], s1_set[i])
            if a != 0:
                print(to_latex(s2_set[j]), to_latex(s1_set[i]))
                s1_s2 += 1
    print('\n', '------------------------------------------------------------------', s1_s2,
          '------------------------------------------------------------------', '\n')

    # s1与s3的合成
    for i in range(len(s1_set)):
        for j in range(len(s3_set)):
            a = combination_item(s1_set[i], s3_set[j])
            if a != 0:
                print(to_latex(s1_set[i]), to_latex(s3_set[j]))
                s1_s3 += 1
    print('\n', '------------------------------------------------------------------', s1_s3,
          '------------------------------------------------------------------', '\n')

    # s1与s4的合成
    for i in range(len(s1_set)):
        for j in range(len(s4_set)):
            a = combination_item(s1_set[i], s4_set[j])
            if a != 0:
                print(to_latex(s1_set[i]), to_latex(s4_set[j]))
                s1_s4 += 1
            a = combination_item(s4_set[j], s1_set[i])
            if a != 0:
                print(to_latex(s4_set[j]), to_latex(s1_set[i]))
                s1_s4 += 1
    print('\n', '------------------------------------------------------------------', s1_s4,
          '------------------------------------------------------------------', '\n')


start_combine()
