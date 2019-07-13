'''
본 내용은 소인수분해의 난해함과 페르마 소정리, 오일러 피함수 그리고 소수의 특성등의 수학적 배경을 이용한
RSA암호화 알고리즘을 통해 암호화와 복호화를 해주며, 브루트포스 알고리즘을 통해 암호문 깨기를 시도해볼 수 있습니다.

1. 암호화하기

1- 입력1>
N=p*q 식에서 p,q에 들어갈 소수들의 최대값MAX를 사용자로부터 입력받습니다. 따라서 N의 값의 상한선은 MAX**2가
되며 이 값을 통해 암호의 안전한 정도(깨기 어려운 정도)를 결정할 수 있습니다.
1- 출력1>
공개키 만들기 버튼을 클릭하면tkinter창에 사용자로부터 입력받은 MAX값 이하의 랜덤 소수 p와 q를 이용해 공개키 N과 e를 만들고 출력합니다.
이를 포함한 전체 키들과 사용된 값(피함수 값, 비밀키 d, MAX값 등)은 터미널 창에 출력하였습니다.(비밀키이기 때문, MAX값 등은 확인용으로)
임의로 만든 키가 마음에 들지 않을 경우 다른 키를 만들 수 있으며, 이후 암호화에 사용되는 키는 가장 최근에 만들어진 키입니다.
1- 입력2>
암호화할 문장을 입력합니다.- 현재 실험해본 결과로는 영어로된 평문만 제한적으로 암호화가 가능하며, 한글도 암호화할 수 있게 개선해보고
싶었으나 파이썬과 tkinter버전마다 지원하는 유니코드 방식이 조금씩 상이하고 만약 유니코드에 십진수를 초과한 숫자들이 사용되었을 경우
아스키코드 값의 범위를 넘어가 저희가 제작한 암호화방식(문자->아스키코드(숫자)로 변환->계산식을 통해 암호화or복호화->문자로 변환)을
적용하는데 어려움이 있었습니다. 따라서 현재 내용은 영어의 암호화만 지원하며 한글을 포함한 다른 문자들의 암호화 기능은 차후에 개선할 사항
중 하나로 남겨두었습니다-
1- 출력2>
암호문 만들기 버튼을 클릭하면 아래에 암호화된 암호문이 출력되며 여러문장을 암호화하면 가장 윗줄에 최근에
암호화한 문장이 출력됩니다.(아래로 갈 수록 오래된 순)
**암호문을 아스키코드 값으로 두기로 하여서 이후 복호화할 경우, 이를 다시 한글짜씩 자를 때 잘라야할 위치를 찾는데
어려움이 있었습니다. 그래서 한글자 사이사이에 그나마 숫자들과 비슷한 영어 대문자 오('O')를 넣어
문자열로 만들어 암호문을 출력하였고 이 내용이 노출된다면 암호의 안전성에 큰 문제가 생길 것이 염려되지만 다른 해결방법을
찾지 못하여 임시방편으로 이 방법을 선택하였습니다. 차후에 시간적 여유가 있다면 한문자씩 구분할 수 있는 알고리즘과 한글 암호화
기능을 추가해보고 싶습니다.

2. 복호화하기

2- 입력>
복호화할 암호문을 입력받습니다. (암호화하기에서 복사해올 수 있습니다.) 그리고 암호화할 때 사용된 키(N)과 비밀키(d)를
입력받습니다.
2- 출력>
입력된 키가 맞는 키라면 (d는 모듈러 합동식에 의해 산출된 값이기 때문에 여러가지 답이 있을 수 있습니다.)
복호화한 알맞는 평문을 출력합니다.


3. 암호깨기

3- 입력>
암호깨기를 시도할 암호문과 공개키 (N)를 입력합니다.
그리고 추측한 평문이 실제로 맞는지 확인하는 과정을 위해 평문을 함께 입력받습니다.
**정답을 입력받은 상태에서 암호깨기를 시도하는 것이 조금 모순적으로 보일 수 있으나 시도해본 d로 해독해본 문장이
실제로 말이 되는 문장인지 컴퓨터가 판단할 수 있는 방법을 이 방법밖에 생각해내지 못해 사람이 '이 문장이 말이 되는
문장인지'를 판단하는 과정을 대신한다고 가정하고 평문과 직접 비교를 통해 암호깨기의 성패를 가리도록 하였습니다.
3- 출력>
d를 1로 가정하고 해독해본 뒤 평문과 비교합니다. 그리고 다를 경우 d를 1증가시키고 다시
평문과 결과값이 같아질 때까지 이과정을 반복합니다.
d가 n을 넘어가면 비밀키가 존재할 수 없다는 의미이므로 잘못된 입력이라고 출력합니다.

'''
#임의의 소수 선택을 위한 random 모듈 재사용 선언
import random
#GUI 구현을 위한 tkinter 모듈 재사용 선언
from tkinter import *
from tkinter import ttk

#유클리드 호제법-> gcd 빠르게 구하기
def gcd(x, y):
    if y==0 : return x
    return gcd(y,x%y)

#공개키 만들기  
def makeKey(w,entry):
    global n,e # d는 global 변수가 아니므로 decrypt함수에서 접근할 수 없다. 사용자로 입력받은 d값만을 사용할 수 있음을 의미한다.
    #에라토스테네스의 체 -> 소수만 들어있는 배열 prime 만들기
    MAX = int(entry.get()) +1
    isPrime=[1]*MAX #0으로 갱신할 것이기 때문에 1로 초기화 해준다.
    isPrime[0]=isPrime[1]=0 #0과 1은 소수가 아니다
    prime=[]
    for i in range(2,MAX):
            if(isPrime[i]==0): continue #i가 합성수이면 지나간다
            prime.append(i) #i가 소수이면 prime 배열이 넣는다
            for j in range(i*i,MAX,i): # i가 소수이면
                    isPrime[j]=0 #i*(정수)는 합성수이다 i*(i-1)까지는 이미 이전에 값을 갱신했을 것이므로 i*i부터 반복문을 시작하여 최적화할 수 있다.

    #매우 큰 소수 p,q 랜덤 선택
    p=prime[random.randint(0,len(prime)-1)]
    q=prime[random.randint(0,len(prime)-1)]
    n = p*q
    totient = (p-1)*(q-1) #오일러 피 함수의 값

    #공개키 정하기
    for i in range(2,totient):
        if(gcd(i,totient)==1): #ppt의 암호화의 원리 부분 증명 참고
            e=i  # e : 공개키
            break

    #비밀키 정하기
    for i in range(1,totient):
        if((i*e)%totient==1) :#ppt의 복호화의 원리 부분 증명 참고
            d=i # d : 비밀키     
    t = Label(w,text="n= "+str(n)+",  e= "+str(e))
    t.pack()

    print("KEY----- n : %d, totient : %d, e : %d, d : %d, MAX: %d"%(n,totient,e,d,MAX))

#암호화 함수
def encrypt(text,w,entry,e,n):
    M = entry.get() #평문 string
    C=[]
    for i,chh in enumerate(M): #한글자씩 가져오기(몇번째 글자인지도 같이)
        ch = ord(chh) #아스키코드로 변환
        C.append(str((ch**e)%n)) #암호화 식으로 암호화 후 스트링형으로 변환
        if(i<len(M)-1): C.append('O') #글자 구분을 위해사이사이에 (끝에 제외) O넣기
    text.insert(2.0,''.join(C)+'\n')
    text.pack()
   
    
#복호화 함수
def decrypt(text, w, entry, entryn, entryd):
    C = entry.get().split('O') #암호문 list (구분문자 O 기준으로 split)
    n= int(entryn.get())
    d= int(entryd.get())
    
    MM=[]
    for chh in C: #한글자씩 가져오기
        ch = int(chh) #정수형으로 변환
        MM.append(chr((ch**d)%n)) #복호화 식으로 복호화 후 캐릭터형으로 변환

    text.insert(2.0,''.join(MM)+'\n')
    text.pack()
     
#브루트 포스로 간단한 RSA 알고리즘 깨보기
def bruteForce(text,w,entryN,entryC,entryM):
    C = entryC.get().split('O') #암호문
    M = entryM.get() #평문(비교용)
    n= int(entryN.get())
    d=1 #비밀키의 가정값
    text.insert(CURRENT,"추측중..")
    while True:
        dec = []  
        for chh in C: #한글자씩 가져오기
            ch = int(chh) #정수형으로 변환
            dec.append(chr((ch**d)%n)) #복호화 식으로 해독해보고 캐릭터형으로 변환
        guess=''.join(dec)   
        text.insert(2.0,guess+'\n')
        text.pack()
        if M == guess:
            text.insert(2.0,"!!!암호깨기 성공!!!!")
            text.pack()
            break
        d = d+1 #비밀키 갱신
################################################### GUI 구현 : tkinter 창 띄우기
#암호화하기 창 띄우기
def encryptSel():
    w1=Toplevel(window)
    w1.title("암호화하기")
    w1.geometry("250x350+100+170")
    w1.resizable(True,True)

    t2 = Label(w1,text="소수(p,q) 최대값")
    t2.pack()

    entry2 = Entry(w1, width=10)
    entry2.pack()
   
    btn1 = Button(w1,width=10, text="공개키 만들기", command=lambda : makeKey(w1,entry2)) #위젯들을 파라미터로 넘겨주어 외부 함수에서 entry 값을 받아올 수 있도록 하였다
    btn1.pack()

    t = Label(w1,text="암호화할 문장")
    t.pack()

    entry1 = Entry(w1,show="*") #암호화할 문장이니까 안보이게 show 속성 넣어주기
    entry1.pack()

    btn1 = Button(w1,width=10, text="암호문 만들기", command=lambda: encrypt(textbox, w1,entry1,e,n))
    btn1.pack()

    textbox = Text(w1)
    textbox.insert(CURRENT,"암호문: "+"\n")
    
#복호화하기 창 띄우기
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
    
#암호깨기 창 띄우기
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
    textbox.insert(CURRENT,"추측중..."+"\n")

############################시작페이지
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
