from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import dialog, xbmcgui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import VSlog
import re
#,xbmcgui,xbmc
try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'vidlo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vidlo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

            # (.+?) .+? ([^<]+)
        oParser = cParser()
        #test pour voir si code
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
        sPattern = ',{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = False

        if (aResult[0] == True):
            
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call + '|User-Agent=' + UA + '&Referer=https://www.vidlo.us' 

        return False, False