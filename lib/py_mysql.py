# coding: utf8
import pymysql

from lib.pr_log import logger


class PyMysql:
    def __init__(self, host, port, username, password, dbase):
        self.host = host
        self.port = int(port)
        self.user = username
        self.password = password
        self.dbase = dbase
        print( host, port, username, password, dbase)
    def connect_base(self):

        self.conn = pymysql.Connect(
            host=self.host, user=self.user, password=self.password,
            database=self.dbase, port=self.port
        )

    def read_cmd(self, sqli):
        try:
            cur = self.conn.cursor()
            result = cur.execute(sqli)
            logger.info('reslt is {}'.format(result))
            info = cur.fetchall()
            logger.info('sqli: {}result {}'.format(sqli,info))
            return info
        finally:
            cur.close()

    # def __del__(self):
    #     self.conn.close()

if __name__ == '__main__':
    db = PyMysql('rm-bp148q2xv8ye4ay3r5o.mysql.rds.aliyuncs.com', 3306, 'qateam', 'ys538741jg', 'biz')
    db.connect_base()
    db.read_cmd('select *;')