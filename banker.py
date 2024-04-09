import re

class OS:
    def __init__(self):
        self.sourceTyprNum = None
        self.processNum = None
        self.available = []  # 一维
        self.ABC = []  # 生成ABCDEFG...
        self.max = []  # 二维,每个进程对每类资源的
        self.allocation = []  # 进程已经占有的
        self.need = []  # 剩余所需
        self.flag = []  # 是否完成

    def judge(self, request, work):
        for i in range(len(request)):
            if request[i] > work[i]:
                return False
        return True  # request <= work

    def source(self, a, b, c):  # b=work, c='+/-'
        d = []
        for i in range(self.sourceTyprNum):
            d.append(b[i] + c*a[i])
        return d

    def output(self):
        print("进程名\t", "\t已分配\t", "最大\t", "尚需\t", "  完成")
        s = " ".join(self.ABC)
        print("\t\t {}\t {}\t {}".format(s,s,s))
        for i in range(self.processNum):
            print("进程p[{}]".format(i+1), "\t", " ".join(map(str, self.allocation[i])), "\t",  " ".join(map(str,self.max[i])), "\t", " ".join(map(str, self.need[i])), '\t','finished' if self.flag[i] else 'working')

    def build(self):
        print("请输入资源种类：")
        typeNum = int(input())
        self.sourceTyprNum = typeNum
        self.ABC = [chr(65+i) for i in range(typeNum)]

        print("请输入进程数：")
        processNum = int(input())
        self.processNum = processNum
        self.flag = [False for i in range(processNum)]
        self.max = [[0 for i in range(typeNum)] for j in range(processNum)]
        self.allocation = [[0 for i in range(typeNum)] for j in range(processNum)]

        print("请输入{}类资源初始化的资源数：".format(typeNum))
        available = input()
        available = re.findall(r'\d+', available)
        self.available = [int(x) for x in available]

        print("请输入{}个进程的进程名".format(processNum))
        print("进程名\t","最大需求量:")
        print("\t", end=' ')
        for x in self.ABC:
            print(x, end=" ")
        print("")
        for i in range(self.processNum):
            pcb = input()
            pcb = re.findall(r'\d+', pcb)
            process = int(pcb[0])
            pcb = pcb[1:]
            pcb = [int(x) for x in pcb]
            if not self.judge(pcb, self.available):
                pcb = [0 for _ in range(self.sourceTyprNum)]
                self.flag[process-1] = True
                print("该进程所需最大资源超出系统最大资源！已被弹出！")
            self.max[process-1] = pcb
        self.need = [x for x in self.max]

    def security(self):
        work = self.available[:]
        Finish = [False for _ in range(self.processNum)]
        anquan = []
        while False in Finish:
            found = False
            for i in range(self.processNum):
                if Finish[i] == False and self.judge(self.need[i], work):
                    work = self.source(self.allocation[i], work, 1)
                    Finish[i] = True
                    found = True
                    if self.flag[i] == False:
                        anquan.append(i+1)
                    break
            if not found:
                return [False]
        return [True,anquan]

    def more(self, now, request):
        temp = self.allocation[:]
        if self.judge(self.source(request, temp[now], 1), self.max[now]):
            if self.judge(request, self.need[now]):
                if self.judge(request, self.available):
                    self.available = self.source(request, self.available, -1)
                    self.allocation[now] = self.source(request, self.allocation[now], 1)
                    self.need[now] = self.source(request, self.need[now], -1)
                    security = self.security()
                    if security[0]:
                        if self.judge(self.need[now],[0 for _ in range(self.sourceTyprNum)]):
                            self.flag[now] = True
                            self.available = self.source(self.allocation[now], self.available, 1)
                            self.allocation[now] = [0 for _ in range(self.sourceTyprNum)]
                            self.need[now] = [0 for _ in range(self.sourceTyprNum)]

                        if self.flag.count(False) == 0:
                            print("所有进程以运行完成！")
                        else:
                            print("申请成功！安全序列为:", end = '')
                            for i in range(len(security[1])):
                                if self.flag[security[1][i]-1] == False:
                                    if i == len(security[1])-1:
                                        print(security[1][i])
                                    else:
                                        print(security[1][i], end='->')
                            self.output()
                            print("")
                    else:
                        self.available = self.source(request, self.available, 1)
                        self.allocation[now] = self.source(request, self.allocation[now], -1)
                        self.need[now] = self.source(request, self.need[now], 1)
                        print("无安全序列!申请失败")
                        print("剩余可用资源:", ' '.join([str(x) for x in os.available]))
                else:
                    print("申请失败!剩余资源不足以满足申请")
            else:
                print("申请失败!申请资源超过尚需资源")
        else:
            print("申请失败!申请资源超过了最大需求")

if __name__ == '__main__':
    os = OS()
    os.build()
    print("请输入{}个进程的：".format(os.processNum))
    print("进程名\t","第一次申请量:")
    print("\t", end=' ')
    for x in os.ABC:
        print(x, end=" ")
    print("")
    # 第一次申请
    for i in range(os.processNum):
        if i != 0:
            print("进程名\t","第一次申请量:")
        pcb = input()
        pcb = re.findall(r'\d+', pcb)
        now = int(pcb[0])-1
        request = [int(x) for x in pcb[1:]]
        os.more(now, request)
        print("系统剩余资源:", ' '.join([str(x) for x in os.available]))
    print("是否需要再申请资源?(Y/N)")
    n = input()
    number = [str(x) for x in range(1, os.processNum+1)]
    while (n == 'y'or n == 'Y'):
        print("请输入进程编号{}".format(str(1)+'-'+str(os.processNum)))
        now = input()
        while now not in number:
            print("请输入标准进程名:{}-{}".format(1, os.processNum), end=' ')
            now = input()
        now = int(now)
        print("请输入进程{}对{}类资源的申请量".format(now, os.sourceTyprNum))
        now -= 1
        request = input()
        request = re.findall(r'\d+', request)
        request = [int(x) for x in request]
        os.more(now, request)
        print("剩余资源:", ' '.join([str(x) for x in os.available]))
        if False not in os.flag:
            os.output()
            print("资源剩余:", ' '.join([str(x) for x in os.available]))
        print("是否需要再申请资源?(Y/N)")
        n = input()
