__author__ = 'liyong'
import sys,re
import urllib.request
import mysql.connector
import os,platform,logging

def getIdlist(url,i):
    '''
    用正则获取指定url网页里第i页的条目所有id',返回id的list
    '''
    Idlist=[]
    try:
        postdata = urllib.parse.urlencode({'current Page': i})
        postdata = postdata.encode('utf-8')
        page = urllib.request.urlopen(url,postdata)
        html =str(page.read(),"utf-8")
        reg=re.compile(r"\[<a .*id=\"(\d+)\">查看.*\]")
        Idlist=reg.findall(html)
    except Exception as err:
        print(err)
        writeLog('访问：%s获取Idlist出错，错误为：%s'%(url,err))
    return Idlist

def writeLog(message=''):
    '''
    写日志personmore.log，写入Windows用户目录
    '''
    if platform.platform().startswith('Windows'):
        logging_file=os.path.join(os.getenv('homedrive'),os.getenv('homepath'),'personmore.log')
    else:
        logging_file=os.path.join(os.getenv('home'),'personmore.log')
    logging.basicConfig(
        level=logging.NOTSET,
        format='线程号：%(thread)d，线程名：%(threadName)s，%(asctime)s，%(message)s',
        filename=logging_file,
        filemode='w',
    )
    logging.info(message)

def getAllItems(x,y):
    '''
    获取x页至y-1页的所有失信被执行人的条目,写入mysql数据库，最后返回总条目数count
    '''
    count=0
    for i in range(x,y): #页数，根据需要填写，也可以通过正则从网页中分析出来。
        idlist = getIdlist("http://shixin.court.gov.cn/personMore.do",i)
        if len(idlist)==0:
            break
            writeLog('未匹配到idlist')
        print (idlist)
        for k in idlist: #k 是detail页面的id，每页的id
            html=getSingleItem(k)#获取单个条目json字符串
            print(html)#控制台上打印出当前条目
            html=eval(html) #字符串转dict
            insertIntoDB(**html)#写入数据库
            count+=1

    return count
def getSingleItem(id):
    '''
    获取单条失信被执行人信息（为json格式）
    :param id:单条失信被执行人的id
    :return:返回单条json数据
    '''
    jsonresult=''
    try:
        html_value="http://shixin.court.gov.cn/detail?id="+id
        jsonresult=str(urllib.request.urlopen(html_value).read(),"utf-8")
        jsonresult=jsonresult.replace("\\n","")
    except Exception as err:
        print(err)
        writeLog('访问：%s获取单条失信json时出错，错误为：%s'%(html_value,err))
    return jsonresult
def insertIntoDB(**html):
    '''
    :param html: 插入单条失信被执行人的json数据（转成dict类型数据再插入）
    :return:返回
    '''
    try:
        config = {
                'user': 'root',
                'password': 'ly123',
                'host': '127.0.0.1',
                'database': 'shixinDB',
                'raise_on_warnings': True,
                }
        cnx = mysql.connector.connect(**config)
        cursor=cnx.cursor()
        add_personMore = ("INSERT INTO personMore "
               "(id, iname,"
               " caseCode, age,"
               " sexy,cardNum,"
               "courtName,areaName,"
               "partyTypeName,gistId,"
               "regDate,gistUnit,duty,"
               "performance,disruptTypeName,"
               "publishDate) "
               "VALUES (%(id)s, %(iname)s,"
               " %(caseCode)s, %(age)s,"
               " %(sexy)s," "%(cardNum)s,"
               "%(courtName)s,""%(areaName)s,"
               "%(partyTypeName)s,%(gistId)s,"
               "%(regDate)s,%(gistUnit)s,"
               "%(duty)s,%(performance)s,"
               "%(disruptTypeName)s,%(publishDate)s)")
        cursor.execute(add_personMore, html)
        cnx.commit()
    except Exception as err:
        print(err+html)
        writeLog('插入数据库时发生错误：'+err)
        writeLog('错误条目为：'+html)
    finally:
        cursor.close()
        cnx.close()
