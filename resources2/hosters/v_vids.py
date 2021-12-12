from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import cUtil
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'V-Vids'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'v_vids'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        return ''
        
    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl
        
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
        
        sPattern =  "file: '(.+?)'"
              
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True): 
            cGui().showInfo(self.__sDisplayName, 'Streaming', 5)
            return True, aResult[1][0]
        else:
                cGui().showInfo(self.__sDisplayName, 'file not found' , 5)
                return False, False
        
        return False, False
