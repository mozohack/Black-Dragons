import cv2 as cv
import numpy as np
import time
from matplotlib import pyplot as plt
import os
from PIL import Image
import pytesseract
import argparse
import pymysql
import datetime

plate_timing=1
plate_threshold=0.8

CONFIDENCE = 0.5
THRESHOLD = 0.3

weights_path = "yolo/yolov3.weights"
config_path = "yolo/yolov3.cfg"
label_path = "yolo/coco.names"
Labels = open(label_path).read().strip().split("\n")
motor_count = 0


#colors
np.random.seed(42)
colours = np.random.randint(0,255, size = (len(Labels),3), dtype = "uint8")

print("[Message]Loading the yolo detector")
net = cv.dnn.readNetFromDarknet(config_path,weights_path)
ln = net.getLayerNames()
ln = [ln[i[0]-1] for i in net.getUnconnectedOutLayers()]


cap = cv.VideoCapture('videos/maingate.avi')
writer = None
(W,H) = (None,None)
count =0
name="Aj"
vehicle="Bus"
location="SVCE"
db = pymysql.connect("192.168.43.104","kishore","suresh26","placemain" )
cursor = db.cursor()



try:
        length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        print("[Message] {} total number of frames in the video".format(length)) 
        
except:
        print("[Message] Could'nt determine the number of frames in the video")
        total = -1

while True:
        ret, frame = cap.read()
        count += 10
        cap.set(1,count)
        
        if not ret:
                break
        
        if W is None or H is None:
                (H,W) = frame.shape[:2]
                #print(frame.shape)
        
        blob = cv.dnn.blobFromImage(frame, 1/255.0, (416,416), swapRB = True, crop = False)
        # forward the blob to the network
        net.setInput(blob)
        
        
        layerOutputs = net.forward(ln)
        boxes = []
        confidences =[]
        classIDs = []
        
        for output in layerOutputs:
                for detection in output:
                        scores = detection[5:]
                        classID = np.argmax(scores)
                        confidence = scores[classID]
                        
                        if confidence > CONFIDENCE:
                                box = detection[0:4] * np.array([W,H,W,H])
                                (centerX, centerY, width, height) = box.astype("int")
                                
                                x = int(centerX - (width/2))
                                y = int(centerY - (height/2))
                                
                                boxes.append( [x,y,int(width), int(height)])
                                confidences.append(float(confidence))
                                classIDs.append(classID)
                                
        idxs = cv.dnn.NMSBoxes(boxes, confidences , CONFIDENCE , THRESHOLD)
                        
        if len(idxs) > 0:
                for i in idxs.flatten():
                        (x,y) = (boxes[i][0], boxes[i][1])
                        (w,h) = (boxes[i][2], boxes[i][3])
                        color = [int(c) for c in colours[classIDs[i]]]
                        if Labels[classIDs[i]] == 'bus':
                                cv.rectangle(frame, (x,y), (x + w, y + h), color , 2)
                                text = "{}: {:.4f}".format(Labels[classIDs[i]],confidences[i])
                                cv.putText(frame , text, (x, y-5) ,  cv.FONT_HERSHEY_SIMPLEX, 0.5, color , 2)
                                        

                                
                                motor_count =motor_count + 1
                                #ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                ROI = frame[y:y+h , x:x+w , :]
                                print(text)
                                resized_image = cv.resize(frame, (100, 50))
                                	
					
                                
                                if ROI is not False:
                                        #print(y,y+h,x,x+w)


                                        if (y==38 and y+h==899 and x==410 and  x+w==1420):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot8_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold =plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)

                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                
                                                name ='Unifast Logistics Private Ltd'
                                                location = 'SVCE'
                                                vehicle = 'car'
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()



                                        if (y==12 and y+h==1063 and x==-32 and  x+w==1291):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot8_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)


                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()


                                        if (y==77 and y+h==780 and x==412 and  x+w==1269):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot7_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)

                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()

                                        
                                        if (y==54 and y+h==1055 and x==-44 and  x+w==1316):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot6_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()



					
                                        if (y==73 and y+h==720 and x==580 and  x+w==1358):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot5_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()



                                        
                                        if (y==54 and y+h==1035 and x==3 and  x+w==1252):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot4_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()

                                        
                                        if (y==69 and y+h==729 and x==664 and  x+w==1372):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot3_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()
                                                

                                        
                                        if (y==81 and y+h==679 and x==612 and  x+w==1352):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot2_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()
                                                

                                        
                                        if (y==157 and y+h==281 and x==417 and  x+w==532):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot2_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)

                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if "T" not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, text, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()


                                        if (y==127 and y+h==295 and x==508 and  x+w==916):#y+!
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                
                                                main_image = ROI
                                                gray_image = cv.cvtColor(main_image, cv.COLOR_BGR2GRAY)
                                                #open the template as gray scale image
                                                template = cv.imread('svce_templates/Screenshot_.png', 0)
                                                width, height = template.shape[::-1] #get the width and height
                                                #match the template using cv2.matchTemplate
                                                match = cv.matchTemplate(gray_image, template, cv.TM_CCOEFF_NORMED)
                                                threshold = plate_threshold
                                                position = np.where(match >= threshold) #get the location of template in the image
                                                for point in zip(*position[::-1]): #draw the rectangle around the matched template
                                                   cv.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
                                                cv.waitKey(plate_timing)
                                                preprocess = "blur"
                                                image = template
                                                gray = image
                                                cv.imshow("Image", gray)
                                                if preprocess == "thresh":
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        tamilnadu="TN"
                                                        gray = cv.medianBlur(gray, 3)
                                                elif preprocess=="blur":
                                                        gray = cv.medianBlur(gray, 3)
                                                        tamilnadu="TN"
                                                        gray = cv.threshold(gray, 0, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                                                        gray = cv.medianBlur(gray, 3)

                                                filename="{}.png".format(os.getpid())
                                                cv.imwrite(filename, gray)
                                                
                                                text = pytesseract.image_to_string(Image.open(filename))
                                                os.remove(filename)
                                                if tamilnadu not in text:
                                                        text=tamilnadu+text
                                                if "]" in text:
                                                        text= text.replace("]", "")
                                                if "-" in text:
                                                        text=text.replace("-","")
                                                if " " in text or ":" in text:
                                                        text=text.replace(" ","")
                                                print("No_plate: ",text)
                                                cv.imshow("Output", gray)
                                                cv.waitKey(1)
                                                
                                                print("Number plate pushed to database successfully")
                                                #db.close()

												
							
							
						
							
						
							
							

						# write the grayscale image to disk as a temporary file so we can
						# apply OCR to it
						
						# load the image as a PIL/Pillow image, apply OCR, and then delete
						# the temporary file
						
						
						

						# show the output images
						# cv2.imshow("Image", image)
						
						

                                        	
                                        	
                                                
                                                
                                                        
		                                
                                                                                

        cv.imshow('frame' , frame)
        k=cv.waitKey(1)
        if k ==ord('q'):
                break

	
        
        
        
        if writer is None:
                # initialize our video writer
                fourcc = cv.VideoWriter_fourcc(*"MJPG")
                writer = cv.VideoWriter('output/aj.mp4', fourcc, 20,
                        (frame.shape[1], frame.shape[0]), True)

                # some information on processing single frame
                '''if total > 0:
                        elap = (end - start)
                        print("[INFO] single frame took {:.4f} seconds".format(elap))
                        print("[INFO] estimated total time to finish: {:.4f}".format(
                                elap * total))'''

        # write the output frame to disk
        writer.write(frame)
        '''if ROI is not False:
                cv.imshow('ROI',ROI)
                cv.waitKey(1000)'''
        #end = time.time()
        #elapse = 1000*(end - start)
        #print(elapse)
        
        if k==ord('q'):
                break
print("[Message] {} Motor bikes detected".format(motor_count))
cv.destroyAllWindows()












'''
import cv2
import numpy as np
#open the main image and convert it to gray scale image
main_image = cv2.imread('main_image.png')
gray_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
#open the template as gray scale image
template = cv2.imread('template1.png', 0)
width, height = template.shape[::-1] #get the width and height
#match the template using cv2.matchTemplate
match = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
position = np.where(match >= threshold) #get the location of template in the image
for point in zip(*position[::-1]): #draw the rectangle around the matched template
   cv2.rectangle(main_image, point, (point[0] + width, point[1] + height), (0, 204, 153), 0)
cv2.imshow('Template Found', main_image)
cv2.waitKey(0)
'''                                                     
                                     
						

