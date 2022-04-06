#How to use:
#Decode a x.raw file using decode.py
#Use the following to get a map of ADCs:
# ldmx python3 map.py adc_x.root

#A program that maps the testbeam channels to the sipms.
#So far untested. Expected to work when all HGCROCs are connected

# import time
# start = time.perf_counter()
# print(time.perf_counter()-start) 
from mapping import *

eventsOfInterest = range(4,5)
channelsOfInterest = range(0,384)


#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
r.gStyle.SetOptStat("ne")
hists =   [r.TH1F(str(channel), "Pulse shape for SiPM",4, 0, 4) for channel in range(0,NumberOfChannels)]
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

#creates the pulse shape
start = time.perf_counter()
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest: 
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: hists[realChannel].Fill(t.i_sample,t.adc)


for hist in hists: #makes the histograms
    if int(hist.GetName()) in channelsOfInterest:
        c =r.TCanvas('c','The canvas of anything', 1100, 900)
        hist.SetYTitle('ADC sum')
        hist.SetXTitle('Timestamp')
        # hist.Scale(1./hist.Integral(), "width")
        hist.SetMinimum(0)
        hist.Draw('HIST')
        label = r.TLatex()
        label.SetNDC()  
        l= realChannel_to_SipM(int(hist.GetName()))
        label.DrawLatex(0,  0.91, "This is the SiPM of layer "+str(l[0])+", bar "+str(l[1])+", side "+str(l[2])  )
        if (len(eventsOfInterest)==1): 
            label.DrawLatex(0,  0.04, "This is event "+str(eventsOfInterest[0]))            
            c.SaveAs("plots/pulse-shape_event-"+str(eventsOfInterest[0])+"_channel"+str(l)+".png")  
        else:    c.SaveAs("plots/pulse-shape_"+str(l)+".pdf")  
        c.Close()

