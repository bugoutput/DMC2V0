# -*- coding: utf-8 -*-
from obspy.clients.fdsn import Client 
from jinja2 import Template

client = Client("IRIS")
network="RE"
station="JKLK2"

inventory = client.get_stations(network=network, station=station, level="channel")
invc=inventory.get_contents()
chans=list(invc.values())[2]
chnum=0

for n in chans:
    md = inventory.get_channel_metadata(chans[chnum], datetime=None)
    scnl = chans[chnum].split(".")
    tdata = {
        "lat": float("%.3f" % md['latitude']),
        "lon": float("%.3f" % md['longitude']),
        "az": md['azimuth'],
        "nc": network,
        "sta": station,
        "ch": scnl[3],
        "chn": chnum+1,
        "lc": scnl[2]
        }
    template = """Raw acceleration counts   (Format v01.20 with 13 text lines)                    
    Record of                 Earthquake of Sun Jun 17, 2018  11:34 PDT             
    Hypocenter:  TBD                H=   km                                         
    Origin:  TBD                                                                    
    Statn No: 06-000000 Code:{{nc}}-{{sta}}        Calipatria 2                            
    Coords: {{lat}}  {{lon}}    Site Geology:                                        
    Recorder:       Deg           Unk  s/n  1114   ( 3 Chns of   6 at Sta)   Sensor:   
    Rcrd start time:06/17/2018, 18:34:36.000 GMT (Q=5) RcrdId:38199368.CI.CLI2.--.H 
    Sta Chan   {{chn}}  {{az}}    {{ch}}           Location:   {{lc}}
    Raw record length =177.700  sec, Uncor max = 114459  c, at   26.630 sec.        
    Processed: 06/17/18 12:00 PDT UCB                                               
    No filtering!                                                                   
    Values used when parameter of data value is unknown/unspecified:  -999, -999.000
     100 Integer-header values follow on  10 lines, Format = (10I8)                 
           0       1      50     120       1    -999    -999       0    -999    -999
           6       6    -999       6    -999       1    -999    -999       3    -999
        -999    -999       6    -999    -999    -999    -999    -999    -999       0
           3    1114       6       3       0    -999    -999    -999    -999    2018
         168       6      17      18      34       5       5    -999    -999       1
           1      20    -999      90    -999    -999    -999    -999    -999    -999
        -999    -999    -999    -999    -999    -999    -999    -999    -999    -999
        -999    -999    -999    -999       1    -999    -999    -999    -999    -999
       17770     100      18      34      36       0       6      17    2018    -999
         360    -999       3    -999    -999    -999       0    -999    -999    -999
     100 Real-header values follow on  20 lines, Format =(5F15.6)
          33.121120    -115.580162     -60.200001    -999.000000    -999.000000
        -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
        -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
        -999.000000    -999.000000    -999.000000    -999.000000    -999.000000
        -999.000000       0.596047       0.000000    -999.000000    -999.000000
        -999.000000    -999.000000    -999.000000    -999.000000      36.000000
        -999.000000    -999.000000    -999.000000       0.010000     177.699997
        -999.000000    -999.000000    -999.000000    -999.000000     200.000000
           0.707100       4.995260      20.000000       4.000000    -999.000000
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
    
    
    v0temp = Template(template)
    outtext = v0temp.render(tdata)
    print(v0temp.render(tdata))
    fname = chans[chnum] + ".dlv0"
    with open(fname, 'w') as f:
        f.write(outtext)
    chnum+=1
