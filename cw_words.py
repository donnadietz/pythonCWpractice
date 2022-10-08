import os
import random
import curses, time


#os.system('play -n synth %s sin %s' % (seconds, freq))
#os.system('play -n synth %s sin %s > /dev/null 2>&1' % (seconds, freq))


def setup(b,f,p):
    global baseSpeed
    global freq
    global CW
    global keys
    baseSpeed = b*.1
    global pauses
    pauses = p
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

    global words
    words=[]
    f2=open("google-10000-english-usa.txt","r")
    for line in f2:
      words.append(line)
    for i in range(len(words)):
        words[i]=words[i][0:len(words[i])-1]
    #words from length 1 to 18
    print("Setup complete. Use wordset(n,a,b), wordset2(n,a,b,sec), playword(a,b),  buildUp(n) or buildUpSet(n,word) next!")
    
def play(ch):
    global baseSpeed
    global freq
    global CW
    global pauses
    if ord(ch)>=ord('a') and ord(ch)<=ord('z'):
        ch=chr(ord(ch)-32)
    for e in CW[ch]:
        os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed*e, freq))
        os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed, 0)) #pauses
    for e in range(pauses):    
        os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed, 0))  #for each character, add e-length pauses
        
def playword(a,b):
    if a<1 or b>18:
        return
    global words
    #length a to b inclusive
    wordlength=0
    myword=''
    while not a<=wordlength<=b:
        myword=words[random.randint(0,9999)]
        wordlength=len(myword)
    stoploop=0
    while not stoploop:        
        word(myword)
        myresponse=input("* to repeat or type word here > ")
        if myresponse.upper()==myword.upper():
            print("GOOD WORK!")
            stoploop=1
            return 1
        elif myresponse=="*":
            stoploop=0
        else:
            print("No. The word was actually: "+myword)
            stoploop=1
            return 0

def wordset(n,a,b):
    correct=0
    for i in range(n):
        print(str(i)+" of "+str(n)+":")
        correct+=playword(a,b)
    print("You got "+str(correct)+" correct of "+str(n)+".")    

def wordset2(n,a,b,s):
    starttime=time.time()
    spw=s/n #seconds per word goal
    correct=0
    for i in range(n):
        ktime=time.time()
        if ktime-starttime > (spw*i +.1):
            print("You are BEHIND: "+str(int((ktime-starttime)-(spw*i)))+" sec.")
        else:
            print("You have banked "+str(int(spw*i-ktime+starttime))+" sec.")
        print("Score: "+str(correct)+" correct of "+str(i)+".")    
        print("Words remaining: "+str(n-i))
        correct+=playword(a,b)
    ktime=time.time()
    usedtime=ktime-starttime
    print("FINAL SCORE: You got "+str(correct)+" correct of "+str(n)+".")
    print("You used a total of "+str(int(usedtime))+" seconds.")
    if s-usedtime>0:
        print("This was "+str(int(s-usedtime))+" seconds better than your goal.")
    else:    
        print("This was "+str(int(usedtime-s))+" seconds worse than your goal.")
def word(w):
    for e in w:
        if e==' ':
            os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed*7, 0))
        else:
            play(e)
            os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed*3, 0))
    
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
        os.system('play -n -q synth %s sin %s > /dev/null 2>&1' % (baseSpeed*7, freq/2))
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


print("Use setup(b,f,p) to start. b=1 is basic speed, f=frequency, p=pauses")    
print("USE PYTHON3 PLEASE!!!")
