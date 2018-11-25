# -*- coding: utf-8 -*-

class Settings():

    SELENIUM_TIMEOUT = 120
    CHROMEDRIVER_PATH = "//usr//bin//chromedriver"

    RSYNC_PRD1 = "//home//dev//Data//rsyncData//prd4"
    RSYNC_PRD2 = "//home//dev//Data//rsyncData//prd3"

    LOG_PATH = RSYNC_PRD1 + "//log"

    MONGO_URI = 'mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019'
    REPLICASET = 'repset'

    SETTINGS_HUXIU = 'huxiu'
    HUXIU = {
        'NAME': SETTINGS_HUXIU,
        'MONGO': SETTINGS_HUXIU,
        'WORK_PATH_PRD1': RSYNC_PRD1 + "//" + SETTINGS_HUXIU,
        'WORK_PATH_PRD2': RSYNC_PRD2 + "//" + SETTINGS_HUXIU,
        'FINISHED_TXT_PATH': RSYNC_PRD1 + "//" + SETTINGS_HUXIU + "//txt",
        'FINISHED_ID_PATH': RSYNC_PRD1 + "//" + SETTINGS_HUXIU + "//finished_id.csv",
        'FINISHED_CONTENT_PATH': RSYNC_PRD1 + "//" + SETTINGS_HUXIU + "//" + SETTINGS_HUXIU + "_content.csv",
        'URL_PATH': RSYNC_PRD2 + "//" + SETTINGS_HUXIU + "//" + SETTINGS_HUXIU + "_urls.csv",
        'MAX_POOL_SIZE': 2
    }

    SETTINGS_IFENG = 'ifeng'
    IFENG = {
        'NAME': SETTINGS_IFENG,
        'MONGO': SETTINGS_IFENG,
        'WORK_PATH_PRD1': RSYNC_PRD1 + "//" + SETTINGS_IFENG,
        'WORK_PATH_PRD2': RSYNC_PRD2 + "//" + SETTINGS_IFENG,
        'FINISHED_TXT_PATH': RSYNC_PRD1 + "//" + SETTINGS_IFENG + "//txt",
        'FINISHED_ID_PATH': RSYNC_PRD1 + "//" + SETTINGS_IFENG + "//finished_id.csv",
        'FINISHED_CONTENT_PATH': RSYNC_PRD1 + "//" + SETTINGS_IFENG + "//" + SETTINGS_IFENG + "_content.csv",
        'URL_PATH': RSYNC_PRD2 + "//" + SETTINGS_IFENG + "//" + SETTINGS_IFENG + "_urls.csv",
        'MAX_POOL_SIZE': 4
    }


