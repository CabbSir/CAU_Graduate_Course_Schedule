class Config:
    SECRET_KEY = 'dssdfhs2sdd21k238sdfaksfaf32rf3'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/schedule_dev?charset=utf8'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/schedule_test?charset=utf8'


class OnlineConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/schedule_online?charset=utf8'


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': OnlineConfig,
    # 默认配置
    'default': DevConfig
}
