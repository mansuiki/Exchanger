import time
import urllib.request
import json
import random
import os
import sys

'''
---------------------------------------------------------------------------

                      ##                                                   
 #####                ##                                    ##  ##    ##   
 ##     ## ##   ###  ## ##   ####  ## ##   ####   ###      ###  ##    ##   
 ##     ## ##  ##    #####  ## ##  #####  ## ##  # ##     # ##  ##    ##   
#####    ###  ##     ## ## ##  ##  ## ## ##  ## ## ##    ## ## ###   ###   
##      ###   ##    ##  #  ## ##  ##  #  ## ##  ####     ##### ##    ##    
##     ## ##  ##    ## ##  #####  ## ##  #####  ##      ##  ## ##    ##    
#####  ## ##   ###  ## ##  ## ##  ## ##  ## ##   ###    ##  ## ##### ##### 
                                            ##                             
                                         ####                              

---------------------------------------------------------------------------                                         
'''

client_id = "***REMOVED***"  # 개발자센터에서 발급받은 Client ID 값
client_secret = "***REMOVED***"  # 개발자센터에서 발급받은 Client Secret 값


def start_menu(i):
    if i == '1':
        trans() # 번역기능 호출
        return 0

    elif i == '2':
        bitcoin() # 비트코인 기능 호출
        return 0

    elif i == '3':
        enigma() # 에니그마 기능 호출
        return 0

    else:
        print("\n다시한번 숫자만 입력해주세요. \n\n")
        return 1 # 잘못입력하면 1 리턴


def trans():
    print("\n\nPapagoNMT(신경망 번역) API를 사용한 번역 기능입니다.")
    print("1. 외국어를 한국어로")
    print("2. 한국어를 외국어로")
    transel = input("\n원하는 기능의 숫자를 입력해주세요 : ")

    if transel == '1':
        # 외국어 -> 한국어 번역기능
        print("\n\n외국어는 자동으로 인식됩니다. \n번역을 원하는 문장이나 단어를 입력하세요.\n")
        trans_text = input("입력 : ")

        sourcelan = trans_Detect_Language(trans_text) # 언어를 감지 할 수 있는 api 호출후 리턴값을 받음

        # 리턴값에 따라서 안내메시지 출력

        if sourcelan == 'en':
            print("영어를 한국어로 번역합니다.")

        elif sourcelan == 'ja':
            print("일본어를 한국어로 번역합니다.")

        elif sourcelan == 'zh-ch':
            print("중국어 간체를 한국어로 번역합니다")

        elif sourcelan == 'zh-tw':
            print("중국어 번체를 한국어로 번역합니다.")

        elif sourcelan == 'vi':
            print("베트남어를 한국어로 번역합니다.")

        elif sourcelan == 'id':
            print("인도네시아어를 한국어로 번역합니다.")

        elif sourcelan == 'th':
            print("태국어를 한국어로 번역합니다.")

        elif sourcelan == 'de':
            print("독일어를 한국어로 번역합니다.")

        elif sourcelan == 'ru':
            print("러시아어를 한국어로 번역합니다.")

        elif sourcelan == 'es':
            print("스페인어를 한국어로 번역합니다")

        elif sourcelan == 'fr':
            print("프랑스어를 한국어로 번역합니다.")

        else:
            # 번역기 Api에서 사용할 수 없는 언어가 나오면 안내메시지 출력
            print("\n\n죄송합니다. 지원하지 않는 언어입니다. \n")
            print("지원하는 언어는 영어, 일본어, 중국어, 베트남어, 인도네시아어, 태국어, 독일어, 러시아어, 스페인어, 프랑스어 입니다.")
            exit(0)

        print("\n\n", trans_text, "\n ------번역------\n", trans_NMT(trans_text, sourcelan, "ko"))
        # 번역후 번역값을 출력
        print("\n\n------번역완료------\n\n")

    elif transel == '2':
        # 한국어 -> 외국어 번역 기능

        print("""\


    1.en : 영어
    2.zh-CN : 중국어 간체
    3.zh-TW : 중국어 번체
    4.es : 스페인어
    5.fr : 프랑스어
    6.vi : 베트남어
    7.th : 태국어
    8.id : 인도네시아어


    """)

        print("번역을 원하는 언어의 숫자를 선택하세요.")
        sourcelan = input("숫자입력 : ")

        # 번역을 원하는 언어를 선택 -> 그 언어의 코드로 변환

        if sourcelan == '1':
            print("한국어를 영어로 번역합니다.")
            langcode = 'en'

        elif sourcelan == '2':
            print("한국어를 중국어 간체로 번역합니다.")
            langcode = 'zh-CN'

        elif sourcelan == '3':
            print("한국어를 중국어 번체로 번역합니다.")
            langcode = 'zh-TW'

        elif sourcelan == '4':
            print("한국어를 스페인어로 번역합니다.")
            langcode = 'es'

        elif sourcelan == '5':
            print("한국어를 프랑스어로 번역합니다.")
            langcode = 'fr'

        elif sourcelan == '6':
            print("한국어를 베트남어로 번역합니다.")
            langcode = 'vi'

        elif sourcelan == '7':
            print("한국어를 태국어로 번역합니다.")
            langcode = 'th'

        elif sourcelan == '8':
            print("한국어를 인도네시아어로 번역합니다.")
            langcode = 'id'

        else:
            print("\n\n죄송합니다. 오류가 발생했습니다. \n다시 진행해주세요.\n")
            exit(0)

        trans_text = input("\n\n번역을 원하는 한국어 문장이나 단어를 입력하세요 : ")

        # 번역후 번역 결과를 출력

        print("\n\n", trans_text, "\n ------번역------\n", trans_NMT(trans_text, "ko", langcode))

    else:
        print("\n다시한번 입력해주세요. \n\n")
        start_menu('1')


def trans_NMT(sourcetext, sourcelan, targetlan):
    # 네이버 파파고 신경만기반 번역 API
    # 문자 / 문장, 번역전 언어코드, 번역후 언어코드를 입력 받고 번역 결과를 내보냄

    # 네이버 API 출력을 받아오는 부분

    enc_text = urllib.parse.quote(sourcetext)
    data = "source=" + sourcelan + "&target=" + targetlan + "&text=" + enc_text
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if rescode == 200: # 출력을 잘 받아 왔으면
        response_body = response.read()
        response_dict = json.loads(response_body.decode('utf-8')) # 처리를 위해서 딕셔너리로 변환

        return response_dict['message']['result']['translatedText'] # 번역값 반환

    else:
        print("Error Code:" + rescode)


def trans_Detect_Language(targettext):
    # 네이버 파파고 언어 인식 API
    # 문자 / 문장을 입력 받아서 언어 코드를 내보냄

    # 네이버 API 출력을 받아오는 부분

    enc_query = urllib.parse.quote(targettext)
    data = "query=" + enc_query
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if rescode == 200: # 출력을 잘 받아 왔으면
        response_body = response.read()
        response_dict = json.loads(response_body.decode('utf-8')) # 처리를 위해서 딕셔너리로 변환

        return response_dict['langCode'] # 언어코드 반환

    else:
        print("Error Code:" + rescode)
        return 0


def bitcoin():
    # 비트코인 기능

    bitdata = bitcoin_getdata() # 비트코인 시세, 마지막 거래 값등을 가지고 있는 데이터를 받아옴

    print("\n\n현재 1 비트코인은", bitdata['15m'], "원 입니다.\n\n")

    print("1. 손익률 계산")
    print("2. 예상 비트코인 구입 가능량")

    bitsel = input("원하시는 메뉴를 선택해 주세요 : ")

    if bitsel == '1':
        blackcow = float(input("\n비트코인을 구입했던 시세를 입력해주세요 : "))
        coin = float(input("구입한 비트코인의 양을 입력해주세요 : "))

        bitcoin_cal(blackcow, coin, float(bitdata['15m'])) # 비트코인 관련 계산을 위해서 함수 호출 -> 출력도 그 함수가 담당

    elif bitsel == '2':
        howmany = float(input("\n현재 얼마가 있으신가요 : "))
        bitcoin_buy(float(bitdata['15m']), howmany) # 비트코인 관현 계산을 위해서 함수 호출 -> 출력도 그 함수가 담당


def bitcoin_getdata():
    # 웹에서 비트코인 데이터를 받아오는 함수

    # 비트코인 데이터 받아오기

    url = "https://blockchain.info/ticker"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200: # 잘 받아왔으면
        response_body = response.read()

        bitdata = json.loads(response_body) # 데이터 처리를 위해서 딕셔너리로 변환

        return bitdata['KRW'] # 처리한 데이터를 반환 ----- 한국(원) 데이터만 반환함

    else:
        print("ERROR" + rescode)


def bitcoin_cal(blackcow, coin, now):
    # 비트코인 시세를 비교해서 손익률 계산을 하고 출력하는 함수

    print("\n\n현재와 과거의 시세 차이는 %.2f원 입니다." % (now - blackcow))

    plormi = (now / blackcow * 100) - 100 # 손익률 계산

    plormi_money = (now * coin) - (blackcow * coin) # 손해 / 이득본 돈을 계산

    # 손해 / 이득에 따라서 출력이 달라짐

    if plormi < 0:
        print("%.1f%%의 손해를 보셨습니다." % -plormi)
        print("%.1f원을 잃으셨습니다.\n" % -plormi_money)

        time.sleep(2)

        # 1국밥 = 6000원 -> 국밥단위로 손해 본 돈을 계산 후 출력
        print("이는 6000원 국밥 %.0f그릇을 먹을 수 있는 돈입니다." % -(plormi_money / 6000))
        # 최저시급 기준 손해 본 돈을 계산 후 출력
        print("또한 최저시급 8350원을 받을 때 %.0f시간 만큼 일해야 받을 수 있는 돈입니다." % -(plormi_money / 8350))

    elif plormi > 0:
        print("%.1f%%의 이득을 보셨습니다." % plormi)
        print("%.1f원을 얻으셨습니다.\n" % plormi_money)

        time.sleep(2)

        # 진심어린 충고!
        print("존버하지마시고 어서 비트코인을 파세요.")

    elif plormi == 0:
        print("본전은 건지셨네요.")


def bitcoin_buy(now, howmany):
    # 비트코인 현재시세로 살수 있는 비트코인 계수를 출력하는 함수

    print("\n\n현재 비트코인 시세는 약 %.0f원 입니다." % now) # 시세 출력
    # 귀입가능한 비트코인 개수 출력
    print("%.0f원으로 구입할 수 있는 비트코인 양은 약 %.4f개 입니다." % (howmany, howmany / now))


def enigma():
    # 에니그마 기능을 수행하는 함수
    # 에니그마를 구현해 보았음

    # 기본적인 알파벳 순서
    Default = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # 에니그마안에 들어가 있는 로터들
    Rotor = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', \
             'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'JPGVOUMFYQBENHZRDKASXLICTW', \
             'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'FKQHTLXOCBJSPDZRAMEWNIUYGV']
    # 순서대로 1, 2, 3, 4, 5, 6, 7, 8 로터

    # 에니그마안에 들어가 있는 리플렉터들
    Reflector = ['EJMZALYXVBWFCRQUONTSPIKHGD', 'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'FVPJIAOYEDRZXWGCTKUQSBNMHL']
    # 순서대로 A, B, C 형 반사체

    print("\n\n에니그마를 파이썬에서 구현해보았습니다.\n\n")
    print("1. 에니그마를 활용한 암호화")
    print("2. 암호화된 문장을 원래 평문으로 복호화")

    enisel = input("원하는 기능을 입력해주세요 : ")

    if enisel == '1':
        origin = input("\n\n암호화를 원하는 영어 단어나 문장을 입력하세요\n입력형식 : 'ORANGE', 'I LIKE APPLE'\n입력 : ")

        SelRotor1 = random.randrange(0, 7) # 첫번째 로터 무작위 추출

        SelRotor2 = random.randrange(0, 7) # 두번째 로터 무작위 추출

        while SelRotor2 == SelRotor1: # 만약 첫번째와 두번째가 같다면
            SelRotor2 = random.randrange(0, 7) # 다시추출

        SelRotor3 = random.randrange(0, 7) # 세번째 로터 무작위 추출

        while ((SelRotor3 == SelRotor1) or (SelRotor3 == SelRotor2)): # 둘중 하나라도 같다면
            SelRotor3 = random.randrange(0, 7) # 다시추출

        SelReflector = random.randrange(0, 2) # 리플렉터 추출

        if SelReflector == 0: # 숫자는 보기 힘드니 영어로 출력 해주자
            ASelReflector = 'A'

        elif SelReflector == 1:
            ASelReflector = 'B'

        elif SelReflector == 2:
            ASelReflector = 'C'

        # 리스트 값은 0부터 시작하므로 1 더해서 출력
        print("\n\nRotor1는 '%d'이 Rotor2는 '%d'이 Rotor3는 '%d'이 Reflector는 '%s'가 선택되었습니다.\n" % (SelRotor1 + 1, \
                                                                                             SelRotor2 + 1, \
                                                                                             SelRotor3 + 1, \
                                                                                             ASelReflector))

        print("이 값을 기록해 주세요.")
        input("기록하셨다면 아무키를 눌러 주세요.")

        # 암호화를 위해서 로터 리스트를 만듬 (뒤쪽은 얼마나 당겨주나 차이) -> 이값은 아무렇게 변형해도 상관 없음
        Rotor1 = [Rotor[SelRotor1], 1]
        Rotor2 = [Rotor[SelRotor2], 2]
        Rotor3 = [Rotor[SelRotor3], 3]

        # 암호화 기능 수행
        enc = enigma_enc(Rotor1, Rotor2, Rotor3, Reflector[SelReflector], Default, origin, 0)

        # 암호화 전 문장과 암호화된 문장을 출력
        print("\n\n암호화된 '%s' 는 '%s' 입니다." % (origin, enc))

    elif enisel == '2':
        origin = input("\n\n복호화를 원하는 암호화된 단어나 문장을 입력하세요\n입력 : ")

        # 암호화 부분에서 1를 더해서 출력 했으므로 1을 빼줌
        SelRotor1 = int(input("\nRotor1을 입력해 주세요 : ")) - 1
        SelRotor2 = int(input("\nRotor2을 입력해 주세요 : ")) - 1
        SelRotor3 = int(input("\nRotor3을 입력해 주세요 : ")) - 1

        SelReflector = input("\nReflector을 입력해 주세요 : ")

        # 암호화 부분에서 영어로 출력 했으므로 다시 숫자로 변환
        if SelReflector == 'A':
            SelReflector = 0
        elif SelReflector == 'B':
            SelReflector = 1
        elif SelReflector == 'C':
            SelReflector = 2
        else:
            print("ERROR")
            exit(0)

        # 복호화를 위해서 복호화 리스트를 만듬 (뒤쪽은 얼마나 당겨주나 차이) -> 이값은 암호화때 정한 값이랑 같아야 함
        Rotor1 = [Rotor[SelRotor1], 1]
        Rotor2 = [Rotor[SelRotor2], 2]
        Rotor3 = [Rotor[SelRotor3], 3]

        # 복호화 수행
        dec = enigma_enc(Rotor1, Rotor2, Rotor3, Reflector[SelReflector], Default, origin, 1)

        # 복호화 전 문장과 암호화된 문장을 출력
        print("\n\n복호화된 '%s' 는 '%s' 입니다." % (origin, dec))


def enigma_enc(Rotor1, Rotor2, Rotor3, Reflector, Default, origin, ende):
    # 에니그마 암호화, 복호화를 담당하는 함수
    # 순서대로 각각의 로터의 리스트, 리플랙터 값, 기본 알파벳 순서값, 원래 문장, 암호화 / 복호화 설정
    # ende 가 0 이면 암호화 ////// 1이면 복호화

    origin = origin.upper()  # 대문자로 변환

    encorigin = []  # 암호화된 값을 받기 위한 리스트

    list1 = list(Rotor1[0])  # 치환을 하기위해서 리스트 먼저 대입
    list2 = list(Rotor2[0])
    list3 = list(Rotor3[0])

    rot1 = Rotor1[1] # 돌아가는 횟수
    rot2 = Rotor2[1]
    rot3 = Rotor3[1]

    dict1 = {} # 치환값을 담을 딕셔너너리
    dict2 = {}
    dict3 = {}
    refle = {}

    # 암호화 / 복호화를 위한 치환 딕셔너리 작성 부분
    if ende == 0:
        for i in range(0, 4, 1):
            alphabet = list(Default)
            z = 0

            for a in range(len(Default)):
                if i == 0:
                    if z == 0:
                        for b in range(rot1):
                            alphabet.append(alphabet[0]) # 기본 알파벳 순서를 rot값에 따라서 돌림
                            del alphabet[0]
                        z = 1

                    dict1.setdefault(list1[a], alphabet[a]) # 치환 딕셔너리 작성

                elif i == 1:
                    if z == 0:
                        for b in range(rot2):
                            alphabet.append(alphabet[0])
                            del alphabet[0]
                        z = 1

                    dict2.setdefault(list2[a], alphabet[a])

                elif i == 2:
                    if z == 0:
                        for b in range(rot3):
                            alphabet.append(alphabet[a])
                            del alphabet[0]
                        z = 1

                    dict3.setdefault(list3[a], alphabet[a])

                elif i == 3:
                    refle.setdefault(Reflector[a], alphabet[a])

    else:
        for i in range(0, 4, 1):
            alphabet = list(Default)
            z = 0

            for a in range(len(Default)):
                if i == 0:
                    if z == 0:
                        for b in range(rot1):
                            alphabet.append(alphabet[0]) # 기본 알파벳 순서를 rot값에 따라서 돌림
                            del alphabet[0]
                        z = 1

                    dict1.setdefault(alphabet[a], list1[a]) # 치환 딕셔너리 작성

                elif i == 1:
                    if z == 0:
                        for b in range(rot2):
                            alphabet.append(alphabet[0])
                            del alphabet[0]
                        z = 1

                    dict2.setdefault(alphabet[a], list2[a])

                elif i == 2:
                    if z == 0:
                        for b in range(rot3):
                            alphabet.append(alphabet[a])
                            del alphabet[0]
                        z = 1

                    dict3.setdefault(alphabet[a], list3[a])

                elif i == 3:
                    refle.setdefault(alphabet[a], Reflector[a])

    # 딕셔너리를 가지고 암호화 / 복호화를 수행하는 부분

    for i in range(0, len(origin), 1):
        if origin[i] not in Default:
            encorigin.append(origin[i]) # 처리할수 없는 문자들이라면 그대로 다시 리턴
        else:
            enc = origin[i] # 처음부터 순서대로 한글자 씩 대입

            enc = dict1[enc] # dict1에 따라서 치환
            enc = dict2[enc] # 치환
            enc = dict3[enc] # 치환
            enc = refle[enc] # 치환
            enc = dict3[enc] # 치환
            enc = dict2[enc] # 치환
            enc = dict1[enc] # 치환

            encorigin.append(enc) # 반환할 출력값에 한글자식 추가

    encstr = ''.join(encorigin) # 문자열로 반환하기 위해서 문자열로 치환

    return encstr # 반환


t = 0.2  # 처음 로딩화면 속도 조절 // 0.2 가 초기값

time.sleep(t)
print("---------------------------------------------------------------------------")
time.sleep(t)
print("                      ##                                                   ")
time.sleep(t)
print(" #####                ##                                    ##  ##    ##   ")
time.sleep(t)
print(" ##     ## ##   ###  ## ##   ####  ## ##   ####   ###      ###  ##    ##   ")
time.sleep(t)
print(" ##     ## ##  ##    #####  ## ##  #####  ## ##  # ##     # ##  ##    ##   ")
time.sleep(t)
print("#####    ###  ##     ## ## ##  ##  ## ## ##  ## ## ##    ## ## ###   ###   ")
time.sleep(t)
print("##      ###   ##    ##  #  ## ##  ##  #  ## ##  ####     ##### ##    ##    ")
time.sleep(t)
print("##     ## ##  ##    ## ##  #####  ## ##  #####  ##      ##  ## ##    ##    ")
time.sleep(t)
print("##     ## ##  ##    ## ##  #####  ## ##  #####  ##      ##  ## ##    ##    ")
time.sleep(t)
print("#####  ## ##   ###  ## ##  ## ##  ## ##  ## ##   ###    ##  ## ##### ##### ")
time.sleep(t)
print("                                            ##                             ")
time.sleep(t)
print("                                         ####                              ")
time.sleep(t)
print("---------------------------------------------------------------------------\n\n\n\n")
time.sleep(t)

retry = 1

while retry == 1: # 메뉴 선택 부분
    sel = input("\n"
                "1. 번역 - 구현 끝\n"
                "2. 비트코인 환율 - 구현 끝\n"
                "3. 에니그마 - 구현 끝\n"
                "원하는 메뉴를 선택하세요. : ")

    retry = start_menu(sel) # 함수 실행후 리턴값이 계속 1이라면 반복
