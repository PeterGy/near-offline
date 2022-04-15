#usage: ldmx python3 LED-finder.py LED_run.root pedestals.csv

from mapping import *
import csv
import ROOT as r
from optparse import OptionParser

r.gStyle.SetLineScalePS(0.3)

parser = OptionParser()	
parser.add_option('-o','--outputPath', dest='outputPath', default = '', help='Determines the output folder')
options = parser.parse_args()[0]
outputPath = options.outputPath
if outputPath != '' and outputPath[-1] != '/': outputPath +='/'

pedestalFileName=sys.argv[2]
csv_reader = csv.reader(open(pedestalFileName), delimiter=',')

pedestals ={}
for row in csv_reader:
    try:  pedestals[int(row[0])] = float(row[2])
    except:pass
# print(pedestals)


inputFileName=sys.argv[1]
inputFile=r.TFile(inputFileName, "read")
inputFileNameNoExtension=sys.argv[1][inputFileName.find('adc'):inputFileName.find('.root')]
outputFileName = outputPath+'LEDs_'+inputFileNameNoExtension
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #


IDpositions={}
hists={}
for t in allData : #for timestamp in allData
    if t.raw_id not in hists:
        hists[t.raw_id] = r.TH1F(str(t.raw_id),'',1024,0,1024)
        polarfire= t.fpga
        hrocindex= int(t.link/2)
        channel= 36*(t.link%2) + t.channel
        IDpositions[t.raw_id] = str(polarfire)+':'+str(hrocindex)+':'+str(channel)
    hists[t.raw_id].Fill(t.adc)

csvfile = open('LEDs/'+outputFileName+'.csv', 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',')

csvwriter.writerow(['DetID', 'ElLoc', 'ADC_PEDESTAL', 'LED_MEDIAN'])


pedestalPlots=[]
LEDPlots=[]
for fpga in range(0,2):
    for ROC in range(0,3):
        pedestalPlots.append(r.TH1F('','Pedestals',72,-0.5,71.5))
        LEDPlots.append(r.TH1F('','Pedestals',72,-0.5,71.5))

# pedestalPlot = r.TH1F('','Pedestals',384,0,0)
# LEDPlot = r.TH1F('','LEDs',384,0,0)

for i in hists: 
    # μ = hists[i].GetMean()-pedestals[i]
    hists[i].GetXaxis().SetRangeUser(int(pedestals[i])+20,1024) #corps off the pedestal plus an arbitrary threshold
    μ = hists[i].GetMean()-pedestals[i]

    fpga = int(IDpositions[i].split(':')[0])
    ROC = int(IDpositions[i].split(':')[1])
    channel = int(IDpositions[i].split(':')[2])

    pedestalPlots[fpga*3+ROC].Fill(channel,pedestals[i])
    LEDPlots[fpga*3+ROC].Fill(channel,μ)
    # LEDPlot.Fill(int(i),μ)

    csvwriter.writerow([i, IDpositions[i], pedestals[i], μ])

    c = r.TCanvas('','', 400, 300)

r.gStyle.SetHistLineWidth(0)
r.gStyle.SetOptStat("ne")

c = r.TCanvas('','', 600, 600)
c.Divide(1,6)
for i in range(0,6):
    c.cd(1+i)
    c.GetPad(1+i).SetGrid()

    LEDPlots[i].Draw('HIST SAME')
    LEDPlots[i].SetLineColor(4)  
    pedestalPlots[i].Draw('HIST SAME')
    pedestalPlots[i].SetLineColor(3) 

c.SaveAs("Plots/LEDsummary_"+inputFileNameNoExtension+".pdf")
c.Close()
# file = r.TFile("pedestals.root", "RECREATE")
# pedestalPlot.SetDirectory(file)
# pedestalPlot.Write()
# file.Close()
# file = r.TFile('LEDs/'+outputFileName+".root", "RECREATE")
# LEDPlot.SetDirectory(file)
# LEDPlot.Write()
# file.Close()        

 