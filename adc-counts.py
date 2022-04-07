#How to use:
#Decode a x.raw files using decode.py
#Use the following to get a plot of ADCS, with no pedestals subtracted:
# ldmx python3 this_file.py interesting_run.root

#A program that plots the adc counts for each channel

from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(4,5)
channelsOfInterest = range(0,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
r.gStyle.SetOptStat("ne")
hists =   [r.TH1F(str(channel), "ADC counts",256, 0, 256) for channel in range(0,NumberOfChannels)]
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#Gets data from interesting events
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hists[realChannel].Fill(t.adc)

#makes the histograms
canvases=[r.TCanvas(str(i+1),'The canvas of anything', 250, 1200) for i in range(0,19)]
for c in canvases: c.Divide(2,12)

r.gStyle.SetLineScalePS(0.3)
for hist in hists: 
    if int(hist.GetName()) in channelsOfInterest:
        l= realChannel_to_SipM(int(hist.GetName()))
        c =canvases[l[0]-1]
        c.cd(l[1]*2+l[2]+1)
        hist.SetYTitle('timestamp counts')
        hist.SetXTitle('ADC')
        hist.SetMinimum(0)
        hist.SetLineColor(4)
        hist.SetLineWidth(1)
        hist.Draw('same')
        label = r.TLatex()
        label.SetNDC()  
        label.DrawLatex(0,  0.91, "SiPM of layer "+str(l[0])+", bar "+str(l[1])+", side "+str(l[2])  )
for c in canvases: c.SaveAs("plots/adc-counts_layer-"+c.GetName()+".pdf") 
