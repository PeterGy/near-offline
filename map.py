#How to use:
#Decode a x.raw file using decode.py
#Use the following to get a map of ADCs:
# ldmx python3 map.py adc_x.root

#A program that maps the testbeam channels to the sipms.
#So far untested. Expected to work when all HGCROCs are connected

from mapping import *

inputFile=r.TFile(sys.argv[1], "read")

#prepares the plot
allData=inputFile.Get('ntuplizehgcroc').Get("hgcroc") #
r.gStyle.SetOptStat("ne")
c=r.TCanvas('t','The canvas of anything', 1100, 900)
c.cd()
hist = r.TH2F('Map', "Mapped average SiPM ADCs",40, 0.5, 40.5, 12, -0.5, 11.5)
adcCountMap = zeros((40,12))
adcSumMap = zeros((40,12))


#averages all adcs in a python array
for t in allData : #for timestamp in allData
    realChannel = FpgaLinkChannel_to_realChannel([t.fpga,t.link,t.channel])
    # print([t.fpga,t.link,t.channel])
    # print(realChannel)
    if realChannel != None:
        LayerBarSide = realChannel_to_SipM(realChannel)
        # print(LayerBarSide)
        if LayerBarSide[2]==1: LayerBarSide[0] +=20
        adcCountMap[LayerBarSide[0],LayerBarSide[1]] +=1 
        adcSumMap[LayerBarSide[0],LayerBarSide[1]] +=t.adc


#fills a root histogram with the sipm averages
adcCountMap[adcCountMap == 0 ] = 1 
for i in range(40):
    for j in range(12):
        hist.Fill(i+1,j,adcSumMap[i,j]/adcCountMap[i,j])        


hist.SetYTitle('Bar number')
hist.SetXTitle('Layer number')
hist.Draw("COLZ")

#a helpful label to explain the plot
label = r.TLatex()
label.SetTextFont(42)
label.SetTextSize(0.025)
label.SetNDC()
label.DrawLatex(0,  0.92, "Left side: left and top SiPMs. Right side: right and bottom SiPMs.")
label.DrawLatex(0,  0.04, "Odd layers: vertical bars; Even layers: horizontal bars")

c.SaveAs("plots/map.png")  