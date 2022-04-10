#usage: ldmx python3 HCal-dqm-offline.py ../adc_<run-number>.root
#dqm = data quality monitoring

from mapping import *
from optparse import OptionParser
import os
import csv

# csvFile=open()
ReconConditionsFileLocation='DumbReconConditions.csv'
csv_reader = csv.reader(open(ReconConditionsFileLocation), delimiter=',')

directory = 'plots'
try: os.stat(directory)
except: os.mkdir(directory)
 
parser = OptionParser()	
parser.add_option('-t','--threshold', dest='includeThresholdPlots', default = True, help='Determines if PE threshold plots should be included. Leave blank or True to inlcude, anything else ot exclude.')
options = parser.parse_args()[0]
includeThresholdPlots=options.includeThresholdPlots

#keeps only events we are interested in
eventsOfInterest = range(4,5)
channelsOfInterest = range(0,40)

inputFileName=sys.argv[1]
inputFile=r.TFile(inputFileName, "read")
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #
r.gStyle.SetOptStat("ne")

#defines boundaries
def getTimestampRange(allData):
    samples=[]
    sample_sample=40 #the number of timestamps it looks at before it decides the range
    for t in allData:
        samples.append(t.i_sample)
        sample_sample+=1
        if len(samples)>sample_sample: break
    return  range(min(samples),max(samples)+1)
timestampRange=getTimestampRange(allData)
print('The number of timestamps is',len(timestampRange))
channelRange=range(0,384)
ADCRange=range(0,1024)
TOTRange=range(0,1024)
TOARange=range(0,1024)
PERange=range(0,30)
barMapRange=range(1,12)
layerRange=range(1,41)
adcCountMap = zeros((40,12))
adcSumMap = zeros((40,12))

#sets the threshold
threshold_PE = 5. #aribtrary for now
energy_per_mip = 4.66 #MeV/MIP
voltage_hcal = 5. #mV/PE
PE_per_mip = 68. #PEs/mip
mV_per_PE = 1/energy_per_mip * voltage_hcal * PE_per_mip #mV per MIP is about 73 for now
adc_ped = 1. #Dummy Value
# adc_gain = 1.2 #Dummy Value
# threshold = adc_ped + mV_per_PE / adc_gain * threshold_PE
# print('threshold is an ADC of',threshold)
def ADC_to_PE(adc): return adc*adc_gain/mV_per_PE 
def calculateThreshold(adc_gain): return adc_ped + mV_per_PE / adc_gain * threshold_PE

thresholds=[]
for row in csv_reader:
    try:    
        [fpga,ROC,channel] = row[1].split(':') 
        # a slightly different format, that shall now be converted
        fpga = int(fpga)
        link = int(ROC)*2+int( (int(channel)) /36 ) 
        channel = int(channel)%36
        RealChannel = FpgaLinkChannel_to_realChannel([fpga,link,channel])
    except: RealChannel = None
    if RealChannel != None: 
        adc_gain = float(row[3])
        thresholds.append(calculateThreshold(adc_gain))

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

hists["event-of-PE"] =  r.TH1F("event-of-PE", "event-of-PE", 
        len(PERange), PERange[0]-0.5, PERange[-1]+0.5,)
hists["event-of-PE"].SetYTitle('Event count')
hists["event-of-PE"].SetXTitle('PE')  

hists["PE-of-channel"] =  r.TH2F("PE-of-channel", "PE-of-channel", 
        len(channelRange), channelRange[0]-0.5, channelRange[-1]-0.5,
        len(PERange), PERange[0]-0.5, PERange[-1]+0.5,)
hists["PE-of-channel"].SetYTitle('PE')
hists["PE-of-channel"].SetXTitle('Channel')  

hists["max_sample-of-channel"] =  r.TH2F("max_sample-of-channel", "max_sample-of-channel", 
        len(channelRange), channelRange[0]-0.5, channelRange[-1]-0.5,
        len(timestampRange), timestampRange[0]-0.5, timestampRange[-1]+0.5,)
hists["max_sample-of-channel"].SetYTitle('Timestamp')
hists["max_sample-of-channel"].SetXTitle('Channel') 

hists["map"] =  r.TH2F("map", "map", 
        len(layerRange), layerRange[0]-0.5, layerRange[-1]+0.5,
        len(barMapRange), barMapRange[0]-0.5, barMapRange[-1]+0.5,)
hists["map"].SetYTitle('Bar')
hists["map"].SetXTitle('Layer') 


#Gets data from interesting events
maxADC=0
maxSample=-1
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
                if maxADC>0: #future option for non-PE related threshold
                    hists["event-of-max_sample"].Fill(maxSample)
                    hists["max_sample-of-channel"].Fill(realChannel,maxSample)
                if maxADC>thresholds[realChannel]:   
                    hists["event-of-PE"].Fill(ADC_to_PE(maxADC))
                    hists["PE-of-channel"].Fill(realChannel,ADC_to_PE(maxADC))
                maxADC=0
                maxSample=-1

            #fills the map
            LayerBarSide = realChannel_to_SipM_fast[realChannel].copy() #the copy is what makes the fast not so fast
            if LayerBarSide[2]==1: LayerBarSide[0] +=20
            adcCountMap[LayerBarSide[0],LayerBarSide[1]] +=1 
            adcSumMap[LayerBarSide[0],LayerBarSide[1]] +=t.adc    

adcCountMap[adcCountMap == 0 ] = 1 
for i in range(40):
    for j in range(12):
        hists["map"].Fill(i,j,adcSumMap[i,j]/adcCountMap[i,j])     


#makes the overview pdf
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
if includeThresholdPlots == True:
    c.cd(6)
    hists["event-of-PE"].Draw('HIST')
    c.cd(7)
    hists["PE-of-channel"].Draw('COLZ')
c.cd(8)
hists["max_sample-of-channel"].Draw('COLZ')
c.cd(9)
hists["map"].Draw('COLZ')

for i in range(1,10):c.GetPad(i).SetLeftMargin(0.12)
c.cd(0)
label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.05)
label.SetNDC()  
if len(eventsOfInterest) == 1: context= "This is only event "+str(eventsOfInterest[0])
else: context="These are events "+str(eventsOfInterest[0])+" to "+str(eventsOfInterest[-1]) 
label.DrawLatex(0,  0, context)  
saveFileName=inputFileName[inputFileName.find('adc'):inputFileName.find('.root')]
c.SaveAs("plots/Hcal-dqm_overview_"+saveFileName+".pdf") 
c.Close()

#makes individual pdfs
import copy
channelsPerROC=64
plots=(hists["ADC-of-channel"],hists["TOT-of-channel"],hists["TOA-of-channel"],hists["max_sample-of-channel"])
for hist in plots:
    c = r.TCanvas('','', 300, 200)
    c.Divide(3,2)
    subplots=[]
    for i in range(0,6):
        c.cd(i+1)
        c.GetPad(i+1).SetLeftMargin(0.12)
        subplots.append(copy.deepcopy(hist))
        subplots[-1].GetXaxis().SetRangeUser(i*channelsPerROC, (i+1)*channelsPerROC-1)
        subplots[-1].SetTitle('ROC '+str(i))
        subplots[-1].Draw('COLZ')
    c.SaveAs("plots/Hcal-dqm_"+hist.GetName()+".pdf") 
    c.Close()




#makes the root histos
for hist in hists:
    file = r.TFile("plots/"+hists[hist].GetName()+".root", "RECREATE")
    hists[hist].SetDirectory(file)
    hists[hist].Write()
    file.Close()
