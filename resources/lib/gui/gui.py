# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib import xbmc

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import listitem, addon, dialog, isKrypton, window
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.db import cDb
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.contextElement import cContextElement
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.guiElement import cGuiElement
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.pluginHandler import cPluginHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import QuotePlus
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, GetCacheSubDir

import pickle
import time

class cGui:

    SITE_NAME = 'cGui'
    CONTENT = 'files'
    searchResults = []
    listing = []
    ADDON = addon()

    if isKrypton():
        CONTENT = 'addons'

    def addNewDir(self, Type, sId, sFunction, sLabel, sIcon, sThumbnail='', sDesc='', oOutputParameterHandler='', sMeta=0, sCat=None):
        oGuiElement = cGuiElement()
        # dir ou link => CONTENT par défaut = files
        if Type != 'dir' and Type != 'link':
            cGui.CONTENT = Type
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)

        if sThumbnail == '':
            oGuiElement.setThumbnail(oGuiElement.getIcon())
            
        else:       
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        oGuiElement.setMeta(sMeta)
        oGuiElement.setDescription(sDesc)

        if sCat is not None:
            oGuiElement.setCat(sCat)
            
        # Pour addLink on recupere le sCat precedent.
        elif Type == 'link':
            oInputParameterHandler = cInputParameterHandler()
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat:
                oGuiElement.setCat(sCat)

        oOutputParameterHandler.addParameter('sFav', sFunction)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        try:
            self.addFolder(oGuiElement, oOutputParameterHandler)
        except:
            pass

    def addMovie(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        self.addNewDir('movies', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 1, 1)

    def addTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        self.addNewDir('tvshows', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 2, 2)

    def addAnime(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        self.addNewDir('tvshows', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 4, 2)

    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        if sThumbnail or sDesc:
            type = 'videos'
        else:
            type = 'files'
        self.addNewDir(type, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, 5)

    def addMoviePack(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        self.addNewDir('movies', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 3, 1)

    def addDir(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler='', sDesc=""):
        self.addNewDir('dir', sId, sFunction, sLabel, sIcon, '', sDesc, oOutputParameterHandler, 0, None)

    def addLink(self, sId, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler=''):
        sIcon = sThumbnail
        self.addNewDir('link', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, None)

    def addSeason(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
        oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('seasons', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 5, 4)


    def addEpisode(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes, l'URL de la saison
        oInputParameterHandler = cInputParameterHandler()
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        if saisonUrl:   # Retenu depuis "addSeason"
            oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
            oOutputParameterHandler.addParameter('nextSaisonFunc', oInputParameterHandler.getValue('nextSaisonFunc'))
        else:           # calculé depuis l'url qui nous a emmené ici sans passé par addSeason
            oOutputParameterHandler.addParameter('saisonUrl', oInputParameterHandler.getValue('siteUrl'))
            oOutputParameterHandler.addParameter('nextSaisonFunc', oInputParameterHandler.getValue('function'))
			
        if not oOutputParameterHandler.getValue('sLang'):
            oOutputParameterHandler.addParameter('sLang', oInputParameterHandler.getValue('sLang'))


        return self.addNewDir('episodes', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 6, 8)

    # Affichage d'une personne (acteur, réalisateur, ..)
    def addPerson(self, sId, sFunction, sLabel, sIcon, sThumbnail, oOutputParameterHandler=''):
        sThumbnail = ''
        sDesc = ''
        self.addNewDir('artists', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 7, None)

    # Affichage d'un réseau de distribution du média
    def addNetwork(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler=''):
        sThumbnail = ''
        sDesc = ''
        self.addNewDir('files', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 8, None)

    def addNext(self, sId, sFunction, sLabel, oOutputParameterHandler):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle('[COLOR teal]' + sLabel + ' >>>[/COLOR]')
        oGuiElement.setIcon('next.png')
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        oGuiElement.setCat(5)

        self.createContexMenuPageSelect(oGuiElement, oOutputParameterHandler)
        self.createContexMenuViewBack(oGuiElement, oOutputParameterHandler)
        self.addFolder(oGuiElement, oOutputParameterHandler)

    # utiliser oGui.addText(SITE_IDENTIFIER)
    def addNone(self, sId):
        return self.addText(sId)

    def addText(self, sId, sLabel='', sIcon='none.png'):
        printDBG('addText0001:')
        # Pas de texte lors des recherches globales
        if window(10101).getProperty('search') == 'true':
            return

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction('DoNothing')
        if not sLabel:
            sLabel = self.ADDON.VSlang(30204)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)

        oOutputParameterHandler = cOutputParameterHandler()
        self.addFolder(oGuiElement, oOutputParameterHandler)

    # non utiliser depuis le 22/04
    def addMovieDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler=''):

        cGui.CONTENT = 'movies'
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(1)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(7)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    # non utiliser 22/04
    def addTVDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler=''):

        cGui.CONTENT = 'tvshows'
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(2)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(7)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    # afficher les liens non playable
    def addFolder(self, oGuiElement, oOutputParameterHandler='', _isFolder=True):
        printDBG('addFolder0001:')
        # recherche append les reponses
        if window(10101).getProperty('search') == 'true':
            import copy
            cGui.searchResults.append({'guiElement': oGuiElement, 'params': copy.deepcopy(oOutputParameterHandler)})
            return

        # Des infos a rajouter ?
        params = {'siteUrl': oGuiElement.setSiteUrl,
                  'sTmdbId': oGuiElement.setTmdbId,
                  'sYear': oGuiElement.setYear}

        try:
            for sParam, callback in params.iteritems():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)
        except AttributeError:
            for sParam, callback in params.items():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)
        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty('IsPlayable', 'false')

        sCat = oGuiElement.getCat()
        if sCat:
            cGui.sCat = sCat
            oOutputParameterHandler.addParameter('sCat', sCat)

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        if cGui.CONTENT in ('movies', 'tvshows', 'episodes'):
            self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
            self.createContexMenuba(oGuiElement, oOutputParameterHandler)
            self.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)

            if self.ADDON.getSetting('bstoken') != '':
                self.createContexMenuTrakt(oGuiElement, oOutputParameterHandler)
            if self.ADDON.getSetting('tmdb_account') != '':
                self.createContexMenuTMDB(oGuiElement, oOutputParameterHandler)
            self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)
            self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        elif sCat and sCat == 5:    # MISC
            self.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)
            self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
        oListItem = self.__createContextMenu(oGuiElement, oListItem)
        self.listing.append((sItemUrl, oListItem, _isFolder))
        # Vider les paramètres pour être recyclé
        self.TsiplayerWrite(oGuiElement, oOutputParameterHandler)
        #oOutputParameterHandler.clearParameter()

    def TsiplayerWrite(self,oGuiElement, oOutputParameterHandler):
        sPluginPath='Tsiplayer'
        sParams    = oOutputParameterHandler.getParameterAsUri()     
        sId        = oGuiElement.getSiteName()
        sLabel     = oGuiElement.getTitle()
        sFunction  = oGuiElement.getFunction()
        sIcon      = oGuiElement.getIcon()
        sThumbnail = oGuiElement.getThumbnail()
        sMeta      = oGuiElement.getMeta()
        sItemUrl = '%s?site=%s&function=%s&title=%s&meta=%s&%s' % (sPluginPath, sId, sFunction, QuotePlus(str(sLabel)),sMeta, sParams)
        if sIcon == 'special://home/addons/plugin.video.matrix/resources2/art/':
            sIcon = sThumbnail  
        #PIK = self.MyPath() + "VStream_listing.dat"
        PIK = self.MyPath() + ("tmdb/matrix_listing_%s.dat" % sId)
        time_now = round(time.time() * 1000)
        data = [oGuiElement, oOutputParameterHandler,time_now]
        with open(PIK, "a+b") as f:
            pickle.dump(data, f)        
        return ''
        
    def MyPath(self):
        return GetCacheSubDir('Tsiplayer')
        
    # affiche les liens playable
    def addHost(self, oGuiElement, oOutputParameterHandler=''):
        oInputParameterHandler = cInputParameterHandler()
        cGui.CONTENT = 'files'

        if oOutputParameterHandler.getValue('siteUrl'):
            sSiteUrl = oOutputParameterHandler.getValue('siteUrl')
            oGuiElement.setSiteUrl(sSiteUrl)

        # On récupere le sCat du fichier précédent.
        sCat = oInputParameterHandler.getValue('sCat')
        if sCat:
            oGuiElement.setCat(sCat)

        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty('IsPlayable', 'true')
        oListItem.setProperty('Video', 'true')
        oListItem.addStreamInfo('video', {})

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        self.listing.append((sItemUrl, oListItem, False))
        self.TsiplayerWrite(oGuiElement, oOutputParameterHandler)

    def createListItem(self, oGuiElement):

        oListItem = listitem(oGuiElement.getTitle())

        # voir : https://kodi.wiki/view/InfoLabels
        oListItem.setInfo(oGuiElement.getType(), oGuiElement.getItemValues())
        oListItem.setArt({'poster': oGuiElement.getPoster(),
                          'thumb': oGuiElement.getThumbnail(),
                          'icon': oGuiElement.getIcon(),
                          'fanart': oGuiElement.getFanart()})

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey, sPropertyValue in aProperties.items():
            oListItem.setProperty(sPropertyKey, str(sPropertyValue))

        return oListItem

    # Marquer vu/Non vu
    def createContexMenuWatch(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'setWatched', self.ADDON.VSlang(30206))

    def createContexMenuPageSelect(self, oGuiElement, oOutputParameterHandler):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('selectPage')
        oContext.setTitle(self.ADDON.VSlang(30017))
        oOutputParameterHandler.addParameter('OldFunction', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuViewBack(self, oGuiElement, oOutputParameterHandler):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('viewBack')
        oContext.setTitle(self.ADDON.VSlang(30018))
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    # marque page
    def createContexMenuBookmark(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler.addParameter('sCleanTitle', oGuiElement.getCleanTitle())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sFav', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'setBookmark', self.ADDON.VSlang(30210))

    def createContexMenuTrakt(self, oGuiElement, oOutputParameterHandler= ''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        sType = cGui.CONTENT.replace('tvshows', 'shows')
        oOutputParameterHandler.addParameter('sType', sType)
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cTrakt', 'cTrakt', 'getAction', self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, oGuiElement, oOutputParameterHandler = ''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'themoviedb_org', 'themoviedb_org', 'getAction', 'TMDB')

    def createContexMenuDownload(self, oGuiElement, oOutputParameterHandler='', status='0'):
        if status == '0':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StartDownloadOneFile', self.ADDON.VSlang(30215))

        if status == '0' or status == '2':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'delDownload', self.ADDON.VSlang(30216))
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'DelFile', self.ADDON.VSlang(30217))

        if status == '1':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StopDownloadList', self.ADDON.VSlang(30218))

        if status == '2':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ReadDownload', self.ADDON.VSlang(30219))
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ResetDownload', self.ADDON.VSlang(30220))

    # Information
    def createContexMenuinfo(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewInfo', self.ADDON.VSlang(30208))

    # Bande annonce
    def createContexMenuba(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())
        oOutputParameterHandler.addParameter('sTrailerUrl', oGuiElement.getTrailer())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewBA', self.ADDON.VSlang(30212))

    # Recherche similaire
    def createContexMenuSimil(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewSimil', self.ADDON.VSlang(30213))

    def createSimpleMenu(self, oGuiElement, oOutputParameterHandler, sFile, sName, sFunction, sTitle):
        oContext = cContextElement()
        oContext.setFile(sFile)
        oContext.setSiteName(sName)
        oContext.setFunction(sFunction)
        oContext.setTitle(sTitle)

        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuDelFav(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delBookmarksMenu', self.ADDON.VSlang(30209))

    def createContexMenuSettings(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'globalParametre', 'globalParametre', 'opensetting', self.ADDON.VSlang(30023))

    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        # Menus classiques reglés a la base
        if len(oGuiElement.getContextItems()) > 0:
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem

    def __ContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        if len(oGuiElement.getContextItems()) > 0:
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus)

        return oListItem

    def __ContextMenuPlay(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        if len(oGuiElement.getContextItems()) > 0:
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus)

        return oListItem

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if (oOutputParameterHandler == ''):
            oOutputParameterHandler = cOutputParameterHandler()

        sParams = oOutputParameterHandler.getParameterAsUri()

        sPluginPath = cPluginHandler().getPluginPath()

        if (len(oGuiElement.getFunction()) == 0):
            sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), QuotePlus(oGuiElement.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), QuotePlus(oGuiElement.getCleanTitle()), sParams)

        return sItemUrl

    def setEndOfDirectory(self, ForceViewMode=False):
        printDBG('set end of dir')

    def updateDirectory(self):  # refresh the content
        xbmc.executebuiltin('Container.Refresh')
        xbmc.sleep(600)    # Nécessaire pour laisser le temps du refresh

    def viewBA(self):
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')
        sYear = oInputParameterHandler.getValue('sYear')
        sTrailerUrl = oInputParameterHandler.getValue('sTrailerUrl')
        sMeta = oInputParameterHandler.getValue('sMeta')

        from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.ba import cShowBA
        cBA = cShowBA()
        cBA.SetSearch(sFileName)
        cBA.SetYear(sYear)
        cBA.SetTrailerUrl(sTrailerUrl)
        cBA.SetMetaType(sMeta)
        cBA.SearchBA()

    def viewBack(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sTest = '%s?site=%s' % (sPluginPath, sId)

        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def viewInfo(self):
        if addon().getSetting('information-view') == "false":
            from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.config import WindowsBoxes

            oInputParameterHandler = cInputParameterHandler()
            sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
            sMeta = oInputParameterHandler.getValue('sMeta') if oInputParameterHandler.exist('sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            sYear = oInputParameterHandler.getValue('sYear') if oInputParameterHandler.exist('sYear') else xbmc.getInfoLabel('ListItem.Year')

            WindowsBoxes(sCleanTitle, sCleanTitle, sMeta, sYear)
        else:
            # On appel la fonction integrer a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')

    def viewSimil(self):
        sPluginPath = cPluginHandler().getPluginPath()

        oInputParameterHandler = cInputParameterHandler()
        sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('searchtext', sCleanTitle)
        oOutputParameterHandler.addParameter('sCat', sCat)
        oOutputParameterHandler.addParameter('readdb', 'False')

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, 'globalSearch', 'globalSearch', sParams)

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % (10028))

        xbmc.executebuiltin('Container.Update(%s)' % sTest)

        return False

    def selectPage(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        if siteUrl.endswith('/'):  # for the url http.://www.1test.com/annee-2020/page-2/
            urlSource = siteUrl.rsplit('/', 2)[0]
            endOfUrl = siteUrl.rsplit('/', 2)[1] + '/'
        else:  # for the url http.://www.1test.com/annee-2020/page-2 or /page-2.html
            urlSource = siteUrl.rsplit('/', 1)[0]
            endOfUrl = siteUrl.rsplit('/', 1)[1]

        oParser = cParser()
        oldNum = oParser.getNumberFromString(endOfUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = urlSource + '/' + endOfUrl.replace(oldNum, newNum, 1)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
                xbmc.executebuiltin('Container.Update(%s)' % sTest)
            except:
                return False

        return False

    def selectPage2(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        selpage = self.showNumBoard()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('Selpage', selpage)

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def setWatched(self):
        if True:
            # Use vStream database
            oInputParameterHandler = cInputParameterHandler()
            sSite = oInputParameterHandler.getValue('siteUrl')
            sTitle = oInputParameterHandler.getValue('sTitleWatched')
            if not sTitle:
                return

            meta = {}
            meta['title'] = sTitle
            meta['site'] = sSite

            db = cDb()
            row = db.get_watched(meta)
            if row:
                db.del_watched(meta)
                db.del_resume(meta)
            else:
                db.insert_watched(meta)
            # To test
            # updateDirectory()

        else:
            # Use kodi buildin feature
            xbmc.executebuiltin('Action(ToggleWatched)')

        # Not usefull ?
        # updateDirectory()

    def showKeyBoard(self, sDefaultText='', heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(heading)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def showNumBoard(self, sDefaultNum=''):
        dialogs = dialog()
        numboard = dialogs.numeric(0, self.ADDON.VSlang(30019), sDefaultNum)
        # numboard.doModal()
        if numboard is not None:
            return numboard

        return False

    def openSettings(self):
        return False

    def showNofication(self, sTitle, iSeconds=0):
        return False

    def showError(self, sTitle, sDescription, iSeconds=0):
        return False

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        return False
        del self.listing[:]

    def updateDirectory(self):  # refresh the content
        xbmc.executebuiltin('Container.Refresh')
        xbmc.sleep(600)    # Nécessaire pour laisser le temps du refresh

    def viewBA(self):
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')
        sYear = oInputParameterHandler.getValue('sYear')
        sTrailerUrl = oInputParameterHandler.getValue('sTrailerUrl')
        sMeta = oInputParameterHandler.getValue('sMeta')

        from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.ba import cShowBA
        cBA = cShowBA()
        cBA.SetSearch(sFileName)
        cBA.SetYear(sYear)
        cBA.SetTrailerUrl(sTrailerUrl)
        cBA.SetMetaType(sMeta)
        cBA.SearchBA()

    def viewBack(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sTest = '%s?site=%s' % (sPluginPath, sId)

        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def viewInfo(self):
        if addon().getSetting('information-view') == "false":
            from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.config import WindowsBoxes

            oInputParameterHandler = cInputParameterHandler()
            sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
            sCleanTitle = sCleanTitle.split('مدبلج')[0]
            sMeta = oInputParameterHandler.getValue('sMeta') if oInputParameterHandler.exist('sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            sYear = oInputParameterHandler.getValue('sYear') if oInputParameterHandler.exist('sYear') else xbmc.getInfoLabel('ListItem.Year')

            WindowsBoxes(sCleanTitle, sCleanTitle, sMeta, sYear)
        else:
            # On appel la fonction integrer a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')
		
    def viewParents(self):
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')
        sFileName = sFileName.split('مدبلج')[0]
        sType = oInputParameterHandler.getValue('sType')
        sImdbId = oInputParameterHandler.getValue('sImdbId')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sIMDb = 'tt9536846'
        if 'movie'in sType:
            meta = cTMDb().get_meta(sType, sFileName, imdb_id = xbmc.getInfoLabel('ListItem.Property(ImdbId)'))
            sIMDb = meta['imdb_id']
            sUrl = 'https://www.imdb.com/title/'+sIMDb+'/parentalguide?ref_=tt_stry_pg'
        else:
            meta = cTMDb().search_tvshow_id(sTmdbId)
            sIMDb = meta['external_ids']['imdb_id']
            sUrl = 'https://www.imdb.com/title/'+sIMDb+'/parentalguide?ref_=tt_stry_pg'
        oRequest = urllib2.Request(sUrl)
        oResponse = urllib2.urlopen(oRequest)
        DIALOG = dialog()

                # En python 3 on doit décoder la reponse
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            sContent = oResponse.read().decode('utf-8')
        else:
            sContent = oResponse.read()
        Stext = "لم يقع تصنيف المحتوى"
        Stext0 = ""
        oParser = cParser()
        sPattern = '>MPAA</td>.+?<td>([^<]+)<'
        aResult = oParser.parse(sContent, sPattern)
        if (aResult[0]):
            Stext0 = aResult[1][0]
        if 'Rated R' in Stext0 and 'sex' not in Stext0:
            Stext = 'غير مناسب للمشاهدة العائلية'
        if 'Rated R' in Stext0 and 'sex'  in Stext0 or 'nudity'  in Stext0:
            Stext = 'تحذير غير مناسب للمشاهدة وجود أو تكرار مشاهد تحتوي على عُري أو لقطات خادشة للحياء'
        if 'Rated R' not in Stext0:
            sPattern = 'Nudity</h4>.+?ipl-status-pill.+?">([^<]+)</span>'
            aResult = oParser.parse(sContent, sPattern)
            if (aResult[0]):
               Stext2 = aResult[1][0]
               if 'None'  in Stext2:
                  Stext = '  مناسب للمشاهدة العائلية'
               if 'Mild'  in Stext2:
                  Stext = '   بعض المواد قد لا تكون مناسبة'
               if 'Moderate'  in Stext2:
                  Stext = '   غير مناسب للمشاهدة العائلية'
               if 'Severe'  in Stext2:
                  Stext = 'تحذير غير مناسب للمشاهدة وجود أو تكرار مشاهد تحتوي على عُري أو لقطات خادشة للحياء'
            Stext1 = re.findall('class="ipl-zebra-list__item">([^<]+)<div', sContent, re.S) 
            if Stext1:
               Stext1 = ' '.join(Stext1)
               if 'kiss'  in Stext1:
                  Stext = Stext+"\n"+' قد يحتوي بعض القبلات '
               if 'cleavage'  in Stext1 or 'bikini'  in Stext1:
                  Stext = Stext+"\n"+' ملابس غير ملائمة في بعض المشاهد '
               if 'have sex'  in Stext1 or 'topless'  in Stext1:
                  Stext = Stext+"\n"+' لقطات غير مناسبة للمشاهدة العائلية '
        Stextf = Stext+"\n"+Stext0

        ret = DIALOG.VSok(Stextf)
						
    def viewSimil(self):
        sPluginPath = cPluginHandler().getPluginPath()

        oInputParameterHandler = cInputParameterHandler()
        sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('searchtext', sCleanTitle)
        oOutputParameterHandler.addParameter('sCat', sCat)
        oOutputParameterHandler.addParameter('readdb', 'False')

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, 'globalSearch', 'globalSearch', sParams)

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % (10028))

        xbmc.executebuiltin('Container.Update(%s)' % sTest)

        return False

    def selectPage(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        if siteUrl.endswith('/'):  # for the url http.://www.1test.com/annee-2020/page-2/
            urlSource = siteUrl.rsplit('/', 2)[0]
            endOfUrl = siteUrl.rsplit('/', 2)[1] + '/'
        else:  # for the url http.://www.1test.com/annee-2020/page-2 or /page-2.html
            urlSource = siteUrl.rsplit('/', 1)[0]
            endOfUrl = siteUrl.rsplit('/', 1)[1]

        oParser = cParser()
        oldNum = oParser.getNumberFromString(endOfUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = urlSource + '/' + endOfUrl.replace(oldNum, newNum, 1)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
                xbmc.executebuiltin('Container.Update(%s)' % sTest)
            except:
                return False

        return False

    def selectPage2(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        selpage = self.showNumBoard()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('Selpage', selpage)

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def setWatched(self):
        if True:
            # Use matrix database
            oInputParameterHandler = cInputParameterHandler()
            sSite = oInputParameterHandler.getValue('siteUrl')
            sTitle = oInputParameterHandler.getValue('sTitleWatched')
            sCat = oInputParameterHandler.getValue('sCat')
            if not sTitle:
                return

            meta = {}
            meta['title'] = sTitle
            meta['titleWatched'] = sTitle
            meta['site'] = sSite
            meta['cat'] = sCat

            from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.db import cDb
            db = cDb()
            row = db.get_watched(meta)
            if row:
                db.del_watched(meta)
                db.del_resume(meta)
            else:
                db.insert_watched(meta)
                db.del_viewing(meta)
            # To test
            # updateDirectory()

        else:
            # Use kodi buildin feature
            xbmc.executebuiltin('Action(ToggleWatched)')

        self.updateDirectory()

    def showKeyBoard(self, sDefaultText='', heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(heading)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def showNumBoard(self, sDefaultNum=''):
        dialogs = dialog()
        numboard = dialogs.numeric(0, self.ADDON.VSlang(30019), sDefaultNum)
        # numboard.doModal()
        if numboard is not None:
            return numboard

        return False

    def openSettings(self):
        return False

    def showNofication(self, sTitle, iSeconds=0):
        return False

    def showError(self, sTitle, sDescription, iSeconds=0):
        return False

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        return False
