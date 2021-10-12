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


# 注册
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
