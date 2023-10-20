import json
import urllib

import easyocr
import os
import requests
import base64

#  如果本地ocr实在无法获得正确的车牌信息，那么我们就需要调用百度智能云的api
API_KEY = "zQfhOGYCOuLPwPLBckEm7p4P"
SECRET_KEY = "NKHfasd5aZRkdmIfEvgoS5KPXfEqnXg"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def get_file_content_as_base64(path, urlencoded=True):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content
def Baidu_ocr(dist):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()

    payload = 'image='+get_file_content_as_base64(dist)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    ans = json.loads(response.text)
    # print(ans)
    return ans["words_result"]

def OCR_raw(dist):

    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # need to run only once to load model into memory
    result = reader.readtext(dist, detail=1)
    tmp = ''
    for i in result:
        tmp += i
    return tmp



#设置识别中英文两种语言

def get_plate(dist):
    ans=[]
    s=os.listdir("plate/")
    for name in s:
        paths="plate/"+name
        # print(paths)
        reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # need to run only once to load model into memory
        result = reader.readtext(paths, detail=0,allowlist="·0123456789京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm")
        tmp=''
        # print(result)
        for i in result:
            tmp+=i
        if len(tmp)>=3:
            # print(tmp)
            ans.append(tmp)
    # print(ans)
    return ans

# get_plate("plate/")

def OCR_detail():
    s=['京', '津', '沪', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁', '新', '苏', '浙', '赣', '鄂', '桂', '甘', '晋', '蒙', '陕', '吉', '闽', '贵', '粤', '青', '藏', '川', '宁', '琼']
    ans=get_plate("plate/")
    anss=[]
    for plate in ans:
        print(plate)
        if plate[0]  not in s:
            continue
        #第二个位是字母
        if not plate[1].isalpha():
            continue
        #有数字
        nums=0
        for i in plate:
            if i.isdecimal():
                nums+=1
        if nums<1:
            continue
        anss.append(plate)
    print(len(anss))
    if len(anss)==0:
        #既然没有符合要求的，就调用精度更好，但是要付费的百度ocr

        print("ocr mode2")
        s = os.listdir("plate/")
        for name in s:
            paths = "plate/" + name
            print(paths)
            words=Baidu_ocr(paths)
            for tmpx in words:
                txt=tmpx["words"]
                if len(txt)>4:
                    anss.append(txt)
                    # print(txt)
    if len(anss)==0:
        return "没能成功识别该车牌"
    anss.sort(key=lambda x:len(x),reverse=True)
    tmp= anss[0]
    # print(tmp)
    if len(tmp)>=3:
        if tmp[2]!="·":
            tmp=tmp[0:2]+"·"+tmp[2:]
    return tmp


# print(OCR_detail())



# print(OCR_detail())