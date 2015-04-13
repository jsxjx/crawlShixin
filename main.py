__author__ = 'liyong'
import spiderShiXin
import time
start_time=time.time()
message=time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))+',抓取开始!'
print(message)
spiderShiXin.writeLog(message)
count=spiderShiXin.getAllItems(1,21)
end_time=time.time()
cost_time=end_time-start_time
message=time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
message+='，抓取结束!\n共花费时间：'+str(cost_time)
message+=",共成功抓取"+str(count)+"条"
print(message)
spiderShiXin.writeLog(message)
