#coding: utf-8
#
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidload', 'VidLoad')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern =  'var token="([^"]+)".+?var crsf="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            aEntry = aResult[1][0]

            oRequest = cRequestHandler('https://www.vidload.net/vid/')
            oRequest.addParameters('gone', aEntry[0])
            oRequest.addParameters('oujda', aEntry[1])
            oRequest.addParameters('referer', self._url)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)

            resolvedUrl = oRequest.request()
            if resolvedUrl:
                resolvedUrl = resolvedUrl.replace('\r\n', '')
                return True, resolvedUrl

        return False, False
