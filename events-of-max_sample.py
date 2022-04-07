from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)



#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfPEs=30
r.gStyle.SetOptStat("ne")

allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

NumberOfTimestamps = max([t.i_sample for t in allData])+1 #takes a while
print('There are',NumberOfTimestamps,'timestamps')
hist =  r.TH1F('', "max sample count", NumberOfTimestamps+1, -1, NumberOfTimestamps,) #-1 in case everything is 0 adc

#Gets data from interesting events
maxADC=0
maxSample=-1
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: 
            # print(t.i_sample)
            if maxADC<t.adc: 
                maxADC=t.adc
                maxSample=t.i_sample
            if t.i_sample == NumberOfTimestamps-1: 
                if maxADC>0: #future option for a threshold
                    hist.Fill(maxSample)
                maxADC=0
                maxSample=-1


#makes the histograms
c = r.TCanvas('','', 2000, 1000)
hist.SetYTitle('event count')
hist.SetXTitle('timestamp')
hist.Draw('COLZ')

label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/event-of-max_sample.pdf") 
