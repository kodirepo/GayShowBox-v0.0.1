# The documentation written by Voinage was used as a template for this addon
# http://wiki.xbmc.org/?title=HOW-TO_write_plugins_for_XBMC
#
# This addon is licensed with the GNU Public License, and can freely be modified
# http://www.gnu.org/licenses/gpl-2.0.html

import urllib
import urllib2
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import MinimalSoup as BeautifulSoup


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                                
    return param

def displayRootMenu():
    addListItem('Latest Videos','most-recent/','scrapeVideoList','DefaultFolder.png')
    addListItem('Random Videos','random/','scrapeVideoList','DefaultFolder.png')
    addListItem('Top Rated Videos','top-rated/','scrapeVideoList','DefaultFolder.png')
    addListItem('Top Favorites','top-favorites/','scrapeVideoList','DefaultFolder.png')
    addListItem('Most Viewed','most-viewed/','scrapeVideoList','DefaultFolder.png')
    addListItem('Most Commented','most-discussed/','scrapeVideoList','DefaultFolder.png')
    # todo: channels; search


def addListItem(name,url,mode,iconimage,page="page1.html"):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)+"&page="+urllib.quote_plus(page)
    ok=True
    name=BeautifulSoup(name, convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    if mode=='scrapeVideoList':
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    elif mode=='playVideo':
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if mode=='scrapeVideoList':
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    elif mode=='playVideo':
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok


def indexVideos(path,page):
    req = urllib2.Request(base_url + path + page)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

#	match=re.compile('<a href="{url}(videos/.*\.html)"><img class="img" src="(.*\.jpg)" alt="(.*)" id='.format(url=base_url)).findall(link)
    match=re.compile('this.src="(?P<thumbnail>http://cdn.gayboystube.com/thumbs/[A-Z0-9a-z/. -_]*[wmvaiflp4]{3}-[0-9].jpg)";\' width="[0-9]{3}" height="[0-9]{3}" alt="(?P<name>[A-Za-z0-9!-@#$%^&*(),.;:\' ]*)" />\r\n\r\n\t\t\t</a>\r\n\r\n\t<a href="http://www.gayboystube.com/(?P<url>video/[0-9]{5,7}/[0-9a-z-]*)" class="title"').findall(link)

    for thumbnail,name,url in match:
        addListItem(name,base_url + url,'playVideo',urllib.quote(thumbnail,':/'),page)

    match2=re.search('<a href=\'(?P<pge>page[0-9]{1,5}\.html)\' class="next">Next</a>', link)
    if match2 is not None:
        addListItem('Go to next page (' + ')',path,'scrapeVideoList','DefaultFolder.png',match2.group('pge'))


def playVideo(url,name,thumb):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('clip: {\r\n\t{7,9}url: \'([A-Za-z0-9_/.:-?&= _]*)\',').findall(link)
    name=BeautifulSoup(urllib.unquote_plus(name), convertEntities=BeautifulSoup.HTML_ENTITIES).contents[0]
    for url in match:
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setThumbnailImage(urllib.unquote_plus(thumb))
       	xbmc.Player().play(url, listitem)


# initialize variables
url=None
name=None
thumb=None
mode=None
page=None

# get parameters passed through plugin URL
params=get_params()

# set any parameters that were passed through the plugin URL
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    thumb=urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass
try:
    page=urllib.unquote_plus(params["page"])
except:
    pass

# ok - the parameters are initialized where are we scraping?
base_url='http://www.gayboystube.com/'
categories_url=base_url + 'channels/'
search_url=base_url + 'search/videos/'

# log some basics to the debug log for funzies.
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
    print base_url
    displayRootMenu()
       
elif mode=='scrapeVideoList':
    print ""+url+page
    indexVideos(url,page)
        
elif mode=='playVideo':
    print ""+url
    playVideo(url,name,thumb)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
