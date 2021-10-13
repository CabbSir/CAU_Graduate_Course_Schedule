import base64

import requests
from flask import Blueprint, session, request

from ..models.user import User, db
from ..utils import ErrorMap, JsonReturn, functions
import time

interface_bp = Blueprint('interface_bp', __name__)


@interface_bp.route('/console/login_status')
def login_status():
    if not session.get("user_id"):
        # 不存在session
        return JsonReturn.error(ErrorMap.NOT_LOGGED)
    # 有 session 查询数据库
    user_id = session.get("user_id")


# 检查用户名是否被使用了
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
    cookie = get_cookie()
