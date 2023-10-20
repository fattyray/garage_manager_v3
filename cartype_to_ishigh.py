import base64
import json
import urllib

import requests

API_KEY = "6YoZzlmVrUTKzZaZGa80ykAt"
SECRET_KEY = "ejoI6OGQN4s7Xpoasdd7XdXSPTdxcFt9sc"


def baidu_ishigh(paths):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/vehicle_detect?access_token=" + get_access_token()

    payload = 'image='+get_file_content_as_base64(paths)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    ans=json.loads(response.text)
    print(ans)
    tmp=ans["vehicle_num"]
    if tmp["bus"]+tmp["truck"]>=1:
        return True
    else:
        return False

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

#print(baidu_ishigh("t1.jpg"))

