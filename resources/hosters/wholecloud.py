# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Wholecloud-Movshare
import re

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'wholecloud', 'Wholecloud')

    def __getIdFromUrl(self):
        sPattern = 'v=([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        if aResult[0]:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = False

        sId = self.__getIdFromUrl()

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        r = re.search('var fkzd="([^"]+)"', sHtmlContent)
        if r:
            url = 'http://www.wholecloud.net/api/player.api.php?key=' + r.group(1) + '&file=' + sId
            oRequest = cRequestHandler(url)
            sHtmlContent = oRequest.request()
            r2 = re.search('^url=([^&]+)&', sHtmlContent)
            if r2:
                api_call = r2.group(1)

        if api_call:
            return True, api_call

        return False, False
