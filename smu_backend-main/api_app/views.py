# api_app/views.py
from io import BytesIO
import os, json, base64, requests
import requests
from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import re
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from api_app.models import Address
from django.conf import settings
#from .models import PDFFile
from PyPDF2 import PdfReader
from django.shortcuts import get_object_or_404
from board.models import Post, PostImage
from django.http import HttpResponseRedirect  #리턴값에필요
from .config import IROS_ID, IROS_PW, EMONEY_PWD, API_KEY, RSA_PUBLICKEY


def success(request):
    full_address = request.GET.get('fullAddress')  # GET 매개변수에서 fullAddress 값을 가져옴
    if full_address:
        # full_address가 존재할 때 Address 모델에 저장
        address_instance = Address(full_address=full_address)
        address_instance.save()

    latest_address = getaddr()
    # 템플릿에 전달할 컨텍스트 사전
    context = {
        'full_address': full_address,
        'latest_address': latest_address
    }
        
    apiKey=API_KEY
    # RSA Public Key 조회
    apiHost="https://api.tilko.net/"
    rsaPublicKey=RSA_PUBLICKEY
    # print(f"rsaPublicKey: {rsaPublicKey}")#f는 포맷임

    # AES Secret Key 및 IV 생성
    aesKey = os.urandom(16)
    aesIv = ('\x00' * 16).encode('utf-8')


    # AES Key를 RSA Public Key로 암호화
    aesCipherKey = base64.b64encode(rsaEncrypt(rsaPublicKey, aesKey))
    # print(f"aesCipherKey: {aesCipherKey}")



    ############################################################################
    #부동산 고유번호 api 호출
    nourl=apiHost +"/api/v1.0/iros/risuconfirmsimplec"
    options     = {
        "headers": {
            "Content-Type"          : "application/json",
            "API-KEY"               : apiKey,
            "ENC-KEY"               : aesCipherKey
        },
        
        "json": {
            "Address"                : latest_address, #변수로 정보를 받아와야함
            "Sangtae"              : "0",
            "KindClsFlag"             : "0",
            "Region"        : "0",
            "Page"            : "1",

        },
    }
    uniqueno_res = requests.post(nourl, headers=options['headers'], json=options['json'])
    print(f"res: {uniqueno_res.json()}")

    #str 형식 확인용 코드
    # data = uniqueno_res.json()['ResultList'][0]['UniqueNo']
    # print(type(data))
    #UniqueNo = base64.b64decode(uniqueno_res.json()['ResultList'][0]['UniqueNo']).decode("utf-8") #부동산 고유번호
    UniqueNo =uniqueno_res.json()['ResultList'][0]['UniqueNo']
    print(f"UniqueNo: {UniqueNo}")

    ##UniqueNo=base64.b64decode(uniqueno_res.json()['ResultList'][0]['UniqueNo']).decode("utf-8")


    # API URL 설정: https://tilko.net/Help/Api/POST-api-apiVersion-FssLifeplan-RegisterStep1)
    url         = apiHost + "/api/v1.0/iros/risuretrieve"
    iros_id=IROS_ID
    iros_pw=IROS_PW
    emoney_pwd=EMONEY_PWD
    #전자민원캐시 비밀번호 : hameuna1209


    # API 요청 파라미터 설정
    options     = {
        "headers": {
            "Content-Type"          : "application/json",
            "API-KEY"               : apiKey,
            "ENC-KEY"               : aesCipherKey
        },
        
        "json": {
            "IrosId"                : aesEncrypt(aesKey, aesIv, iros_id),
            "IrosPwd"              : aesEncrypt(aesKey, aesIv, iros_pw),
            "EmoneyNo1"             : aesEncrypt(aesKey, aesIv, "L8415207"),
            "EmoneyNo2"        : aesEncrypt(aesKey, aesIv, "5583" ),
            "EmoneyPwd"            : aesEncrypt(aesKey, aesIv, emoney_pwd),
            "UniqueNo"           : UniqueNo,  
            "JoinYn"           : "N",
            "CostsYn"           :"N",
            "DataYn"        :"N",
            "ValidYn":          "N",
        },
    }
    ############################################################################



    ############################################################################
    # xml API 호출
    res = requests.post(url, headers=options['headers'], json=options['json'])
    res_json = res.json()
    #print(f"res.json: {res_json}")
    res_xml=res.json()["Message"]
    t_Key = res.json()["TransactionKey"]
    print(f"t_Key: {t_Key}")



    #pdf 변환 api 호출
    get_pdf= apiHost +"api/v1.0/iros/GetPdfFile"
    options     = {
        "headers": {
            "Content-Type"          : "application/json",
            "API-KEY"               : apiKey,
            "ENC-KEY"               : aesCipherKey
        },
        
        "json": {
            "TransactionKey"                : t_Key,
            "IsSummary"              : "Y",
            
        },
    }
    getpdf_res = requests.post(get_pdf, headers=options['headers'], json=options['json'])
    pdf_string = getpdf_res.json()["Message"]
    #print("pdf_string확인용 출력 : ",pdf_string)
    #print(f"getpdf_res: {pdf_string}")


    #pdf_string = getpdf_res.json()["Message"]

    # Base64 디코딩하여 바이너리 데이터로 변환
    if isinstance(pdf_string, str):
        pdf_string = pdf_string.encode('utf-8')  
    pdf_binary_data = base64.b64decode(pdf_string)
   # print("pdf바이너리데이터 확인 :", pdf_binary_data)
    save_pdf_to_db(pdf_binary_data)


    
    #pdf url 설정
    pdf_file_url = None
      

    if Post.objects.exists():
        # 가장 최근에 업로드된 PDF 파일 가져오기
        pdf_file = Post.objects.latest('uploaded_at')
        # MEDIA_URL과 파일 이름을 결합하여 URL 생성
        # pdf_file_url = pdf_file.file_name
        
        # file_name을 기준으로 PDF 파일을 가져옴
        file_name = pdf_file.file_name
        pdf_file = get_object_or_404(Post, file_name=file_name)

        # 바이너리 데이터를 BytesIO 객체로 변환
        pdf_binary_data = pdf_file.file_data
        #print(pdf_binary_data)
        pdf_file_io = BytesIO(pdf_binary_data)
        #print(pdf_file_io)
        # PdfReader를 사용하여 PDF 파일 읽기
        reader = PdfReader(pdf_file_io)
        pages = reader.pages
        text = ""
        

        # PDF의 각 페이지에서 텍스트 추출
        for page in pages:
            sub = page.extract_text()
            text += sub

        print("\n키워드 분석 결과")

        # 분석할 키워드 목록
        keywords = ["가처분", "가압류", "압류", "가등기", "경매개시결정", "임차권등기", "신탁부동산", "근저당권설정", "근질권"]

        # 결과를 담을 리스트
        results = []
        

        # 주요 등기사항 요약(참고용) 이후의 텍스트만 분석
        start_keyword = "주요 등기사항 요약 (참고용)"
        start_index = text.find(start_keyword)

        # 시작 키워드가 발견되면 그 이후의 텍스트만 사용
        if start_index != -1:
            relevant_text = text[start_index + len(start_keyword):]
        else:
            relevant_text = ""

        #print(relevant_text)
        # 텍스트를 줄 단위로 나누기
        lines = relevant_text.splitlines()

        # 각 줄을 순회하면서 키워드가 포함된 줄을 찾기
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    clean_line = re.sub(r"^\d+(-\d+)?\s*", "", line)
                    results.append(clean_line)  # 결과를 리스트에 추가
                    break  # 각 줄에서 한 번만 출력되게 함

        if results:
            summary = "\n".join(results)  # 리스트를 문자열로 변환
            pdf_file.safety = False 
        else:
            summary = "키워드 없음"
            pdf_file.safety = True  #키워드가 없을 시에 안전함으로 바꿈
        print(summary)
        pdf_file.summary = summary
        pdf_file.save() 
        
    # 예시: 파일 업로드 뷰
    
    context = {
        'full_address': full_address,
        'latest_address': latest_address,
        'summary': summary,
    }

    #예전코드
    #return render(request, 'api_app/success.html', context)
    return HttpResponseRedirect('http://127.0.0.1:3000/Input2')

    ###########################################################################

       

    
def get_next_pdf_filename():
    """가장 최근의 PDF 파일 번호를 기반으로 다음 파일 이름 생성"""
    last_pdf_files = Post.objects.order_by('-uploaded_at')  # 업로드 날짜 기준 내림차순으로 모든 파일을 가져옴
    next_number = 1  # 기본 파일 번호는 1로 설정

    for file in last_pdf_files:
        # pdf_로 시작하는 파일을 찾으면 그 번호를 추출하고 다음 번호를 설정
        if file.file_name.startswith("pdf_"):
            last_number = int(file.file_name.split('_')[-1].replace('.pdf', ''))
            next_number = last_number + 1
            break
        elif file.file_name == "noname.pdf":
            continue  # 'noname.pdf' 파일은 건너뜀

    return f"pdf_{next_number}.pdf"




def save_pdf_to_db(pdf_binary_data):
    # 다음 파일 이름을 생성
    file_name = get_next_pdf_filename()
    # PDF 파일을 데이터베이스에 저장
    pdf_file = Post(
        file_name=file_name,
        file_data=pdf_binary_data
    )
    pdf_file.save()

#pdf 다운 로직
# def get_pdf_file(request, pdf_file_name):
#     # 파일 이름으로 PDF 파일을 가져옴
#     pdf_file = get_object_or_404(Post, file_name=pdf_file_name)
    
#     # PDF 파일 데이터를 HTTP 응답으로 반환
#     response = HttpResponse(pdf_file.file_data, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{pdf_file.file_name}"'
#     return response

    # save_pdf_to_disk(pdf_binary_data, file_name)


# def save_pdf_to_disk(pdf_binary_data, file_name):
#     # MEDIA_ROOT 경로를 사용하여 파일 경로 생성
#     file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    
#     # 바이너리 데이터를 파일로 저장
#     with open(file_path, 'wb') as f:
#         f.write(pdf_binary_data)

def getaddr():
    try:
        # 데이터베이스에서 가장 최근에 저장된 주소 불러오기
        latest_address = Address.objects.latest('id')
        print(f"Latest Address: {latest_address.full_address}")
        return latest_address.full_address
    except Address.DoesNotExist:
        print("No addresses found in the database.")
        return None
    
    
# AES 암호화 함수
def aesEncrypt(key, iv, plainText):
    def pad(text):
        text_length     = len(text)
        amount_to_pad   = AES.block_size - (text_length % AES.block_size)

        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
            
        pad     = chr(amount_to_pad)

        result  = None
        try:
            result  = text + str(pad * amount_to_pad).encode('utf-8')
        except Exception as e:
            result  = text + str(pad * amount_to_pad)

        return result
    
    if type(plainText) == str:
        plainText = plainText.encode('utf-8')
    
    plainText   = pad(plainText)
    cipher      = AES.new(key, AES.MODE_CBC, iv)
    
    if(type(plainText) == bytes):
        return base64.b64encode(cipher.encrypt(plainText)).decode('utf-8')
    else:
        return base64.b64encode(cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')


# RSA 암호화 함수(RSA 공개키로 AES키 암호화)
def rsaEncrypt(publicKey, aesKey):
    rsa             = RSA.importKey(base64.b64decode(publicKey))
    cipher          = PKCS1_v1_5.new(rsa.publickey())
    aesCipherKey   = cipher.encrypt(aesKey)
    return aesCipherKey


    # #갑을구 주요정보
    # info=apiHost +"/api/v2.0/IrosArchive/ParseXml"
    # options     = {
    #     "headers": {
    #         "Content-Type"          : "application/json",
    #         "API-KEY"               : apiKey,
    #         "ENC-KEY"               : aesCipherKey
    #     },
        
    #     "json": {
    #         "TransactionKey"                :t_Key , 
            

    #     },
    # }
    # info_res = requests.post(info, headers=options['headers'], json=options['json'])
    # #print(f"info res: {info_res.json()}")


    # # JSON 데이터를 받아온 경우에만 저장하도록 함
    # if info_res.status_code == 200:
    #     json_data = info_res.json()  # JSON 형식의 응답 데이터를 파이썬 객체로 변환

    #     # 데이터베이스에 저장
    #     json_db = JsonDb.objects.create(json_data=json_data)
    #     json_db.save()

    #     response_message = "JSON 데이터를 데이터베이스에 저장했습니다."
    # else:
    #     response_message = f"API 호출 실패: {info_res.status_code}"
    
    # try:
    #     # 데이터베이스에서 가장 최근에 저장된 JSON 데이터 가져오기
    #     json_db = JsonDb.objects.latest('created_at')
    #     json_data = json_db.json_data
        
    # except JsonDb.DoesNotExist:
    #     print("저장된 JSON 데이터가 없습니다.")
    
    # print(response_message)
    # json_string = json.dumps(json_data, indent=4, ensure_ascii=False)


    # # 테스트를 위한 텍스트 데이터
    # text_data = json_string

    # # 주소와 근저당 관련 정보 추출 / 안전한지
    # address, encumbrance_info, issafe = extract_address_and_encumbrance(text_data)

    # print("주소:", address)
   

    # for item in encumbrance_info:
    #     if item['type'] == '근저당권설정' or item['type'] == '근질권' :
    #         amount = item['amount'] if item['amount'] else '정보없음'
    #         holder = item['holder'] if item['holder'] else '정보없음'
    #         print(f"{item['type']} : {amount} {holder}")
    #     if item['type'] == '근저당권이전':
    #         holder = item['holder'] if item['holder'] else '정보없음'
            
    
    # return render(request, 'api_app/success.html', {'full_address': full_address})
    




    ############################################################################