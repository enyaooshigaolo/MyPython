# -*- coding: UTF-8 -*- 
'''
Created on 2017年1月15日

@author: Think
'''
import ctypes
import sys 
  
STD_INPUT_HANDLE = -10 
STD_OUTPUT_HANDLE = -11 
STD_ERROR_HANDLE = -12 

# Windows CMD命令行 字体颜色定义 text colors 
FOREGROUND_BLACK = 0x00 # black. 
FOREGROUND_DARKBLUE = 0x01 # dark blue. 
FOREGROUND_DARKGREEN = 0x02 # dark green. 
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue. 
FOREGROUND_DARKRED = 0x04 # dark red. 
FOREGROUND_DARKPINK = 0x05 # dark pink. 
FOREGROUND_DARKYELLOW = 0x06 # dark yellow. 
FOREGROUND_DARKWHITE = 0x07 # dark white. 
FOREGROUND_DARKGRAY = 0x08 # dark gray. 
FOREGROUND_BLUE = 0x09 # blue. 
FOREGROUND_GREEN = 0x0a # green. 
FOREGROUND_SKYBLUE = 0x0b # skyblue. 
FOREGROUND_RED = 0x0c # red. 
FOREGROUND_PINK = 0x0d # pink. 
FOREGROUND_YELLOW = 0x0e # yellow. 
FOREGROUND_WHITE = 0x0f # white. 

BACKGROUND_BLUE = 0x10 # dark blue. 
BACKGROUND_GREEN = 0x20 # dark green. 
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue. 
BACKGROUND_DARKRED = 0x40 # dark red. 
BACKGROUND_DARKPINK = 0x50 # dark pink. 
BACKGROUND_DARKYELLOW = 0x60 # dark yellow. 
BACKGROUND_DARKWHITE = 0x70 # dark white. 
BACKGROUND_DARKGRAY = 0x80 # dark gray. 
BACKGROUND_BLUE = 0x90 # blue. 
BACKGROUND_GREEN = 0xa0 # green. 
BACKGROUND_SKYBLUE = 0xb0 # skyblue. 
BACKGROUND_RED = 0xc0 # red. 
BACKGROUND_PINK = 0xd0 # pink. 
BACKGROUND_YELLOW = 0xe0 # yellow. 
BACKGROUND_WHITE = 0xf0 # white. 

# get handle 获取输出窗口的句柄 
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE) 
  
def set_cmd_text_color(color, handle=std_out_handle): 
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color) 
    return Bool 

#reset white 
def resetColor(): 
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)  

#绿色 
#green 
def printgreen(str): 
    set_cmd_text_color(FOREGROUND_GREEN) 
    sys.stdout.write(str) 
    resetColor() 
#天蓝色 
#sky blue 
def printSkyBlue(str): 
    set_cmd_text_color(FOREGROUND_SKYBLUE) 
    sys.stdout.write(str) 
    resetColor() 
#白底暗粉字 
def printWHITEDARKPINK(str): 
    set_cmd_text_color(BACKGROUND_WHITE | FOREGROUND_DARKPINK) 
    sys.stdout.write(str) 
    resetColor() 
#绿底粉字 
def printYellowPink(str): 
    set_cmd_text_color(BACKGROUND_GREEN | FOREGROUND_PINK) 
    sys.stdout.write(str) 
    resetColor() 
#黄底红字 
def printYellowRed(str): 
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED) 
    sys.stdout.write(str) 
    resetColor() 

if __name__ == '__main__':      
    print 
printSkyBlue(u'printSkyBlue:天蓝色文字\n') 
input("please press any key") 
printYellowRed(u'printYellowRed:黄底红字输出\n') 
input("please press any key") 
printYellowPink(u'printYellowPink:绿底粉字输出\n') 
input("please press any key") 
printWHITEDARKPINK(u'printWHITEDARKPINK:白底暗粉字输出\n') 