#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.hosters.hoster import iHoster
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.matrix.resources.lib.comaddon import VSlog
#import resolveurl

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'resolver', 'RSLVR-')
        self.__sRealHost = '???'

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'

    def setRealHost(self, sName):
        self.__sRealHost = sName

    def _getMediaLinkForGuest(self):
        VSlog(self._url)
        hmf = resolveurl.HostedMediaFile(url = self._url)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            if stream_url:
                return True, stream_url

        return False, False


