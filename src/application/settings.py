import os


"""
跨域解决
官方文档：https://fastapi.tiangolo.com/tutorial/cors/
"""
# 是否启用跨域
CORS_ORIGIN_ENABLE = True
# 只允许访问的域名列表，* 代表所有
ALLOW_ORIGINS = ["*"]
# 是否支持携带 cookie
ALLOW_CREDENTIALS = True
# 设置允许跨域的http方法，比如 get、post、put等。
ALLOW_METHODS = ["*"]
# 允许携带的headers，可以用来鉴别来源等作用。
ALLOW_HEADERS = ["*"]


SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@localhost:3306/py"
SQLALCHEMY_DATABASE_TYPE = "mysql"


"""项目根目录"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
其他项目配置
"""
# 默认密码，"0" 默认为手机号后六位
DEFAULT_PASSWORD = "0"
# 默认头像
DEFAULT_AVATAR = "https://vv-reserve.oss-cn-hangzhou.aliyuncs.com/avatar/2023-01-27/1674820804e81e7631.png"
# 默认登陆时最大输入密码或验证码错误次数
DEFAULT_AUTH_ERROR_MAX_NUMBER = 5
# 是否开启保存每次请求日志到本地
REQUEST_LOG_RECORD = True
# 是否开启每次操作日志记录到MongoDB数据库
OPERATION_LOG_RECORD = True
# 只记录包括的请求方式操作到MongoDB数据库
OPERATION_RECORD_METHOD = ["POST", "PUT", "DELETE"]
# 忽略的操作接口函数名称，列表中的函数名称不会被记录到操作日志中
IGNORE_OPERATION_FUNCTION = ["post_dicts_details"]
# access_token 过期时间，一天
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
# refresh_token 过期时间，用于刷新token使用，两天
REFRESH_TOKEN_EXPIRE_MINUTES = 1440 * 2

"""安全的随机密钥，该密钥将用于对 JWT 令牌进行签名"""
SECRET_KEY = "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=kbvqacjq75vzps$"
"""用于设定 JWT 令牌签名算法"""
ALGORITHM = "HS256"


VERSION = "1.0.0"
