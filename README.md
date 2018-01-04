# Intelligent-Security-Guards-based-on-Raspberry-Pi
### Author: Eric (HONGCHAO ZHANG), Mike (YUQI ZHAN) 
### Time  : 3-Jan-2018 
### The project is based on raspberry pi 3 whose system version is jessie-2016-5

# Software needed: 
1. libopencv-dev
2. python-opencv
3. mjpg_streamer

# Attention
When you upload this project on your raspberry pi, pay attention to the address used in the code.
Due to the absolute address is needed in python-opencv, the address maybe different. 
There still are some limitation in this project, such as detection algorithm and looking of the website. 

Hope you guys have fun in this interesting project

# How to run
## -step1-
run mjpg_streamer under the direction of files below
with:  ./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www"

## -step2-
use terminal to run programme below
python main.py
python control.py

## -step3-
visit:192.168.1.100:8081/web

## -step4-
Rule your room & have fun!
