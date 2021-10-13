import base64

import requests
from flask import Blueprint, session, request

from ..models.user import User, db
from ..utils import ErrorMap, JsonReturn, functions
import time

interface_bp = Blueprint('interface_bp', __name__)


@interface_bp.route('/console/is_login')
def is_login():
    if not session.get("login_user_id"):
        # 不存在session
        return JsonReturn.error(ErrorMap.NOT_LOGGED)
    return JsonReturn.success(session.get("login_user_id"))


# 检查用户名是否被使用了 @Deprecated
@interface_bp.route('/console/check_name')
def check_name():
    username = request.args.get('username')
    ret = User.query.filter_by(username = username).first()
    if ret:
        return {
            'valid': False
        }
    return {
        'valid': True
    }


# 注册 @Deprecated
@interface_bp.route('/console/register', methods = ['POST'])
def register():
    username = request.form.get('username')
    ret = User.query.filter_by(username = username).first()
    if ret:
        return JsonReturn.error(ErrorMap.USER_ALREADY_REGISTERED)
    # 数据没问题入库
    ip = functions.get_real_ip()
    login_time = int(time.time())
    create_time = int(time.time())
    modify_time = int(time.time())
    user = User(username = username, last_login_ip = ip, last_login_time = login_time, create_time = create_time,
                modify_time = modify_time)
    db.session.add(user)
    db.session.commit()
    return JsonReturn.success()


# 获取cookie
def get_cookie():
    url = "http://gradinfo.cau.edu.cn/"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh',
        'Host': 'gradinfo.cau.edu.cn',
        'Proxy-Connection': 'keep - alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    ret = requests.get(url, headers = headers, allow_redirects = False)
    return ret.headers.get('Set-Cookie').split(';')[0]


# 获取验证码
@interface_bp.route('/console/captcha', methods = ['GET'])
def captcha():
    # 获取cookie存入session
    cookie = get_cookie()
    session['cookie'] = cookie
    url = 'http://gradinfo.cau.edu.cn/getCaptcha.do'
    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    ret = requests.get(url, headers = headers)
    base64_data = base64.b64encode(ret.content)
    return JsonReturn.success("data:image/png;base64," + str(base64_data, encoding = "utf-8"))


# 教务登录
@interface_bp.route('/console/login', methods = ['POST'])
def login():
    # 先验证参数
    name = request.form.get('j_username')
    passwd = request.form.get('md5_passwd')
    captcha_text = request.form.get('captcha_text')

    if name == "" or passwd == "" or len(captcha_text) != 5:
        return JsonReturn.error(ErrorMap.PARAM_INVALID)

    # 从session中获取cookie
    cookie = session.get("cookie")
    url = "http://gradinfo.cau.edu.cn/j_acegi_security_check"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '93',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Origin': 'http://gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    data = {
        'j_username': name,
        'j_password': passwd,
        'j_captcha': captcha_text,
        'groupId': ''
    }
    ret = requests.post(url, data, headers = headers)
    html = ret.text
    if html.find("研究生综合管理系统第二版") == -1:
        return JsonReturn.error(ErrorMap.LOGIN_ERROR)
    # 如果正确登入，先判断入库
    if not User.query.filter_by(j_name = name).first():
        ip = functions.get_real_ip()
        login_time = int(time.time())
        create_time = int(time.time())
        modify_time = int(time.time())
        # 这里存储的是经过md5处理的密码
        user = User(j_name = name, j_passwd = passwd, last_login_ip = ip, last_login_time = login_time,
                    create_time = create_time, modify_time = modify_time)
        db.session.add(user)
        db.session.commit()
        # 提交后获取自增id
        user_id = user.id
    else:
        user_id = User.query.filter_by(j_name = name).first().id
    # 然后保存session一个月
    session.permanent = True
    session['login_user_id'] = user_id
    session['login_user_name'] = name
    return JsonReturn.success()
