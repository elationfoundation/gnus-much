#!/usb/bin/python

# See: Gnus, Dovecot, OfflineIMAP, search: a HOWTO
# URL: http://roland.entierement.nu/blog/2010/09/08/gnus-dovecot-offlineimap-search-a-howto.html


import locale
from subprocess import Popen, PIPE

encoding = locale.getdefaultlocale()[1]

def get_password(p):
    """executes gnome-keyring-query get passwd and returns the output"""
    (out, err) = Popen(["gnome-keyring-query", "get", p], stdout=PIPE).communicate()
    return out.decode(encoding).strip()

#=========================================================
#Adds a new flag that OfflineIMAP will propagate back and forth. By default, only the standard IMAP flags are propagated; we also want to synchronize the gnus-expire flag that Gnus uses to mark expirable articles. It's a hack, but it works for now (maybe someday OfflineIMAP will propagate all the flags it finds?).

# Propagate gnus-expire flag
from offlineimap import imaputil

def lld_flagsimap2maildir(flagstring):
    """Convert string into a flags set"""
    flagmap = {'\\seen': 'S',
               '\\answered': 'R',
               '\\flagged': 'F',
               '\\deleted': 'T',
               '\\draft': 'D',
               'gnus-expire': 'E'}
    retval = []
    imapflaglist = [x.lower() for x in flagstring[1:-1].split()]
    for imapflag in imapflaglist:
        if flagmap.has_key(imapflag):
            retval.append(flagmap[imapflag])
    retval.sort()
    return retval

def lld_flagsmaildir2imap(list):
    """Convert set of flags into a string"""
    flagmap = {'S': '\\Seen',
               'R': '\\Answered',
               'F': '\\Flagged',
               'T': '\\Deleted',
               'D': '\\Draft',
               'E': 'gnus-expire'}
    retval = []
    for mdflag in list:
        if flagmap.has_key(mdflag):
            retval.append(flagmap[mdflag])
    retval.sort()
    return '(' + ' '.join(retval) + ')'

imaputil.flagsmaildir2imap = lld_flagsmaildir2imap
imaputil.flagsimap2maildir = lld_flagsimap2maildir
