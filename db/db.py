import imp
from os.path import isfile
import pymysql.cursors
import time
from config.config import Database

from apscheduler.triggers.cron import CronTrigger

host=Database.host()
port=Database.port()
db=Database.db()
user=Database.user()
password=Database.password()
charset='utf8mb4'

def get_db():
    return pymysql.connect(
        host=host,
        port=port,
        db=db,
        user=user,
        password=password,
        charset=charset,
        autocommit=True
    ).cursor()
