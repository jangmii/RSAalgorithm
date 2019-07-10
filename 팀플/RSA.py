import random
from tkinter import *
from tkinter import ttk

#유클리드 호제법-> gcd
def gcd(x, y):
    if y==0 : return x
    return gcd(y,x%y)

#암호화 함수
def encrypt(w,entry,e,n):
    M = entry.get()
    C=[]
    for chh in M:
        ch = ord(chh)
        C.append(str((ch**e)%n))
    print("암호문 : ",join.(C))
    t=Label(w, text="암호문 : "+''.join(C))
    t.pack()
    
    return C
    
#복호화 함수
def decrypt(w, entry, d, n):
    C = entry.get()
    MM=[]
    for chh in C:
        ch = ord(chh)
        MM.append(str((ch**d)%n))
    print("평문: ",''.join(MM))
    t=Label(w, text="평문 : "+''.join(C))
    t.pack()  
    return MM

#공개키 만들기  
def makeKey(w,entry22):
    #에라토스테네스의 체 -> 소수만 들어있는 배열 Prime 만들기
    MAX = int(entry22.get())
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
    global n,e,d
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

    print("n : %d, totient : %d, e : %d, d : %d, MAX: %d"%(n,totient,e,d,MAX))

################################################### tkinter 창 띄우기
def encryptSel():
    w1=Toplevel(window)
    w1.title("암호화하기")
    w1.geometry("300x420+80+120")

    t2 = Label(w1,text="소수(p,q) 최대값")
    t2.pack()

    entry2 = Entry(w1, width=10)
    entry2.pack()
   
    btn1 = Button(w1,width=10, text="공개키 만들기", command=lambda : makeKey(w1,entry2))
    btn1.pack()

    t = Label(w1,text="암호화할 문장")
    t.pack()

    entry1 = Entry(w1,show="*")
    entry1.pack()

    btn1 = Button(w1,width=10, text="암호문 만들기", command=lambda: encrypt(w1,entry1,e,n))
    btn1.pack()

    w1.resizable(False,True)

def decryptSel():
    w2=Toplevel(window)
    w2.title("복호화하기")
    w2.geometry("300x420+320+120")
    w2.resizable(False,True)

def BruteForceSel():
    w3=Toplevel(window)
    w3.title("암호깨기")
    w3.geometry("300x420+600+120")
    w3.resizable(False,True)

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

image1=PhotoImage(file="팀플/암호화1.png")
label1=Label(image=image1,width=200, height=200)
label1.place(x=100, y=150)

image2=PhotoImage(file="팀플/복호화1.png")
label2=Label(image=image2,width=200, height=200)
label2.place(x=370, y=150)

image3=PhotoImage(file="팀플/암호깨기1.png")
label3=Label(image=image3,width=200, height=200)
label3.place(x=640, y=150)

window.mainloop()

# ################################## RSA 알고리즘
# #에라토스테네스의 체 -> 소수만 들어있는 배열 Prime 만들기
# MAX = 1001 #p,q 상한선
# isPrime=[1]*MAX
# isPrime[0]=isPrime[1]=0
# prime=[]
# for i in range(2,MAX):
#         if(isPrime[i]==0): continue
#         prime.append(i)
#         for j in range(i*i,MAX,i):
#                 isPrime[j]=0


# #매우 큰 소수 p,q 랜덤 선택
# import random
# p=prime[random.randint(0,len(prime)-1)]
# q=prime[random.randint(0,len(prime)-1)]
# n = p*q
# totient = (p-1)*(q-1) #오일러 피 함수의 값

# #공개키 정하기
# for i in range(2,totient):
#     if(gcd(i,totient)==1): 
#         e=i  # e : 공개키
#         break

# #비밀키 정하기
# for i in range(1,totient):
#     if((i*e)%totient==1) :
#         d=i # d : 비밀키


# m=input("암호화할 평문을 입력하세요: ") #평문
# m=[] #평문
# c=[] #암호문
#n=e=d=1

#print("n : %d, totient : %d, e : %d, d : %d, MAX: %d"%(n,totient,e,d,MAX))
# mm=[] #복호문

# print("복호문 : ",end="")

# for chh in c : #복호화
#     ch=int(chh)
#     mm.append(chr(decrypt(d,n,ch)))
# #   mmfinal=''.join(mm)
#     print(mm[-1],end="")

#print("복호문 :",mmfinal)