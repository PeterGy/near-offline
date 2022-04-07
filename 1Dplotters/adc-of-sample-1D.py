from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
r.gStyle.SetOptStat("ne")
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") 

#Determines number fo timestamps automatically. It's slow. Set it yourself if you want it quickly.
NumberOfTimestamps = max([t.i_sample for t in allData])+1 
print('This file has', NumberOfTimestamps,'timestamps')

hist=r.TH1F('', "ADC sum", NumberOfTimestamps, 0, NumberOfTimestamps)

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hist.Fill(t.i_sample,t.adc)

#makes the histograms
c = r.TCanvas('','', 2000, 1000)
hist.SetYTitle('ADC sum')
hist.SetXTitle('Timestamps')
hist.SetMinimum(0)
hist.SetLineColor(4)
hist.Draw('hist')

label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/adc-of-sample.pdf") 