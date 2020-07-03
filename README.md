# fdsnws2ppsd
## What?
Make PPSD analysis directly from an FDSN web service. 
It uses data and metadata from the last 15 minutes.
The code requires `Python3`, `Obspy` and `Matplolib`.

Here's a quick example:
```
/Users/me/anaconda3/bin/python3 ./fdsnws2ppsd.py "CH.FIESA..HHZ" -plot=ppsd ETH                                                               
```

## How?
Given channel `NN.SSSS.LL.CCC`, and fdsnws running at `http:///localhost:8080/`, run as:
```
python3 ./fdsnws2ppsd.py "NN.SSSS.LL.CCC" [-plot=spec,temp,site,ppsd] [http://localhost:8080/]
```
Last argument is fdsnws url is optional and localhost by default.
The `-plot` option specifies plot types, it is optional, does all plots by default.
The last data and metadata are saved locally in the current directory.

The code can also use local files instead of fdsnws, run as:
```
python3 ./fdsnws2ppsd.py "NN.SSSS.LL.CCC" [-plot=spec,temp,site,ppsd] [data (e.g. mseed)] [metadata (e.g. fdsn.xml)]
```
Data and metadata should be in Obspy compatible formats.

## Next?
1. Improve user interface.
1. Add control for time selection. 
