# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:33:27 2020

@author: vincent
"""
import cv2
import time
global t

def save_log(status):
    global t
    import time
    import pandas as pd
    time = time.strftime("%Y/%m/%d %H:%M:%S")
    content = {
        'date': [time],
        'option': [status],
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
    while(True):
      ret, frame = cap.read()
      frame = cv2.flip(frame, -1) #縱向翻轉
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
      # The range for a pixel's value in grayscale is (0-255), 127 lies midway
      if cv2.mean(gray)[0] < 10:
          if not status == 'dark':
              flag = True
          status = 'dark'

      else:
          if not status == 'bright':
              flag = True
          status = 'bright'
    
      if flag == True:
          save_log(status)
          flag = False
          
      if status == 'dark':
          cv2.putText(frame, t, (10, 280), 
                      cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 
                      (0, 255, 255), 1, cv2.LINE_AA)
      frame = cv2.resize(frame, (1280, 720))
      cv2.putText(frame, time.strftime("%Y/%m/%d %H:%M:%S"), (900, 50), 
                  cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 
                  (255, 255, 255), 1, cv2.LINE_AA)
      cv2.imshow('frame', frame)
    
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
