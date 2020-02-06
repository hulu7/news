#coding:utf-8
#------requirement------
#redis-2.10.6
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import PIL.Image as Image
import redis
import hashlib
import urllib
import re
import tarfile
import urlparse
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.mongodbMiddleware import MongoMiddleware
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.bloomfilterOnRedis import BloomFilter

class Doraemon():

    def __init__(self):
        settings = Settings()
        settings.CreateCommonSettings()
        self.file = FileIOMiddleware()
        self.rconn = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
        self.bf_urls = BloomFilter(self.rconn, settings.BLOOMFILTER_URLS)
        self.bf_content = BloomFilter(self.rconn, settings.BLOOMFILTER_CONTENT)
        self.bf_authors = BloomFilter(self.rconn, settings.BLOOMFILTER_AUTHORS)
        self.disable_restart_interval = settings.DISABLE_RESTART_INTERVAL
        self.bf_weixin_url = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_URL_ARTICLE)
        self.bf_weixin_content = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_CONTENT_ARTICLE)
        self.bf_weixin_id = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_URL_ID)
        self.bf_finished_image_id = BloomFilter(self.rconn, settings.FINISHED_IMAGE_ID)
        self.bf_finished_temp_weixin = BloomFilter(self.rconn, settings.FINISHED_TEMP_WEIXIN)
        self.md5 = hashlib.md5()
        self.max_concurrency = settings.MAX_CONCURRENCY
        self.concurrency_file = settings.CONCURRENCY_FILE
        self.concurrency_refresh_file = settings.CONCURRENCY_REFRESH_FILE
        self.refresh_concurrency_interval = settings.REFRESH_CONCURRENCY_INTERVAL
        self.max_concurrency_spider = settings.MAX_CONCURRENCY_SPIDER
        self.concurrency_file_spider = settings.CONCURRENCY_FILE_SPIDER
        self.concurrency_refresh_file_spider = settings.CONCURRENCY_REFRESH_FILE_SPIDER
        self.refresh_concurrency_interval_spider = settings.REFRESH_CONCURRENCY_INTERVAL_SPIDER
        self.bf_huxiu_nlp = BloomFilter(self.rconn, settings.FINISHED_HUXIU_NLP)

    def createFilePath(self, path):
        isFilePathExists = os.path.exists(path)
        if isFilePathExists is False:
            os.makedirs(path)

    def isExceedRestartInterval(self, path, restart_interval):
        isRestartPathExists = os.path.exists(path)
        if isRestartPathExists is False:
            print 'restart file does not exit and create an new one'
            self.file.writeToTxtCover(path, time.time())
            return True
        past = float(self.file.readFromTxt(path))
        now = time.time()
        isExceed = ((now - past) // 60 >= restart_interval) or (self.disable_restart_interval is True)
        if isExceed is True:
            print 'exceeds the restart interval and restart'
            self.file.writeToTxtCover(path, time.time())
        else:
            print 'does not exceed the restart interval and stop'
        return isExceed

    def isEmpty(self, item_list):
        return item_list !=None and len([item for item in item_list if item.strip()]) == 0

    def isTitleEmpty(self, title, url):
        if self.isEmpty(title):
            print 'Empty title for: {0}'.format(url)
            return True
        return False

    def isUrlValid(self, url, good_keys, bad_keys, regx_match_result, valid):
        if regx_match_result == None:
            print 'Invalid url for not match: {0}'.format(url)
            return False
        for good in good_keys:
            if valid == True:
                continue
            if good in url:
                print 'Match good key: {0}'.format(good)
                valid = True
        for bad in bad_keys:
            if valid == False:
                continue
            if bad in url:
                print 'Match bad key: {0}'.format(bad)
                valid = False
        return valid

    def isDuplicated(self, filter, content):
        content_encode = str(content).encode("utf-8")
        if filter.isContains(content_encode):
            print 'Content {0} duplicated!'.format(content)
            return True
        else:
            filter.insert(content_encode)
            print 'Content {0} not duplicated!'.format(content)
            return False

    def isFinished(self, filter, content):
        content_encode = str(content).encode("utf-8")
        if filter.isContains(content_encode):
            print 'Content {0} exists!'.format(content)
            return True
        else:
            return False

    def storeFinished(self, filter, content):
        print 'Start to store content: {0}'.format(content)
        content_encode = str(content).encode("utf-8")
        filter.insert(content_encode)

    def storeMongodb(self, mongo_url, data):
        mongo = MongoMiddleware()
        mongo.insert(mongo_url, data)

    def storeTxt(self, id, content, finished_txt_path, name):
        self.createFilePath(finished_txt_path)
        print 'Start to store txt: {0}'.format(id)
        self.file.writeToTxtCover('{0}//{1}_{2}.txt'.format(finished_txt_path, name, id), content)
        print 'End to store txt: {0}'.format(id)

    def storeTxtAdd(self, author_txt_path, author_name, settingName):
        self.createFilePath(author_txt_path)
        try:
            print 'Start to store txt: {0}'.format(author_name)
            self.file.writeToTxtAdd('{0}//{1}_authors.txt'.format(author_txt_path, settingName), author_name)
        except Exception as e:
            print 'Exception to store txt: {0} , for {1}'.format(author_name, e.strerror)
        print 'End to store txt: {0}'.format(author_name)

    def storeHtml(self, id, content, finished_html_path):
        self.createFilePath(finished_html_path)
        print 'Start to store html: {0}'.format(id)
        self.file.writeToHtmlCover('{0}//{1}.html'.format(finished_html_path, id), content)
        print 'End to store html: {0}'.format(id)

    def filter(self, filter, url_titles):
        new_url_titles = []
        for url_title in url_titles:
            if self.isFinished(filter, url_title[1]) is False:
                new_url_titles.append(url_title)
        return new_url_titles

    def imageFilter(self, filter, ids):
        new_ids = []
        for id in ids:
            if self.isFinished(filter, id) is False:
                new_ids.append(id)
        return new_ids

    def readNewUrls(self, filter, url_path):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(url_path)
        new_url_titles = []
        if isUrlPathExit is True:
            url_titles = np.array(self.file.readColsFromCSV(url_path, ['url', 'title']))
            new_url_titles = self.filter(filter, url_titles)
        return new_url_titles

    def readNewImageIds(self, filter, content_path):
        print 'Start to read ids'
        isContentPathExit = os.path.exists(content_path)
        new_ids = []
        id_list = []
        if isContentPathExit is True:
            ids = np.array(self.file.readColsFromCSV(content_path, ['id']))
            for id in ids:
                id_list.append(id[0])
            new_ids = self.imageFilter(filter, id_list)
        return new_ids

    def downloadImage(self, image_url, store_path):
        try:
            print 'start to download image: {0}'.format(image_url)
            urllib.urlretrieve(image_url, store_path)
        except Exception as e:
            print 'exception to download image: {0} for {1}'.format(image_url, e.message)

    def hashSet(self, name, key, value):
        self.rconn.hset(name, key, value)

    def getHashSet(self, name, key):
        return self.rconn.hget(name, key)

    def getAllHasSet(self, name):
        return self.rconn.hgetall(name)

    def delHashSet(self, name, key):
        return self.rconn.hdel(name, key)

    def delKey(self, key):
        return self.rconn.delete(key)

    def getKeyLen(self, key):
        return self.rconn.hlen(key)

    def getDateOfDaysBefore(self, days):
        return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    def getCurrentYear(self):
        return time.strftime('%Y', time.localtime(time.time()))

    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def getDateTime(self, string, dateFormat, pattern, isMatchDate):
        try:
            match = re.search(dateFormat, string)
            strp = datetime.strptime(match.group(), pattern)
            if isMatchDate:
                print "'Match date success: {0}".format(strp.date())
                return strp.date()
            else:
                print "'Match date success: {0}".format(strp.date())
                return strp.date()
        except:
            print("'Match date fail")
            return None

    def getDateFromChinese(self, string):
        year = self.getCurrentYear()
        try:
            if "今天" in string or "秒前" in string or "分钟前" in string or "小时前" in string:
                return self.getDateOfDaysBefore(0)
            if "昨天" in string or "1天前" in string:
                return self.getDateOfDaysBefore(1)
            if "前天" in string or "2天前" in string:
                return self.getDateOfDaysBefore(2)
            if "3天前" in string:
                return self.getDateOfDaysBefore(3)
            if "4天前" in string:
                return self.getDateOfDaysBefore(4)
            if "5天前" in string:
                return self.getDateOfDaysBefore(5)
            if "6天前" in string:
                return self.getDateOfDaysBefore(6)
            if "1周前" in string:
                return self.getDateOfDaysBefore(7)
            if "年" not in string and "月" in string and "日" in string:
                data = re.split(",", string.replace('月', ',').replace('日', ''))
                return "{0}-{1}-{2}".format(year, data[0], data[1])
            if "年" in string and "月" in string and "日" in string:
                data = re.split(",", string.replace('年', ',').replace('月', ',').replace('日', ','))
                return "{0}-{1}-{2}".format(data[0], data[1], data[2])
        except:
            print ("Fail to match date from Chinese.")
            return None

    def getFinalDate(self, year, month, day):
            return "{0}-{1}-{2}".format(year, month, day)

    def formateMonthDay(self, MD):
        return '{:02d}'.format(MD)

    def getDateFromString(self, string_date):
        _date_chinese = self.getDateFromChinese(string_date)
        if _date_chinese is not None:
            return _date_chinese

        _date_year_month_day_crossing = self.getDateTime(string_date, r'\d{4}-\d{1,2}-\d{1,2}', '%Y-%m-%d', True)
        _date_year2_month_day_crossing = self.getDateTime(string_date, r'\d{2}-\d{1,2}-\d{1,2}', '%y-%m-%d', True)
        _date_month_day_crossing = self.getDateTime(string_date, r'\d{1,2}-\d{1,2}', '%m-%d', True)
        _date_year_month_day_dot = self.getDateTime(string_date, r'\d{4}.\d{1,2}.\d{1,2}', '%Y.%m.%d', True)
        _date_month_day_dot = self.getDateTime(string_date, r'\d{1,2}.\d{1,2}', '%m.%d', True)
        _date_year_month_day_slash = self.getDateTime(string_date, r'\d{4}\/\d{1,2}\/\d{1,2}', '%Y/%m/%d', True)
        _date_month_day_slash = self.getDateTime(string_date, r'\d{1,2}\/\d{1,2}', '%m/%d', True)
        _time_hour_minute_second = self.getDateTime(string_date, r'\d{1,2}:\d{1,2}:\d{1,2}', '%H:%M:%S', False)
        _time_hour_minute = self.getDateTime(string_date, r'\d{1,2}:\d{1,2}', '%H:%M', False)

        year = self.getCurrentYear()

        if _date_year_month_day_crossing is not None:
            return self.getFinalDate(_date_year_month_day_crossing.year,
                                     self.formateMonthDay(_date_year_month_day_crossing.month),
                                     self.formateMonthDay(_date_year_month_day_crossing.day))
        if _date_year2_month_day_crossing is not None:
            return self.getFinalDate(_date_year2_month_day_crossing.year,
                                     self.formateMonthDay(_date_year2_month_day_crossing.month),
                                     self.formateMonthDay(_date_year2_month_day_crossing.day))
        if _date_year_month_day_crossing is None and _date_month_day_crossing is not None:
            return self.getFinalDate(year,
                                     self.formateMonthDay(_date_month_day_crossing.month),
                                     self.formateMonthDay(_date_month_day_crossing.day))

        if _date_year_month_day_dot is not None:
            return self.getFinalDate(_date_year_month_day_dot.year,
                                     self.formateMonthDay(_date_year_month_day_dot.month),
                                     self.formateMonthDay(_date_year_month_day_dot.day))
        if _date_year_month_day_dot is None and _date_month_day_dot is not None:
            return self.getFinalDate(year,
                                     self.formateMonthDay(_date_month_day_dot.month),
                                     self.formateMonthDay(_date_month_day_dot.day))

        if _date_year_month_day_slash is not None:
            return self.getFinalDate(_date_year_month_day_slash.year,
                                     self.formateMonthDay(_date_year_month_day_slash.month),
                                     self.formateMonthDay(_date_year_month_day_slash.day))
        if _date_year_month_day_slash is None and _date_month_day_slash is not None:
            return self.getFinalDate(year,
                                     self.formateMonthDay(_date_month_day_slash.month),
                                     self.formateMonthDay(_date_month_day_slash.day))

        if _time_hour_minute_second is not None or _time_hour_minute is not None:
            return self.getCurrentDate()

    def getMD5(self, content):
        self.md5.update(content.encode('utf-8'))
        return self.md5.hexdigest()

    def compressImage(self, origin_image_path, destination_image_path, multiplier):
        try:
            sImg = Image.open(origin_image_path)
            w, h = sImg.size
            dImg = sImg.resize((int(w / multiplier), int(h / multiplier)), Image.ANTIALIAS)
            os.remove(origin_image_path)
            dImg.save(destination_image_path)
            print "Compress picture {0} success!".format(destination_image_path)
        except Exception as e:
            print"Compress picture {0} failed for {1}".format(destination_image_path, e.message)

    def getSizeOfImage(self, image_path):
        try:
            img = Image.open(image_path)
            return img.size
        except Exception as e:
            print"Exception to open picture {0}, for {1}.".format(image_path, e.message)

    def getFileSize(self, file_path):
        try:
            fsize = os.path.getsize(file_path)
            fsize = fsize / float(1024)
            return round(fsize, 2)
        except Exception as e:
            print"Exception to get file size of {0}, for {1}.".format(file_path, e.message)

    def getFileList(self, diractory):
        file_list = []
        isFilePathExists = os.path.exists(diractory)
        if isFilePathExists is True:
            file_list = os.listdir(diractory)
        return file_list

    def isFileExists(self, file_path):
        return os.path.exists(file_path)

    def deleteFile(self, file_path):
        try:
            print "Start to delete file: {0}".format(file_path)
            os.remove(file_path)
            print "Finished to delete file: {0}".format(file_path)
        except Exception as e:
            print "Exception to delete file: {0} for : {1}".format(file_path, e.message)

    def tar(self, directory):
        file_list = os.listdir(directory)
        if len(file_list) == 0:
            print"There is no file to compress for: {0}".format(directory)
            return
        try:
            print "Start to compress directory: {0}".format(directory)
            t = tarfile.open(directory + ".tar.gz", "w:gz")
            for root, dir, files in os.walk(directory):
                for file in files:
                    fullpath = os.path.join(root, file)
                    t.add(fullpath)
            t.close()
            print "Finished to compress directory: {0}".format(directory)
            for file in files:
                fullpath = os.path.join(root, file)
                self.deleteFile(fullpath)
        except Exception as e:
            print "Exception to compress directory: {0} for :{1}".format(directory, e.message)

    def isCamelReadyToRun(self, settings):
        if self.isWorkTime(settings.START_TIME, settings.END_TIME) is False:
            return False
        if self.isConcurrencyAllowToRun(self.concurrency_refresh_file,
                                        self.refresh_concurrency_interval,
                                        self.concurrency_file,
                                        self.max_concurrency) is False:
            return False
        if self.isExceedRestartInterval(settings.RESTART_PATH, settings.RESTART_INTERVAL) is False:
            self.recoveryConcurrency(self.concurrency_file, self.max_concurrency)
            return False
        return True

    def isSpiderReadyToRun(self):
        return self.isConcurrencyAllowToRun(self.concurrency_refresh_file_spider,
                                            self.refresh_concurrency_interval_spider,
                                            self.concurrency_file_spider,
                                            self.max_concurrency_spider)

    def isWorkTime(self, start_time, end_time):
        if self.isEmpty(start_time):
            print 'start time is empty'
            return False
        if self.isEmpty(end_time):
            print 'end time is empty'
            return False
        if self.isAfterHour(start_time) and self.isBeforeHour(end_time):
            print 'it is work time'
            return True
        else:
            print 'it is not work time before {0} or after {1}'.format(start_time, end_time)
            return False

    def isAfterHour(self, hour):
        if self.isEmpty(hour):
            print 'input hour is empty.'
            return
        current_time = time.strftime('%H', time.localtime(time.time()))
        if int(hour) < int(current_time):
            return True
        else:
            return False

    def isBeforeHour(self, hour):
        if self.isEmpty(hour):
            print 'input hour is empty.'
            return
        current_time = time.strftime('%H', time.localtime(time.time()))
        if int(hour) > int(current_time):
            return True
        else:
            return False

    def isConcurrencyAllowToRun(self,
                                concurrency_refresh_file,
                                refresh_concurrency_interval,
                                concurrency_file,
                                max_concurrency):
        self.updateConcurrencyFile(concurrency_refresh_file,
                                   refresh_concurrency_interval,
                                   concurrency_file,
                                   max_concurrency)
        isFilePathExists = os.path.exists(concurrency_file)
        if isFilePathExists is False:
            print 'concurrency file not exists and create an new one with max concurrency: {0}'.format(str(max_concurrency))
            self.file.writeToTxtCover(concurrency_file, str(max_concurrency))
        concurrency_available = int(self.file.readFromTxt(concurrency_file).strip())
        print 'concurrency file exists : {0}'.format(str(concurrency_available))
        if int(concurrency_available) > 0:
            print 'app is able to run.'
            new_concurrency_available = concurrency_available - 1
            print 'new concurrency is : {0}'.format(str(new_concurrency_available))
            self.file.writeToTxtCover(concurrency_file, str(new_concurrency_available))
            return True
        else:
            print 'app is not able to run for no available concurrency.'
            return False
        return True

    def recoveryConcurrency(self,
                            concurrency_file,
                            max_concurrency):
        isFilePathExists = os.path.exists(concurrency_file)
        if isFilePathExists is False:
            print 'concurrency file not exists and create an new one with max concurrency: {0}'.format(str(max_concurrency))
            self.file.writeToTxtCover(concurrency_file, str(max_concurrency))
            return
        concurrency_available = int(self.file.readFromTxt(concurrency_file).strip())
        print 'concurrency file exists and start to recovery: {0}'.format(str(concurrency_available))
        if int(concurrency_available) < max_concurrency:
            print 'start to recovery concurrenct.'
            new_concurrency_available = concurrency_available + 1
            print 'new concurrency is : {0}'.format(str(new_concurrency_available))
            self.file.writeToTxtCover(concurrency_file, str(new_concurrency_available))
        else:
            print 'concurrency is not normal and write max concurrency to it.'
            self.file.writeToTxtCover(concurrency_file, str(max_concurrency))

    def updateConcurrencyFile(self,
                              concurrency_refresh_file,
                              refresh_concurrency_interval,
                              concurrency_file,
                              max_concurrency):
        if self.isExceedRestartInterval(concurrency_refresh_file, refresh_concurrency_interval) is True:
            print 'refresh concurrency file: {0}'.format(str(max_concurrency))
            self.file.writeToTxtCover(concurrency_file, str(max_concurrency))

    def createCamelData(self,
                        title,
                        url,
                        id,
                        download_time,
                        source):
        return camelDto(title,
                        url,
                        id,
                        download_time,
                        source)

    def createCamelMongoJson(self, camelDto):
        return {
            'title': camelDto.title,
            'url': camelDto.url,
            'id': camelDto.id,
            'download_time': camelDto.download_time,
            'source': camelDto.source
        }

    def createSpiderData(self,
                          url,
                          public_time,
                          author_name,
                          title,
                          id,
                          download_time,
                          source,
                          images,
                          is_open_cache,
                          content):
        return spiderDto(url,
                         public_time,
                         author_name,
                         title,
                         id,
                         download_time,
                         source,
                         images,
                         is_open_cache,
                         content)

    def createSpiderMongoJson(self, spiderDto):
        return {
            'url': spiderDto.url,
            'public_time': spiderDto.public_time,
            'author_name': spiderDto.author_name,
            'title': spiderDto.title,
            'id': spiderDto.id,
            'download_time': spiderDto.download_time,
            'source': spiderDto.source,
            'images': spiderDto.images,
            'is_open_cache': spiderDto.is_open_cache
        }

    def updateImages(self, images, newImages):
        for image in newImages:
            data = image.strip()
            if self.isEmpty(data) is False and data not in images:
                images.append(data)

    def completeImageUrls(self, newImages, current_url):
        result = []
        if len(newImages) == 0:
            print 'No images urls to process'
            return result
        for url in newImages:
            result.append(urlparse.urljoin(current_url, url).strip())
        return result

class camelDto():
    def __init__(self,
                 title,
                 url,
                 id,
                 download_time,
                 source):
        self.title = title
        self.url = url
        self.id = id
        self.download_time = download_time
        self.source = source

class spiderDto():
    def __init__(self,
                 url,
                 public_time,
                 author_name,
                 title,
                 id,
                 download_time,
                 source,
                 images,
                 is_open_cache,
                 content):
        self.url = url
        self.public_time = public_time
        self.author_name = author_name
        self.title = title
        self.id = id
        self.download_time = download_time
        self.source = source
        self.images = images
        self.is_open_cache = is_open_cache
        self.content = content

class noNameDto():
    def __init__(self,
                 page_url,
                 authors):
        self.page_url = page_url
        self.authors = authors

