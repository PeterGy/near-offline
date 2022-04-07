#How to use:
#Decode a x.raw files using decode.py
#Use the following to get a plot of ADCS, with no pedestals subtracted:
# ldmx python3 this_file.py interesting_run.root

#A program that plots the adc counts for each channel

from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
r.gStyle.SetOptStat("ne")
hist=r.TH1F('', "ADC sum", NumberOfChannels, 0, NumberOfChannels)
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hist.Fill(realChannel,t.adc)

#makes the histograms
c = r.TCanvas('','The canvas of anything', 2000, 1000)
hist.SetYTitle('ADC sum (of timestamps)')
hist.SetXTitle('Channel (only real ones)')
hist.SetMinimum(0)
hist.SetLineColor(4)
hist.Draw('hist')

c.SaveAs("plots/adc-of-channel.pdf") 
