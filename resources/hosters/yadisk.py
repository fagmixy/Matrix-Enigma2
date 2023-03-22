#-*- coding: utf-8 -*-


from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import dialog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import VSlog

import re


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'yadisk'
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
        return 'yadisk'

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
        
    def __getIdFromUrl(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        VSlog(self.__sUrl)
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '"height":(.+?)},"url":"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):

            url=[]
            qua=[]
            api_call = False

            for aEntry in aResult[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False
