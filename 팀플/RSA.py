#-*- coding:utf-8 -*-
import random
from tkinter import *
from tkinter import ttk

n=e=1
#유클리드 호제법-> gcd
def gcd(x, y):
    if y==0 : return x
    return gcd(y,x%y)

#공개키 만들기  
def makeKey(w,entry):
    global n,e
    #에라토스테네스의 체 -> 소수만 들어있는 배열 prime 만들기
    MAX = int(entry.get())
    isPrime=[1]*MAX
    isPrime[0]=isPrime[1]=0
    prime=[]
    for i in range(2,MAX):
            if(isPrime[i]==0): continue
            prime.append(i)
            for j in range(i*i,MAX,i):
                    isPrime[j]=0

    #매우 큰 소수 p,q 랜덤 선택
    p=prime[random.randint(0,len(prime)-1)]
    q=prime[random.randint(0,len(prime)-1)]
    n = p*q
    totient = (p-1)*(q-1) #오일러 피 함수의 값

    #공개키 정하기
    for i in range(2,totient):
        if(gcd(i,totient)==1): 
            e=i  # e : 공개키
            break

    #비밀키 정하기
    for i in range(1,totient):
        if((i*e)%totient==1) :
            d=i # d : 비밀키     
    t = Label(w,text="n= "+str(n)+",  e= "+str(e))
    t.pack()
    print("KEY----- n : %d, totient : %d, e : %d, d : %d, MAX: %d"%(n,totient,e,d,MAX))

#암호화 함수
def encrypt(text,w,entry):
    M = entry.get() #평문 string
    C=[]
    for i,chh in enumerate(M):
        ch = ord(chh)
        C.append(str((ch**e)%n))
        if(i<len(M)-1): C.append('O')
    text.insert(2.0,''.join(C)+'\n')
    text.pack()

#복호화 함수
def decrypt(text, w, entry, entryn, entryd):
    C = entry.get().split('O') #암호문 list
    n= int(entryn.get())
    d= int(entryd.get())
    
    MM=[]
    for chh in C:
        ch = int(chh)
        MM.append(chr((ch**d)%n))
    text.insert(2.0,''.join(MM)+'\n')
    text.pack()

#브루트 포스로 간단한 RSA 알고리즘 깨보기
def bruteForce(text,w,entryN,entryC,entryM):
    C = entryC.get().split('O') #암호문
    M = entryM.get() #평문(비교용)
    n= int(entryN.get())
    d=1
    text.insert(1.0,"추측 중..."+"\n")
    text.pack()
    while d<n:
        dec = []  
        for chh in C:
            ch = int(chh)
            dec.append(chr((ch**d)%n))
        guess=''.join(dec)
        text.insert(2.0, guess+"  d = "+str(d)+'\n')
        if M == guess:
            text.delete(1.0, 2.0)   
            text.insert(2.0,"!!!암호깨기 성공!!!!"+'\n')
            return
        d = d+1
    text.insert(2.0,"입력오류: n값을 확인해주세요"+'\n')
    
###################################################

def encryptSel():
    w1=Toplevel(window)
    w1.title("암호화하기")
    w1.geometry("250x350+100+170")
    w1.resizable(True,True)

    t2 = Label(w1,text="소수(p,q) 최대값")
    t2.pack()

    entry2 = Entry(w1, width=10)
    entry2.pack()
   
    btn1 = Button(w1,width=10, text="공개키 만들기", command= lambda : makeKey(w1,entry2))
    btn1.pack()

    t = Label(w1,text="암호화할 문장")
    t.pack()

    entry1 = Entry(w1,show="*")
    entry1.pack()

    btn1 = Button(w1,width=10, text="암호화 하기", command=lambda: encrypt(textbox,w1,entry1))
    btn1.pack()

    textbox = Text(w1)
    textbox.insert(CURRENT,"암호문: "+"\n")
    

def decryptSel():
    w2=Toplevel(window)
    w2.title("복호화하기")
    w2.geometry("250x350+360+170")
    w2.resizable(True,True)

    t3 = Label(w2, text="복호화할 암호문")
    t3.pack()

    entry3 = Entry(w2,width=100)
    entry3.pack()

    t4 = Label(w2, text="키(n) 입력")
    t4.pack()
    entryN = Entry(w2, width=10)
    entryN.pack()
    
    t5 = Label(w2, text="비밀키(d) 입력")
    t5.pack()
    entryD = Entry(w2, width=10)
    entryD.pack()

    btn4 = Button(w2, width=10, text="복호화하기", command=lambda : decrypt(textbox,w2,entry3,entryN,entryD))
    btn4.pack()
    
    textbox = Text(w2)
    textbox.insert(CURRENT,"평문: "+"\n")

def BruteForceSel():
    w3=Toplevel(window)
    w3.title("암호깨기")
    w3.geometry("250x350+620+170")
    w3.resizable(True,True)

    t1 = Label(w3, text="키(n) 입력")
    t1.pack()
    entryN = Entry(w3, width=10)
    entryN.pack()

    t2 = Label(w3, text="암호문 입력")
    t2.pack()
    entryC = Entry(w3,width=100)
    entryC.pack()

    t3 = Label(w3, text="평문 입력")
    t3.pack()
    entryM = Entry(w3,width=100)
    entryM.pack()

    btn7 = Button(w3, width=10, text="암호 깨기", command=lambda : bruteForce(textbox,w3,entryN,entryC,entryM))
    btn7.pack()

    textbox = Text(w3)
############################메인페이지
window=Tk()

window.title("팀1. 암호화 알고리즘")
window.geometry("910x600+20+20") 
window.resizable(False,False)

test1=Button(window, width=25, text="암호화", command=encryptSel)
test1.place(x=100, y=450)

test2=Button(window, width=25, text="복호화",command=decryptSel)
test2.place(x=370, y=450)

test3=Button(window, width=25, text="암호깨기",command=BruteForceSel)
test3.place(x=640, y=450)

image1=PhotoImage(file="./암호화1.png")
label1=Label(image=image1,width=200, height=200)
label1.place(x=100, y=150)

image2=PhotoImage(file="./복호화1.png")
label2=Label(image=image2,width=200, height=200)
label2.place(x=370, y=150)

image3=PhotoImage(file="./암호깨기1.png")
label3=Label(image=image3,width=200, height=200)
label3.place(x=640, y=150)

window.mainloop()
