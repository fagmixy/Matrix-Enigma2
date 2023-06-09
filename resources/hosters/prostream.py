#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.packer import cPacker
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'prostream', 'Prostream')

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern =  '<script type=\'text/javascript\'>(.+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            html = cPacker().unpack(aResult[1][0])
            sPattern = 'sources:\["([^"]+)"\]'
            aResult = oParser.parse(html, sPattern)
            if aResult[0]:
                api_call = aResult[1][0]

        if api_call:
            return True, api_call

        return False, False
