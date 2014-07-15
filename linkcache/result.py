#!/usr/bin/env python

from datetime import datetime
import re

F_SPOILERS = 0x4
F_NSFW = 0x2
F_MAYBE_NSFW = 0x1

class LinkCacheResult:
    def __init__(self, result={}):
        self.url = None
        self.nsfw = 0
        self.private = False
        self.id = None
        self.count = None
        self.timestamp = None
        self.title = None
        self.first_seen = None
        self.request_timestamp = None
        self.url_line = None
        self.user = None
        self.content_type = None
        self.description = None
        self.shorturl = None
        self.id = None

        if type(result) is str:
            self.user = result
            return

        for key, value in result.iteritems():
            setattr(self, key, value)

    def timeAgo(self):
        ago = ""
        delta = self.request_timestamp - self.timestamp

        years = int(delta.days / 365.24)
        days = int(delta.days % 365.24)
        weeks = days / 7
        days %= 7

        hours = delta.seconds / (60*60)
        seconds = delta.seconds % (60*60)
        minutes = seconds / 60
        seconds %= 60

        months = 0
        if weeks > 10:
            months = weeks / 4
            days += weeks * 7
            weeks = 0

        if years > 0:
            hours = minutes = seconds = 0
            ago = str(years) + "y"

        if months > 0:
            hours = minutes = seconds = 0
            if ago != "":
                ago += ", "
            ago += str(months) + "m"

        if days > 0:
            minutes = seconds = 0
            if ago != "":
                ago += ", "
            ago += str(days) + "d"

        if hours > 0:
            seconds = 0
            if ago != "":
                ago += ", "
            ago += str(hours) + "h"

        if minutes > 0:
            if ago != "":
                ago += ", "
            ago += str(minutes) + "m"

        if seconds > 0:
            if ago != "":
                ago += ", "
            ago += str(seconds) + "s"
        else:
            if ago == "":
                ago = "0s"
            ago += " ago"

        return ago

    def pretty_flags(self):
        flags = []
        if self.nsfw & F_NSFW:
            flags.append("NSFW")
        elif self.nsfw & F_MAYBE_NSFW:
            flags.append("~NSFW")

        if self.private:
            flags.append("P")

        if self.nsfw & F_SPOILERS:
            flags.append("SPOILERS")

        if flags:
            return ",".join(flags)
        else:
            return None

    def pretty_title(self):
        title = self.title
        if title:
            title += ""
        else:
            title = self.description

        flags = self.pretty_flags()
        if flags:
            title = "[" + flags + "] " + title

        return title

    def pretty_stats(self):
        alive = ""
        if not self.alive:
            alive = " DEAD"
        return "[%dx, %s, %s%s] " % (self.count, self.user, self.timeAgo(),
                                     alive)

    def __str__(self):
        line = self.pretty_title()
        if line:
            line = '(' + re.sub(r"\n+", "  ", line) + ')'
        else:
            line = ""

        if self.count > 1:
            line += " %s" % self.pretty_stats()

        return line

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
