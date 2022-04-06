#How to use:
#Decode a x.raw files using decode.py
#Use the following to get a plot of ADCS, with no pedestals subtracted:
# ldmx python3 this_file.py interesting_run.root
#Use the following to get a plot of ADCS, with the pedestal subtracted:
# ldmx python3 this_file.py interesting_run.root an_empty_run.root

#A program that plots the adc counts for each channel
#So far untested. Expected to work when all HGCROCs are connected

from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(4,5)
channelsOfInterest = range(1,40)

#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
r.gStyle.SetOptStat("ne")
hists =   [r.TH1F(str(channel), "Pulse shape for SiPM",256, 0, 256) for channel in range(0,NumberOfChannels)]
# hists =   [r.TH1F(str(channel), "Pulse shape for SiPM",512, -256, 256) for channel in range(0,NumberOfChannels)]
pedestals =   [0 for channel in range(0,NumberOfChannels)]
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#Gets data from interesting sample, already subtracting pedestals
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        # if t.i_sample==1: #we define event ADCs as the second time sample for now
            realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
            #fpga -2 because of a board quirk I am told not to worry about for this specific sample
            if realChannel != None: hists[realChannel].Fill(t.adc-pedestals[realChannel])

#makes the histograms
for hist in hists: 
    if int(hist.GetName()) in channelsOfInterest:
        c =r.TCanvas('c','The canvas of anything', 1100, 900)
        hist.SetYTitle('event counts')
        hist.SetXTitle('ADC')
        hist.SetMinimum(0)
        hist.SetLineColor(4)
        hist.Draw('same')
        label = r.TLatex()
        label.SetNDC()  
        label.DrawLatex(0,  0.92, "This is SiPM "+str(realChannel_to_SipM(int(hist.GetName()))))
        if (len(eventsOfInterest)==1): 
            label.DrawLatex(0,  0.85, "This is event "+str(eventsOfInterest[0]))                
            c.SaveAs("plots/adc-counts_events-"+str(eventsOfInterest[0])+"_channel-"+hist.GetName()+".png" ) 
        else:
            c.SaveAs("plots/adc-counts_channel-"+hist.GetName()+".png")  
        c.Close()

