from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(4,7)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
r.gStyle.SetOptStat("ne")
hist=r.TH1F('', "TOT sum", NumberOfChannels, 0, NumberOfChannels)
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hist.Fill(realChannel,t.tot)

#makes the histograms
c = r.TCanvas('','', 2000, 1000)
hist.SetYTitle('TOT sum (of timestamps)')
hist.SetXTitle('Channel (only real ones)')
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

c.SaveAs("plots/tot-of-channel.pdf") 
