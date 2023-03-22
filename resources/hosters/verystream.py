#coding: utf-8
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
import re
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib 
#import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VeryStream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'verystream'

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
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        api_call = ''

        sPattern =  'id="videolink">([^<>]+)<\/p>'
        aResult = re.findall(sPattern, sHtmlContent)

        if (aResult):

            api_call = 'https://verystream.com/gettoken/' + aResult[0] + '?mime=true'

        if (api_call):
            return True, api_call

        return False, False
