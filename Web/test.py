import base64

import requests

if __name__ == '__main__':
    name = "SY20213213219"
    passwd = "306186753@qq"
    captcha = ""

    url = "http://gradinfo.cau.edu.cn/j_acegi_security_check"
    data = {
        'j_username': name,
        'j_password': passwd,
        'j_captcha': captcha,
        'groupId': ''
    }
    ret = requests.post(url, data)
    print(ret.content)