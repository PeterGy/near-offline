#usage: ldmx python3 pedestal-finder.py pedestal_run.root

from mapping import *
import csv
import ROOT as r

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

csvfile = open('pedestals.csv', 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=',')

csvwriter.writerow(['DetID', 'ElLoc', 'ADC_PEDESTAL'])
pedestalPlot = r.TH1F('','Pedestals',384,0,0)

for i in hists: 
    μ = hists[i].GetMean()
    pedestalPlot.Fill(int(i),μ)
    csvwriter.writerow([i, IDpositions[i], μ])

file = r.TFile("pedestals.root", "RECREATE")
pedestalPlot.SetDirectory(file)
pedestalPlot.Write()
file.Close()

        

 