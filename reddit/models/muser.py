from __future__ import unicode_literals
from django.db import models
from .mbase import mbase

# *****************************************************************************
class muser(mbase, models.Model):
    name            = models.CharField(max_length=30)
    poi             = models.BooleanField(default=False)
    cHistoryGot     = models.BooleanField(default=False)
    def __str__(self):
        s = self.name
        if self.poi: s += " (poi)"
        if self.cHistoryGot: s += " (cHistoryGot = True)"
        else:                s += " (cHistoryGot = False)"
        return format(s)


# # ----------------------------------------------------------------------------
# # REDDITOR attributes
# # Ex
# # rUser = reddit.redditor('stp2007')
# # logger.info(rUser.name) # to make it non-lazy
# # pprint.pprint(vars(rUser))
# {
#   '_fetched':           False,
#   '_info_params':       {},
#   '_listing_use_sort':  True,
#   '_path':              'user/stp2007/',
#   '_reddit':            <praw.reddit.Reddit object at 0x7f45d99f9128>,
#   'name':               'stp2007'
#  }







