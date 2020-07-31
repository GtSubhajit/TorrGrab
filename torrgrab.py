import urllib.request,urllib.parse
import os, sys, subprocess
import requests

banner = """
  ______                ______           __
 /_  __/___  __________/ ____/________ _/ /_
  / / / __ \/ ___/ ___/ / __/ ___/ __ `/ __ \\
 / / / /_/ / /  / /  / /_/ / /  / /_/ / /_/ /
/_/  \____/_/  /_/   \____/_/   \__,_/_.___/  V.1.0

"""
print(banner)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

request=requests.session()
name=[]
link=[]
data=[]
trackers=[
"udp://tracker.coppersurfer.tk:6969/announce",
"udp://9.rarbg.to:2920/announce",
"udp://tracker.opentrackr.org:1337",
"udp://tracker.internetwarriors.net:1337/announce",
"udp://tracker.leechers-paradise.org:6969/announce",
"udp://tracker.coppersurfer.tk:6969/announce",
"udp://tracker.pirateparty.gr:6969/announce",
"udp://tracker.cyberia.is:6969/announce"]
def scrapmagnet(hash,name):
    prefix="magnet:?xt=urn:btih:"
    dn="dn="+urllib.parse.quote(name,safe='')
    tr=[ "tr="+urllib.parse.quote(t,safe='') for t in trackers]
    tr="&".join(tr)
    return prefix+hash+"&"+dn+"&"+tr

def sizeof_fmt(num, suffix='B'):
    try:
        num=int(num)
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
               return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)
    except:
        return num


def piratebay(term):
    global data
    base_link="https://beaindia.org"
    print('\n\n[i] Please Wait Searching Data...')
    
    url = base_link+"/apibay/q.php?q="+term
    cookies = {"__cfduid": "dfa53d7227d2614eca69ee49261e0958e1596182467", "_ga": "GA1.2.1067275401.1596182469", "_gid": "GA1.2.2013677734.1596182469", "ppu_main_b1f57639c83dbef948eefa8b64183e1e": "1", "sb_main_740b003479a7eba76fd37c6ed9b4e91a": "1", "dom3ic8zudi28v8lr6fgphwffqoz0j6c": "5b26a583-ce6b-49fb-b679-fdf4d45980a9%3A1%3A2", "494668b4c0ef4d25bda4e75c27de2817": "5b26a583-ce6b-49fb-b679-fdf4d45980a9:1:2", "sb_count_740b003479a7eba76fd37c6ed9b4e91a": "2", "ppu_sub_b1f57639c83dbef948eefa8b64183e1e": "4"}
    headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": base_link+"/search.php?q=saf", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
    data = requests.get(url, headers=headers, cookies=cookies).json()
    
    RESULTS_PER_LOAD=10
    ndata=[ data[i:i + RESULTS_PER_LOAD ] for i in range(0, len(data), RESULTS_PER_LOAD)]
    for i,x in enumerate(ndata):
        for j,dt in enumerate(x):
            tn=i*RESULTS_PER_LOAD+j+1
            print(f'''[ {tn} ] TORRENT NUMBER #{tn} ''')
            print('\tName: ',dt.get('name','undefined'))
            print("\tSeeders | Leechers: ",dt.get("seeders",'undefined')+" | "+dt.get("leechers",'undefined'))
            print("\tSize: ",sizeof_fmt(dt.get("size","undefined")))
            print("\tStatus: ",dt.get("status","undefined"))
            print('\n')
        cho=input('\n\n\n[!] Load More(Y/N) : ')
        if cho.lower().strip()=='y':
            continue
        else:
            break

def torrentz(term):
    global name,link
    pblnk="https://utorrentz2.in"
    print('\n\n[i] Please Wait Searching Data...')
    term=urllib.parse.quote_plus(term.strip())
    site=pblnk+"/search.php?q="+term
    np=0
    #site="https://torrentz2eu.in/?q=sacred+games"
    req = urllib.request.Request(site, headers=hdr)
    try:
        page = urllib.request.urlopen(req)
    except:
        print('[-] Connection Error')
    name=[]
    link=[]
    seed=[]
    info=[]
    page=page.read().decode('utf-8')
    det=page.split('<tr>')[2:]
    for dt in det:
        p1=dt.find('Name">')+6
        tmp=dt[p1:dt.find('</td>',p1)]
        name.append(tmp)
        p1=dt.find('Seeds">')+7
        tmp=dt[p1:dt.find('</td>',p1)]
        seed.append(tmp)
        p1=dt.find('Size">')+6
        tmp=dt[p1:dt.find('</td>',p1)]
        info.append('Size: '+tmp)
        p1=dt.find('magnet',p1)+6
        tmp=dt[p1:dt.find('"',p1)]
        link.append(tmp)
    for i in range(len(link)):
        print(f'''\n\n[ {i+1} ] TORRENT NUMBER #{i+1} ''')
        print('\tName: ',name[i])
        #print('\tLink: ',link[i])
        print('\tSeed: ',seed[i])
        print('\tInfo: ',info[i])
def mag2tor(name,hash):
    base="https://itorrents.org"
    base+="/torrent/"+hash+".torrent"
    opener = urllib.request.build_opener()
    opener.addheaders= [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlretrieve(base, name)
        print("\n\n\n[i] Torrent File Saved To ",name)
        return True
    except:
        print("\n\n\n[!] You Need To use A VPN To Fetch Torrent...")
        return False
print('\tChecking For Updates...')
ver = urllib.request.urlopen("https://raw.githubusercontent.com/TheSpeedX/TorrGrab/master/.version").read().decode('utf-8')
verl = ''
try:
    verl = open(".version", 'r').read()
except Exception:
    pass
if ver != verl:
    print('\n\t\tAn Update is Available....')
    print('\tStarting Update...')
    urllib.request.urlretrieve('https://raw.githubusercontent.com/TheSpeedX/TorrGrab/master/torrgrab.py', 'torrgrab.py')
    print("Your Version is Updated")
    print("Exiting TorrGrab!!! Run it Again...")
    sys.exit()
else:
    print("Your Version is Up-To-Date")
if len(sys.argv)==2:
    if "u" in sys.argv[1]:
        print('\n\nUpdating TorrGrab...')
        urllib.request.urlretrieve('https://raw.githubusercontent.com/TheSpeedX/TorrGrab/master/torrgrab.py', 'torrgrab.py')
    print("Your Version is Updated")
    print("Exiting TorrGrab!!! Run it Again...")
    sys.exit()
print("[i] Search Engines Available: 2\n")
print('\t[1]\tPirateBay')
print('\t[2]\tTorrentz [ Out of service ]')
print('\n\n')
se=''

cho=input("Choose Engine [ 1 - 2 ]: ")

term=input("[?] Enter What to search: ").replace(' ','+')
if "1" in cho:
    se='piratebay'
    piratebay(term)
elif "2" in cho:
    se='torrentz'
    torrentz(term)
else:
    print('[-] Wrong Input.. \n\n[i]Using PirateBay By default')
    piratebay(term)
if len(data)==0:
    print("Sorry No Links Found...\nExiting...")
    exit()
try:
    inp=int(input("Enter Torrent Number: "))
except:
    print('Exiting TorrGrab')
    sys.exit()

torrent=data[inp-1]

name=torrent.get("name")
hash=torrent['info_hash']
magnet=scrapmagnet(hash,name)
fn=name.replace(" ","_")+".torrent"

print("[i] Files will be Downloaded by default torrent app on your System\n\n")
print('[i] Name: ',name)
print("[i] Seeders | Leechers: ",torrent.get("seeders",'undefined')+" | "+torrent.get("leechers",'undefined'))
print("[i] Size: ",sizeof_fmt(torrent.get("size","undefined")))
print("[i] Status: ",torrent.get("status","undefined"))
print("[i] Hash: ",hash)
print("[i] Total Files: ",torrent.get("num_files","undefined"))
print("[i] Magnet: ",magnet)

print('\n\n Fetching .torrent File From Magnet Link...')
res=mag2tor(fn,hash)

if not res:
    print('[i] Exiting TorrGrab..')
    sys.exit()


cho=input('\n\n\n[i] Start Download (Y/N) : ')
if cho.lower().strip()=='y':
    if sys.platform == "win32":
        os.startfile(fn)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, fn])
#   elif platform.system() == 'Darwin':  # macOS
#       subprocess.call(('open', fn))
#   elif platform.system() == 'Linux':
#       subprocess.call(('xdg-open', fn))
else:
    print('[i] Exiting TorrGrab..')
    exit()
