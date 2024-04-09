class Time:
    def __init__(self):
        self.hour = 0
        self.min = 0

class Node:
    def __init__(self, id=None, name=None, arrive=None, zx=None, good=None):
        self.id = id
        self.name = name
        self.good = good  # 优先级
        self.arrive = arrive
        self.arrive_int = None
        self.arrive_int_backup = None
        self.atime = Time()
        self.zx = zx  # int
        self.sart = None
        self.finish = None

        self.nowstart = arrive  # 当前开始时间
        self.remaintime = zx  # 剩余时间执行
        self.donetime = 0  # 已完成时间
        self.use = 0

        self.next = None


class queue:
    def __init__(self):
        tQueueNode = Node()  # 必须要这样，否则初始的 front 和 rear 不相等
        self.head = tQueueNode
        self.tail = tQueueNode
        self.num = 0
        self.at = None

    def isEmpty(self):
        return self.head == self.tail

    def cleanAll(self):
        q = Node()
        self.haed = q
        self.tail = q
        self.num = 0

    # 把时间转化成分钟  # s:str
    def convert(self, s):
        li = [str(i) for i in range(10)]
        for i in range(len(s)):
            if s[i] not in li:
                return int(s[:i])*60 + int(s[i+1:])

    def convert_str(self, time):  # time:int
        time = str(time//60).rjust(2, '0') + ':' + str(time % 60).rjust(2, '0')
        return time

    # p:Node()
    def enQueue(self, p):
        self.tail.next = p
        self.tail = p
        self.num += 1

    # return num
    def deQueu(self):
        if self.isEmpty():
            return None
        else:
            p = self.head.next
            self.head.next = p.next
            if self.tail == p:
                self.head = self.tail
            self.num -= 1
            return p

    def createQueue(self):
        print('ID号 名字 到达时间 执行时间(分钟)：(输入ID号为-1表示进程输入结束)')
        n = 0
        li = [str(i) for i in range(10)]
        while n != -1:
            temp = [x for x in input().split()]
            n = int(temp[0])
            if n == -1:
                break
            p = Node(int(temp[0]), temp[1], temp[2], int(temp[3]))
            s = temp[3]
            for i in range(len(s)):
                if s[i] not in li:
                    p.atime.hour = int(s[:i])
                    p.atime.min = int(s[i+1:])
            self.enQueue(p)

    # 打印name
    def printQueue(self):
        if self.isEmpty():
            print("队列为空")
        else:
            p = self.head
            while p != self.tail:
                p = p.next
                if p == self.tail:
                    print(p.name)
                    break
                print(p.name, '->', end=' ')

    # 按照到达时间先后排序进程队列
    def sort(self):
        temp = []
        while not self.isEmpty():
            temp.append(self.deQueu())
            if self.isEmpty():
                break
        at = [x.arrive for x in temp]
        # 字符串转数字，进制转换
        for i in range(len(at)):
            at[i] = self.convert(at[i])
            temp[i].arrive_int = at[i]
            temp[i].arrive_int_backup = at[i]

        # 进行排序
        at = sorted(at)
        self.at = at
        i = 0
        new = sorted(temp, key=lambda x: x.arrive_int)

        # 每当出队完后，需要清空head 和 tail,否则 head.next 指向错误
        p = Node()
        self.head = p
        self.tail = p

        for x in new:
            self.enQueue(x)

    def rr(self, ts):
        temp = []
        q = self.head
        while q != self.tail:
            q = q.next
            if q == self.tail:
                temp.append(q)
                break
            temp.append(q)

        h = Node()
        self.head = h
        self.tail = h

        n = len(temp)
        start,end = 0, 0
        j, k = 0, 1
        completed = []  # 完成队列
        waiting = []  # 就绪队列

        while j < n:
            for i in range(n):
                if temp[i].arrive_int <= end and temp[i] not in waiting:
                    if temp[i] not in completed:  # 已经处理过的不用再进入
                        waiting.append(temp[i])
            # 如果队列为空，则时间跳转到下一个进程到达时间
            if not waiting:
                start = temp[j].arrive_int
                end = start + ts
            else:
                p = waiting.pop(0)
                p.use = 1
                if p.remaintime == p.zx:
                    p.start = start  # 第一次开始的时间
                p.nowstart = start  # 程序本轮的开始时间
                if p.remaintime <= ts:
                    p.donetime = p.zx
                    start = start + p.remaintime
                    end = start + ts
                    p.remaintime = 0
                    p.finish = start
                    completed.append(p)
                    self.enQueue(p)
                    j += 1
                else:
                    p.remaintime = p.remaintime - ts
                    p.donetime = p.zx - p.remaintime
                    start = end
                    end = start + ts
                    p.arrive_int = start
                    waiting.append(p)

                print('第{}轮执行和就绪队列结果'.format(k))
                print('ID号\t名字\t到达时间  总执行时间(分钟)   当前开始时间    已完成时间    剩余时间:')
                print(p.id, '\t', p.name, '\t', p.arrive, '\t', '\t', p.zx, '\t', '\t', self.convert_str(p.nowstart), '\t', '\t', p.donetime, '\t     ', p.remaintime)
                for x in waiting:
                    if x.arrive_int <= start:
                        if x.use == 0:
                            print(x.id, '\t', x.name, '\t', x.arrive, '\t', '\t', x.zx, '\t', '\t', "00:00", '\t', '\t', x.donetime, '\t     ', x.remaintime)
                        else:
                            x.use = 0
                print('')
                k += 1
            if j==n:
                break


    def start_finish_turn(self):
        if self.isEmpty():
            return
        node = []
        p = self.head
        while p != self.tail:
            p = p.next
            if p == self.tail:
                node.append(p)
                break
            node.append(p)
        start = []
        finish = []
        turn = []
        turn_wg = []
        ave_turn = 0
        ave_turn_wg = 0
        for i in range(len(node)):
            p = node[i]
            start.append(p.start)
            finish.append(p.finish)
            turn.append(p.finish-p.arrive_int_backup)
            ave_turn_wg += turn[i]/p.zx
            turn_wg.append("%.2f" % (turn[i]/p.zx))  # 保留两位小数
        ave_turn = sum(turn)/len(node)
        ave_turn_wg = ave_turn_wg/len(node)

        for i in range(len(node)):
            start[i] = str(start[i]//60).rjust(2, '0') + ':' + str(start[i] % 60).rjust(2, '0')
            finish[i] = str(finish[i]//60).rjust(2, '0') + ':' + str(finish[i] % 60).rjust(2, '0')

        print('模拟时间片轮转调度过程输出结果：')
        print('ID号    名字    到达时间    执行时间(分钟)     首次开始时间 完成时间    周转时间(分钟)    带权周转系数')
        for i in range(len(node)):
            print(node[i].id, '\t', node[i].name, '\t', node[i].arrive, '\t'*2, node[i].zx, '\t'*2, start[i], '\t    ', finish[i], '\t   ', turn[i], '\t'*2, '   ', turn_wg[i])
        print('系统平均周转周期时间为：', '\t'*6, '%.2f' % ave_turn)
        print('系统带权平均周转周期为：', '\t'*8, '   ', '%.2f' % ave_turn_wg)


if __name__ == '__main__':
    print('请输入任意数字开始进程调度,输入0结束')
    k = input()
    while k != '0':
        m = int(input('请输入进程数：'))
        ts = int(input('请输入时间片：'))
        ep = queue()
        ep.createQueue()
        print('原始队列为：', end='')
        ep.printQueue()
        ep.sort()
        ep.rr(ts)
        print('完成先后顺序：', end='')
        ep.printQueue()
        ep.start_finish_turn()

        k = (input('请输入任意数字开始，输入0结束：'))
