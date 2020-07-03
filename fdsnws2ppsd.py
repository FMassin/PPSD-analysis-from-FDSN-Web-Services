
from obspy import read_inventory, read, UTCDateTime
from obspy.imaging.cm import pqlx
from  matplotlib.pyplot import figure
from  sys import argv
from obspy.signal import PPSD
from obspy.clients.fdsn import Client



# Map function
def sitemap(inventory,
    xpixels=500, # zoom level
    dpi=96,     # image quality
    zoom=99):

    from mpl_toolkits.basemap import Basemap
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset

    def fillmap(f,inventory,zoom=1,xpixels=xpixels):
        f.bmap.arcgisimage(server='http://server.arcgisonline.com/ArcGIS',
                    service='World_Imagery',
                      xpixels=xpixels/zoom**.1,
                          dpi=dpi)

        im1 = f.bmap.arcgisimage(service='Reference/World_Boundaries_and_Places_Alternate',
                                       xpixels=xpixels/zoom**.1,
                                       zorder=999999,
                          dpi=dpi)
        if False:
            im3 = f.bmap.arcgisimage(server='http://server.arcgisonline.com/ArcGIS',
                                     service='Elevation/World_Hillshade',
                                           xpixels=xpixels/zoom**.1,
                          dpi=dpi)
            data=im3.get_array()
            data[:,:,3] = 1 - (data[:,:,0]*data[:,:,1]*data[:,:,2])
            im3.set_array(data)

        f=inventory.plot(fig=f,
                         color='0.0',
                         water_fill_color='None',
                         continent_fill_color='None',
                         resolution='i')


    f = figure()
    ax = f.add_subplot(111)
    f.bmap = Basemap(llcrnrlon=inventory[0][0].longitude-2,
                       llcrnrlat=inventory[0][0].latitude-1.5,
                       urcrnrlon=inventory[0][0].longitude+2.5,
                       urcrnrlat=inventory[0][0].latitude+2,
                     epsg=4326,
                      projection='merc',
                     suppress_ticks=False,
                     resolution='h',
                     ax=ax)
    fillmap(f,inventory)

    axins = zoomed_inset_axes(ax, zoom, loc=1)
    axins.set_xlim(inventory[0][0].longitude-0.011, inventory[0][0].longitude+0.011)
    axins.set_ylim(inventory[0][0].latitude-0.008, inventory[0][0].latitude+.008)

    f.bmap = Basemap(llcrnrlon=inventory[0][0].longitude-0.011,
                       llcrnrlat=inventory[0][0].latitude-0.008,
                       urcrnrlon=inventory[0][0].longitude+0.011,
                       urcrnrlat=inventory[0][0].latitude+.008,
                     epsg=4326,
                      projection='merc',
                     suppress_ticks=False,
                     resolution='h',
                     ax=axins)
    fillmap(f,inventory,zoom=zoom)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")


if __name__ == "__main__":
    try:
        inventory = read_inventory(argv[-1])
        stream = read(argv[1])
    except:
        print('cannot find local storage')
        pass
    try:
        client = Client(argv[-1])
    except:
        print('cannot connect fdsnws url')
        pass
    try:
        client = Client('http://localhost:8080/')
    except:
        print('cannot connect local fdsnws url')
        pass
    try:
        mseedid = {'network':argv[1].split('.')[0],
           'station':argv[1].split('.')[1],
           'location':argv[1].split('.')[2],
           'channel':argv[1].split('.')[3],
           'starttime':UTCDateTime()-8000,
           'endtime':UTCDateTime()}
        stream = client.get_waveforms(**mseedid)
        stream.write('last.mseed')
        inventory = client.get_stations(level='response',**mseedid)
        inventory.write('last.xml', format="STATIONXML")
    except:
        print('cannot get data from fdsnws')
        pass
    try:
        print(inventory[0][0][0])
        print(stream)
    except:
        print('cannot get any data')
        print('Run as: python3 %s "NN.SSSS.LL.CCC" [-plot=spec,temp,site,ppsd] [http://localhost:8080/] '%argv[0])
        print('    or: python3 %s "NN.SSSS.LL.CCC" [-plot=spec,temp,site,ppsd] [data (e.g. mseed)] [metadata (e.g. fdsn.xml)]'%argv[0])


    stream._cleanup()
    ids=[]
    for trace in stream:
        if trace.id in ids:
            continue
        ids +=[trace.id]
        ppsd = PPSD(trace.stats,
                inventory,
                db_bins=(-200, -50, .5),
                period_step_octaves=0.125/2.,
                ppsd_length=min([int(trace.stats.npts/4/trace.stats.sampling_rate),800]))
        ppsd.add(stream)

        if "site" in argv[-2]:
            sitemap(inventory)
        if "spec" in argv[-2]:
            ppsd.plot_spectrogram()
        if "temp" in argv[-2]:
            ppsd.plot_temporal([10,0.1,1])
        ppsd.plot(show_mode=True,
                  cmap=pqlx)


