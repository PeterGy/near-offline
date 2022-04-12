#usage: ldmx python3 LED-finder.py LED_run.root pedestals.csv

from mapping import *
import csv
import ROOT as r

pedestalFileName=sys.argv[2]
csv_reader = csv.reader(open(pedestalFileName), delimiter=',')

pedestals ={}
for row in csv_reader:
    try:  pedestals[int(row[0])] = float(row[2])
    except:pass
# print(pedestals)


inputFileName=sys.argv[1]
inputFile=r.TFile(inputFileName, "read")
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #

IDpositions={}
hists={}
for t in allData : #for timestamp in allData
    if t.raw_id not in hists:
        hists[t.raw_id] = r.TH1F(str(t.raw_id),'',1024,0,1204)
        polarfire= t.fpga
        hrocindex= int(t.link/2)
        channel= 36*t.link%2 + t.channel
        IDpositions[t.raw_id] = str(polarfire)+':'+str(hrocindex)+':'+str(channel)
    hists[t.raw_id].Fill(t.adc)

csvfile = open('LEDs.csv', 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',')

csvwriter.writerow(['DetID', 'ElLoc', 'ADC_PEDESTAL', 'LED_MEDIAN'])

pedestalPlot = r.TH1F('','Pedestals',384,0,0)
LEDPlot = r.TH1F('','LEDs',384,0,0)

for i in hists: 
    μ = hists[i].GetMean()-pedestals[i]
    pedestalPlot.Fill(int(i),pedestals[i])
    LEDPlot.Fill(int(i),μ)
    csvwriter.writerow([i, IDpositions[i], pedestals[i], μ])

file = r.TFile("pedestals.root", "RECREATE")
pedestalPlot.SetDirectory(file)
pedestalPlot.Write()
file.Close()
file = r.TFile("LEDs.root", "RECREATE")
LEDPlot.SetDirectory(file)
LEDPlot.Write()
file.Close()        

 