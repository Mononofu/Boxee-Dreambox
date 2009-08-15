# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
import urllib, urllib2, re, string, time
channelWhitelist = [
                    'ATV+', 
                    'BBC World', 
                    'CNBC Europe', 
                    'MTV AUSTRIA', 
                    'ORF1', 
                    'ORF2', 
                    'Kabel 1 Austria', 
                    'N24', 
                    'ProSieben Austria', 
                    'SAT.1 A', 
                    'RTL Austria', 
                    'RTL2 Austria', 
                    'Super RTL A' 
                    'VOX Austria', 
                    '3sat', 
                    'ZDF', 
                    'ZDFdokukanal', 
                    'Al Jazeera', 
                    'BR-alpha*', 
                    'Das Erste', 
                    'arte'
                    ]
                    
def getChannelUrl(channelRef):
    urllib2.urlopen("http://192.168.2.60:90/cgi-bin/zapTo?path={0:s}".format(channelRef))   #This changes the channel
    time.sleep(1)
    return urllib2.urlopen("http://192.168.2.60:90/video.m3u").read()   #This gets the url from the playlist

def isInWhitelist(bouquet, channel):
    i = channel.find(' - ')
    if i < 0:
        i = len(channel)
    for c in channelWhitelist:
        if channel[0:i] == c:
            return True
    return False

def channel(request, channel_id):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, "http://192.168.2.60:90", 'root', '8FohwitNEF-KRk')
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    url = getChannelUrl(channel_id)
    return HttpResponseRedirect( url )

def index(request):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, "http://192.168.2.60:90", 'root', '8FohwitNEF-KRk')
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    dreambox_senderliste = urllib2.urlopen("http://192.168.2.60:90/body").read()
    result = re.findall(r'var bouquets = new Array\(\s\s\s(("[^"]+", )*"[^"]+")\s\s\s\);', dreambox_senderliste)
    bouquets = re.findall(r'"([^"]+)"', result[0][0])
    channels = []
    channelRefs = []
    for i in range(len(bouquets)):
        result = re.findall(r'channels\[{0:n}\] = new Array\((("[^"]+", )*"[^"]+")\);'.format(i), dreambox_senderliste)
        channels.append(re.findall(r'"([^"]+)"', result[0][0]))

    for i in range(len(bouquets)):
        result = re.findall(r'channelRefs\[{0:n}\] = new Array\((("[^"]+", )*"[^"]+")\);'.format(i), dreambox_senderliste)
        channelRefs.append(re.findall(r'"([^"]+)"', result[0][0]))
        
    channelDict = [] 
    for i in range(len(bouquets)):
        for j in range(len(channels[i])):
            if isInWhitelist(bouquets[i], channels[i][j]):
                k = channels[i][j].find(' - ')
                if k < 0:
                    k = len(channels[i][j])
                name = channels[i][j][0:k]
                name = string.capitalize(name[:1]) + name[1:]
                channelDict.append( {
                                    'name': name, 
                                    'url': "http://localhost/django/dream/{0:s}".format( channelRefs[i][j] ),
                                    'thumbnail': "http://localhost/media/thumbs/{0:s}.jpg".format( channels[i][j][0:k].replace(' ', '') )
                                    } )
    return render_to_response('dreambox/index.html', {'channels': channelDict})
