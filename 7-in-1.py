from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)


def getTimestampRange(allData):
    samples=[]
    sample_sample=40 #the number of timestamps it looks at before it decides the range
    for t in allData:
        samples.append(t.i_sample)
        sample_sample+=1
        if len(samples)>sample_sample: break
    return  range(min(samples),max(samples)+1)



inputFile=r.TFile(sys.argv[1], "read")
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #
r.gStyle.SetOptStat("ne")

#defines boundaries
timestampRange=getTimestampRange(allData)
print('The range of timestamps is',timestampRange)
print('The range of timestamps is',timestampRange[-1])
print('The range of timestamps is',len(timestampRange))
channelRange=range(0,384)
ADCRange=range(0,1024)
TOTRange=range(0,1024)
TOARange=range(0,1024)

#prepares plots
hists = {}

hists["ADC-of-channel"] =  r.TH2F("ADC-of-channel", "ADC-of-channel", 
        len(channelRange), channelRange[0]-0.5, channelRange[-1]-0.5,
        len(ADCRange), ADCRange[0]-0.5, ADCRange[-1]-0.5,)
hists["ADC-of-channel"].SetYTitle('ADC (of timestamps)')
hists["ADC-of-channel"].SetXTitle('Channel (only real ones)')   

hists["TOT-of-channel"] =  r.TH2F("TOT-of-channel", "TOT-of-channel", 
        len(channelRange), channelRange[0]-0.5, channelRange[-1]-0.5,
        len(TOTRange), TOTRange[0]-0.5, TOTRange[-1]-0.5,)
hists["TOT-of-channel"].SetYTitle('TOT (of timestamps)')
hists["TOT-of-channel"].SetXTitle('Channel (only real ones)')        

hists["TOA-of-channel"] =  r.TH2F("TOA-of-channel", "TOA-of-channel", 
        len(channelRange), channelRange[0]-0.5, channelRange[-1]-0.5,
        len(TOARange), TOARange[0]-0.5, TOARange[-1]-0.5,)
hists["TOA-of-channel"].SetYTitle('TOA (of timestamps)')
hists["TOA-of-channel"].SetXTitle('Channel (only real ones)')        

hists["ADC-of-sample"] =  r.TH2F("ADC-of-sample", "ADC-of-sample", 
        len(timestampRange), timestampRange[0]-0.5, timestampRange[-1]+0.5,
        len(ADCRange), ADCRange[0]-0.5, ADCRange[-1]-0.5,)
hists["ADC-of-sample"].SetYTitle('ADC')
hists["ADC-of-sample"].SetXTitle('Sample')  

hists["event-of-max_sample"] =  r.TH1F("event-of-max_sample", "event-of-max_sample", 
        len(timestampRange), timestampRange[0]-0.5, timestampRange[-1]+0.5,)
hists["event-of-max_sample"].SetYTitle('Event count')
hists["event-of-max_sample"].SetXTitle('Sample')  




maxADC=0
maxSample=-1
#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: 
            
            
            hists["ADC-of-channel"].Fill(realChannel,t.adc)
            hists["TOT-of-channel"].Fill(realChannel,t.tot)
            hists["TOA-of-channel"].Fill(realChannel,t.toa)
            hists["ADC-of-sample"].Fill(t.i_sample,t.adc)

            if maxADC<t.adc: 
                maxADC=t.adc
                maxSample=t.i_sample
            if t.i_sample == timestampRange[-1]: 
                if maxADC>0: #future option for a threshold
                    hists["event-of-max_sample"].Fill(maxSample)
                maxADC=0
                maxSample=-1
            

#makes the histograms



c = r.TCanvas('','', 300, 300)
c.Divide(3,3)

c.cd(1)
hists["ADC-of-channel"].Draw('COLZ')
c.cd(2)
hists["TOT-of-channel"].Draw('COLZ')
c.cd(3)
hists["TOA-of-channel"].Draw('COLZ')
c.cd(4)
hists["ADC-of-sample"].Draw('COLZ')
c.cd(5)
hists["event-of-max_sample"].Draw('HIST')
# file = r.TFile("plots/"+hists["ADC-of-channel"].GetName()+".root", "RECREATE")
# hists["ADC-of-channel"].SetDirectory(file)
# hists["ADC-of-channel"].Write()
# file.Close()












label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/7-in-1.pdf") 
