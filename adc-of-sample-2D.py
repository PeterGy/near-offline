from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
r.gStyle.SetOptStat("ne")
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") 

def getNumberOfTimestamps(allData):
        samples=[]
        sample_sample=40 #the number of timestamps it looks at before it decides the range
        for t in allData:
                samples.append(t.i_sample)
                sample_sample+=1
                if len(samples)>sample_sample: break
        return  1+max(samples)-min(samples)

NumberOfADCs = 1024 
NumberOfTimestamps = getNumberOfTimestamps(allData)
print('This file has', NumberOfTimestamps,'timestamps')

hist =  r.TH2F('', "ADC of sample", 
        NumberOfTimestamps, 0, NumberOfTimestamps,
        NumberOfADCs, 0, NumberOfADCs,)

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hist.Fill(t.i_sample,t.adc)

#makes the histograms
c = r.TCanvas('','', 1000, 1000)
hist.SetYTitle('ADC')
hist.SetXTitle('Timestamps')
hist.Draw('COLZ')

label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/ADC-of-sample.pdf") 
