import math

class VRV:

    def __init__(self, A=[], N=0):
        self.schet = 0
        self.schet2 = 0
        self.schet_to_get_line = 0
        self.schet_reqursion = 0
        self.mass = []
        self.N = N
        self.A = A
        self.line = []
        self.ii = 0
        self.CnCn = 0
        self.mass_var = []
        self.Nost = N

    def toVar(self, A):
        max_list_N = [] 
        maxim = []
        for i in A:
            for j in i:
                maxim.append(j)
        max_el = max(maxim)  # наибольший из оставшихся
        Nost = len(maxim)
        if self.schet == 0:
            self.schet += 1
            self.mass.append([Nost, [1 for i in range(Nost)]])
        C = []  # количество элементов в объекте, кроме списка с максимальным элементом
        ENDLIST = []
        for j in A:
            if max_el in j:
                j.remove(max_el)
                max_list_N = len(j)
            elif max_el not in j:
                for o in j:
                    C.append(o)
                ENDLIST.append(j)
        k = Nost - max_list_N - 1
        self.mass.append([k, self.get_line(C, maxim)])
        if k >= 1:
            self.toVar(ENDLIST) 
        return self.mass # получение варианта дерева

    def get_line(self, C, maxim):
        res = []
        max_max = max(maxim)
        for q in reversed(range(1, max_max+1)):
            if (q in C) and (q in maxim):
                res.append(1)
            else:
                if (q in maxim):
                    res.append(0)
        res.pop(0)
        if sum(res) == 0:
            res = []
        return res # получение кода сочетаний

    def wC(self, k_i=0, Nost=0):
        if k_i == 0:
            res = 1
        elif k_i == Nost:
            res = 1
        else:
            res = math.factorial(Nost) / (math.factorial(Nost - k_i) * math.factorial(k_i))
        return res # кол-во сочетаний

    def B(self, j):
        if (j < 2):
            return 1
        else:
            resb = 0
            for g in range(j):
                resb += (self.wC(g, j - 1) * self.B(g))
        if g == j - 1:
            return resb # числа Белла

    def wB(self, k_i, N):
        if k_i == 0:
            return 0
        elif k_i == 1:
            return 1
        else:
            resb = 0
            for g in range(k_i):
                resb += (self.wC(g, N - 1) * self.B(g))
        if g == k_i - 1:
            return int(resb) # кол-во вариантов до выбранной ветки k=...

    def lC(self, ls=[]):
        res = 0
        b = len(ls)
        a = 0
        for i in ls:
            a += i
        for l in ls:
            if a == 0 or a == b:
                break
            elif l == 0:
                res += self.wC(a - 1, b - 1)
                b -= 1
            elif l == 1:
                a -= 1
                b -= 1
        return res # кол-во веток до выбранного сочетания

    def lK(self, i, r, N):
        if self.mass[i][1] != None:
            res = self.lC(self.mass[i][1]) + self.wC(self.mass[i][0], self.mass[i - 1][0] - 1) * self.lB(i, r, N)
        return res # обработка "первого сына"

    def lB(self, i, r , N):
        self.toVar(VRV().UnRank(r, N))
        i += 1
        if self.mass[i][0] == 0:
            return 0
        else:
            res = self.lK(i, r, N) + self.wB(self.mass[i][0], self.mass[i - 1][0])
            return res # обработка "второго сына"

    def Rank(self, A):

        self.toVar(A)
        res = self.lB(0)
        return res # получение ранга

    def to_get_line(self, l1, Cn, i):

        if self.schet_to_get_line == 0:
            self.schet_to_get_line = 1
            self.ii = i
            self.CnCn = Cn
            self.line = []
        if i==Cn or i==0:
            g = 0
            for j in self.line:
                g += j
            if g < self.ii:
                for p in range(self.CnCn - len(self.line)):
                    self.line.append(1)
            else:
                for p in range(self.CnCn - len(self.line)):
                    self.line.append(0)
        else:
            d = self.wC(i-1, Cn-1)
            if d<=l1:
                l1 -= d
                Cn -= 1
                self.line.append(0)
                self.to_get_line(l1, Cn, i)
            else:
                i -= 1
                Cn -= 1
                self.line.append(1)
                self.to_get_line(l1, Cn, i) # получение кода сочетания

    def getVar(self, r, N):

        self.Nost = N
        self.N_C = N
        if N == 0:
            print('Элементов нет')
            return [] 
        if N > 0:
            if self.schet_reqursion == 0:
                self.schet_reqursion += 1
                self.mass.append([N, [1 for i in range(1, N + 1)]])
            i = 0
            while self.wB(i, N) <= r:
                i += 1
            i -= 1
            k_i = i
            r -= self.wB(i, self.Nost)
            self.N_C -= 1  
            self.Nost = k_i
            l1 = r % self.wC(i, self.N_C)
            l2 = r // self.wC(i, self.N_C)
            self.schet_to_get_line = 0
            if l1 >= 0:
                if i != 0:
                    self.to_get_line(l1, self.N_C, i)
                    self.mass.append([k_i, self.line])
            if l2 == 0:
                self.mass.append([int(l2), []])
            else:
                self.getVar(int(l2), k_i)
            N_C = k_i
        return self.mass # получение варианта дерева

    def UnRank(self, r, N):
        self.A = []
        aa = []
        self.getVar(r, N)
        maxim = []
        iter = 0
        for i in reversed(range(1, N + 1)):
            maxim.append(i)
        while len(maxim) > 0:
            aa = []
            add_aa = []
            aa.append(maxim[0])
            maxim.pop(0)
            if self.mass[iter+1][0] == 0:
                aa += maxim
                maxim = []
            else:
                for i, j in zip(self.mass[iter+1][1], maxim):
                    if i == 0:
                        aa.append(j)

                        add_aa.append(j)
                for el in add_aa:
                    maxim.remove(el)
            self.A.append(aa)
            iter += 1 # получение элемента

        return self.A # получение элемента


N = int(input("Введите количество объектов: "))

#r = int(input("Введите ранг: "))
#print('Ранг:'       , r)
#print('Дерево:'     , VRV().getVar(r, N))
#A = VRV().UnRank(r, N)
#print('Элемент'     , A)
#print('Дерево:'    , VRV().toVar(A))
#print('Ранг:'    , int(VRV().lB(0, r, N)))

#import time

#N = int(input("Введите количество объектов: "))
s = 0
#start = time.time()
#if N == 0:
#   print("Элементов нет")
#else:
for r in range(int(VRV().B(N))):

#        VRV().getVar(r, N)
#        A = VRV().UnRank(r, N)
#        VRV().toVar(A)
#        int(VRV().lB(0, r, N))
#times = time.time() - start #float('{:.10f}'.format(time.time() - start))
#print(f'Время выполнения {times}')

    print('Ранг:'       , r)
    print('Дерево:'     , VRV().getVar(r, N))
    A = VRV().UnRank(r, N)
    print('Элемент'     , A)
    print('Дерево:'    , VRV().toVar(A))
    print('Ранг:'    , int(VRV().lB(0, r, N)))
    if r != int(VRV().lB(0, r, N)):
        print('Что то не так с рангом:', r, '\n')
        s += 1
    else:
        print('Все окей!', '\n' )
        s += 0
print('Количество найденых ошибок:', s)




