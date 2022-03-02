import json
import pymongo
from pymongo import MongoClient
import util
from constant import Constant


jsonfile = util.get_json_from_log(Constant.LOGFILE_DIR + "/startup.log")

dbfile = {"date": util.get_curr_date_str(), "LogfileName": "Startup.log", "logfilePath": Constant.LOGFILE_DIR,
          "timestamp": util.get_epoch(), "file": jsonfile}
util.insert_log_to_mango(dbfile)
