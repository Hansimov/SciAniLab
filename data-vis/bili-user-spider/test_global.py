
a = 1
b = 'bee'
def changeInFunction():
    a = 2
    print('a in changeInFunction: ', a)

def changeGlobal():
    global a, b
    a = 3
    print('a in changeGlobal: ', a)
    print('b in changeGlobal: ', b)

if __name__ == '__main__':
    print('a in main:', a)
    changeInFunction()
    changeGlobal()
    print('a in main:', a)
    changeInFunction()
