import os
import random
import curses, time

#os.system('play -n synth %s sin %s' % (seconds, freq))


def setup(b,f):
    global baseSpeed
    global freq
    global CW
    global keys
    baseSpeed = b*.1
    freq = f
    CW={'A':(1,3), 'B':(3,1,1,1), 'C':(3,1,3,1), 'D':(3,1,1), 'E':(1,),
           'F':(1,1,3,1), 'G':(3,3,1), 'H':(1,1,1,1), 'I':(1,1), 'J':(1,3,3,3),
           'K':(3,1,3), 'L':(1,3,1,1), 'M':(3,3), 'N':(3,1), 'O':(3,3,3),
           'P':(1,3,3,1), 'Q':(3,3,1,3), 'R':(1,3,1), 'S':(1,1,1), 'T':(3,),
           'U':(1,1,3), 'V':(1,1,1,3), 'W':(1,3,3), 'X':(3,1,1,3),
           'Y':(3,1,3,3), 'Z':(3,3,1,1), '/':(3,1,1,3,1), '.':(1,3,1,3,1,3),
           '?':(1,1,3,3,1,1), ',':(3,3,1,1,3,3),
           '0':(3,3,3,3,3), '1':(1,3,3,3,3), '2':(1,1,3,3,3), '3':(1,1,1,3,3),
           '4':(1,1,1,1,3), '5':(1,1,1,1,1), '6':(3,1,1,1,1), '7':(3,3,1,1,1),
           '8':(3,3,3,1,1), '9':(3,3,3,3,1), '@':(1,3,3,1,3,1),'=':(3,1,1,1,3)}
    
    keys = ['Y', '.', 'S', '5', 'B', 'R', 'D', 'C', 'I', 'U', '3',
            'H', '4', 'Z', 'W', 'L', 'M', 'G', '6', '1', '9', 'X', 'P', '8',
            '?', 'N', 'Q', ',', 'J', 'E', 'A', 'T', '0', 'K', 'V', '7', '2',
            'F', '/', 'O','@','=']
    print("Setup complete. Use buildUp(n) or buildUpSet(n,word) next!")
    
def play(ch):
    global baseSpeed
    global freq
    global CW
    if ord(ch)>=ord('a') and ord(ch)<=ord('z'):
        ch=chr(ord(ch)-32)
    for e in CW[ch]:
        os.system('play -n -t alsa -q synth %s sin %s ' % (baseSpeed*e, freq))
        os.system('play -n -t alsa -q synth %s sin %s ' % (baseSpeed, 0))


def word(w):
    for e in w:
        if e==' ':
            os.system('play -n -t alsa -q synth %s sin %s ' % (baseSpeed*7, 0))
        else:
            play(e)
            os.system('play -n -t alsa -q synth %s sin %s ' % (baseSpeed*3, 0))
    
def pick():
    global keys
    return random.choice(keys)

def testOne():
    ch=pick()
    play(ch)
    reply=input_char("")
    if ch==reply or ch==chr(ord(reply)-32):
        print('CORRECT: '+ch)
        return True
    else:    
        print('SORRY! '+ch, 'not '+reply)
        input("Please hit enter to continue!")
        return False

def testCh(ch):
    play(ch)
    reply=input_char("")
    if ch==reply or ch==chr(ord(reply)-32):
        print('CORRECT: '+ch)
        return True
    else:    
        print('SORRY! '+ch, 'not '+reply)
        os.system('play -n -t alsa -q synth %s sin %s' % (baseSpeed*7, freq/2))
        input("Please hit enter to continue!")
        return False    

def input_char(message):
    try:
        win = curses.initscr()
        win.addstr(0, 0, message)
        while True: 
            ch = win.getch()
            if ch in range(32, 127): break
            time.sleep(0.05)
    except: raise
    finally:
        curses.endwin()
    return chr(ch)    


def repeatThis(n):
    ok=0
    for i in range(n):
        ok+=testOne()
    print(str(ok)+" correct out of "+str(n))


def buildUp(n):
    starttime=time.time()
    ok=0
    bad=0
    L=[]
    for i in range(n):
        L.append(pick())
    while len(L):
        results=testCh(L[0])
        if results:
            L.pop(0)
            ok+=1
        else:
            L.insert(random.randint(0,len(L)-1), L[0])
            L.insert(random.randint(0,len(L)-1), L[0])
            bad+=1
    endtime=time.time()        
    print(str(ok)+" correct out of "+str(ok+bad))                
    cps=(ok+bad)/(endtime-starttime)
    print("%0.1f cps"%(cps))
    print("%0.1f wpm"%(cps*12))



def buildUpSet(n,word):
    starttime=time.time()
    ok=0
    bad=0
    L=[]
    for i in range(n):
        L.append(random.choice(word))
    while len(L):
        results=testCh(L[0])
        if results:
            L.pop(0)
            ok+=1
        else:
            L.insert(random.randint(0,len(L)-1), L[0])
            L.insert(random.randint(0,len(L)-1), L[0])
            bad+=1
    endtime=time.time()        
    print(str(ok)+" correct out of "+str(ok+bad))                
    cps=(ok+bad)/(endtime-starttime)
    print("%0.1f cps"%(cps))
    print("%0.1f wpm"%(cps*12))    


print("Use setup(b,f) to start. b=1 is normal speed, f=frequency")    
print("USE PYTHON3 PLEASE!!!")
