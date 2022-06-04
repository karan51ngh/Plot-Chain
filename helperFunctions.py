def checklogin():
    file2 = open('loginstate.txt', 'r')

    if file2.read()[-1] == '1':
        file2.close()
        return True

    else:
        file2.close()
        return False


def login():
    file2 = open('loginstate.txt', 'a')
    file2.write('1')
    file2.close()


def logout():
    file2 = open('loginstate.txt', 'a')
    file2.write('0')
    file2.close()
