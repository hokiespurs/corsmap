import ftplib
import re
from time import gmtime, strftime

MAXDEPTH = 10
DODEBUG = 2

def getftpfiles(ftp, fulldname = '', dname_changeto = '', depth=0):
    """
    returns a list of all of the filenames
    """
    if depth<=DODEBUG:
        print('[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '] ' + '(' + str(depth) + ') ' + fulldname)
    # Change ftp directory to the dname_change to variable
    # set a flag so it changes back at the end
    changedirbackup = False
    if dname_changeto != '':
        changedirbackup = True
        ftp.cwd(dname_changeto)
    
    # Dont dig deeper than MAXDEPTH
    if depth > MAXDEPTH:
        return []

    # return a list of folders and filenames
    ls = []
    ftp.retrlines('LIST', ls.append)

    # parse the list
    """
    folder: 'drwxrwxr-x    3 ftp      ftp         81125 May 01 21:48 Plots'
    file:   '-rw-r--r--    1 ftp      ftp         17539 Jun 18  2015 README.txt'
    """
    
    pattern = r'(^.).* ([A-Z|a-z].. .. .....) (.*)'
    fnames = []
    for line in ls:
        found = re.match(pattern, line)
        if (found is not None): # string was able to be parsed
            if (found.groups()[0]=='d'): #Directory
                dname_inst = found.groups()[2]
                if fulldname =='':
                    fnames_inst = getftpfiles(ftp,dname_inst, dname_inst, depth+1)
                else:
                    fnames_inst = getftpfiles(ftp,fulldname + '/' + dname_inst, dname_inst, depth+1)
                if (fnames_inst != []): # didnt return 0 files
                    for eachname in fnames_inst:
                        fnames.append(eachname)
            elif (found.groups()[0]=='-'): # File
                fname_inst = found.groups()[2]
                if fulldname!='':
                    full_path = fulldname + '/' + fname_inst
                else:
                    full_path = fname_inst
                fnames.append(full_path)
                if DODEBUG==0:
                    print(full_path)

    if changedirbackup:
        ftp.cwd('..')

    return fnames
        

site = 'geodesy.noaa.gov'
user = ''
pwd  = ''
startdir = 'cors/rinex/2018/001'

ftp = ftplib.FTP(site)
ftp.connect()
ftp.login(user,pwd)
ftp.set_pasv(True)

for eachdir in startdir.split('/'):
    ftp.cwd(eachdir)
    
fnames = getftpfiles(ftp)

for i in fnames:
    print(i)
