from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from ..config import clog
from ..models import msubreddit, mcomment, muser
import pprint

# # *****************************************************************************
def poiUsersOfSubreddit(request, subreddit, minNumComments):
    mi = clog.dumpMethodInfo()
    # clog.logger.info(mi)

    vs = "vbase.vanalysis.poiUsersOfSubreddit: "

    prawReddit = msubreddit.getPrawRedditInstance()
    prawSubreddit = prawReddit.subreddit(subreddit)

    subredditDict = {}

    # Get a list of users who've posted in this subreddit
    # and sort this by number of comments
    qs = mcomment.objects.filter(subreddit=prawSubreddit.name).values('username').annotate(num_count=Count('username')).order_by('-num_count')
    for i_mcommentAnnotatedUserCount in qs:
        # {'num_count': 785, 'username': 'RobRoyWithTwist'}
        if i_mcommentAnnotatedUserCount['num_count'] >= int(minNumComments):
            # print(i_mcommentAnnotatedUserCount)

            # Add this user as poi
            prawRedditor = prawReddit.redditor(i_mcommentAnnotatedUserCount['username'])
            i_muser = muser.objects.addOrUpdate(prawRedditor)
            i_muser.ppoi = True
            i_muser.save()
            if i_muser.addOrUpdateTempField == "new":
                vs += "<br>" + i_mcommentAnnotatedUserCount['username']

            # # Get subreddits this person also comments in
            qs2 = mcomment.objects.filter(username=i_mcommentAnnotatedUserCount['username']).values('rsubreddit_name_prefixed').annotate(num_count2=Count('rsubreddit_name_prefixed')).order_by('-num_count2')
            for i_mcommentAnnotatedSubredditCount in qs2:
                if i_mcommentAnnotatedSubredditCount['rsubreddit_name_prefixed'] not in subredditDict:
                    subredditDict[i_mcommentAnnotatedSubredditCount['rsubreddit_name_prefixed']] = 0
                subredditDict[i_mcommentAnnotatedSubredditCount['rsubreddit_name_prefixed']] += i_mcommentAnnotatedSubredditCount['num_count2']

    topCount = 10
    vs += "<br>Top " + str(topCount) + " subreddits these poi also post to are:"
    from operator import itemgetter
    sortedList = sorted(subredditDict.items(), key=itemgetter(1), reverse=True)
    for v in sortedList:
        # print(v)
        # # ('r/The_Donald', 34890)
        # # ('r/politics', 224)
        # # ('r/AskThe_Donald', 205)
        # # ('r/Le_Pen', 188)
        # # ('r/conspiracy', 140)
        # # ('r/tucker_carlson', 115)
        if topCount >= 1:
            vs += "<br>" + v[0]
        topCount -= 1

    sessionKey = 'blue'
    request.session[sessionKey] = vs
    return redirect('vbase.main', xData=sessionKey)










