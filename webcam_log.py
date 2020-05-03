# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:33:27 2020

@author: vincent
"""
import cv2

def save_log(status):
    import time
    import pandas as pd
    content = {
        'date': [time.strftime("%Y/%m/%d %H:%M:%S")],
        'option': [status],
    }
    dataFrame =  pd.DataFrame(content)
    dataFrame.to_csv('log.csv', mode='a',index=False, header=False)
    
def main():
    # select camera
    cap = cv2.VideoCapture(0)
    status = 'open'
    flag = True
    while(True):
      ret, frame = cap.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
      if flag == True:
          save_log(status)
          flag = False
          
      # The range for a pixel's value in grayscale is (0-255), 127 lies midway
      if cv2.mean(gray)[0] < 10:
          if not status == 'dark':
              flag = True
          status = 'dark'
      else:
          if not status == 'bright':
              flag = True
          status = 'bright'
          
      cv2.imshow('frame', frame)
    
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
