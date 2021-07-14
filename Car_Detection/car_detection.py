import cv2
import time
import numpy as np
# Load Yolo
def detect():
    net = cv2.dnn.readNet("Car_Detection\yolov3.weights", "Car_Detection\yolov3.cfg") #specify the path for weight and cfg file
    classes = []
    with open("Car_Detection\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    cp=cv2.VideoCapture(0) #capturing the video using camera to take pictures
    imnum=10 #image number that we are about to take
    while True:
        ret, img = cp.read()
        cv2.imshow('image show', img)
        k = cv2.waitKey(1) #wait key specifies the wait time before next frame
        # set the key for the countdown
        Timer = int(2)  #our timer in which we take the next image
        if k == ord('e'): #if e is pressed we take pic
            prev = time.time() #to take starting time  with which we know how much time passed
            while Timer >= 0:
                ret, img = cp.read()
                font = cv2.FONT_ITALIC
                cv2.putText(img, str(Timer),(50, 50), font,2, (0, 144, 170))     #showing timer on curent frame
                cv2.imshow('image show', img) #show current image
                cv2.waitKey(1)
                cur = time.time() #current time
                if (cur-prev >= 1): #checking if 1 sec has passed or not
                    prev = cur
                    Timer = Timer-1
            ret, img = cp.read()
            #cv2.imshow('clicked image', img)
            cv2.waitKey(2000)
            cv2.imwrite('./'+str(imnum)+'.png', img)
            img = cv2.imread('./'+str(imnum)+'.png')
            imnum=imnum+1
            img = cv2.resize(img, None, fx=0.4, fy=0.4)
            height, width, channels = img.shape
            # Detecting objects
            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #blob converted by yolo
            net.setInput(blob)
            outs = net.forward(output_layers)
            car,bicycle,vehicle,bus,motorbike,truck=0,0,0,0,0,0
            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)   #the one with max score is what we think is the best prediction for the detection
                    confidence = scores[class_id]
                    if confidence > 0.5:   #if the confidence on the class id is more then 50 percent we take it as a valid detection
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        print(classes[class_id])

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            #print(indexes)
            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    if(label=="car"):
                        car+=1
                        vehicle+=1
                    if(label=="truck"):
                        truck+=1
                        vehicle+=1
                    if(label=="bicycle"):
                        bicycle+=1
                        vehicle+=1
                    if(label=="bus"):
                        bus+=1
                        vehicle+=1
                    if(label=="motorbike"):
                        bus+=1
                        vehicle+=1

                    color = colors[class_ids[i]]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label, (x, y + 30), font, .9, color)
            
            cv2.waitKey(2000)  #wait 2 sec and destroy windows
            cv2.destroyAllWindows()
            break
        elif(k==27):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return car,truck,bicycle,bus,motorbike,vehicle