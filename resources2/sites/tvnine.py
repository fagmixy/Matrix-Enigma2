#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'tvnine'
SITE_NAME = 'tv96'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.tv96.tv'

SPORT_LIVE = ('https://www.tv96.tv', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'البث المباشر', 'sport.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

   
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
# ([^<]+) .+? (.+?)

    sPattern = '<div class="containerMatch"><a href="(.+?)" target=.+?<div style="font-weight: bold">(.+?)</div>.+?<div class="matchTime">(.+?)</div>.+?<div style="font-weight: bold">(.+?)</div>'



    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
 
            sTitle =  aEntry[1]+' vs '+aEntry[3]
            sThumbnail = ""
            siteUrl = aEntry[0]
            sInfo = aEntry[2]
			
			
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addMisc(SITE_IDENTIFIER, 'showLive', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showLive():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # (.+?) # ([^<]+) .+? 
    sPattern = 'data-embed="(.+?)">(.+?)</li>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
   
    if (aResult[0] == True):
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = ''
            oRequestHandler = cRequestHandler(siteUrl)
            data = oRequestHandler.request()
            oParser = cParser()
    # (.+?) # ([^<]+) .+? 
            sPattern = 'source: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if (aResult[0] == True):
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)  
    # (.+?) # ([^<]+) .+? 
            sPattern = "hls: '(.+?)'"
            aResult = oParser.parse(data, sPattern)
            if (aResult[0] == True):
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
    # (.+?) # ([^<]+) .+? 
            sPattern = 'file: "(.+?)",'
            aResult = oParser.parse(data, sPattern)
            if (aResult[0] == True):
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)   
    # (.+?) # ([^<]+) .+? 
            sPattern = '<iframe src=".+?stream_url=(.+?)" height'
            aResult = oParser.parse(data, sPattern)
            UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
            if (aResult[0] == True):
               for aEntry in aResult[1]:
            
                   url = aEntry
                   sHosterUrl = url+ '|User-Agent=' + UA + '&Referer=https://yastatic.net/' 
                   sMovieTitle = sTitle
            

                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if (oHoster != False):
                       oHoster.setDisplayName(sMovieTitle)
                       oHoster.setFileName(sMovieTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)    
           

             
    oGui.setEndOfDirectory() 
	
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    # (.+?) # ([^<]+) .+? 
    sPattern = 'source: "(.+?)",'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = aEntry
            sHosterUrl = url
            sMovieTitle = sMovieTitle
            

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

                
    oGui.setEndOfDirectory()