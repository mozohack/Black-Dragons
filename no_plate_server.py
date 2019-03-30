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


cap = cv.VideoCapture('videos/car.mp4')
writer = None
(W,H) = (None,None)
count =0

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
                        if Labels[classIDs[i]] == 'car':
                                cv.rectangle(frame, (x,y), (x + w, y + h), color , 2)
                                text = "{}: {:.4f}".format(Labels[classIDs[i]],confidences[i])
                                cv.putText(frame , text, (x, y-5) ,  cv.FONT_HERSHEY_SIMPLEX, 0.5, color , 2)
                                        
                                
                                motor_count =motor_count + 1
                                #ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                ROI = frame[y:y+h , x:x+w , :]
                                print(text)
                                        
                                if ROI is not False:
                                        if (y==205 and y+h==538 and x==0 and  x+w==385):
                                                ROI = frame[y+30:y+h -10, x+10:x+w -30, :]
                                                
                                                template = cv.imread('plate0.png')
                                                preprocess = "blur"
                                                image = template
                                                gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
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
                                                if " " in text:
                                                        text=text.replace(" ","")
                                                print("The Number Plate : ",text)
                                                        
                                  
                                  		
                                                db = pymysql.connect("192.168.43.104","kishore","suresh26","placemain" )
                                                #db = pymysql.connect("localhost","aj","aj","stam" )
                                                cursor = db.cursor()
                                                no = text
                                                name ='Unifast Logistics Private Ltd'
                                                location = 'SVCE'
                                                vehicle = 'car'
                                                DT = datetime.datetime.now()
                                                #sql="""CREATE TABLE DETAILS(First_NAME VARCHAR(20), Vehicle_type VARCHAR(30) , Location VARCHAR(30) , Time_stamp VARCHAR(30))"""
                                                sql1 = "INSERT INTO details(First_NAME,No_Plate, Vehicle_type, Location, Time_stamp) VALUES ('%s', '%s', '%s', '%s', '%s' )"%(name, no, vehicle,location, DT)
                                                cursor.execute(sql1)
                                                db.commit()
                                                print("Number plate pushed to database successfully")
                                                db.close()
                                                cv.imshow("Output", gray)
                                                cv.waitKey(5)
        cv.imshow("f",frame)
        cv.waitKey(1)
                                                
	
                                                                                                
						
						




   
   
   



# disconnect from server



                                                #print(text)
                                                #print(no)

                                                
                                                        
                                                
						
							
							
							
						
							
						
							
							

						# write the grayscale image to disk as a temporary file so we can
						# apply OCR to it
						
						# load the image as a PIL/Pillow image, apply OCR, and then delete
						# the temporary file
						
						
						

						# show the output images
						# cv2.imshow("Image", image)
						
						

                                        	
                                        	
                                                
                                                
                                                        
		                                
                                                                                

	
#if k ==ord('q'):
#   break

	
        
        
        
'''        if writer is None:
                # initialize our video writer
                fourcc = cv.VideoWriter_fourcc(*"MJPG")
                writer = cv.VideoWriter('output/aj.mp4', fourcc, 20,
                        (frame.shape[1], frame.shape[0]), True)

                # some information on processing single frame
                if total > 0:
                        elap = (end - start)
                        print("[INFO] single frame took {:.4f} seconds".format(elap))
                        print("[INFO] estimated total time to finish: {:.4f}".format(
                                elap * total))

        # write the output frame to disk
        writer.write(frame)
        if ROI is not False:
                cv.imshow('ROI',ROI)
                cv.waitKey(1000)
        #end = time.time()
        #elapse = 1000*(end - start)
        #print(elapse)
        
        if k==ord('q'):
                break
print("[Message] {} Motor bikes detected".format(motor_count))'''
cv.destroyAllWindows()
