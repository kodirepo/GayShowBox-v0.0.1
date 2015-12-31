'''
    Ultimate Whitecream
    Copyright (C) 2015 mortael
    Copyright (C) 2015 anton40

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, re, base64
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

import utils

progress = utils.progress

def Main():
    utils.addDir('[COLOR green]Search[/COLOR]','http://www.boyfriendtv.com/searchgate.php', 394, '', '')
    utils.addDir('[COLOR green]Channels[/COLOR]','http://www.boyfriendtv.com/channels/', 393, '', '')
	utils.addDir('[COLOR green]Best Recent[/COLOR]','http://www.boyfriendtv.com/?s=', 392, '', '')
	utils.addDir('[COLOR green]Date Added[/COLOR]','http://www.boyfriendtv.com/videos/newest/?s=', 391, '', '')
	utils.addDir('[COLOR green]Most Popular[/COLOR]','http://www.boyfriendtv.com/videos/most-popular/today/?s=', 390, '', '')
	utils.addDir('[COLOR green]Top Rated[/COLOR]','http://www.boyfriendtv.com/videos/top-rated/?s=', 389, '', '')
	utils.addDir('[COLOR green]Longest[/COLOR]','http://www.boyfriendtv.com/videos/longest/?s=', 388, '', '')
	utils.addDir('[COLOR green]Random[/COLOR]','http://www.boyfriendtv.comvideos/random/?s=', 387, '', '')
    List('http://www.boyfriendtv.com')
    xbmcplugin.endOfDirectory(utils.addon_handle)

def List(url):
    print "boyfriendtv::List " + url
    listhtml = utils.getHtml(url, '')
    match = re.compile('<li class="videoblock".+?<a href="([^"]+)" title="([^"]+)".+?<var class="duration">([^<]+).*?data-mediumthumb="([^"]+)"', re.DOTALL).findall(listhtml)
    for videopage, name, duration, img in match:
        name = utils.cleantext(name)
        name = name + " [COLOR blue]" + duration + "[/COLOR]"
        utils.addDownLink(name, 'http://www.boyfriendtv.com' + videopage, 386, img, '')
    try:
        nextp=re.compile('<li class="page_next"><a href="(.+?)" class="orangeButton">Next</a></li>', re.DOTALL).findall(listhtml)
        utils.addDir('Next Page', 'http://www.boyfriendtv.com' + nextp[0].replace('&amp;','&'), 385,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def Search(url):
    searchUrl = url
    vq = utils._get_keyboard(heading="Searching for...")
    if (not vq): return False, 0
    title = urllib.quote_plus(vq)
    title = title.replace(' ','+')
    searchUrl = searchUrl + title
    print "Searching URL: " + searchUrl
    List(searchUrl)

def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<div class="category-wrapper">.+?<a href="(.+?)"  alt="(.+?)">.+?<img src="(.+?)"', re.DOTALL).findall(cathtml)
    for catpage, name, img, in sorted(match, key=lambda item: item[1]):
        if '?' in catpage:
            utils.addDir(name, 'http://www.boyfriendtv.com' + catpage + "&o=cm", 385, img, '')
        else:
            utils.addDir(name, 'http://www.boyfriendtv.com' + catpage + "?o=cm", 385, img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)
    
def Playvid(url, name, download=None):
    html = utils.getHtml(url, '')
    videourl = re.compile("var player_quality_.+? = '(.+?)'").findall(html)
    videourl = videourl[-1]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)