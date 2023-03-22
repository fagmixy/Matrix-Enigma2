#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser

#from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'HdVid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'hdvid'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        api_call = False

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]

        else:
            sPattern = 'file:"([^"]+)",label:"[0-9]+"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0] + '|User-Agent=' + UA# + '&Referer=' + self.__sUrl


        if (api_call):
            return True, api_call

        return False, False
