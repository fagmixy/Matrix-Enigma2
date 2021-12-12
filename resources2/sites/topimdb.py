# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.mino60.TmpName

import re
import unicodedata

from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.comaddon import progress
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.inputParameterHandler import cInputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.outputParameterHandler import cOutputParameterHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.requestHandler import cRequestHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.parser import cParser
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import Quote

SITE_IDENTIFIER = 'topimdb'
SITE_NAME = '[COLOR orange]Top 1000 IMDb[/COLOR]'
SITE_DESC = 'Base de donnees videos.'


URL_MAIN = 'https://www.imdb.com/'
POSTER_URL = 'https://ia.media-imdb.com/images/m/'
FANART_URL = 'https://ia.media-.imdb.com/images/m/'
# FANART_URL = 'https://image.tmdb.org/t/p/w780/'
# FANART_URL = 'https://image.tmdb.org/t/p/original/'

MOVIE_WORLD = (URL_MAIN + 'search/title?groups=top_1000&sort=user_rating,desc&start=1', 'showMovies')
MOVIE_TOP250 = (URL_MAIN + 'search/title?count=100&groups=top_250', 'showMovies')
# MOVIE_TOP2021 = (URL_MAIN + 'search/title?year=2021,2021&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2020 = (URL_MAIN + 'search/title?year=2020,2020&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2019 = (URL_MAIN + 'search/title?year=2019,2019&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2018 = (URL_MAIN + 'search/title?year=2018,2018&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2017 = (URL_MAIN + 'search/title?year=2017,2017&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2016 = (URL_MAIN + 'search/title?year=2016,2016&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2015 = (URL_MAIN + 'search/title?year=2015,2015&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2014 = (URL_MAIN + 'search/title?year=2014,2014&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2013 = (URL_MAIN + 'search/title?year=2013,2013&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2012 = (URL_MAIN + 'search/title?year=2012,2012&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2011 = (URL_MAIN + 'search/title?year=2011,2011&title_type=feature&explore=languages', 'showMovies')
MOVIE_TOP2010 = (URL_MAIN + 'search/title?year=2010,2010&title_type=feature&explore=languages', 'showMovies')
MOVIE_FAMILY = (URL_MAIN + 'search/title/?genres=family&title_type=feature&explore=genres', 'showMovies')
MOVIE_SAFE1 = (URL_MAIN + 'list/ls071966357/', 'showMovies')
MOVIE_SAFE2 = (URL_MAIN + 'list/ls051507148/', 'showMovies')
MOVIE_SAFE3 = (URL_MAIN + 'list/ls049481487/', 'showMovies')
MOVIE_SAFE4 = (URL_MAIN + 'list/ls025574708/', 'showMovies')
MOVIE_SAFE5 = (URL_MAIN + 'list/ls036376058/', 'showMovies')


def unescape(text):
    try:  # python 2
        import htmlentitydefs
    except ImportError:  # Python 3
        import html.entities as htmlentitydefs

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WORLD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WORLD[1], 'Top Films Mondial', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP250[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP250[1], 'Top 250', 'star.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2021[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2021[1], 'Top Films 2021', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2020[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2020[1], 'Top Films 2020', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2019[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2019[1], 'Top Films 2019', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2018[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2018[1], 'Top Films 2018', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2017[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2017[1], 'Top Films 2017', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2016[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2016[1], 'Top Films 2016', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2015[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2015[1], 'Top Films 2015', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2014[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2014[1], 'Top Films 2014', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2013[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2013[1], 'Top Films 2013', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2012[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2012[1], 'Top Films 2012', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2011[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2011[1], 'Top Films 2011', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP2010[1], 'Top Films 2010', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FAMILY[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FAMILY[1], 'Top 50 Family Movies', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAFE1[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAFE1[1], 'SAFE MOVIES 1', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAFE2[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAFE2[1], 'SAFE MOVIES 2', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAFE3[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAFE3[1], 'SAFE MOVIES 3', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAFE4[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAFE4[1], 'SAFE MOVIES 4', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAFE5[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAFE5[1], 'SAFE MOVIES 5', 'star.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    # bGlobal_Search = False

    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    # if URL_SEARCH[0] in sSearch:
        # bGlobal_Search = True

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'img alt="([^"]+).+?loadlate="([^"]+).+?primary">([^<]+).+?unbold">([^<]+).+?(?:|rated this(.+?)\s.+?)muted">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # sTitle = unicode(aEntry[0], 'utf-8')  # converti en unicode
            # sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')  # vire accent
            # sTitle = unescape(str(aEntry[1]))
            # sTitle = sTitle.encode( "utf-8")

            sTitle = ('%s %s [COLOR fuchsia]%s[/COLOR]') % (aEntry[2], aEntry[0], aEntry[4])
            sThumb = aEntry[1].replace('UX67', 'UX328').replace('UY98', 'UY492').replace('67', '0').replace('98', '0')
            sYear = re.search('([0-9]{4})', aEntry[3]).group(1)
            sDesc = aEntry[5]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'none')
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('searchtext', showTitle(str(aEntry[0]), str('none')))
            oGui.addMovie('globalSearch', 'showSearch', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory('500')


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="flat-button lister-page-next next-page" href="([^<]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = ('%s/%s') % (URL_MAIN, aResult[1][0])
        return sUrl
    sPattern = 'href="([^"]+?)"class="lister-page-next'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = ('%s/%s') % (URL_MAIN, aResult[1][0])
        return sUrl

    return False


def showTitle(sMovieTitle, sUrl):

    sExtraTitle = ''
    # si c'est une serie
    if sUrl != 'none':
        sExtraTitle = sUrl.split('|')[1]
        sMovieTitle = sUrl.split('|')[0]

    try:
        # ancien decodage
        sMovieTitle = unicode(sMovieTitle, 'utf-8')  # converti en unicode pour aider aux convertions
        sMovieTitle = unicodedata.normalize('NFD', sMovieTitle).encode('ascii', 'ignore').decode("unicode_escape")  # vire accent et '\'
        sMovieTitle = sMovieTitle.encode("utf-8").lower()  # on repasse en utf-8
    except:
        sMovieTitle = sMovieTitle.lower()

    sMovieTitle = Quote(sMovieTitle)
    sMovieTitle = re.sub('\(.+?\)', ' ', sMovieTitle)  # vire les tags entre parentheses

    # modif venom si le titre comporte un - il doit le chercher
    sMovieTitle = re.sub(r'[^a-z -]', ' ', sMovieTitle)  # vire les caracteres a la con qui peuvent trainer
    # sMovieTitle = re.sub('( |^)(le|la|les|du|au|a|l)( |$)', ' ', sMovieTitle)  # vire les articles

    # vire les espaces multiples et on laisse les espaces sans modifs car certains codent avec %20 d'autres avec +
    sMovieTitle = re.sub(' +', ' ', sMovieTitle)
    # modif ici
    if sExtraTitle:
        sMovieTitle = sMovieTitle.replace('%C3%A9', 'e').replace('%C3%A0', 'a')
        sMovieTitle = sMovieTitle + sExtraTitle
    else:
        sMovieTitle = sMovieTitle

    return sMovieTitle
