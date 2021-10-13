import requests,schedule,time

def job():
    try:
        requests.put('http://127.0.0.1:8000/squadBlog/unblocker_post/')
        requests.put('http://127.0.0.1:8000/mohavereh/unblocker_informaltext/')
    except:
        print('error')    

schedule.every().day.at("18:34").do(job)    
while 1:
    schedule.run_pending()
    time.sleep(1)
