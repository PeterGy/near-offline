from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
NumberOfADCs=1024
r.gStyle.SetOptStat("ne")
hist =  r.TH2F('', "ADC sum", NumberOfChannels, 0, NumberOfChannels,
        NumberOfADCs, 0, NumberOfADCs,)
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hist.Fill(realChannel,t.adc)

#makes the histograms
c = r.TCanvas('','', 2000, 1000)
hist.SetYTitle('ADC (of timestamps)')
hist.SetXTitle('Channel (only real ones)')
hist.Draw('COLZ')

label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/ADC-of-channel.pdf") 
