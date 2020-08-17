#!/usr/bin/env python
# coding: utf-8

# In[1]:


#flask with cv2
from flask import Flask, render_template
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import pygame
from pygame import mixer

def nothing(x):
        pass

def playGuitar():
        cam=cv2.VideoCapture(0)

        mixer.init() 

        time.sleep(2)
        circle_radius = 1

        while True:
            status, frame = cam.read()

            height,width = frame.shape[:2]

            #Flipped the frame so that left hand appears on the left side and right hand appears on the right side
            frame = cv2.flip(frame,1);

            # resize the frame, blur it, and convert it to the HSV color space
            frame = imutils.resize(frame, height=300)
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # crteate a mask for the orange color and perform dilation and erosion to remove any small
            # blobs left in the mask
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            blueLower = np.array([77,95,42])
            blueUpper = np.array([255,255,255])

            mask = cv2.inRange(hsv, blueLower, blueUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            #find the contours in the frame to find the center of the object
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                # find the center from the moments 0.000001 is added to the denominator so that divide by 
                # zero exception doesn't occur
                center = (int(M["m10"] / (M["m00"]+0.000001)), int(M["m01"] / (M["m00"]+0.000001)))
                #print("center_left",center_left)
                # only proceed if the radius meets a minimum size
                if radius > circle_radius:
                    # draw the circle and centroid on the frame,
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 0, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

                    if center[0]>50 and center[0]<550 and center[1]>50 and center[1]<75:
                        cv2.putText(frame,'E {Low}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                        pygame.mixer.music.load(r'Music\Open-E-note-low-sixth-string.mp3')
                        pygame.mixer.music.play(0)

                    elif center[0]>50 and center[0]<550 and center[1]>100 and center[1]<125:
                        cv2.putText(frame,'A',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                        pygame.mixer.music.load(r'\Music\Open-A-note-fifth-string.mp3')
                        pygame.mixer.music.play(0)

                    elif center[0]>50 and center[0]<550 and center[1]>150 and center[1]<175:
                        cv2.putText(frame,'D',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
                        pygame.mixer.music.load(r'\Music\Open-D-note-fourth-string.mp3')
                        pygame.mixer.music.play(0)

                    elif center[0]>50 and center[0]<550 and center[1]>200 and center[1]<225 :
                        cv2.putText(frame,'G',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
                        pygame.mixer.music.load(r'\Music\Open-G-note-third-string.mp3')
                        pygame.mixer.music.play(0)

                    elif center[0]>50 and center[0]<550 and center[1]>250 and center[1]<275 :
                        cv2.putText(frame,'B',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)
                        pygame.mixer.music.load(r'\Music\Open-B-note-second-string.mp3')
                        pygame.mixer.music.play(0)

                    elif center[0]>50 and center[0]<550 and center[1]>300 and center[1]<325:
                        cv2.putText(frame,'E {High}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),3)
                        pygame.mixer.music.load(r'\Music\Open-E-note-high-first-string.mp3')
                        pygame.mixer.music.play(0)

            frame_copy=frame.copy()

            frame_copy = cv2.rectangle(frame_copy,(50,50),(550,75),(255,255,255),1)
            cv2.putText(frame_copy,'E {Low}',(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

            frame_copy = cv2.rectangle(frame_copy,(50,100),(550,125),(0,0,0),1)
            cv2.putText(frame_copy,'A',(50,100),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

            frame_copy = cv2.rectangle(frame_copy, (50,150),(550,175),(255,255,255),1)
            cv2.putText(frame_copy,'D',(50,150),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

            frame_copy = cv2.rectangle(frame_copy, (50,200),(550,225),(0,0,0),1)
            cv2.putText(frame_copy,'G',(50,200),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

            frame_copy = cv2.rectangle(frame_copy, (50,250),(550,275),(255,255,255),1)
            cv2.putText(frame_copy,'B',(50,250),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)

            frame_copy = cv2.rectangle(frame_copy, (50,300),(550,325),(0,0,0),1)
            cv2.putText(frame_copy,'E {High}',(50,300),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

            cv2.putText(frame_copy,'GUITAR',(150,425),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),3)

            # show the frame to our screen
            cv2.imshow("Frame", frame_copy)

            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

        # close all windows
        cam.release()
        cv2.destroyAllWindows()

def playDrums():
    cam=cv2.VideoCapture(0)

    mixer.init() 

    time.sleep(2)
    circle_radius = 1

    while True:
        status, frame = cam.read()

        height,width = frame.shape[:2]

        #Flipped the frame so that left hand appears on the left side and right hand appears on the right side
        frame = cv2.flip(frame,1);

        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, height=300)
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # crteate a mask for the orange color and perform dilation and erosion to remove any small
        # blobs left in the mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        blueLower = np.array([77,95,42])
        blueUpper = np.array([255,255,255])

        mask = cv2.inRange(hsv, blueLower, blueUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        maskLeft = mask[:,0:width//2,]
        maskRight = mask[:,width//2:,]

        #find the contours in the left frame to find the center of the object
        cntsLeft = cv2.findContours(maskLeft.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsLeft = imutils.grab_contours(cntsLeft)
        centerLeft = None

        #find the contours in the right frame to find the center of the object
        cntsRight = cv2.findContours(maskRight.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntsRight = imutils.grab_contours(cntsRight)
        centerRight = None

        if len(cntsLeft) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            c1 = max(cntsLeft, key=cv2.contourArea)
            ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            # find the center from the moments 0.000001 is added to the denominator so that divide by 
            # zero exception doesn't occur
            centerLeft = (int(M1["m10"] / (M1["m00"]+0.000001)), int(M1["m01"] / (M1["m00"]+0.000001)))
            #print("center_left",center_left)
            # only proceed if the radius meets a minimum size
            if radius1 > circle_radius:
                # draw the circle and centroid on the frame,
                cv2.circle(frame, (int(x1), int(y1)), int(radius1),(0, 0, 255), 2)
                cv2.circle(frame, centerLeft, 5, (0, 0, 255), -1)
                if centerLeft[1]>50 and centerLeft[1]<150 and centerLeft[0]>50 and centerLeft[0]<150:
                    cv2.putText(frame,'Snare',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                    #Snare= playsound(r'C:\Users\Ishan\Downloads\Snare-Drum-10.wav')
                    pygame.mixer.music.load(r'\Music\Snare-Drum-10.wav')
                    pygame.mixer.music.play(0)

                elif centerLeft[1]>150 and centerLeft[1]<250 and centerLeft[0]>175 and centerLeft[0]<275:
                    cv2.putText(frame,'Claves',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
                    #claves = playsound(r'C:\Users\Ishan\Downloads\Claves.wav')
                    pygame.mixer.music.load(r'\Music\Claves.wav')
                    pygame.mixer.music.play(0)

                elif centerLeft[0]>250 and centerLeft[0]<300 and centerLeft[1]>300 and centerLeft[1]<350:
                    cv2.putText(frame,'Kick',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
                    #kick = playsound(r'C:\Users\Ishan\Downloads\Electronic-Kick-3.wav')
                    pygame.mixer.music.load(r'\Music\Electronic-Kick-3.wav')
                    pygame.mixer.music.play(0)


        if len(cntsRight) > 0:
            c2 = max(cntsRight, key=cv2.contourArea)
            ((x2,y2), radius2) = cv2.minEnclosingCircle(c2)
            M2 = cv2.moments(c2)
            centerRight = (int(M2["m10"] / (M2["m00"]+0.000001)), int(M2["m01"] / (M2["m00"]+0.000001)))
            centerRight = (centerRight[0]+width//2,centerRight[1])
            if radius2 > circle_radius:
                cv2.circle(frame, (int(x2)+width//2, int(y2)), int(radius2),
                    (0, 255, 0), 2)
                cv2.circle(frame, centerRight, 5, (0, 255, 0), -1)
                if centerRight[0]>350 and centerRight[0]<450 and centerRight[1]>175 and centerRight[1]<275:
                    cv2.putText(frame,'Clap',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)
                    #clap = playsound(r'C:\Users\Ishan\Downloads\Clap-1.wav')
                    pygame.mixer.music.load(r'\Music\Clap-1.wav')
                    pygame.mixer.music.play(0)

                elif centerRight[0]>450 and centerRight[0]<550 and centerRight[1]>50 and centerRight[1]<150 :
                    cv2.putText(frame,'Tom',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
                    #tom = playsound(r'C:\Users\Ishan\Downloads\Electronic-Tom-1.wav')
                    pygame.mixer.music.load(r'\Music\Electronic-Tom-1.wav')
                    pygame.mixer.music.play(0)

                elif centerRight[0]>300 and centerRight[0]<350 and centerRight[1]>350 and centerRight[1]<400:
                    cv2.putText(frame,'Kick',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
                    #kick = playsound(r'C:\Users\Ishan\Downloads\Electronic-Kick-3.wav')
                    pygame.mixer.music.load(r'\Music\Electronic-Kick-3.wav')
                    pygame.mixer.music.play(0)

        frame_copy=frame.copy()

        frame_copy = cv2.rectangle(frame_copy,(50,50),(150,150),(255,255,255),1)
        cv2.putText(frame_copy,'Snare',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

        frame_copy = cv2.rectangle(frame_copy,(150,175),(250,275),(0,0,0),1)
        cv2.putText(frame_copy,'Claves',(150,175),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        frame_copy = cv2.rectangle(frame_copy, (350,175),(450,275),(0,0,0),1)
        cv2.putText(frame_copy,'Clap',(350,175),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        frame_copy = cv2.rectangle(frame_copy, (450,50),(550,150),(255,255,255),1)
        cv2.putText(frame_copy,'Tom',(450,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

        frame_copy = cv2.rectangle(frame_copy, (250,300),(350,400),(255,255,255),1)
        cv2.putText(frame_copy,'Kick',(250,300),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        
        cv2.putText(frame_copy,'DRUMS',(195,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),3)

        # show the frame to our screen
        cv2.imshow("Frame", frame_copy)

        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # close all windows
    cam.release()
    cv2.destroyAllWindows()
app=Flask(__name__)
#run_with_ngrok(app)

@app.route('/guitar')
def guitar():
    playGuitar()
    return render_template('guitar.html') 

@app.route('/piano')
def piano():
    #playPiano() //N0t yet ready...
    return render_template('piano.html')

@app.route('/drums')
def drums():
    playDrums()
    return render_template('drums.html')

@app.route('/')
def instruments():
    return render_template('instruments.html')
    
if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
