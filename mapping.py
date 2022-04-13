# from numpy import *
# import sys
# import ROOT as r
# r.gROOT.SetBatch(1); 
# r.gSystem.Load("libFramework.so")




# converts the link-channel provided by the HGCROC into a 'real' channel: goes from 1 to 384, representing a SiPM each
def FpgaLinkChannel_to_realChannel(FpgaLinkChannel): #link is the chip halves, channel is just the channel
    channel = FpgaLinkChannel[2]
    if 0 <= channel and channel <= 7:  realChannel = channel
    elif 9 <= channel and channel <= 16:  realChannel = channel-1
    elif 18 <= channel and channel <= 25:  realChannel = channel-2
    elif 27 <= channel and channel <= 34:  realChannel = channel-3
    else: return None
    realChannel+=FpgaLinkChannel[1]*32
    realChannel+=(FpgaLinkChannel[0])*32*6
    return realChannel

#converts the 'real' channel into a 3 vector that describes the SiPM really well

#I'm pretty sure this one's wrong
def realChannel_to_SipM(c):#[layer,bar,side]  
    if c == None: return None  
    for i in range(1,2):
        if 0 <= c and c <= 3: return [i,c,0]
        if 4 <= c and c <= 7: return [i,c-4,1]
        if 8 <= c and c <= 11: return [i,c-4,0]
        if 12 <= c and c <= 15: return [i,c-8,1]
        c-=16
    for i in range(2,3): #this one CMB row is quite flipped
        if 0 <= c and c <= 3: return [i,3-(c),0]
        if 4 <= c and c <= 7: return [i,3-(c-4),1]
        if 8 <= c and c <= 11: return [i,3-(c-4),0]
        if 12 <= c and c <= 15: return [i,3-(c-8),1]
        c-=16                
    # for i in range(2,3):
    #     if 0 <= c and c <= 3: return [i,c,0]
    #     if 4 <= c and c <= 7: return [i,c-4,1]
    #     if 8 <= c and c <= 11: return [i,c-4,0]
    #     if 12 <= c and c <= 15: return [i,c-8,1]
    #     c-=16
    for i in range(3,10):
        if 0 <= c and c <= 3: return [i,c,0]
        if 4 <= c and c <= 7: return [i,c-4,1]
        if 8 <= c and c <= 11: return [i,c-4,0]
        if 12 <= c and c <= 15: return [i,c-8,1]
        c-=16
    for i in range(10,20): 
        if 0 <= c and c <= 3: return [i,c,0]
        if 4 <= c and c <= 7: return [i,c-4,1]
        if 8 <= c and c <= 11: return [i,c-4,0]
        if 12 <= c and c <= 15: return [i,c-8,1]
        if 16 <= c and c <= 19: return [i,c-8,0]
        if 20 <= c and c <= 23: return [i,c-12,1]
        c-=24   
    return 'too many layers'    

def realChannel_to_SipM(c):#[layer,bar,side]  
    if c == None: return None  
    for i in range(1,10):
        if 0 <= c and c <= 3: return [i,3-c,0]
        if 4 <= c and c <= 7: return [i,7-c,1]
        if 8 <= c and c <= 11: return [i,11+4-c,0]
        if 12 <= c and c <= 15: return [i,15+4-c,1]
        c-=16
    for i in range(10,20): 
        if 0 <= c and c <= 3: return [i,3-c,0]
        if 4 <= c and c <= 7: return [i,7-c,1]
        if 8 <= c and c <= 11: return [i,11+4-c,0]
        if 12 <= c and c <= 15: return [i,15+4-c,1]
        if 16 <= c and c <= 19: return [i,19+8-c,0]
        if 20 <= c and c <= 23: return [i,23+8-c,1]
        c-=24   
    return 'too many layers'    

def realChannel_to_SipM(c):#[layer,bar,side]  
    # if int(c/4)%2==0: side=0
    # elif int(c/4)%2==1: side=1
    side=int(c/4)%2
    if c in range(0,9*16): layer=int(c/16)
    if c in range(9*16,9*16+10*24): layer=int( (c-9*16)/24 )+9

    if layer in range(0,9): index =  c-layer*16-side*4
    if layer in range(9,19): index =  (c-9*16)-(layer-9)*24-side*4

    quadbar = int(index/8)
    quadbar_bar=index-quadbar*4

    if layer in (0,1,2,4,6,8,10,12,14,16,18): #if it's in a vertical layer or the flipped horizontal one
        bar = 3-quadbar_bar+quadbar*4
    if layer in (3,5,7,9,11,13,15,17): 
        bar = quadbar_bar+quadbar*4


    return [layer,bar,side]

    # if c == None: return None  

    # #layer 1
    # if c == 0: return [0,3,0]
    # if c == 1: return [0,2,0]
    # if c == 2: return [0,1,0]
    # if c == 3: return [0,0,0]
    # if c == 4: return [0,3,1]
    # if c == 5: return [0,2,1]
    # if c == 6: return [0,1,1]
    # if c == 7: return [0,0,1]

    # if c == 8: return [0,7,0]
    # if c == 9: return [0,6,0]
    # if c == 10: return [0,5,0]
    # if c == 11: return [0,4,0]
    # if c == 12: return [0,7,1]
    # if c == 13: return [0,6,1]
    # if c == 14: return [0,5,1]
    # if c == 15: return [0,4,1]

    # #layer 2 #not yet flipped
    # if c == 16: return [1,0,0]
    # if c == 17: return [1,1,0]
    # if c == 18: return [1,2,0]
    # if c == 19: return [1,3,0]
    # if c == 20: return [1,0,1]
    # if c == 21: return [1,1,1]
    # if c == 22: return [1,2,1]
    # if c == 23: return [1,3,1]

    # if c == 24: return [1,4,0]
    # if c == 25: return [1,5,0]
    # if c == 26: return [1,6,0]
    # if c == 27: return [1,7,0]
    # if c == 28: return [1,4,1]
    # if c == 29: return [1,5,1]
    # if c == 30: return [1,6,1]
    # if c == 31: return [1,7,1]

    # #layer 3 
    # if c == 32: return [2,3,0]
    # if c == 33: return [2,2,0]
    # if c == 34: return [2,1,0]
    # if c == 35: return [2,0,0]
    # if c == 36: return [2,3,1]
    # if c == 37: return [2,2,1]
    # if c == 38: return [2,1,1]
    # if c == 39: return [2,0,1]

    # if c == 40: return [2,7,0]
    # if c == 41: return [2,6,0]
    # if c == 42: return [2,5,0]
    # if c == 43: return [2,4,0]
    # if c == 44: return [2,7,1]
    # if c == 45: return [2,6,1]
    # if c == 46: return [2,5,1]
    # if c == 47: return [2,4,1]

    # #layer 4 #not yet flipped
    # if c == 48: return [4,0,0]
    # if c == 49: return [4,1,0]
    # if c == 50: return [4,2,0]
    # if c == 51: return [4,3,0]
    # if c == 52: return [4,0,1]
    # if c == 53: return [4,1,1]
    # if c == 54: return [4,2,1]
    # if c == 55: return [4,3,1]

    # if c == 56: return [4,4,0]
    # if c == 57: return [4,5,0]
    # if c == 58: return [4,6,0]
    # if c == 59: return [4,7,0]
    # if c == 60: return [4,4,1]
    # if c == 61: return [4,5,1]
    # if c == 62: return [4,6,1]
    # if c == 63: return [4,7,1]




    # if c == 8: return [0,0,0]



    
    # for i in range(1,10):
    #     if 0 <= c and c <= 3: return [i,3-c,0]
    #     if 4 <= c and c <= 7: return [i,7-c,1]
    #     if 8 <= c and c <= 11: return [i,11+4-c,0]
    #     if 12 <= c and c <= 15: return [i,15+4-c,1]
    #     c-=16
    # for i in range(10,20): 
    #     if 0 <= c and c <= 3: return [i,3-c,0]
    #     if 4 <= c and c <= 7: return [i,7-c,1]
    #     if 8 <= c and c <= 11: return [i,11+4-c,0]
    #     if 12 <= c and c <= 15: return [i,15+4-c,1]
    #     if 16 <= c and c <= 19: return [i,19+8-c,0]
    #     if 20 <= c and c <= 23: return [i,23+8-c,1]
    #     c-=24   
    # return 'too many layers'        


# realChannel_to_SipM_fast={}
# for c in range(0,385):
#     realChannel_to_SipM_fast[c] = realChannel_to_SipM(c)
# print(realChannel_to_SipM_fast)                
for c in range(0,384):
            print(c,realChannel_to_SipM(c))
