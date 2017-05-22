from django.http import HttpResponse
from django.shortcuts import redirect
from ..config import clog
from ..models import mcomment, msubreddit, mthread, muser
import pprint

# *****************************************************************************
def displayDatabaseModelCounts():
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    users_poi               = muser.objects.filter(ppoi=True).count()
    users_notPoi            = muser.objects.filter(ppoi=False).count()
    users_ci                = mcomment.objects.filter(pdeleted=False).count()
    users_ci_deleted        = mcomment.objects.filter(pdeleted=True).count()
    subreddits              = msubreddit.objects.all().count()
    subreddits_si           = mthread.objects.filter(pdeleted=False).count()
    subreddits_si_deleted   = mthread.objects.filter(pdeleted=True).count()
    s = ''
    s += '<BR>==========================='
    s += '<BR>musers: ppoi = ' + str(users_poi)
    s += ', !ppoi = ' + str(users_notPoi)
    s += '<BR>mcomments = ' + str(users_ci)
    s += ', deleted = ' + str(users_ci_deleted)
    s += '<BR>msubreddits = ' + str(subreddits)
    s += '<BR>mthreads = ' + str(subreddits_si)
    s += ', deleted = ' + str(subreddits_si_deleted)
    s += '<BR>==========================='
    s += '<BR>'

    # clog.logger.critical("critical")
    # clog.logger.error("error")
    # clog.logger.warning("warning")
    # clog.logger.info("info")
    # clog.logger.debug("debug")
    # clog.logger.trace("trace")

    return s

# *****************************************************************************
def main(request, xData=None):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs  = ''
    moreData = request.session.get(xData, '')
    vs += moreData

    vs += '<br><a href="http://localhost:8000/reddit/vbase/test">vbase.test</a>'
    vs += '<br><b>vuser</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vuser/list">list</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vuser/delAll">delAll</a>'
    vs += '<br><b>vuser add</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vuser/add/OldDevLearningLinux">OldDevLearningLinux</a>'
    vs += ', <a href="http://localhost:8000/reddit/vuser/add/RoadsideBandit">RoadsideBandit</a>'

    vs += '<br><b>vsubreddit</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vsubreddit/list">list</a>'
    # vs += ', <a href="http://localhost:8000/reddit/vsubreddit/delAll">delAll</a>'
    vs += ' <b>add</b>: '
    vs += '  <a href="http://localhost:8000/reddit/vsubreddit/add/Molw">Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vsubreddit/add/politics">Politics</a>'

    vs += '<br><b>vthread</b>:'
    # vs += '  <a href="http://localhost:8000/reddit/vthread/delAll">delAll</a>'
    vs += '  <b>list</b>:'
    vs += '  <a href="http://localhost:8000/reddit/vthread/list/Molw">list Molw</a>'
    vs += ', <a href="http://localhost:8000/reddit/vthread/list/politics">list Politics</a>'

    vs += '<br><b>Tasks</b>:'
    vs += '<br><a href="http://localhost:8000/reddit/vsubreddit/update">Subreddit: update threads</a>'
    vs += '<br><a href="http://localhost:8000/reddit/vthread/update">Thread: update comments</a>'
    vs += '<br><a href="http://localhost:8000/reddit/comment/updateUsers">Comments: update users</a>'
    vs += '<br><br><a href="http://localhost:8000/reddit/vuser/update">User: update comments</a>'

    vs += '<br>' + displayDatabaseModelCounts()


    return HttpResponse(vs)

# *****************************************************************************
from ..tasks import task_testLogLevels
def test(request):
    mi = clog.dumpMethodInfo()
    clog.logger.info(mi)

    vs = "vbase.test: "

    task_testLogLevels.delay()

    clog.logger.info(vs)
    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)

# # *****************************************************************************
# def test(request):
#     mi = clog.dumpMethodInfo()
#     clog.logger.info(mi)
#
#     vs = "vbase.test: update mcomment username field from user field"
#     qs = mcomment.objects.all()
#     if qs.count() == 0:
#         vs += "No comments found."
#     else:
#         for item in qs:
#             item.username = item.user.name;
#             item.save()
#         vs += str(qs.count()) + "comments updated"
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)

# # *****************************************************************************
# from django.db.models import Count
# def test(request):
#     mi = clog.dumpMethodInfo()
#     # clog.logger.info(mi)
#
#     vs = "vbase.test: nothing here at the moment"
#
#     subPoi = 't5_38unr'        # TD
#     # qs = mcomment.objects.filter(subreddit=subPoi)
#     # clog.logger.info("qs.count() = %d" % (qs.count()))
#
#     prawReddit = mcomment.getPrawRedditInstance()
#
#     subredditDict = {}
#
#     # Get a list of users who've posted in TD and sort this by number of comments
#     qs = mcomment.objects.filter(subreddit=subPoi).values('username').annotate(num_count=Count('username')).order_by('-num_count')
#     for ii in qs:
#         if ii['num_count'] > 50:
#             # print(ii)
#             # {'num_count': 785, 'username': 'deleted'}
#             # {'num_count': 110, 'username': 'TheWhiteEnglishLion'}
#             # {'num_count': 104, 'username': 'littleirishmaid'}
#             # {'num_count': 102, 'username': 'journey345'}
#             # {'num_count': 91, 'username': 'ActivatedJoeBot'}
#
#             # prawRedditor = prawReddit.redditor(ii['username'])
#             # i_muser = muser.objects.addOrUpdate(prawRedditor)
#             # i_muser.ppoi = True
#             # i_muser.save()
#
#
#             # # Get subreddits this person also comments in
#             qs2 = mcomment.objects.filter(username=ii['username']).values('rsubreddit_name_prefixed').annotate(num_count2=Count('rsubreddit_name_prefixed')).order_by('-num_count2')
#             for jj in qs2:
#                 if jj['rsubreddit_name_prefixed'] not in subredditDict:
#                     subredditDict[jj['rsubreddit_name_prefixed']] = 0
#                 subredditDict[jj['rsubreddit_name_prefixed']] += jj['num_count2']
#
#
#     for k in subredditDict:
#         clog.logger.info("%06d: %s" % (subredditDict[k], k))
#
#         # 20:11:23 I vbase.py           (line  157): 000001: r/2meirl4meirl
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Anarcho_Capitalism
#         # 20:11:23 I vbase.py           (line  157): 000001: r/AndyMilonakisLive
#         # 20:11:23 I vbase.py           (line  157): 000001: r/antifa
#         # 20:11:23 I vbase.py           (line  157): 000001: r/AnythingGoesNews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/badphilosophy
#         # 20:11:23 I vbase.py           (line  157): 000001: r/BeAmazed
#         # 20:11:23 I vbase.py           (line  157): 000001: r/BlackPeopleTwitter
#         # 20:11:23 I vbase.py           (line  157): 000001: r/blunderyears
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Boxing
#         # 20:11:23 I vbase.py           (line  157): 000001: r/brighton
#         # 20:11:23 I vbase.py           (line  157): 000001: r/ButHillary
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Canning
#         # 20:11:23 I vbase.py           (line  157): 000001: r/celebnsfw
#         # 20:11:23 I vbase.py           (line  157): 000001: r/consoles
#         # 20:11:23 I vbase.py           (line  157): 000001: r/CrappyDesign
#         # 20:11:23 I vbase.py           (line  157): 000001: r/creepy
#         # 20:11:23 I vbase.py           (line  157): 000001: r/curvy
#         # 20:11:23 I vbase.py           (line  157): 000001: r/dankmemes
#         # 20:11:23 I vbase.py           (line  157): 000001: r/dating
#         # 20:11:23 I vbase.py           (line  157): 000001: r/dragonquest
#         # 20:11:23 I vbase.py           (line  157): 000001: r/europe
#         # 20:11:23 I vbase.py           (line  157): 000001: r/exmuslim
#         # 20:11:23 I vbase.py           (line  157): 000001: r/explainlikeimfive
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Fat_Donald
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Fitness
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Foodforthought
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Futurology
#         # 20:11:23 I vbase.py           (line  157): 000001: r/gamemusic
#         # 20:11:23 I vbase.py           (line  157): 000001: r/gamernews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Games
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Gaming4Gamers
#         # 20:11:23 I vbase.py           (line  157): 000001: r/germanshepherds
#         # 20:11:23 I vbase.py           (line  157): 000001: r/germany
#         # 20:11:23 I vbase.py           (line  157): 000001: r/HailCorporate
#         # 20:11:23 I vbase.py           (line  157): 000001: r/highereducation
#         # 20:11:23 I vbase.py           (line  157): 000001: r/holdmyjuicebox
#         # 20:11:23 I vbase.py           (line  157): 000001: r/IdiotsFightingThings
#         # 20:11:23 I vbase.py           (line  157): 000001: r/im14andthisisdeep
#         # 20:11:23 I vbase.py           (line  157): 000001: r/ImagesOfCalifornia
#         # 20:11:23 I vbase.py           (line  157): 000001: r/inthenews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/ipad
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Jokes
#         # 20:11:23 I vbase.py           (line  157): 000001: r/JonTron
#         # 20:11:23 I vbase.py           (line  157): 000001: r/JRPG
#         # 20:11:23 I vbase.py           (line  157): 000001: r/lacortenews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/LearnUselessTalents
#         # 20:11:23 I vbase.py           (line  157): 000001: r/lifehacks
#         # 20:11:23 I vbase.py           (line  157): 000001: r/madlads
#         # 20:11:23 I vbase.py           (line  157): 000001: r/malehairadvice
#         # 20:11:23 I vbase.py           (line  157): 000001: r/MaliciousCompliance
#         # 20:11:23 I vbase.py           (line  157): 000001: r/MapsWithoutNZ
#         # 20:11:23 I vbase.py           (line  157): 000001: r/miamidolphins
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Miyazaki
#         # 20:11:23 I vbase.py           (line  157): 000001: r/modnews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/NatureIsFuckingLit
#         # 20:11:23 I vbase.py           (line  157): 000001: r/NeverTrump
#         # 20:11:23 I vbase.py           (line  157): 000001: r/newsbotbot
#         # 20:11:23 I vbase.py           (line  157): 000001: r/nflstreams
#         # 20:11:23 I vbase.py           (line  157): 000001: r/NSFWFunny
#         # 20:11:23 I vbase.py           (line  157): 000001: r/pcgaming
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PedoGate
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PenmanshipPorn
#         # 20:11:23 I vbase.py           (line  157): 000001: r/personalfinance
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PERU
#         # 20:11:23 I vbase.py           (line  157): 000001: r/philosophy
#         # 20:11:23 I vbase.py           (line  157): 000001: r/photoshop
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PixelCanvas
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Planetside
#         # 20:11:23 I vbase.py           (line  157): 000001: r/pol
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Political_Revolution
#         # 20:11:23 I vbase.py           (line  157): 000001: r/President_Rock
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PS4Deals
#         # 20:11:23 I vbase.py           (line  157): 000001: r/PS4Pro
#         # 20:11:23 I vbase.py           (line  157): 000001: r/qotsa
#         # 20:11:23 I vbase.py           (line  157): 000001: r/quityourbullshit
#         # 20:11:23 I vbase.py           (line  157): 000001: r/relationships
#         # 20:11:23 I vbase.py           (line  157): 000001: r/shitpost
#         # 20:11:23 I vbase.py           (line  157): 000001: r/shittyaskscience
#         # 20:11:23 I vbase.py           (line  157): 000001: r/sophieturner
#         # 20:11:23 I vbase.py           (line  157): 000001: r/SpecialAccess
#         # 20:11:23 I vbase.py           (line  157): 000001: r/sports
#         # 20:11:23 I vbase.py           (line  157): 000001: r/SquareEnix
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Star_wars_Rogue_One
#         # 20:11:23 I vbase.py           (line  157): 000001: r/StartledCats
#         # 20:11:23 I vbase.py           (line  157): 000001: r/StoppedWorking
#         # 20:11:23 I vbase.py           (line  157): 000001: r/StreetFights
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Switch
#         # 20:11:23 I vbase.py           (line  157): 000001: r/textdoor
#         # 20:11:23 I vbase.py           (line  157): 000001: r/The_Donald_Discuss
#         # 20:11:23 I vbase.py           (line  157): 000001: r/The_Donald_TN
#         # 20:11:23 I vbase.py           (line  157): 000001: r/The_Farage
#         # 20:11:23 I vbase.py           (line  157): 000001: r/The_Ivanka
#         # 20:11:23 I vbase.py           (line  157): 000001: r/The_NewDonald
#         # 20:11:23 I vbase.py           (line  157): 000001: r/TheBlogFeed
#         # 20:11:23 I vbase.py           (line  157): 000001: r/TheGrittyPast
#         # 20:11:23 I vbase.py           (line  157): 000001: r/thelastofus
#         # 20:11:23 I vbase.py           (line  157): 000001: r/thenewcoldwar
#         # 20:11:23 I vbase.py           (line  157): 000001: r/therewasanattempt
#         # 20:11:23 I vbase.py           (line  157): 000001: r/thevoice
#         # 20:11:23 I vbase.py           (line  157): 000001: r/TheYonatan
#         # 20:11:23 I vbase.py           (line  157): 000001: r/ThisCrazyBitch
#         # 20:11:23 I vbase.py           (line  157): 000001: r/transgender
#         # 20:11:23 I vbase.py           (line  157): 000001: r/Trump_Legal
#         # 20:11:23 I vbase.py           (line  157): 000001: r/TrumpEra
#         # 20:11:23 I vbase.py           (line  157): 000001: r/TrumpForPrison
#         # 20:11:23 I vbase.py           (line  157): 000001: r/underpopular
#         # 20:11:23 I vbase.py           (line  157): 000001: r/UnresolvedMysteries
#         # 20:11:23 I vbase.py           (line  157): 000001: r/UpliftingNews
#         # 20:11:23 I vbase.py           (line  157): 000001: r/wacom
#         # 20:11:23 I vbase.py           (line  157): 000001: r/WhereIsAssange
#         # 20:11:23 I vbase.py           (line  157): 000002: r/amateur_boxing
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Amd
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Art
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Ask_TheDonald
#         # 20:11:23 I vbase.py           (line  157): 000002: r/bodybuilding
#         # 20:11:23 I vbase.py           (line  157): 000002: r/climate
#         # 20:11:23 I vbase.py           (line  157): 000002: r/ColoradoRights
#         # 20:11:23 I vbase.py           (line  157): 000002: r/consoledeals
#         # 20:11:23 I vbase.py           (line  157): 000002: r/dbz
#         # 20:11:23 I vbase.py           (line  157): 000002: r/EarthPorn
#         # 20:11:23 I vbase.py           (line  157): 000002: r/excel
#         # 20:11:23 I vbase.py           (line  157): 000002: r/finance
#         # 20:11:23 I vbase.py           (line  157): 000002: r/harrypotter
#         # 20:11:23 I vbase.py           (line  157): 000002: r/history
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Impeach_Trump
#         # 20:11:23 I vbase.py           (line  157): 000002: r/instant_regret
#         # 20:11:23 I vbase.py           (line  157): 000002: r/joker
#         # 20:11:23 I vbase.py           (line  157): 000002: r/knitting
#         # 20:11:23 I vbase.py           (line  157): 000002: r/KotakuInAction
#         # 20:11:23 I vbase.py           (line  157): 000002: r/nintendo
#         # 20:11:23 I vbase.py           (line  157): 000002: r/nostalgia
#         # 20:11:23 I vbase.py           (line  157): 000002: r/ofcoursethatsathing
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Prematurecelebration
#         # 20:11:23 I vbase.py           (line  157): 000002: r/residentevil
#         # 20:11:23 I vbase.py           (line  157): 000002: r/RocketLeagueExchange
#         # 20:11:23 I vbase.py           (line  157): 000002: r/shittyreactiongifs
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Sorosforprison
#         # 20:11:23 I vbase.py           (line  157): 000002: r/The_Donald_Texas
#         # 20:11:23 I vbase.py           (line  157): 000002: r/The_Guacbowl
#         # 20:11:23 I vbase.py           (line  157): 000002: r/TheDonaldUltra
#         # 20:11:23 I vbase.py           (line  157): 000002: r/TheRecordCorrected
#         # 20:11:23 I vbase.py           (line  157): 000002: r/TheRightBoycott
#         # 20:11:23 I vbase.py           (line  157): 000002: r/thick
#         # 20:11:23 I vbase.py           (line  157): 000002: r/Tinder
#         # 20:11:23 I vbase.py           (line  157): 000002: r/unexpectedjihad
#         # 20:11:23 I vbase.py           (line  157): 000002: r/wannacry
#         # 20:11:23 I vbase.py           (line  157): 000002: r/WayOfTheBern
#         # 20:11:23 I vbase.py           (line  157): 000002: r/wholesomegifs
#         # 20:11:23 I vbase.py           (line  157): 000002: r/wiiu
#         # 20:11:23 I vbase.py           (line  157): 000002: r/WorldOfTanksBlitz
#         # 20:11:23 I vbase.py           (line  157): 000002: r/YouShouldKnow
#         # 20:11:23 I vbase.py           (line  157): 000002: u/ShinyMegaCharizardX
#         # 20:11:23 I vbase.py           (line  157): 000003: r/AgainstHateSubreddits
#         # 20:11:23 I vbase.py           (line  157): 000003: r/aww
#         # 20:11:23 I vbase.py           (line  157): 000003: r/berkeley
#         # 20:11:23 I vbase.py           (line  157): 000003: r/eagles
#         # 20:11:23 I vbase.py           (line  157): 000003: r/EmpireDidNothingWrong
#         # 20:11:23 I vbase.py           (line  157): 000003: r/gamers
#         # 20:11:23 I vbase.py           (line  157): 000003: r/gamingsuggestions
#         # 20:11:23 I vbase.py           (line  157): 000003: r/gardening
#         # 20:11:23 I vbase.py           (line  157): 000003: r/GetMotivated
#         # 20:11:23 I vbase.py           (line  157): 000003: r/holdmybeer
#         # 20:11:23 I vbase.py           (line  157): 000003: r/ideasfortheadmins
#         # 20:11:23 I vbase.py           (line  157): 000003: r/ireland
#         # 20:11:23 I vbase.py           (line  157): 000003: r/Journalism
#         # 20:11:23 I vbase.py           (line  157): 000003: r/Kossacks_for_Sanders
#         # 20:11:23 I vbase.py           (line  157): 000003: r/MarchForScience
#         # 20:11:23 I vbase.py           (line  157): 000003: r/MemeEconomy
#         # 20:11:23 I vbase.py           (line  157): 000003: r/Music
#         # 20:11:23 I vbase.py           (line  157): 000003: r/MyTheoryIs
#         # 20:11:23 I vbase.py           (line  157): 000003: r/neoliberal
#         # 20:11:23 I vbase.py           (line  157): 000003: r/niceguys
#         # 20:11:23 I vbase.py           (line  157): 000003: r/Our_Politics
#         # 20:11:23 I vbase.py           (line  157): 000003: r/PoliticalVideo
#         # 20:11:23 I vbase.py           (line  157): 000003: r/redacted
#         # 20:11:23 I vbase.py           (line  157): 000003: r/RussiaLago
#         # 20:11:23 I vbase.py           (line  157): 000003: r/vita
#         # 20:11:23 I vbase.py           (line  157): 000003: r/xboxone
#         # 20:11:23 I vbase.py           (line  157): 000003: u/Here_Comes_The_King
#         # 20:11:23 I vbase.py           (line  157): 000004: r/AskTrumpSupporters
#         # 20:11:23 I vbase.py           (line  157): 000004: r/Chargers
#         # 20:11:23 I vbase.py           (line  157): 000004: r/circlejerk
#         # 20:11:23 I vbase.py           (line  157): 000004: r/DebateFascism
#         # 20:11:23 I vbase.py           (line  157): 000004: r/kekistan
#         # 20:11:23 I vbase.py           (line  157): 000004: r/POLITIC
#         # 20:11:23 I vbase.py           (line  157): 000004: r/PrettyGirls
#         # 20:11:23 I vbase.py           (line  157): 000004: r/PSVR
#         # 20:11:23 I vbase.py           (line  157): 000004: r/PussyPass
#         # 20:11:23 I vbase.py           (line  157): 000004: r/science
#         # 20:11:23 I vbase.py           (line  157): 000004: r/subredditcancer
#         # 20:11:23 I vbase.py           (line  157): 000004: r/The_Italia
#         # 20:11:23 I vbase.py           (line  157): 000004: r/TheNewsFeed
#         # 20:11:23 I vbase.py           (line  157): 000004: r/Unexpected
#         # 20:11:23 I vbase.py           (line  157): 000004: r/Vaping
#         # 20:11:23 I vbase.py           (line  157): 000004: r/windows
#         # 20:11:23 I vbase.py           (line  157): 000005: r/3DS
#         # 20:11:23 I vbase.py           (line  157): 000005: r/amiibo
#         # 20:11:23 I vbase.py           (line  157): 000005: r/Conservative
#         # 20:11:23 I vbase.py           (line  157): 000005: r/coolguides
#         # 20:11:23 I vbase.py           (line  157): 000005: r/hottiesfortrump
#         # 20:11:23 I vbase.py           (line  157): 000005: r/JoeRogan
#         # 20:11:23 I vbase.py           (line  157): 000005: r/me_irl
#         # 20:11:23 I vbase.py           (line  157): 000005: r/NoStupidQuestions
#         # 20:11:23 I vbase.py           (line  157): 000005: r/nottheonion
#         # 20:11:23 I vbase.py           (line  157): 000005: r/OutOfTheLoop
#         # 20:11:23 I vbase.py           (line  157): 000005: r/patientgamers
#         # 20:11:23 I vbase.py           (line  157): 000005: r/sadcringe
#         # 20:11:23 I vbase.py           (line  157): 000005: r/sjw_hate
#         # 20:11:23 I vbase.py           (line  157): 000005: r/socialism
#         # 20:11:23 I vbase.py           (line  157): 000005: r/TheBlackList
#         # 20:11:23 I vbase.py           (line  157): 000005: r/TrumpPA
#         # 20:11:23 I vbase.py           (line  157): 000005: r/Wellthatsucks
#         # 20:11:23 I vbase.py           (line  157): 000006: r/fireemblem
#         # 20:11:23 I vbase.py           (line  157): 000006: r/gadgets
#         # 20:11:23 I vbase.py           (line  157): 000006: r/IAmA
#         # 20:11:23 I vbase.py           (line  157): 000006: r/iamverybadass
#         # 20:11:23 I vbase.py           (line  157): 000006: r/investing
#         # 20:11:23 I vbase.py           (line  157): 000006: r/marchagainstrump
#         # 20:11:23 I vbase.py           (line  157): 000006: r/place
#         # 20:11:23 I vbase.py           (line  157): 000006: r/PoliticalHumor
#         # 20:11:23 I vbase.py           (line  157): 000006: r/promos
#         # 20:11:23 I vbase.py           (line  157): 000006: r/space
#         # 20:11:23 I vbase.py           (line  157): 000006: r/SubredditDrama
#         # 20:11:23 I vbase.py           (line  157): 000006: r/television
#         # 20:11:23 I vbase.py           (line  157): 000007: r/apple
#         # 20:11:23 I vbase.py           (line  157): 000007: r/GrandTheftAutoV_PC
#         # 20:11:23 I vbase.py           (line  157): 000007: r/ImGoingToHellForThis
#         # 20:11:23 I vbase.py           (line  157): 000007: r/OldSchoolCool
#         # 20:11:23 I vbase.py           (line  157): 000007: r/redditrequest
#         # 20:11:23 I vbase.py           (line  157): 000008: r/chronotrigger
#         # 20:11:23 I vbase.py           (line  157): 000008: r/CringeAnarchy
#         # 20:11:23 I vbase.py           (line  157): 000008: r/MadeMeSmile
#         # 20:11:23 I vbase.py           (line  157): 000008: r/mildlyinteresting
#         # 20:11:23 I vbase.py           (line  157): 000008: r/SquaredCircle
#         # 20:11:23 I vbase.py           (line  157): 000008: r/technology
#         # 20:11:23 I vbase.py           (line  157): 000008: r/User_Simulator
#         # 20:11:23 I vbase.py           (line  157): 000009: r/aclfestival
#         # 20:11:23 I vbase.py           (line  157): 000009: r/BannedFromThe_Donald
#         # 20:11:23 I vbase.py           (line  157): 000009: r/buildapc
#         # 20:11:23 I vbase.py           (line  157): 000009: r/Documentaries
#         # 20:11:23 I vbase.py           (line  157): 000009: r/movies
#         # 20:11:23 I vbase.py           (line  157): 000009: r/Physical_Removal
#         # 20:11:23 I vbase.py           (line  157): 000009: r/The_DonaldUnleashed
#         # 20:11:23 I vbase.py           (line  157): 000010: r/BravoRealHousewives
#         # 20:11:23 I vbase.py           (line  157): 000010: r/EmDrive
#         # 20:11:23 I vbase.py           (line  157): 000010: r/funny
#         # 20:11:23 I vbase.py           (line  157): 000010: r/HillaryMeltdown
#         # 20:11:23 I vbase.py           (line  157): 000010: r/mariokart
#         # 20:11:23 I vbase.py           (line  157): 000010: r/PrequelMemes
#         # 20:11:23 I vbase.py           (line  157): 000010: r/Sneakers
#         # 20:11:23 I vbase.py           (line  157): 000010: r/The_Europe
#         # 20:11:23 I vbase.py           (line  157): 000010: r/todayilearned
#         # 20:11:23 I vbase.py           (line  157): 000011: r/AntiTrumpAlliance
#         # 20:11:23 I vbase.py           (line  157): 000011: r/books
#         # 20:11:23 I vbase.py           (line  157): 000011: r/drunkenpeasants
#         # 20:11:23 I vbase.py           (line  157): 000011: r/esist
#         # 20:11:23 I vbase.py           (line  157): 000011: r/FinalFantasy
#         # 20:11:23 I vbase.py           (line  157): 000011: r/overclocking
#         # 20:11:23 I vbase.py           (line  157): 000011: r/Whatcouldgowrong
#         # 20:11:23 I vbase.py           (line  157): 000011: r/WikiLeaks
#         # 20:11:23 I vbase.py           (line  157): 000012: r/PeopleFuckingDying
#         # 20:11:23 I vbase.py           (line  157): 000013: r/Deusex
#         # 20:11:23 I vbase.py           (line  157): 000013: r/Fuckthealtright
#         # 20:11:23 I vbase.py           (line  157): 000013: r/Monitors
#         # 20:11:23 I vbase.py           (line  157): 000014: r/sjwhate
#         # 20:11:23 I vbase.py           (line  157): 000014: r/TheNewRight
#         # 20:11:23 I vbase.py           (line  157): 000014: r/uncensorednews
#         # 20:11:23 I vbase.py           (line  157): 000015: r/Donald_Trump
#         # 20:11:23 I vbase.py           (line  157): 000015: r/gifs
#         # 20:11:23 I vbase.py           (line  157): 000015: r/WTF
#         # 20:11:23 I vbase.py           (line  157): 000016: r/pussypassdenied
#         # 20:11:23 I vbase.py           (line  157): 000017: r/HillaryForPrison
#         # 20:11:23 I vbase.py           (line  157): 000017: r/The_Donald_CA
#         # 20:11:23 I vbase.py           (line  157): 000017: r/TwoXChromosomes
#         # 20:11:23 I vbase.py           (line  157): 000018: r/BlocParty
#         # 20:11:23 I vbase.py           (line  157): 000018: r/Showerthoughts
#         # 20:11:23 I vbase.py           (line  157): 000018: r/steroids
#         # 20:11:23 I vbase.py           (line  157): 000019: r/AdviceAnimals
#         # 20:11:23 I vbase.py           (line  157): 000020: r/PS4
#         # 20:11:23 I vbase.py           (line  157): 000021: r/linux
#         # 20:11:23 I vbase.py           (line  157): 000022: r/RocketLeague
#         # 20:11:23 I vbase.py           (line  157): 000023: r/netsec
#         # 20:11:23 I vbase.py           (line  157): 000023: r/PublicFreakout
#         # 20:11:23 I vbase.py           (line  157): 000024: r/EnoughTrumpSpam
#         # 20:11:23 I vbase.py           (line  157): 000024: r/techsupport
#         # 20:11:23 I vbase.py           (line  157): 000025: r/ukpolitics
#         # 20:11:23 I vbase.py           (line  157): 000026: r/nfl
#         # 20:11:23 I vbase.py           (line  157): 000032: r/gaming
#         # 20:11:23 I vbase.py           (line  157): 000034: r/Drama
#         # 20:11:23 I vbase.py           (line  157): 000035: r/Seth_Rich
#         # 20:11:23 I vbase.py           (line  157): 000036: r/TickTockManitowoc
#         # 20:11:23 I vbase.py           (line  157): 000038: r/OTMemes
#         # 20:11:23 I vbase.py           (line  157): 000040: r/StarWars
#         # 20:11:23 I vbase.py           (line  157): 000043: r/nvidia
#         # 20:11:23 I vbase.py           (line  157): 000043: r/survivor
#         # 20:11:23 I vbase.py           (line  157): 000045: r/MarchAgainstTrump
#         # 20:11:23 I vbase.py           (line  157): 000045: r/unitedkingdom
#         # 20:11:23 I vbase.py           (line  157): 000048: r/TruthLeaks
#         # 20:11:23 I vbase.py           (line  157): 000048: r/worldnews
#         # 20:11:23 I vbase.py           (line  157): 000054: r/AskReddit
#         # 20:11:23 I vbase.py           (line  157): 000054: r/pics
#         # 20:11:23 I vbase.py           (line  157): 000084: r/Catholicism
#         # 20:11:23 I vbase.py           (line  157): 000085: r/news
#         # 20:11:23 I vbase.py           (line  157): 000087: r/videos
#         # 20:11:23 I vbase.py           (line  157): 000107: r/tucker_carlson
#         # 20:11:23 I vbase.py           (line  157): 000113: r/conspiracy
#         # 20:11:23 I vbase.py           (line  157): 000133: r/AskThe_Donald
#         # 20:11:23 I vbase.py           (line  157): 000181: r/Le_Pen
#         # 20:11:23 I vbase.py           (line  157): 000211: r/politics
#         # 20:11:23 I vbase.py           (line  157): 028725: r/The_Donald
#
#
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)



# # *****************************************************************************
# from celery.task.control import inspect # for ispectTasks
# def test(request):
#     mi = clog.dumpMethodInfo()
#     # clog.logger.info(mi)
#
#     vs = "vbase.test: celery inspectTasks"
#
#     # Inspect all nodes.
#     i = inspect()
#     # print("all nodes: %s" % (vars(i)))
#
#     # Show the items that have an ETA or are scheduled for later processing
#     # print("scheduled: %s" % (vars(i.scheduled())))
#     print("scheduled: %s" % (pprint.pformat(i.scheduled())))
#
#     # Show tasks that are currently active.
#     # print("active: %s" % (vars(i.active())))
#     print("active: %s" % (pprint.pformat(i.active())))
#
#     # Show tasks that have been claimed by workers
#     # print("reserved: %s" % (vars(i.reserved())))
#     print("reserved: %s" % (pprint.pformat(i.reserved())))
#
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)


# # *****************************************************************************
# from celery.task.control import inspect # for ispectTasks
# def test(request):
#     mi = clog.dumpMethodInfo()
#     # clog.logger.info(mi)
#
#     # ------------------------------------
#     vs = "vbase.test: empty"
#
#
#     # ------------------------------------
#
#     clog.logger.info(vs)
#     sessionKey = 'blue'
#     request.session[sessionKey] = vs
#     return redirect('vbase.main', xData=sessionKey)















