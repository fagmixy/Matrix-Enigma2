#-*- coding: utf-8 -*-
#zombi https://github.com/zombiB/zombi-addons/

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress, isMatrix
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
import re
 
SITE_IDENTIFIER = 'familymoviz'
SITE_NAME = 'familymoviz'
SITE_DESC = 'arabic vod'
 
URL_MAIN = 'https://www.familymoviz.net'

MOVIE_FAM = ('https://www.familymoviz.net/category/movies/familymovies/', 'showMovies')
MOVIE_EN = ('https://www.familymoviz.net/category/movies/', 'showMovies')
MOVIE_AR = ('https://www.familymoviz.net/category/movies/arabicmovies/', 'showMovies')
KID_MOVIES = ('https://www.familymoviz.net/category/movies/familymovies/', 'showMovies')

SERIE_EN = ('https://www.familymoviz.net/foreignseries/', 'showSeries')

URL_SEARCH = ('https://www.familymoviz.net/?s=', 'showSeriesSearch')
URL_SEARCH_MOVIES = ('https://www.familymoviz.net/?s=%D9%81%D9%8A%D9%84%D9%85+', 'showMoviesSearch')
URL_SEARCH_SERIES= ('https://www.familymoviz.net/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_MOVIES', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'SEARCH_SERIES', 'search.png', oOutputParameterHandler)
    

            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.familymoviz.net/?s=%D9%81%D9%8A%D9%84%D9%85+'+sSearchText
        showMoviesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
 
def showSeriesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'https://www.familymoviz.net/?s=%D9%85%D8%B3%D9%84%D8%B3%D9%84+'+sSearchText
        showSearchSeries(sUrl)
        oGui.setEndOfDirectory()
        return
  
def showMoviesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    # (.+?) ([^<]+) .+?
    sPattern = '<div class="news-post"><a href="([^<]+)" class="imgnews"><noscript><img.+?src="([^<]+)" class="attachment-thumbnail size-thumbnail wp-post-image" alt="([^<]+)" />.+?<p class="exp-news">([^<]+)<a'
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
 
            sTitle = aEntry[2] 
            sTitle = sTitle.replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("HD","").replace("Cut","")
             
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = aEntry[3]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear) 

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
  
def showSearchSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    # (.+?) ([^<]+) .+?
    sPattern = '<div class="news-post"><a href="([^<]+)" class="imgnews"><noscript><img.+?src="([^<]+)" class="attachment-thumbnail size-thumbnail wp-post-image" alt="([^<]+)" />.+?<p class="exp-news">([^<]+)<a'
 
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
 
            sTitle = aEntry[2]
            sTitle = sTitle.replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("Season","S").replace("season","S").replace("S ","S").replace("Cut","")
             
            sThumbnail = aEntry[1]
            siteUrl = aEntry[0]
            sInfo = aEntry[3]



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
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
 
    # (.+?) ([^<]+) .+?
    sPattern = '<div class="watch_aflam2"><a href="([^<]+)">([^<]+)</a></div>.+?src="([^<]+)" class=.+?<p class="description"><a style="color:#fff;" href=".+?">([^<]+)</a>'

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
 
            sTitle = aEntry[1].replace("مشاهدة","").replace("مترجمة","").replace("مترجم","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("HD","").replace("Cut","")
            sThumbnail = aEntry[2]
            siteUrl = aEntry[0]
            sInfo = aEntry[3]
            sYear = ''
            m = re.search('([0-9]{4})', sTitle)
            if m:
                sYear = str(m.group(0))
                sTitle = sTitle.replace(sYear,'')



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sYear', sYear) 

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
 
    # (.+?) ([^<]+) .+?
    sPattern = '<div class="watch_aflam2"><a>([^<]+)</a></div><a class="imaf" href="([^<]+)"><noscript><img src="([^<]+)"></noscript>'
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
 
            
            sTitle = aEntry[0].replace("مشاهدة","").replace("مسلسل","").replace("انمي","").replace("مترجمة","").replace("مترجم","").replace("مترجمة","").replace("فيلم","").replace("اون لاين","").replace("WEB-DL","").replace("BRRip","").replace("720p","").replace("HD-TC","").replace("HDRip","").replace("HD-CAM","").replace("DVDRip","").replace("BluRay","").replace("1080p","").replace("WEBRip","").replace("WEB-dl","").replace("مترجم ","").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("Season","S").replace("season","S").replace("S ","S").replace("Cut","").replace("(","").replace(")","").replace("الموسم","S")
            sThumbnail = aEntry[2]
            siteUrl = aEntry[1]
            sInfo = ""
            sDisplayTitle = sTitle.split('S')[0]



            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
        
        progress_.VSclose(progress_)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
     
def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^<]+)'>&rsaquo;</a>"
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
     
def __checkForNextPageEpisodes(sHtmlContent):
    sPattern = '<link rel="next" href="([^<]+)" />'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        #print aResult[1][0]
        return aResult[1][0]

    return False
	
def showEpisodes():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
	
    # (.+?) ([^<]+) .+?
    sPattern = '<div class="watch_aflam2"><a href="([^<]+)">([^<]+)</a></div>.+?<p class="description"><a style=".+?" href=".+?">([^<]+)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

   
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()    
        for aEntry in aResult[1]:
 
            sTitle = aEntry[1].replace("Cut","").replace("مترجمة","").replace("مترجم","") 
            sThumbnail = sThumbnail
            siteUrl = aEntry[0]
            sInfo = ""


 
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            

 
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sInfo, oOutputParameterHandler)
 
        sNextPage = __checkForNextPageEpisodes(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)


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
    
    #Recuperation infos
    sNote = ''
    # (.+?) ([^<]+) .+?
    sPattern = '<td class="h_af">مده الحذف</td><td class="h_af2">(.+?)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote = aResult[1][0]
    if (sNote):
        oGui.addText(SITE_IDENTIFIER,'مده الحذف : ' + str(sNote))
   
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]---------[/COLOR]')
    sNote2 = ''
    # (.+?) ([^<]+) .+?
    sPattern = '<td class="h_af">الارشاد العائلي</td><td class="h_af2">(.+?)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0]):
        sNote2 = aResult[1][0]
    if (sNote2):
        oGui.addText(SITE_IDENTIFIER,'الارشاد العائلي : ' + str(sNote2))
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]---------[/COLOR]')

    sPattern = 'SRC="(.+?)".+?width'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)


    # (.+?) ([^<]+) .+?
    sPattern = '<a class="stor2" href="(.+?)">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url

            if 'goo.gl' in url or 'bit.ly' in url:
                try:
                    import requests
                    url = url
                    session = requests.Session()  # so connections are recycled
                    resp = session.head(url, allow_redirects=True)
                    url = resp.url
                except:
                    pass
            if 'file-up.org' in url:
                url = url.replace('file-up.org/','file-up.org/embed-')
                url = url + '.html'
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)


    oGui.setEndOfDirectory()