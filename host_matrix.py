#coding: utf-8
###################################################
from Plugins.Extensions.IPTVPlayer.tools.iptvtools             import printDBG,printExc, GetCacheSubDir
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools      import TSCBaseHostClass,tscolor
from Plugins.Extensions.IPTVPlayer.components.e2ivkselector    import GetVirtualKeyboard
###################################################
from Components.config import config
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.libs.urlparser              import urlparser
import time,os
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes          import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper     import getDirectM3U8Playlist
###################################################
import re,sys,inspect,urllib
###################################################
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.tmdb import cTMDb
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.handler.rechercheHandler import cRechercheHandler
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.util import cUtil
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.gui import cGui
from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.home import cHome
import pickle
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from os import listdir
from os.path import isfile, join
import glob
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils            import IsPython3
MAIN_URL0   = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/resources2/sites'
fncs_search = ['showsearch','myshowsearchmovie','myshowsearchserie','showmoviessearch','showsearchtext']

def getinfo():	
    info_={}
    info_['name']='Matrix'
    info_['version']='1.0 11/11/2019'
    info_['dev']='RGYSOFT'
    info_['cat_id']='902'
    info_['desc']='Matrix (KODI Addon)'
    info_['icon']='https://i.ibb.co/wJ5k47d/icon.png'
    return info_
    
def get_url_meta(URL):
    printDBG('get_url_meta='+URL)
    tags =''
    meta_={}
    if '|' in URL:
        URL,tags = URL.split('|')
        if tags!='':
            if '&' in tags:
                tags = tags.split('&')
                for tag in tags:
                    id_,val_ = tag.split('=',1)
                    meta_[id_]=val_.replace('+',' ')							
            else:	
                id_,val_ = tags.split('=')
                meta_[id_]=val_
            #URL = strwithmeta(URL,meta_)
    return (URL,meta_)

def getHosts():	
    Hosts=[]
#   Hosts.append(('26','LIVETV','livetv'             ,'1.0 18/01/2021','Live Sports'              ,'New Host',''))	
#    Hosts.append(('26','','adkami_com'         ,'1.0 18/01/2021','Animés, Mangas & Séries'  ,'New Host',''))	
#    Hosts.append(('26','','animecomplet'       ,'1.0 18/01/2021','Series & Anime'           ,'New Host',''))
    
    Hosts_=[]
    for (id_,titre,hst_,version_,desc_,up_,image) in Hosts:
        if image=='': image = 'file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/resources2/art/sites/'+hst_+'.png'
        if titre=='': titre = hst_.replace('_','.').title()
        imp0  = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.sites.'
        imp1  = 'from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.host_matrix import '
        desc  = tscolor('\c00????00')+' Info: '+tscolor('\c00??????')+desc_+'\\n '+tscolor('\c00????00')+'Version: '+tscolor('\c00??????')+version_+'\\n '
        desc  = desc+tscolor('\c00????00')+'Adaptation: '+tscolor('\c00??????')+'RGYSOFT'+'\\n'+tscolor('\c00????00')+' Last Update: '+tscolor('\c00??????')+up_+'\\n '
        desc  = desc+tscolor('\c00????00')+'Origine: '+tscolor('\c00??????')+'matrix (KODI Addon)'+'\\n '
        desc  = desc+tscolor('\c00????00')+'Source: '+tscolor('\c00??????')+'https://github.com/zombiB/zombi-addons'+'\\n '
        elm_ = {'category': 'host2', 'params': {}, 'import_': imp0+hst_+' import ', 'title': titre,'desc':desc, 'import': imp1, 'mode': '10', 'icon':image, 'type': 'category', 'sSiteName':hst_}
        Hosts_.append((id_,elm_))
    return Hosts_
    

def replaceColors(titre):
    color_replace = [('%5BCOLOR+coral%5D','\c00??7950'),('%5B%2FCOLOR%5D','\c00??????'),('%5BCOLOR+COLOR+gold%5D','\c00??9900'),
                     ('%5BCOLOR+COLOR+violet%5D','\c00??0099'), ('%5BCOLOR+COLOR+orange%5D','\c00??6600'),('%5BCOLOR+COLOR+dodgerblue%5D','\c00??90??')]

    color_replace = [('[COLOR violet]','\c00??90??'),('[COLOR dodgerblue]','\c007070??'),('[COLOR lightcoral]','\c00?08080'),('[/COLOR]','\c00??????'),
                     ('[COLOR gold]','\c00????00'),('[COLOR orange]','\c00???020'),('[COLOR red]','\c00??5555'),('[COLOR skyblue]','\c0000????'),
                     ('[COLOR teal]','\c00009999'),('[COLOR coral]','\c00??7950'),('[COLOR khaki]','\c00997050'),('[COLOR 0]','\c00??????'),
                     ('[COLOR crimson]','\c00??5555'),('[COLOR grey]','\c00999999'),('[COLOR olive]','\c00808000'),('[COLOR fuchsia]','\c00??40??')]



    for cl0,cl1 in color_replace:
        titre = titre.replace(cl0,tscolor(cl1))
        titre = titre.replace(cl0,tscolor(cl1))        
    return titre

def convert_desc(SITE_DESC):
    desc  = tscolor('\c00????00')+' Info: '+tscolor('\c00??????')+SITE_DESC+'\\n '
    desc  = desc+tscolor('\c00????00')+'Adaptation: '+tscolor('\c00??????')+'RGYSOFT'+'\\n'
    desc  = desc+tscolor('\c00????00')+'Origine: '+tscolor('\c00??????')+'matrix (KODI Addon)'+'\\n '
    desc  = desc+tscolor('\c00????00')+'Source: '+tscolor('\c00??????')+'https://github.com/zombiB/zombi-addons'+'\\n '
    return desc

def get_desc(inf):
        desc0=''
        elm = inf[0]['other_info']
        if elm.get('tmdb_rating','')    != '': desc0 = desc0+tscolor('\c00????00')+'TMDB: '+tscolor('\c00??????')+elm['tmdb_rating']+' | '
        if elm.get('year','')           != '': desc0 = desc0+tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+elm['year']+' | '	
        if elm.get('duration','')       != '': desc0 = desc0+tscolor('\c00????00')+'Duration: '+tscolor('\c00??????')+elm['duration']+' | '	
        if elm.get('genres','')         != '': desc0 = desc0+'\n'+tscolor('\c00????00')+'Genre: '+tscolor('\c00??????')+elm['genres']
        if inf[0].get('text','')        != '':
            if desc0.strip()!='': desc0 = desc0+'\n'+inf[0]['text']
            else: desc0 = inf[0]['text']
        desc0 = desc0.strip()
        return desc0

def _pluginSearch(plugin, sSearchText):
    try:  
        plugins = __import__('Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.sites.%s' % plugin['identifier'], fromlist=[plugin['identifier']])
        function = getattr(plugins, plugin['search'][1])
        sUrl = plugin['search'][0] + str(sSearchText)
        function(sUrl)    
        printDBG('Load Search: ' + str(plugin['identifier']))
    except:
        VSlog(plugin['identifier'] + ': search failed')

   
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'tsiplayer.cookie'})
        self.USER_AGENT    = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        self.MAIN_URL      = '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/matrix'
        self.MAIN_URL0     = MAIN_URL0
        self.fncs_search   = fncs_search
        self.MAIN_IMP      = 'from '+self.MAIN_URL0.replace('/usr/lib/enigma2/python/','').replace('/','.')
        self.HTTP_HEADER   = {'User-Agent': self.USER_AGENT}
        self.defaultParams = {'header':self.HTTP_HEADER}
        self.getPage       = self.cm.getPage
        self.MyPath        = GetCacheSubDir('Tsiplayer')
        printDBG('------------ MyPath= '+self.MyPath)
        self.path_listing  = self.MyPath + 'matrix_listing'
        self.DB_path       = self.MyPath + 'matrix_DB'
        if config.plugins.iptvplayer.tsi_resolver.value=='tsiplayer':
            self.ts_up = ts_urlparser()
        else:
            self.ts_up = urlparser()
        
        if not os.path.exists(self.MyPath + 'tmdb'):
            os.makedirs(self.MyPath + 'tmdb')
        files = glob.glob(self.MyPath + 'tmdb/*')
        for f in files:
            os.remove(f)   
 
    def showmenu(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'Sites','icon':cItem['icon'],'mode':'01'})
        printDBG(str({'import':cItem['import'],'category' : 'host2','title':'Main','icon':cItem['icon'],'mode':'03'}))
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'Main','icon':cItem['icon'],'mode':'03'})

    def showmenuHome(self,cItem):
        sys.argv = ''
        oHome = cHome()
        oHome.load()
        self.get_listing()
        self.pro_listing(cItem)	        
        
    def showmenu0(self,cItem):
        folder = self.MAIN_URL0 #self.MAIN_URL+'/resources2/sites'
        lst    = os.listdir(folder)
        lst.sort()
        params={}
        for (dir_) in lst:
            if (dir_.endswith('.py')) and ('init' not in dir_) and ('globalSources' not in dir_)and ('globalSearch' not in dir_):
                file_   = dir_.replace('.py','')   
                elm = ['plugin://plugin.video.matrix/', '13', 'site='+file_+'&siteUrl=&sTitleWatched=']
                sys.argv = elm                
                image   = 'file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/resources2/art/sites/'+file_+'.png'
                import_ = self.MAIN_IMP+'.' + file_+' import '
                printDBG('import_+SITE_DESC='+import_+'SITE_DESC')
                exec (import_+'SITE_DESC',globals())
                desc = convert_desc(SITE_DESC) 
                elm={'import':cItem['import'],'category' : 'host2','argv':elm,'sSiteName':file_,'params':params,'import_':import_,'title':file_.replace('_','.').title(),'desc':desc,'icon':image,'mode':'10'}
                self.addDir(elm)	
                
    def showmenu1(self,cItem):
        sFunction   = cItem.get('sFunction','load')
        sSiteName   = cItem.get('sSiteName','')
        siteurl     = cItem.get('sSiteUrl','')
        sys.argv    = cItem.get('argv',['plugin://plugin.video.matrix/', '13', '?'])   
        import_     = self.MAIN_IMP+'.' + sSiteName+' import '
        if sFunction.lower() in self.fncs_search:
            printDBG('Afficher keybord')
            if sSiteName != 'globalSearch':
                self.write_search()


        if (sSiteName=='globalSearch'):
            sFunction = 'showSearch'
            f = open(self.path_listing+'.search', "w")
            f.write('OK')
            f.close()
            
        if (sSiteName=='cHome'):
            oHome = cHome()
            exec ('oHome.'+sFunction+'()')
            
        else:
            printDBG('site='+import_+sFunction)
            printDBG('sys.argv='+str(sys.argv))
            printDBG('siteurl='+str(siteurl))
            exec (import_+sFunction)
            exec (sFunction+'()')           
        
        if os.path.exists(self.path_listing+'.search'):	
            os.remove(self.path_listing+'.search')
            
        self.get_listing()        						 
        self.pro_listing(cItem)
        
    def pro_listing(self,cItem):
        image     = cItem['icon']
        EPG_      = cItem.get('EPG',False)
        import_   = cItem.get('import_','')
        nb_list = len(self.datas)
        if EPG_:
            desc_tmdb = get_desc(self.getArticle(cItem))
        else:
            desc_tmdb = ''
        for elm in self.datas:
            sTitle             = elm['sTitle']
            sDescription       = elm['sDescription']
            sSiteName          = elm['sSiteName'] 
            sHosterIdentifier  = elm['sHosterIdentifier']
            sFunction          = elm['sFunction'] 
            sSiteUrl           = elm['sSiteUrl']
            sMediaUrl          = elm['sMediaUrl']            
            sMeta              = elm['sMeta']
            argv               = elm['argv']
            #sIcon              = elm['sIcon']
            sThumbnail         = elm['sThumbnail']           
            sFileName          = elm['sFileName']  
            Year               = elm['Year']
            
            sMeta = str(sMeta).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'collection').replace('4', 'anime').replace('7', 'person').replace('8', 'network')
            if sMeta in ['tvshow','movie','collection','anime','person','network']:
                EPG = True
            else:
                EPG = False 
            if sFunction.lower() in self.fncs_search:
                EPG = False 
            sThumbnail   = sThumbnail.replace('special://home/addons/plugin.video.matrix/resources2/','file:///usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer/addons/resources2/')
            image        = sThumbnail

            printDBG(sTitle)
            
            printDBG(sTitle)
            sTitle       = replaceColors(str(sTitle))
            
            if desc_tmdb!= '': 
                sDescription = desc_tmdb
            else:
                sDescription = replaceColors(str(sDescription)).strip()
                sDescription = sDescription.replace('[I]','').replace('[/I]','')
                if str(Year).strip()!='':
                    if sDescription=='':
                        sDescription = tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+str(Year)
                    else:
                        sDescription = sDescription + '\n' + tscolor('\c00????00')+'Year: '+tscolor('\c00??????')+str(Year)
            printDBG(sTitle)
            if ('Outils' != sTitle.strip()) and ('Mes comptes' != sTitle.strip()) and ('Marque-pages' != sTitle.strip()):
                if sFunction=='DoNothing':
                    if (nb_list==1) and (sTitle.strip()==''):
                        sTitle = tscolor('\c00??8888')+ 'No informations'
                    self.addMarker({'title':sTitle,'desc':'','icon':image} )	
                elif (sFunction=='play') or ((sSiteName=='radio') and (sFunction=='')): 
                    if (sMediaUrl!=''):
                        url = sMediaUrl
                    else:
                        url = sSiteUrl

                    if (sHosterIdentifier =='lien_direct'):
                        host = 'direct'
                    else:
                        host = 'none' 
                    host = 'tshost'
                    #if (sSiteName=='radio'):
                    #    url = sMediaUrl
                        #host = 'direct'
                    color = ''
                    host_ = urlparser.getDomain(url).replace('www.','')
                    if sHosterIdentifier=='lien_direct':
                        color = tscolor('\c0060??60')  
                    elif ts_urlparser().checkHostSupportbyname(host_):
                        color = tscolor('\c0090??20')
                    elif ts_urlparser().checkHostNotSupportbyname(host_):
                        color = tscolor('\c00??3030')
                    elif ts_urlparser().checkHostSupportbyname_e2iplayer(host_):
                        color = tscolor('\c00????60')
                            
                    sTitle = '| '+sTitle +' | '+color+urlparser.getDomain(url).replace('www.','').title()
                    sDescription  = tscolor('\c00????00')+'Host: '+tscolor('\c00??????')+sHosterIdentifier.title()+'\n'+sDescription
                    self.addVideo({'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': url,'sHosterIdentifier':sHosterIdentifier,'title':sTitle,'desc':sDescription,'icon':image,'hst':host,'gnr':1} )									 
                    printDBG(str({'import':cItem['import'],'good_for_fav':True,'category' : 'video','url': url,'sHosterIdentifier':sHosterIdentifier,'title':sTitle,'desc':sDescription,'icon':image,'hst':host,'gnr':1} )	)								 
                
                elif sTitle!='None':
                    dir = {'good_for_fav':True,'EPG':EPG,'sMeta':sMeta,'import':cItem['import'],'sFileName':sFileName,'Year':Year,'category' : 'host2','title':sTitle,'sFunction':sFunction,'sSiteUrl':sSiteUrl,'desc':sDescription,'sSiteName':sSiteName,'argv':argv,'icon':image,'mode':'10','import_':import_,'hst':'tshost'}
                    printDBG(dir)
                    self.addDir(dir)			
       
    def get_listing(self):
        listing      = []
        datas_   = []
        mypath = self.MyPath + 'tmdb/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        printDBG('Files = '+str(onlyfiles))
        HST = []
        for file_ in onlyfiles:
            path_listing = mypath + file_
            with open(path_listing, 'rb') as handle:
                try:
                    while True:
                        listing.append(pickle.load(handle))
                except EOFError:
                    pass	
        printDBG('listing='+str(listing))
        for (oGuiElement, oOutputParameterHandler,time_now) in listing:
            elm                      = {}
            titre_ = oGuiElement.getTitle()
            try:
                titre_ = str(titre_, "utf-8")
            except:
                pass
            elm['sSiteName']         = oGuiElement.getSiteName()            
            elm['sFunction']         = oGuiElement.getFunction()
            elm['sTitle']            = titre_
            elm['sMeta']             = oGuiElement.getMeta()
            #elm['sIcon']             = oGuiElement.getIcon()
            elm['sThumbnail']        = oGuiElement.getThumbnail()
            elm['sDescription']      = oGuiElement.getDescription()
            elm['sSiteUrl']          = oGuiElement.getSiteUrl()            
            elm['sMediaUrl']         = oGuiElement.getMediaUrl() 
            elm['sFileName']         = oGuiElement.getFileName()
            elm['Year']              = oGuiElement.getYear()
            
            
            
            
            
            if oOutputParameterHandler!='':
                elm['sHosterIdentifier'] = oOutputParameterHandler.getValue('sHosterIdentifier')            
                if elm['sMediaUrl']=='':
                    elm['sMediaUrl']     = oOutputParameterHandler.getValue('sMediaUrl') 
                sParams                  = oOutputParameterHandler.getParameterAsUri()
            else:
                elm['sHosterIdentifier'] = 'lien_direct'
                sParams                  = ''
            elm['argv']              = self.create_argv(sParams)
            datas_.append((elm,time_now))
        printDBG('datas_='+str(datas_))
        datas_.sort(key=lambda x:x[1])
        printDBG('datas_='+str(datas_))
        self.datas = []
        for (a,b) in datas_:
           self.datas.append(a) 
        printDBG('self.datas='+str(self.datas))    
    def create_argv(self,sParams=''):      
        return ['plugin://plugin.video.matrix/', '13','?'+sParams]

    def get_links(self,cItem): 	
        urlTab = []
        gnr    = cItem.get('gnr',0)
        sHosterIdentifier = cItem['sHosterIdentifier']
        sMediaUrl         = cItem['url']
        printDBG('get_links URL='+str(sMediaUrl))
        printDBG('sys.argv='+str(sys.argv))
        if (sHosterIdentifier == 'lien_direct') or (sHosterIdentifier ==''): gnr=0
        if gnr ==0:
            URL,meta_ = get_url_meta(sMediaUrl)
            if 'm3u8' in URL:
                URL = strwithmeta(URL,meta_)	
                urlTab = getDirectM3U8Playlist(URL, False, checkContent=True, sortWithMaxBitrate=999999999)
            else:
                URL=strwithmeta(URL,meta_)
                urlTab.append({'name':'Direct', 'url':URL, 'need_resolve':0})
        elif gnr==1:
            try_tsiplayer = False
            try:
                from Plugins.Extensions.IPTVPlayer.tsiplayer.addons.resources2.lib.gui.hoster import cHosterGui
                cHoster = cHosterGui()
                oHoster = cHoster.getHoster(sHosterIdentifier)
                oHoster.setUrl(sMediaUrl)				
                aLink = oHoster.getMediaLink()
                printDBG('aLink='+str(aLink))
            except Exception as e:
                aLink = [False,'']
                printExc()
            if aLink:
                if (aLink[0] == True):
                    URL = aLink[1]
                    if'||'in URL: urls = URL.split('||')
                    else: urls = [URL]
                    for URL in urls:
                        if URL.strip()!='':
                            label=''
                            if '|tag:' in URL: URL,label = URL.split('|tag:',1)
                            URL,meta = get_url_meta(URL)
                            URL = strwithmeta(URL, meta)
                            printDBG('URL='+URL)
                            urlTab.append({'url':URL , 'name': sHosterIdentifier+' '+label})
                else:
                    try_tsiplayer = True
            else:
                try_tsiplayer = True
            if try_tsiplayer:
                printDBG('Try with TSIPLAYER Parser')
                if (ts_urlparser().checkHostSupport(str(sMediaUrl))==1) or (urlparser().checkHostSupport(str(sMediaUrl))==1):
                    url_ = str(sMediaUrl).replace('://www.youtube.com/embed/','://www.youtube.com/watch?v=')
                    printDBG('TSIPLAYER Parser Found :'+url_+ '('+str(sMediaUrl)+')')
                    urlTab.append({'name':'Tsiplayer', 'url':url_, 'need_resolve':1})  
        return urlTab	


    def getArticle(self,cItem):
        otherInfo = {}
        icon       = cItem.get('icon','')
        titre      = cItem.get('title','')
        desc       = cItem.get('desc','')        
        sFileName  = cItem.get('sFileName','')
        Year       = cItem.get('Year','')
        sMeta      = cItem.get('sMeta','')
        grab       = cTMDb()
        elm        = grab.get_meta(sMeta, sFileName, year=str(Year))
        printDBG('elm='+str(elm))
        duration = elm.get('duration',0)
        if (duration!='') and (duration!=0):
            try:
                duration = time.strftime('%-Hh %Mmn', time.gmtime(int(duration)))
            except:
                pass        
        if (duration != 0) and (duration != ''): 
            otherInfo['duration'] = str(duration)
        if elm.get('rating',0)          != 0 : otherInfo['tmdb_rating'] = str(elm['rating'])
        if elm.get('year',0)            != 0 : otherInfo['year']        = str(elm['year'])
        if elm.get('writer','')         != '': otherInfo['writers']     = str(elm['writer'])
        if elm.get('genre','')          != '': otherInfo['genres']      = str(elm['genre'])
        if elm.get('studio','')         != '': otherInfo['station']     = str(elm['studio'])
        if elm.get('director','')       != '': otherInfo['directors']   = str(elm['director'])
        if elm.get('plot','')           != '':
            desc = tscolor('\c00????00')+'Plot: '+tscolor('\c0000????')+str(elm['plot'])
        if elm.get('cover_url','')      != '':
            cover_url = str(elm['cover_url']).replace('/0/','/w400/')
            if cover_url !='https://image.tmdb.org/t/p/0None':
                icon = cover_url             
        return [{'title':titre, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo}]        


    def start(self,cItem):      
        if os.path.exists(self.path_listing+'.search'):	
            os.remove(self.path_listing+'.search')
            GetIPTVSleep().Sleep(5)
        files = glob.glob(self.MyPath + 'tmdb/*')
        for f in files:
            os.remove(f)
        self.currList = []
        mode=cItem.get('mode', None)
        printDBG('Start:'+str(cItem))
        if mode=='00':
            self.showmenu(cItem)
            #self.showmenuHome(cItem)
        if mode=='01':
            self.showmenu0(cItem)	
        if mode=='02':
            self.searchGlobal(cItem)
        if mode=='03':
            self.showmenuHome(cItem)	            
        if mode=='10':
            self.showmenu1(cItem)
        

    def write_search(self,txt='',txt_def=''):
        if txt_def == '':
            if os.path.isfile(self.MyPath +'searchSTR'):
                with open(self.MyPath + 'searchSTR','r') as f:
                    txt_def = f.read().strip() 
        if txt == '':
            ret = self.sessionEx.waitForFinishOpen(GetVirtualKeyboard(), title=_('Set file name'), text=txt_def)
            input_txt = ret[0]
        else: input_txt = txt 
        try:
            basestring
        except NameError:
            basestring = str
        if isinstance(input_txt, basestring):
            file = open(self.MyPath + 'searchSTR', 'w')
            file.write(input_txt)
            file.close() 
 
