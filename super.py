#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import time
import vlc
import subprocess
import os
import pygame
import sys
import cv2
import numpy as NP
from PIL import Image,ImageDraw,ImageFont
os.environ['PYGAME_CAMERA']='opencv'

"""
from pygame.locals import * 
import pygame.camera as CAM
width = 645
height = 480
pygame.init()
CAM.init()
cam = CAM.Camera("/dev/video0",(width,height))
cam.start()
WSJ = pygame.display.set_mode((width,height),1,16)
pygmae.display.set_caption('Camera')
image= cam.get_image()
cam.stop()
CSJ = image
WSJ.blit(CSJ,(0,0))
pygame.display.update()
pygame.image.save(WSJ,'a.jpg')
"""

"""
import pygame
import pygame.camera
from pygame.locals import*
def capture():
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0",(1280,720))
    cam.start()
    image = cam.get_image()
    cam.stop()
    pygame.image.save(image,'a.jpg')
"""

camera = cv2.VideoCapture(0)
def capture():
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280.0)
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720.0)
    while(camera.isOpened() == False):
        print 'not opened'
    return_value, image = camera.read()
    cv2.imwrite('b.jpg', image)
#del(camera)

global g_word
global g_word_pos
global g_word_color
global g_white_beg
global g_white_end
global g_secs

def make_defaults(word,word_pos,word_color,white_beg,white_end,secs):
    global g_word,g_word_pos,g_word_color,g_white_beg,g_white_end,g_secs
    if (secs == 0) :
        g_secs = 2000
    else :
       g_secs = secs*1000
    if (word == 0) :
        g_word = "歡迎"
    else :
        g_word = word
    if (word_pos == 0) :
        g_word_pos = (375,10)
    else :
        g_word_pos = word_pos
    if (word_color == 0) :
        g_word_color = (0,150,105) #RGB
    else :
        g_word_color = word_color
    if (white_beg == 0):
        g_white_beg = (360,17)
    else :
        g_white_beg = white_beg
    if (white_end == 0):
        g_white_end = (900,69)
    else :
        g_white_end = white_end

def add_words_and_show(photo,word,word_pos,word_color,white_beg,white_end,secs):
    img=cv2.imread(photo,3)
    make_defaults(word,word_pos,word_color,white_beg,white_end,secs)
    cv2.rectangle(img,g_white_beg,g_white_end,(255,255,255),-1)
    img_pil = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    font=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',40)
    fillcolor=g_word_color
    position=g_word_pos
    Word=g_word
    if not isinstance(Word,unicode):
        Word=Word.decode('utf8')
    draw=ImageDraw.Draw(img_pil)
    draw.text(position,Word,font=font,fill=fillcolor)
    img=cv2.cvtColor(NP.asarray(img_pil),cv2.COLOR_RGB2BGR)
    cv2.namedWindow("PHO",0);
    cv2.resizeWindow("PHO", 1280,720);
    cv2.setWindowProperty('PHO',cv2.WND_PROP_FULLSCREEN,cv2.cv.CV_WINDOW_FULLSCREEN)#cv2.WINDOW_FULLSCREEN)
    cv2.imshow("PHO",img)   #show the picture
    cv2.imwrite('photo_with_word.jpg',img)#mark this if you dont want to save
    cv2.waitKey(g_secs)
    cv2.destroyAllWindows()

trigger_pin = 23
echo_pin = 24
trigger2= 27
echo2= 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trigger2,GPIO.OUT)
GPIO.setup(echo2,GPIO.IN)

def display(file_name):#play mp3 file for 5 seconds
    p = vlc.MediaPlayer(file_name)
    p.play()
#    time.sleep(5)
    return p
def close_song(p) :    
    p.stop()
#p=subprocess.Popen(["/usr/bin/vlc",file_name])
#    time.sleep(10)
# p=subprocess.Popen.kill(p)
# return 1

def send_trigger_pulse(OUT):
    GPIO.output(OUT, True)
    time.sleep(0.001)
    GPIO.output(OUT, False)
    
def wait_for_echo(value, timeout,IN):
    count = timeout
    while GPIO.input(IN) != value and count > 0:
        count = count - 1
song1="hi.mp3"
song2="bye.mp3"
def get_distance(a):
    if a==1:
        OUT=trigger_pin 
        IN=echo_pin
    else:
        OUT=trigger2
        IN=echo2
    send_trigger_pulse(OUT)
    wait_for_echo(True, 5000,IN)
    start = time.time()
    wait_for_echo(False, 5000,IN)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    distance_in = distance_cm / 2.5
    return distance_cm

def welcome(a):
    if a==1:
#        sg=display(song1)
        capture()
        sg=display(song1)
        add_words_and_show("b.jpg","Welcome to D-School@NTU!!",0,0,0,0,5)
#        sg=display(song1)
        close_song(sg)
    else:
        sg=display(song2)
        time.sleep(5)
        close_song(sg)
last_in=200
last_out=200
"""
while True:
    print get_distance(1),
    print get_distance(2)
    time.sleep(1)
"""

while True:
    time.sleep(0.8)
    rec=0
    cur_in=get_distance(1)
    cur_out=get_distance(2)
    print cur_in,cur_out
    if cur_in<=1000 and cur_in<last_in:
        welcome(1)
        rec=1
    if cur_out<=1000 and cur_out<last_out:
        welcome(2)
        rec=1
    last_in=cur_in
    last_out=cur_out
    if rec==1:
        time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()

