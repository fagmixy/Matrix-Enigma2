from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.pluginHandler import cPluginHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, VSlog, addon
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler

def globalSources():
    oGui           = cGui()
    oPluginHandler = cPluginHandler()
    aPlugins = oPluginHandler.getAvailablePlugins(True)

    if len(aPlugins) == 0:
        addons = addon()
        addons.openSettings()
        oGui.updateDirectory()
    else:
        for aPlugin in aPlugins:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
            icon = 'sites/%s.png' % (aPlugin[1])
            # icon = 'https://imgplaceholder.com/512x512/transparent/fff?text=%s&font-family=Roboto_Bold' % aPlugin[1]
            oGui.addDir(aPlugin[1], 'load', aPlugin[0], icon, oOutputParameterHandler)
    oGui.setEndOfDirectory()
    return
    
def searchGlobal():
    oGui = cGui()
    addons = addon()

    oInputParameterHandler = cInputParameterHandler()
    sSearchText = oInputParameterHandler.getValue('searchtext')
    sCat = oInputParameterHandler.getValue('sCat')

    oHandler = cRechercheHandler()
    oHandler.setText(sSearchText)
    oHandler.setCat(sCat)
    aPlugins = oHandler.getAvailablePlugins()
    if not aPlugins:
        return True

    total = len(aPlugins)
    progress_ = progress().VScreate(large=True)

    # kodi 17 vire la fenetre busy qui se pose au dessus de la barre de Progress
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
    except:
        pass

    oGui.addText('globalSearch', addons.VSlang(30081) % sSearchText, 'search.png')
    sSearchText = Quote(sSearchText)

    count = 0
    for plugin in aPlugins:
 
        progress_.VSupdate(progress_, total, plugin['name'], True)
        if progress_.iscanceled():
            break
 
        oGui.searchResults[:] = []  # vider le tableau de résultats pour les récupérer par source
        _pluginSearch(plugin, sSearchText)

        if len(oGui.searchResults) > 0:  # Au moins un résultat
            count += 1

            # nom du site
            oGui.addText(plugin['identifier'], '%s. [COLOR olive]%s[/COLOR]' % (count, plugin['name']), 'sites/%s.png' % (plugin['identifier']))
            for result in oGui.searchResults:
                oGui.addFolder(result['guiElement'], result['params'])
 
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
        
        function(sUrl)
        
        VSlog('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

    window(10101).setProperty('search', 'false')