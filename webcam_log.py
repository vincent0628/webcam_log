# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:33:27 2020

@author: vincent
"""
import cv2
import datetime
global t

def save_log(time, status,avg=None):
    global t
    import pandas as pd
    content = {
        'date': [time],
        'option': [status],
        'pixel_value': [avg],
    }
    if status == 'dark':
        t = time+' dark'
    dataFrame =  pd.DataFrame(content)
    dataFrame.to_csv('log.csv', mode='a',index=False, header=False)
    
def main():
    global t
    # select camera
    cap = cv2.VideoCapture(0)
    status = 'open'
    flag = True
    save_log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), status)
    while(True):
        now = datetime.datetime.now()
        time = now.strftime("%Y/%m/%d %H:%M:%S")
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1) #縱向翻轉
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 平時avg為70
        avg = round(cv2.mean(gray)[0])
        # print(avg)
        if avg < 5:
            if not status == 'dark': flag = True
            status = 'dark'
        elif 55> avg > 10:
            if not status == 'bright': flag = True
            status = 'bright'
        
        elif avg > 60:
            if not status == 'light': flag = True
            status = 'light'
            
        if flag == True:
            save_log(time, status,avg)
            flag = False
              
        if status == 'dark':
            cv2.putText(frame, t, (10, 280), 
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 
                        (0, 255, 255), 1, cv2.LINE_AA)
        frame = cv2.resize(frame, (720, 480))
        cv2.putText(frame, time , (350, 50), 
                    cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 
                    (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
