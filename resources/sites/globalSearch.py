# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.rechercheHandler import cRechercheHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, VSlog, addon, window
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib import xbmc
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import Quote
import os
from Plugins.Extensions.IPTVPlayer.tools.iptvtools       import GetCacheSubDir

def showSearch():
    VSlog('showSearch global0')
    oGui = cGui()
    addons = addon()
    VSlog('showSearch global1')
    oInputParameterHandler = cInputParameterHandler()
    VSlog('showSearch global2')
    sSearchText = oInputParameterHandler.getValue('searchtext')
    VSlog('showSearch global3')
    sCat = oInputParameterHandler.getValue('sCat')
    VSlog('showSearch global4')
    VSlog('sText='+str(sSearchText))
    oHandler = cRechercheHandler()
    oHandler.setText(sSearchText)
    oHandler.setCat(sCat)
    aPlugins = oHandler.getAvailablePlugins()
    if not aPlugins:
        return True
    VSlog('aPlugins='+str(len(aPlugins)))
    total = len(aPlugins)
    progress_ = progress().VScreate(large=True)

    # kodi 17 vire la fenetre busy qui se pose au dessus de la barre de Progress
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
    except:
        pass

    oGui.addText('globalSearch', addons.VSlang(30081) % sSearchText, 'search.png')
    sSearchText = Quote(sSearchText)

    count = 1
    for plugin in aPlugins:
        if not os.path.exists(GetCacheSubDir('Tsiplayer')+'matrix_listing.search'):
            break
        progress_.VSupdate(progress_, total, plugin['name'], True)
        if progress_.iscanceled():
            break
        oGui.addText(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']), 'sites/%s.png' % (plugin['identifier']))
        oGui.searchResults[:] = []  # vider le tableau de résultats pour les récupérer par source
        
        _pluginSearch(plugin, sSearchText)
        count += 1
 
    if not count:   # aucune source ne retourne de résultats
        oGui.addText('globalSearch')  # "Aucune information"

    progress_.VSclose(progress_)

    cGui.CONTENT = 'files'

    oGui.setEndOfDirectory()
    return True


def _pluginSearch(plugin, sSearchText):

    # Appeler la source en mode Recherche globale
    window(10101).setProperty('search', 'true')
    
    try:
        plugins = __import__('Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)
        if os.path.exists(GetCacheSubDir('Tsiplayer')+'matrix_listing.search'):
            function(sUrl)
        
        VSlog('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')