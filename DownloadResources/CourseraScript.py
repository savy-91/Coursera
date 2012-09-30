#!/usr/bin/env python

#This code was written on python 2.6.5, by S.K.Manoj
#Used mechanize module (Stateful programmatic web browsing in Python), and this was very helpful
#Did not implement multi threading, so videos download one after other.

import re,cookielib,sys,os,getpass
try:
    import mechanize
except ImportError as e:
    print "You must install mechanize package"
    sys.exit(1)
    

def init(uname,pwd,course):
    #set what all we want mechanize to handle, like url redirecting etc.
    print 'Initialize browsering session...'
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)#useful in downloading videos here at coursera
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 0)    
    auth_url = 'https://class.coursera.org/****/auth/auth_redirector?type=login&subtype=normal&email'.replace('****', course)
    br.open(auth_url)
    
    br.select_form(nr = 0) #as it is first form
    br.form['email'] =  uname
    br.form['password'] = pwd
    br.submit()
    print 'Verifying UserName and Password...\n'

    if 'https://class.coursera.org/****/auth/login_receiver?data='.replace('****', course) not in br.geturl():
        print 'Incorrect username or password'
        sys.exit(1)

    VideoLectures = 'https://class.coursera.org/****/lecture/index'.replace('****', course)
    br.open(VideoLectures)
    return br    

def createDir(course):
    while True:
        print 'Enter path to store videos: ',
        DirPath=raw_input()
        DirPath=DirPath+'/'+course
        if not os.path.exists(DirPath):
            try:
                os.mkdir(DirPath)
            except Exception, e:
                print e
                sys.exit(1)
            return os.path.abspath(DirPath)
        else:
            print 'Entered Path already exists, enter Correct Path'
            continue

def resolve_name_with_illegal_char(name):
    return re.sub(r'[\\/:*?"<>|]', ' -', name)

def getVideoLinks(br,path,course):
    link=[]
    title=[]
    for tmp in br.links():
        m_title = re.search(r'text=[\'\"](.+)[\'\"], tag=\'a\', .+\'class\', \'lecture-link\'', str(tmp))
        m_video = re.search(r'https:[\S]+download.mp4[\S]+\'', str(tmp))
        if m_title:
            title.append(resolve_name_with_illegal_char(m_title.group(1).strip()))
        if m_video:
            link.append(m_video.group().rstrip("'"))
    if len(title) == len(link):
        video = zip([t+'.mp4' for t in title], link)
    else:
        print 'Unable to match title to video links.'
        video = []
    return video    

def download(br,video,path):
    for r in video:
        filename = os.path.join(path, r[0])
        print 'Downloading', r[0]
        br.retrieve(r[1], filename)

def main():
    print 'UserName: ',
    uname=raw_input()
    pwd=getpass.getpass('Password: ')
    print 'CourseID: ',
    course=raw_input()
    br=init(uname,pwd,course)#initialize browser
    path=createDir(course)
    vid=getVideoLinks(br,path,course);
    download(br,vid,path)
    
if __name__=='__main__':
    main()        
