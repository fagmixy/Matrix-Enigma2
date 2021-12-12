# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://femax20.com/v/xxxxxxxxxx

import json
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import dialog, VSlog


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Femax'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def isDownloadable(self):
        return False

    def getPluginIdentifier(self):
        return 'femax'

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self, api_call=None):

        req = self.__sUrl.replace('/v/','/api/source/')
        pdata = 'r' # 'r' ou n'importe quelle chaine (ne doit pas etre vide)
        oRequestHandler = cRequestHandler(req)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParametersLine(pdata)
        sHtmlContent = oRequestHandler.request()
        jsonrsp  = json.loads(sHtmlContent )

        list_url = []
        list_q = []
        bfind = False
        for rsp in jsonrsp:
            if rsp == 'data':
                bfind = True   
        if not bfind:
            return False, False

        try:
            for idata in range(len(jsonrsp['data'])):
                url = jsonrsp['data'][idata]['file']
                stype = jsonrsp['data'][idata]['type']
                q = jsonrsp['data'][idata]['label']
                list_url.append(url + '.' + stype)
                list_q.append(q)

            api_call = dialog().VSselectqual(list_q, list_url)

        except:
            return False, False

        if api_call:
            return True, api_call

        return False, False
