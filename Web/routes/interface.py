import base64
import re

import requests
from flask import Blueprint, session, request, render_template

from ..models.user import User, db as user_db
from ..models.course import Course, db as course_db
from ..models.detail import Detail, db as detail_db
from ..models.user_course_relation import UserCourseRelation, db as ucr_db
from ..utils import ErrorMap, JsonReturn, functions
import time
from bs4 import BeautifulSoup

interface_bp = Blueprint('interface_bp', __name__)


@interface_bp.route('/console/is_login')
def is_login():
    if not session.get("login_user_id"):
        # 不存在session
        return JsonReturn.error(ErrorMap.NOT_LOGGED)
    return JsonReturn.success(session.get("login_user_id"))


@interface_bp.route('/console/logout')
def logout():
    session.clear()
    return render_template('user_info.html')


@interface_bp.route('/console/build_status')
def build_status():
    user_id = session.get('login_user_id')
    user = User.query.filter_by(id = user_id)
    return JsonReturn.success(user.build_status)


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
                modify_time = modify_time, build_schedule = 2)
    user_db.session.add(user)
    user_db.session.commit()
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
    url = "http://gradinfo.cau.edu.cn/j_acegi_security_check;jsessionid=" + cookie
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
    login_cookie = ret.history[0].headers['Set-Cookie'].split(';')[0]
    session['login_cookie'] = login_cookie
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
        user_db.session.add(user)
        user_db.session.commit()
        # 提交后获取自增id
        user_id = user.id
    else:
        user = User.query.filter_by(j_name = name).first()
        user_id = user.id
    # 然后保存session一个月
    session.permanent = True
    session['login_user_id'] = user_id
    session['login_user_name'] = name
    result = build_schedule(login_cookie)
    if not result:
        # 插入失败
        session.clear()
        return JsonReturn.error(ErrorMap.DATA_INSERT_ERROR)
    else:
        # 更新user表
        user.build_status = 1
        user_db.session.commit()
    return JsonReturn.success()


def build_schedule(cookie):
    url = 'http://gradinfo.cau.edu.cn/studentschedule/showStudentSchedule.do?groupId=&moduleId=20101'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/index.do',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }
    ret = requests.get(url, headers = headers)
    ret = ret.text.replace("<br>", '|hh|')
    soup = BeautifulSoup(ret, "html.parser")
    table = soup.body.table
    trs = table.find_all('tr')
    del trs[0]  # 删除th行
    empty_list = []
    for tr in trs:
        tds = tr.find_all('td')
        no = tds[0].get_text(strip = True)
        name = tds[1].get_text(strip = True)
        class_no = tds[2].get_text(strip = True)
        point = tds[3].get_text(strip = True)
        week_start = tds[5].string.split('--')[0]
        week_end = tds[5].string.split('--')[1]
        create_time = int(time.time())
        modify_time = int(time.time())
        if tds[6].get_text(strip = True) == '':
            is_specail = 1
            build_status = 2
        else:
            is_specail = 2
            build_status = 1
        course = Course(no = no, name = name, class_no = class_no, point = point, week_start = week_start,
                        week_end = week_end, is_special = is_specail, build_status = build_status,
                        create_time = create_time, modify_time = modify_time)
        # 首先查询数据库看看是否已经有这个课程
        db_course = Course.query.filter_by(no = no, class_no = class_no).first()
        if not db_course:
            # 入库
            course_db.session.add(course)
            course_db.session.commit()
            course_id = course.id
        else:
            course_id = db_course.id
        ucr = UserCourseRelation(user_id = session.get("login_user_id"), course_id = course_id)
        ucr_db.session.add(ucr)
        ucr_db.session.commit()
        # 需要更进一步操作的列表
        if tds[6].get_text(strip = True) == '':
            empty_list.append({
                'course_id': course_id,
                'course_name': name,
                'class_no': class_no,
                'no': no
            })
        else:
            for location in tds[6].get_text(strip = True).split('|hh|'):
                if location == '':
                    continue
                data = location.split('-')
                weekday = data[0]
                class_start = data[1][1]
                class_end = data[2][0]
                classroom = data[3]
                detail = Detail(course_id = course_id, weekday = weekday, class_start = class_start,
                                class_end = class_end, classroom = classroom, create_time = create_time,
                                modify_time = modify_time)
                detail_db.session.add(detail)
            try:
                detail_db.session.commit()
            except Exception as e:
                detail_db.session.rollback()
                return False
    build_advanced_schedule(empty_list, cookie)
    return True


def build_advanced_schedule(class_list, cookie):
    url = 'http://gradinfo.cau.edu.cn/stuelectcourse/listCourse.do'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh,zh-CN;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '157',
        'Cookie': cookie,
        'Host': 'gradinfo.cau.edu.cn',
        'Origin': 'http://gradinfo.cau.edu.cn',
        'Referer': 'http://gradinfo.cau.edu.cn/stuelectcourse/preQueryCourse.do?groupId=&moduleId=24104',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    for course_info in class_list:
        data = {
            'paging_action': 'paging',
            'depid': '1',
            'coursecode': course_info['course_name'],
            'teacher': '',
            'courseSort': '',
            'week': '',
            'section': ''
        }
        ret = requests.post(url, data, headers = headers)
        soup = BeautifulSoup(ret.text, "html.parser")
        table = soup.body.table
        trs = table.find_all('tr')
        del trs[0]
        # 确认课程条目
        for tr in trs:
            tds = tr.find_all('td')
            no = tds[0].get_text(strip = True)
            class_no = tds[2].get_text(strip = True)
            if no == course_info['no'] and class_no == course_info['class_no']:
                # 确定是这个，入库
                classroom = tds[9].get_text(strip = True)
                create_time = int(time.time())
                modify_time = int(time.time())
                # 将这个原文添加到备注中
                course = Course.query.filter_by(id=course_info['course_id']).first()
                course.remark = tds[11].get_text(strip = True)
                course_db.session.commit()
                # 先生成列表
                for week in tds[11].get_text(strip = True).split("。")[0].split("；"):
                    # 用冒号分割天数
                    week_str = week.split('：')[0]
                    week_str = week_str.replace('第', '').replace('周', '')
                    if week_str.find('-') != -1:
                        begin = week_str.split('-')[0]
                        end = week_str.split('-')[1]
                        week_list = []
                        for i in range(int(begin), int(end) + 1):
                            week_list.append(i)
                    else:
                        week_list = [week_str]
                    days = week.split('：')[1]
                    # 分割days,
                    for w in week_list:
                        week_str = str(w)
                        last_week_day = ''
                        for day in days.split('，'):
                            if day[0] == '周':
                                weekday = day[0: 2]
                                last_week_day = weekday
                            else:
                                weekday = last_week_day
                            hour_begin = re.findall('\d+', day.split('-')[0])[0]
                            hour_end = re.findall('\d+', day.split('-')[1])[0]

                            detail = Detail(course_id = course_info['course_id'], week = week_str, weekday = weekday,
                                            class_start = hour_begin, class_end = hour_end, classroom = classroom,
                                            create_time = create_time, modify_time = modify_time)
                            detail_db.session.add(detail)
                try:
                    detail_db.session.commit()
                except Exception as e:
                    detail_db.session.rollback()
                    return False
    return True
