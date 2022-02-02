# -*- coding: utf-8 -*-
from obspy.clients.fdsn import Client 
from jinja2 import Template

client = Client("IRIS")

# Select your desired station to create V0 files for here:
network="RE"
stations=["BFSK","BRBY","CAFE","CAFE2","CSTS","DDWD","EACA","EACA1","EACA2","ECHO",
          "FRNT","GRCO2","HHRS","HOVR2","HOVR3","HOVR4","HOVR6","JKLK","JKLK1","JKLK2",
          "JRDN","JRDN1","JRDN2","MRTZ","MTCL","MTCL1","MTCL2","MTCL3","NEME","NEME1","NEME3",
          "NORM","NORM1","NORM2","ONFB","ONFB1","ONFB2","SHST","SNJT","SNJT1","SNJT2","TRNT",
          "UPST","UPST1","UPST2","UPST3","UPST4"]
#stations=["CSTS","DDWD","EACA","EACA1","EACA2","ECHO","FRNT","GRCO2","HHRS","HOVR2","HOVR3","HOVR4","HOVR6","JKLK","JKLK1","JKLK2",
#          "JRDN","JRDN1","JRDN2","MRTZ","MTCL","MTCL1","MTCL2","MTCL3","NEME","NEME1","NEME3",
#          "NORM","NORM1","NORM2","ONFB","ONFB1","ONFB2","SHST","SNJT","SNJT1","SNJT2","TRNT",
#          "UPST","UPST1","UPST2","UPST3","UPST4"]
for station in stations:

    # Grab channel metadata from IRIS:
    inventory = client.get_stations(network=network, station=station, level="channel")
    invc=inventory.get_contents()
    chans=list(invc.values())[2]
    chnum=0
    
    # Loop over available channels for selected station and create corresponding V0 files: 
    for n in chans:
        md = inventory.get_channel_metadata(chans[chnum], datetime=None)
        scnl = chans[chnum].split(".")
        azim=int(md['azimuth']) if md['azimuth'] is not None else 0
        # Channel parameters being written to the newly-created V0 files:
        tdata = {
            "latr": float("%.3f" % md['latitude']),
            "lonr": float("%.3f" % md['longitude']),
            "lat": float("%.6f" % md['latitude']),
            "lon": float("%.6f" % md['longitude']),
            "elev": md['elevation'],
            "az": azim,
            "nc": network,
            "sta": station,
            "ch": scnl[3],
            "chn": chnum+1,
            "lc": scnl[2],
            "netnum": 3, # network code, use 3 for USBR
            "recsn": -999, # recorder serial number
            "rectype": 0, # recorder type, use 1000 for "other"
            "senstype": 900, # sensor type, use 900 for "other"
            "statype": 12, # station type, use 12 for "dam" or 1 for freefield
            "units": 50, # units, use 50 for counts
            "numchan": len(chans), # number of channels in recorder
            "rLSB": -999.00, # uV per count (LSB in microvolts)
            "vpp": 40, # recorder full scale input (volts)
            "wordlen": 0, # sample word length
            "corner": -999, # anti-alias filter corner freq (Hz)
            "sens": 15, # sensitivity (volts/g)
            "spp": 60.0000, # full scale output of sensor (volts)
            "sg": 4, # full scale range of sensor (g)
            "gain": -999 # sensor gain factor
            }
        
        # COSMOS V0 template being modified and written per each channel: 
        
        template = """Raw acceleration counts   (Format v01.20 with 13 text lines)                    
        Record of                 Earthquake of Sun Jun 17, 2018  11:34 PDT             
        Hypocenter:  TBD                H=   km                                         
        Origin:  TBD                                                                    
        Statn No: 06-000000 Code:{{nc}}-{{sta}}        Calipatria 2                            
        Coords: {{latr}}  {{lonr}}    Site Geology:                                        
        Recorder:       Deg           Unk  s/n  1114   ( 3 Chns of   6 at Sta)   Sensor:   
        Rcrd start time:06/17/2018, 18:34:36.000 GMT (Q=5) RcrdId:38199368.CI.CLI2.--.H 
        Sta Chan   {{chn}}  {{az}}    {{ch}}           Location:   {{lc}}
        Raw record length =177.700  sec, Uncor max = 114459  c, at   26.630 sec.        
        Processed: 06/17/18 12:00 PDT UCB                                               
        No filtering!                                                                   
        Values used when parameter of data value is unknown/unspecified:  -999, -999.000
         100 Integer-header values follow on  10 lines, Format = (10I8)                 
               0       1      {{units}}     120       1    -999    -999       0    -999    -999
               {{netnum}}       {{netnum}}    -999       {{netnum}}    -999       1    -999    -999      {{statype}}    -999
            -999    -999       {{numchan}}    -999    -999    -999    -999    -999    -999       {{rectype}}
               3    {{recsn}}       {{numchan}}       {{numchan}}       {{wordlen}}    -999    -999    -999    -999    2018
             168       6      17      18      34       5       5    -999    -999       {{chn}}
               {{chn}}     {{senstype}}    -999       {{az}}    -999      {{lc}}    -999    -999    -999    -999
            -999    -999    -999    -999    -999    -999    -999    -999    -999    -999
            -999    -999    -999    -999       1    -999    -999    -999    -999    -999
           17770     100      18      34      36       0       6      17    2018    -999
             360    -999       3    -999    -999    -999       0    -999    -999    -999
         100 Real-header values follow on  20 lines, Format =(5F15.6)
               {{lat}}     {{lon}}         {{elev}}    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000         {{rLSB}}             {{vpp}}    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000             36
            -999.000000    -999.000000    -999.000000       0.010000     177.699997
            -999.000000    -999.000000    -999.000000    -999.000000     200.000000
               0.707100             {{sens}}           {{spp}}              {{sg}}    -999.000000
            -999.000000       1.000000    -999.000000    -999.000000    -999.000000
            -999.000000       0.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000      10.000000     177.699997  114459.000000      26.629999
           -2530.949707    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
            -999.000000    -999.000000    -999.000000    -999.000000       2.120000
           2 Comment line(s) follow, each starting with a |
        | Cosmos version 01.20  written by ms_to_v0 Version 2.12
        |   2015/09/24 00:00:00 to 3000/01/01 00:00:00 UTC   """
        
        # Render template with modified parameters and write it to a .dlv0 text file: 
        
        v0temp = Template(template)
        outtext = v0temp.render(tdata)
        print(v0temp.render(tdata))
        # fname = chans[chnum] + ".dlv0"
        foo = chans[chnum].split('.')
        fname = network + "_" + foo[1] + "_" + foo[2] + "_" + scnl[3] + ".dlv0"
        with open(fname, 'w') as f:
            f.write(outtext)
        chnum+=1