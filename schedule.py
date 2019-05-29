import time 
import os 
while True: 
    print('the spider') 
    os.system("scrapy crawl tonghuashun --nolog") 
    # 12hours
    time.sleep(60 * 60 * 12)