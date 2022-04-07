from mapping import *
#keeps only events we are interested in
eventsOfInterest = range(0,100)
channelsOfInterest = range(0,40)

threshold_PE = 5. #aribtrary for now
energy_per_mip = 4.66 #MeV/MIP
voltage_hcal = 5. #mV/PE
PE_per_mip = 68. #PEs/mip
mV_per_PE = 1/energy_per_mip * voltage_hcal * PE_per_mip #mV per MIP is about 73 for now
adc_ped = 1. #Dummy Value
adc_gain = 1.2 #Dummy Value
threshold = adc_ped + mV_per_PE / adc_gain * threshold_PE
print('threshold is an ADC of',threshold)
def ADC_to_PE(adc):
    return adc*adc_gain/mV_per_PE 



#prepares the plots
inputFile=r.TFile(sys.argv[1], "read")
NumberOfChannels=384
NumberOfPEs=30
r.gStyle.SetOptStat("ne")
hist =  r.TH2F('', "PEs per channel", NumberOfChannels, 0, NumberOfChannels,
        NumberOfPEs, 0, NumberOfPEs,)
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

NumberOfTimestamps = max([t.i_sample for t in allData]) #takes a while

#Gets data from interesting events
maxADC=0
for t in allData : #for timestamp in allData
    if t.event in eventsOfInterest:
        realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
        if realChannel != None: 
            if maxADC<t.adc: maxADC=t.adc
            if t.i_sample == NumberOfTimestamps:
                if maxADC>threshold:   
                    hist.Fill(realChannel,ADC_to_PE(maxADC))
                maxADC=0


#makes the histograms
c = r.TCanvas('','', 2000, 1000)
hist.SetYTitle('PEs')
hist.SetXTitle('Channel (only real ones)')
hist.Draw('COLZ')

label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  

c.SaveAs("plots/PE-of-channel.pdf") 
