import time
import urllib
import json
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
        trans()
        return 0

    elif i == '2':
        bitcoin()
        return 0

    elif i == '3':
        enigma()
        return 0

    elif i == '4':
        today_luck()
        return 0

    else:
        print("\n다시한번 숫자만 입력해주세요. \n\n")
        return 1


def trans():
    print("PapagoNMT(신경망 번역) API를 사용한 번역 기능입니다.")
    print("1. 외국어를 한국어로")
    print("2. 한국어를 외국어로")
    transel = input("\n원하는 기능의 숫자를 입력해주세요 : ")

    if transel == '1':
        print("\n\n외국어는 자동으로 인식됩니다. \n번역을 원하는 문장이나 단어를 입력하세요.\n")
        trans_text = input("입력 : ")

        sourcelan = trans_Detect_Language(trans_text)

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
            print("\n\n죄송합니다. 지원하지 않는 언어입니다. \n")
            print("지원하는 언어는 영어, 일본어, 중국어, 베트남어, 인도네시아어, 태국어, 독일어, 러시아어, 스페인어, 프랑스어 입니다.")
            exit(0)

        print("\n\n", trans_text, "\n ------번역------\n", trans_NMT(trans_text, sourcelan, "ko"))
        print("\n\n------번역완료------\n\n")

    elif transel == '2':

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

        print("\n\n", trans_text, "\n ------번역------\n", trans_NMT(trans_text, "ko", langcode))

    else:
        print("\n다시한번 입력해주세요. \n\n")
        start_menu('1')


def trans_NMT(sourcetext, sourcelan, targetlan):
    # print("Translate NMT")

    enc_text = urllib.parse.quote(sourcetext)
    data = "source=" + sourcelan + "&target=" + targetlan + "&text=" + enc_text
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        # print(response_body.decode('utf-8'))
        response_dict = json.loads(response_body.decode('utf-8'))
        # print(response_dict['message']['result']['translatedText'])

        return response_dict['message']['result']['translatedText']

    else:
        print("Error Code:" + rescode)


def trans_Detect_Language(targettext):
    # print("Translate Sel Language")

    enc_query = urllib.parse.quote(targettext)
    data = "query=" + enc_query
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response_dict = json.loads(response_body.decode('utf-8'))
        # print(response_dict[1])

        return response_dict['langCode']

    else:
        print("Error Code:" + rescode)
        return 0


def bitcoin():
    print("bitcoin")

    url = "https://blockchain.info/ticker"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        bitdata = json.loads(response_body)
        print(bitdata['KRW'])
        # {'15m': 5881078.13, 'last': 5881078.13, 'buy': 5881078.13, 'sell': 5881078.13, 'symbol': '₩'}
        '''
        손익률 계산
            -> 국밥 계산 + 최저임금 계산
        얼마야?
        '''

    else:
        print("ERROR" + rescode)


def enigma():
    print("enigma")


def today_luck():
    print("today_luck")


t = 0.1  # 원래는 0.5

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

while retry == 1:
    sel = input("\n"
                "1. 번역 - 구현 중\n"
                "2. 비트코인 환율 - 구현 예정\n"
                "3. 에니그마 - 구현 예정\n"
                "4. 오늘의 운 - 구현 예정\n"
                "원하는 메뉴를 선택하세요. : ")

    retry = start_menu(sel)
