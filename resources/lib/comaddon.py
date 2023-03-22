# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib import xbmc
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib import xbmcgui
import re,os.path,sys

# class addon(xbmcaddon.Addon):
class none_(object):
    def __new__(cls, *args):
        return object.__new__(cls)
    def __init__(self, *args):
        pass
    def __getattr__(self, name):
        return self
    def __call__(self, *args, **kwargs):
        return self
    def __int__(self):
        return 0
    def __float__(self):
        return 0
    def __str__(self):
        return '0'
    def __nonzero__(self):
        return False
    def __getitem__(self, key):
        return self
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __len__(self):
        return 3
    def __iter__(self):
        return iter([self, self, self])


        
class listitem(none_):

    #ListItem([label, label2, iconImage, thumbnailImage, path])
    def __init__(self, label = '', label2 = '', iconImage = '', thumbnailImage = '', path = ''):
        pass

class addon():
    def __init__(self, addonId = None):
        self.addonId = addonId

    def openSettings(self):
        return None
        
    def getSetting(self, key):
        if key   == 'poster_tmdb'     : return 'w342' 
        elif key == 'poster_tmdb'     : return 'w1280'
        elif key == 'api_tmdb'        : return 'b7cf9324cbeb6f4fb811144aa9397093'    
        elif key == 'tmdb_session'    : return ''
        elif key == 'history-view'    : return 'true'       
        elif key == 'home_update'     : return 'false'
        elif key == 'deco_color'      : return 'lightcoral'
        elif key == 'deco_color'      : return 'lightcoral'
        elif key == 'ZT'              :
            if os.path.exists(GetCacheSubDir('Tsiplayer')+'zt.url'):
                f = open(GetCacheSubDir('Tsiplayer')+'zt.url', "r")
                out = f.read()
                f.close() 
                printDBG('print_url='+out.strip())
                return out.strip()
            else:
                out = 'https://www.zt-za.net/index.php'
                return out.strip()
        elif '_nbItemParPage' in key  : return '25' 
        elif '_cacheDuration' in key  : return '12' 
        elif ('search' in key) and ('_type' in key)  : return False 
        elif key.startswith('plugin_'):
            if '__init__' not in key:
                return 'true' 
        return 'false'  
     
    def setSetting(self, key, value):
        if key == 'ZT':
            f = open(GetCacheSubDir('Tsiplayer')+'zt.url', "w")
            f.write(value)
            f.close()
        return None
     
    def getAddonInfo(self, info):
        return None
     
    def VSlang(self, lang):
        lng = 'French'
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/resources2/language/'+lng+'/strings.po', "r")
        data = f.read()     
        str_out = str(lang)
        lst_data=re.findall('msgctxt.*?"(.*?)".*?msgid.*?"(.*?)".*?msgstr.*?"(.*?)".*?', data, re.S)
        for (msgctxt,msgid,msgstr) in lst_data:
            if (msgctxt.replace('#','').strip() == str(lang)):
                if msgstr.strip() != '':
                    str_out = msgstr
                else:
                    str_out = msgid
                break
        return str_out

class dialog():       
    def VSselectqual(self, list_qual, list_url):
        VSlog('start:'+str(list_url))
        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]
        ret = 0
        i=0
        urlout = ''
        for url in list_url:
            urlout=urlout+url+'|tag:'+list_qual[i]+'||'
            i=i+1
        VSlog('start:'+str(urlout))
        return urlout

    def VSinfo(self, desc, title='matrix', iseconds=0, sound = False):
        return ''
        
    def VSerror(self, e):
        printDBG('VSerror: '+str(e))
        return

class progress():
    def VScreate(self, title='matrix', desc='', large=False):
        return self
    def VSupdate(self, dialog, total, text='', search = False):
        count=0
    def VSupdatesearch(self, dialog, total, text=''):
        count=0
    def VSclose(self, dialog=''):
        return
    def iscanceled(self):
        return False


class window():
    def __init__(self, winID):
        pass
        
    def getProperty(self,prop):
        return 'false'

    def clearProperty(self,prop):
        return ''        

    def setProperty(self,prop,val):
        return ''         
       
        

def VSlog(e, level=''):
    printDBG('VSlog: '+str(e))
    return

def isKrypton():
    return True

def IsPython3():
    if sys.version_info[0] < 3:
        return False
    else:
        return True


def isMatrix():
    if IsPython3():
        return True
    else:
        return False

def isNexus():
    return False


def VSPath(path):
    path = path.replace('special://temp/',GetCacheSubDir('Tsiplayer'))
    path = path.replace('special://home/userdata/addon_data/plugin.video.matrix/',GetCacheSubDir('Tsiplayer'))
    return path

def VSupdate():
    return ''