from datetime import *
import time
class User():
    def __init__(self, mid, name, regtime):
        self.mid     = int(mid)
        self.name    = name
        self.regtime = int(regtime)
        self.getDays()
        # self.getNext()
        # self.getPrev()
    def getDays(self):
        # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        self_datetime = datetime.fromtimestamp(self.regtime)
        self_days_str = self_datetime.strftime('%Y%m%d')
        self.days     = int(self_days_str)
    # def getPrev(self):
    #     if self.mid == 1:
    #         self.prev = self
    #     else:
    #         self.prev = getUserById(self.mid-1)
    # def getNext(self):
    #     self.next = getUserById(self.mid+1)

def getUserById():
    pass

def isValid(user):
    if user.mid == 1:
        return True
    if user.prev.days < user.days and user.next.days >= user.days:
        return True
    else:
        return False

if __name__ == '__main__':
    a = User('11','name','120690001')
    b = User('11','name','124500000')
    print(a.mid)
    print(a.name)
    print(a.regtime)
    print(a.days)
    print(a.days-b.days)
    