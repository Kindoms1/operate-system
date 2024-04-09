class Time:
    def __init__(self):
        self.hour = 0
        self.min = 0


class Node:
    def __init__(self, id=None, name=None, good=None, arrive=None, zx=None):
        self.id = id
        self.name = name
        self.good = good  # 优先级,
        self.arrive = arrive
        self.arrive_int = None
        self.atime = Time()
        self.zx = zx  # int
        self.sart = None
        self.finish = None

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

    # 把时间转化成分钟
    def convert(self, s):
        li = [str(i) for i in range(10)]
        for i in range(len(s)):
            if s[i] not in li:
                return int(s[:i])*60 + int(s[i+1:])
            
    # 传入的p是一个Node
    def enQueue(self, p):
        self.tail.next = p
        self.tail = p
        self.num += 1

    # 返回name
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
        print('ID号 名字 优先级 到达时间 执行时间(分钟)：(输入ID号为-1表示进程输入结束)')
        n = 0
        li = [str(i) for i in range(10)]
        while n != -1:
            temp = [x for x in input().split()]
            n = int(temp[0])
            if n == -1:
                break
            p = Node(int(int(temp[0])), temp[1], temp[2], temp[3], int(temp[4]))
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

        # 进行排序
        at = sorted(at)
        self.at = at
        i = 0
        new = sorted(temp, key=lambda x:x.arrive_int)

        # 每当出队完后，需要清空head 和 tail,否则 head.next 指向错误
        p = Node()
        self.head = p
        self.tail = p

        for x in new:
            self.enQueue(x)

    # priority scheduling
    def ps(self):
        # 按到达时间排序
        temp = []
        while not self.isEmpty():
            temp.append(self.deQueu())
            if self.isEmpty():
                break
        n = len(temp)

        p = Node()
        self.head = p
        self.tail = p

        current_time, completed = 0, 0  # 初始化最初开始时间为0
        waiting = []
        done = []
        # 循环处理进程
        while completed < n:
            # 添加到达的进程到队列中
            for i in range(n):
                if temp[i].arrive_int <= current_time and temp[i] not in waiting:
                    if temp[i] not in done:  # 已经处理过的不用再进入
                        waiting.append(temp[i])
            # 如果队列为空，则时间跳转到下一个进程到达时间
            if not waiting:
                current_time = temp[completed].arrive_int
            else:
                # 按照优先级 从大到小
                waiting.sort(key=lambda x: (-int(x.good), x.zx, x.id), reverse=False)
                p = waiting.pop(0)
                done.append(p)
                self.enQueue(p)
                # 更新当前时间和已完成进程数
                current_time += p.zx
                completed += 1

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
            arrive_time = self.convert(p.arrive)
            if i >= 1:
                if finish[i-1] <= arrive_time:
                    start.append(arrive_time)
                    finish.append(arrive_time + p.zx)
                    turn.append(p.zx)
                else:
                    start.append(finish[i-1])
                    finish.append(start[i] + p.zx)
                    turn.append(finish[i] - arrive_time)

            # 对于第一个来的进程而言
            else:
                start.append(arrive_time)
                finish.append(arrive_time+p.zx)
                turn.append(p.zx)
            ave_turn_wg += turn[i]/p.zx
            turn_wg.append("%.2f" % (turn[i]/p.zx))  # 保留两位小数
        ave_turn = sum(turn)/len(node)
        ave_turn_wg = ave_turn_wg/len(node)

        for i in range(len(node)):
            start[i] = str(start[i]//60).rjust(2, '0') + ':' + str(start[i] % 60).rjust(2, '0')
            finish[i] = str(finish[i]//60).rjust(2, '0') + ':' + str(finish[i] % 60).rjust(2, '0')

        print('模拟优先级调度过程输出结果：')
        print('ID号    名字   优先级   到达时间    执行时间(分钟)     开始时间 完成时间    周转时间(分钟)    带权周转系数')
        for i in range(len(node)):
            print(node[i].id, '\t', node[i].name, '\t', node[i].good, '\t', node[i].arrive, '\t'*2, node[i].zx, '\t'*2, start[i], '\t', finish[i], '\t'*2, turn[i], '\t'*2, turn_wg[i])
        print('系统平均周转周期时间为：', '\t'*7, '%.2f' % ave_turn)
        print('系统带权平均周转周期为：', '\t'*9, '%.2f' % ave_turn_wg)


if __name__ == '__main__':
    print('请输入任意数字开始进程调度,输入0结束')
    k = input()
    while k != '0':
        m = int(input(('请输入进程数：')))
        ep = queue()
        ep.createQueue()
        print('原始队列为：', end='')
        ep.printQueue()
        ep.sort()
        ep.ps()
        print("完成顺序为：", end='')
        ep.printQueue()
        ep.start_finish_turn()

        k = (input('请输入任意数字开始，输入0结束：'))
