#-*- coding:utf-8 -*-
from pyquery import PyQuery as pq
import tornado.ioloop
import tornado.web
import os
import time
import urlparse
import urllib
import urllib2
import struct
import json
import re
import sys
import redis
import signal
from copy import deepcopy

gRed = 0
goOn = True
#MIN_ARRAY = [565, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900]
MIN_ARRAY = [925, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054,
        1055, 1056, 1057, 1058, 1059, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346,
        1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1500]


def onsignal_int(a,b):
    global goOn
    print "signal"
    goOn = False

def getRedis():
    global gRed
    if gRed == 0:
        gRed = redis.Redis()
        return gRed
    else:
        return gRed

def getPage(url):
    for i in range(1,5):
        try:
            conn = urllib2.urlopen(url, timeout=10)
            page = conn.read()
            conn.close()
            return page

        except:
            info = sys.exc_info()
            print info, url

    print "!!!!! ERROR, url = %s"%(url)
    return False

def getChengFen(bkid):
    page = 1
    gs = []
    name = []
    while True:
        url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%d&num=80&sort=changepercent&asc=0&node=%s&symbol=&_s_r_a=init"%(page,bkid)
        val = getPage(url)
        if val == False:
            break

        val = val.decode("gb2312").encode("utf-8")
        gids = re.findall('code:"(\d+)"', val, re.DOTALL)
        names = re.findall('name:"([^"]+)"', val, re.DOTALL)

        gs = gs + gids
        name = name + names
        count = len(gids)
        page = page + 1
        if count == 0:
            break

    res = [ [ int(gs[i]), name[i] ] for i in range(len(gs)) ]
    return res

def initData():
    red = getRedis()
    urls = [
            "http://money.finance.sina.com.cn/q/view/newFLJK.php?param=class",
            "http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php"
            ]

    for url in urls:
        page = getPage(url)
        if page == False:
            break

        page = page.decode("gb2312").encode("utf-8")

        idx = page.find("=")
        val = page[ idx+1: ]
        decode = json.loads(val)

        for key in decode:
            vals = decode[key].split(',')
            bkid = vals[0]
            name = vals[1]
            gps = getChengFen(bkid)
            gids = [ int(x[0]) for x in gps ]

            red.hset("names", bkid, name)
            bkkey = "bk:%s"%(bkid)
            for gid in gps:
                red.sadd(bkkey, gid[0])
                red.sadd("gp:%d"%(gid[0]), bkkey)
                red.hset("names", gid[0], gid[1])


def doGetData(days, url):
    page = getPage(url)
    if not page:
        return

    try:
        d = pq(page)
        p = d('#FundHoldSharesTable')
        rs = p.children("tr")

        if len(rs) > 0:
            for row in rs[1:]:
                node = []
                for item in pq(row).children("td"):
                    node.append(pq(item).text())

                day = node[0]
                day = day.split("-")

                day = "%d%02d%02d"%(int(day[0]), int(day[1]), int(day[2]))
                day = int(day)

                kp = int(round(100*float(node[1])))
                zg = int(round(100*float(node[2])))
                sp = int(round(100*float(node[3])))
                zd = int(round(100*float(node[4])))
                vol = int(node[5])
                amo = int(node[6])
                if vol > 0:
                    n = [ day, kp, zg, zd, sp, amo, vol]
                    days.append(n)

    except:
        print "datas:%s error"%(page)


def getDataHistory(gid):
    t = time.localtime()
    year = t.tm_year
    mon = t.tm_mon
    jidu = (mon+2)/3
    days = []
    for i in range(4):
        symbol = "%06d"%(gid)
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d"%(symbol, year, jidu)
        doGetData(days, url)

        jidu = jidu - 1
        if jidu == 0 :
            year = year - 1
            jidu = 4

    red = getRedis()
    key = "dayk:%d"%(gid)
    red.delete(key)
    for v in days:
        red.zadd(key, json.dumps(v), v[0])

    print gid

def fillIndex():
    t = time.localtime()
    year = t.tm_year
    mon = t.tm_mon
    jidu = (mon+2)/3
    days = []
    for i in range(4):
        url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml?year=%d&jidu=%d"%(year, jidu)
        doGetData(days, url)
        jidu = jidu - 1
        if jidu == 0 :
            year = year - 1
            jidu = 4

    key = "dayK:index"
    red = getRedis()
    red.delete(key)
    red.delete("dates")
    for v in days:
        red.zadd(key, json.dumps(v), v[0])
        red.zadd("dates", v[0], v[0])

    print "done"


def clean():
    red = getRedis()

    red.zremrangebyrank("dates", 0, -210)
    d30 = int(red.zrange("dates", -30, -30)[0])
    d200 = int(red.zrange("dates", 0, 0)[0])

    keys = red.keys("rank:*")
    for key in keys:
        day = int(key.split(":")[1])
        if day < d30:
            red.delete(key)

    keys = red.keys("rankbk:*")
    for key in keys:
        day = int(key.split(":")[1])
        if day < d30:
            red.delete(key)

    keys = red.keys("tick:*")
    for key in keys:
        day = int(key.split(":")[1])
        if day < d30:
            red.delete(key)

    keys = red.keys("dayk:*")
    for key in keys:
        red.zremrangebyscore(key, 0, d200)

    print d30, d200


def daily():
    clean()
    fillIndex()
    getDataToday()
    makeBanKuaiRank(1)

def getDataAll():
    global goOn
    fillIndex()
    red = getRedis()
    gids = red.keys("gp:*")
    total = len(gids)
    count = 0
    for gid in gids:

        ns = gid.split(":")
        gid = int(ns[1])

        res = red.sismember("update", str(gid))
        if not res:
            getDataHistory(gid)
            red.sadd("update", str(gid))

        count = count + 1
        print gid, total, count, total - count

        if goOn == False:
            break

def getVal(red, val):
    vals = val.split(",")
    if len(vals) < 10:
        print "getVal", vals
        return

    code = int(vals[0].split("=")[0][-6:])

    kp =  int(round(100*float(vals[1])))
    zs =  int(round(100*float(vals[2])))
    sp =  int(round(100*float(vals[3])))
    zg =  int(round(100*float(vals[4])))
    zd =  int(round(100*float(vals[5])))
    vol = int(vals[8])
    amo = int(float(vals[9]))
    day = vals[30]
    day = int("%s%s%s"%(day[0:4], day[5:7], day[8:10]))

    key = "dayk:%d"%(code)
    if vol == 0:
        m = [ day, kp, zg, zd, sp, amo, vol ]
        n = [ day, zs, zs, zs, zs, amo, vol ]

    else:
        n = [ day, kp, zg, zd, sp, amo, vol ]

    if red != None:
        red.zremrangebyscore(key, day, day)
        red.zadd(key,  json.dumps(n), day)
        return

    return (key, n)

def getDataToday() :
    red = getRedis()
    ids = red.keys("gp:*")

    num = 0
    base = "http://hq.sinajs.cn/list="
    page = "http://hq.sinajs.cn/list="
    node = ""

    for key in ids:
        i = key.split(":")[1]
        i = "%06d"%(int(i))

        if i[:2] == "60":
            node = "sh%s,"%i
        else:
            node = "sz%s,"%i

        page += node
        num += 1
        if num >= 10:
            print page
            val = getPage(page)
            nodes = val.split(";")
            for m in nodes:
                if len(m) > 10:
                    getVal(red, m)

            page = base
            num = 0

    if num > 0:
        val = getPage(page)
        nodes = val.split(";")
        for m in nodes:
            if len(m) > 10:
                getVal(red, m)

# Rank Start --------------------
def getGidScore(days, gid):
    red = getRedis()
    num = len(days) + 1

    rs = red.zrange(gid, -num, -1)
    rs = [ json.loads(x) for x  in rs ]

    last = 0
    res = {}
    for r in rs:
        vol = r[5]
        if vol > 0:
            day = r[0]
            sp = r[4]
            if last == 0:
                last = sp

            if last != 0 :
                rate = sp*1.0/last
                if rate > 1.2:
                    rate = 1.2
                if rate < 0.8:
                    rate = 1

                res[ day ] = int(round(rate*1000))

            last = sp

    scores = []
    for day in days:
        if res.has_key(day):
            scores.append(res[day])
        else:
            scores.append(0)
    return scores

def makeBanKuaiRank(num):
    print "makeBanKuaiRank", num

    red = getRedis()
    days = red.zrange("dates", 0, -1)

    days = [ int(x) for x in days ]
    days = days[-num:]

    syms = red.keys("dayk:*")

    num = len(days)
    alls = {}
    for sym in syms:
        rs = getGidScore(days, sym)
        if len(rs) == num:
            rs.reverse()
            gid = int(sym.split(":")[1])
            alls[ gid ] = rs

    bksyms = red.keys("bk:*")
    bks = []
    for sym in bksyms:
        bkname = sym.split(":")[1]
        gids = red.smembers(sym)
        gids = [ int(x) for x in gids ]
        bks.append([ bkname, gids ])

    mode = ["new", "gn"]

    for day in days:
        gids = {}
        for gid in alls:
            gidDay = alls[ gid ].pop()
            if gidDay > 0:
                gids[ gid ] = gidDay

        for mod in mode:
            res = []
            nmod = len(mod)

            bks1 = filter(lambda x:x[0][:nmod] == mod, bks)
            for bk in bks1:
                ks = []
                for gid in bk[1]:
                    if gids.has_key(gid):
                        ks.append([ gid, gids[gid] ])

                ks = sorted(ks, key=lambda x:x[1])
                avg = sum( [ x[1] for x in ks ] ) / len(ks)
                res.append( [ bk[0], avg, ks ] )

            res = sorted(res, key=lambda x:x[1] )
            res.reverse()
            bot10 = []
            for b in res[-10:]:
                bot10.append( [ b[0], b[1] ] )
                red.set("rankbk:%d:%s"%(day, b[0]), json.dumps(b[2]))

            top10 = []
            for b in res[:10]:
                top10.append( [ b[0], b[1] ] )
                red.set("rankbk:%d:%s"%(day, b[0]), json.dumps(b[2]))

            avg = int( round( sum( [ x[1]  for x in res ] ) / len(res)))

            red.hset("rank:%d:%s"%(day, mod), "avg", avg)
            red.hset("rank:%d:%s"%(day, mod), "top", json.dumps(top10))
            red.hset("rank:%d:%s"%(day, mod), "bot", json.dumps(bot10))

            print day, avg, top10


# Web Interface ------------------
# gid, day is str
def web_getTick(gid, day):
    print "web_getTick", gid, day
    red = getRedis()
    idx = red.zrank("dates", day)
    days = red.zrange("dates", idx-1, idx+1)
    res = ""
    for d in days:
        rs = doGetTick(int(gid), int(d))
        if len(rs) > 0:
            if res == "":
                res = rs[1:-1]
            else:
                res = "%s,%s"%(res, rs[1:-1])
    res =  "[%s]"%(res)
    return res


# gid, day is number
def doGetTick(gid, day):
    red = getRedis()
    key = "tick:%d:%d"%(day, gid)
    r = red.get(key)
    if r != None:
        print "hit", gid, day
        return r

    sday = str(day)
    date = "%s-%s-%s"%(sday[0:4], sday[4:6], sday[6:8])

    sgid = "%06d"%(gid)
    if sgid[0:2] == "60":
        gid1 = "sh" + sgid
    else:
        gid1 = "sz" + sgid

    url = "http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s"%(date, gid1)
    page = getPage(url)
    if not page:
        #red.set(key, "")
        print "getTick error", gid, day 
        return ""

    ms = page.split("\n")[1:-1]
    ms.reverse()

    ds = []
    for m in ms:
        n = m.split("\t")
        if len(n) < 5:
            print "tick error", gid, day
            red.set(key, "")
            return ""

        t = n[0]
        t = int("%s%s"%(t[0:2], t[3:5]))
        if (t>=925 and t<=1130) or (t>=1300 and t<=1510):
            jg =  int(round(float(n[1]) * 100))
            vol = int(n[3])
            ds.append([t, jg, vol])

    start = time.mktime([ int(sday[0:4]), int(sday[4:6]), int(sday[6:8]), 0, 0, 0, 0, 0, 0 ])
    ds.append([ 1600, 0, 0 ])

    num = len(ds)
    ts = []
    pri = 0
    vol = 0
    i = 0
    for t in MIN_ARRAY:
        while i < num:
            node = ds[i]
            i = i+1

            if node[0] == t:
                pri = node[1]
                vol = vol + node[2]
            else:
                h = t / 100
                m = t % 100
                tm = int(start + h * 3600 + m * 60)
                ts.append([ tm, pri, vol ])
                #ts.append([ t, pri, vol ])
                vol = 0
                i = i - 1
                break

    vals = json.dumps(ts)
    red.set(key, vals)
    return vals


def web_getDayTable():
    red = getRedis()
    days = red.zrange("dates", 0, -1)
    rs = {}
    for day in days:
        tm = time.mktime([ int(day[0:4]), int(day[4:6]), int(day[6:8]), 0, 0, 0, 0, 0, 0 ]) + 8*3600
        rs[ day ] =  int(tm * 1000)

    return json.dumps(rs)


def web_getDayK(gid, day):
    gid = int(gid)
    day = int(day)
    key = "dayk:%d"%(gid)

    red = getRedis()
    rs = red.zrangebyscore(key, day, day)
    r = rs[0]
    idx = red.zrank(key, r)
    if idx < 100 :
        idx = 100

    rs = red.zrange(key, idx-100, idx + 10)
    print gid, day, len(rs)
    rs = ",".join(rs)

    name = red.hget("names", gid)
    n1 = json.dumps([ name ])

    val = "[ %s, [ %s ] ]"%(n1, rs)
    return val


def web_bkday(name, day):
    key = "rankbk:%s:%s"%(day, name)
    red = getRedis();
    val = red.get(key)
    return val


def web_bkrank():
    red = getRedis()
    keys = red.keys("rank:*")
    t1 = []
    t2 = []
    b1 = []
    b2 = []

    for key in keys:
        r = red.hgetall(key)
        day = int( key.split(":")[1] )
        mod = key.split(":")[2]
        top = json.loads(r['top'])
        bot = json.loads(r['bot'])
        top.insert(0, day)
        bot.insert(0, day)

        if mod == "new":
            t1.append(top)
            b1.append(bot)
        else:
            t2.append(top)
            b2.append(bot)

    t1 = sorted(t1, key=lambda x:x[0])
    t2 = sorted(t2, key=lambda x:x[0])
    b1 = sorted(b1, key=lambda x:x[0])
    b2 = sorted(b2, key=lambda x:x[0])

    names = {}
    all = [ t1, b1, t2, b2 ]
    for i in all:
        i.reverse()
        for j in i:
            for n in j[1:]:
                sym = n[0]
                if names.has_key(sym):
                    n.insert(1, names[sym])
                else:
                    name = red.hget("names", sym)
                    n.insert(1, name)
                    names[ sym ] = name


    return json.dumps(all)


# Rank End --------------------

# Web Start --------------------

class DailyJob(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        daily()
        self.write("done")
        self.finish()

class Index(tornado.web.RequestHandler):
    def get(self):
	print "income, ip", self.request.remote_ip
        self.redirect('/static/grid.html', permanent=True)

#class Index(tornado.web.RequestHandler):
#    def get(self):
#        self.redirect('/static/grid.html', permanent=True)

class FakeHandler(tornado.web.RequestHandler):
    def get(self):
	print "fake, income, ip", self.request.remote_ip
        print "fake, income, ip", self.request.remote_ip
	return

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        action = self.get_argument('action')
        print action
        if action == 'bkrank':
            res = web_bkrank()

        elif action == 'day':
            day = self.get_argument('day')
            gid = self.get_argument('gid')
            res = web_getDayK(gid, day)

        elif action == 'tick':
            day = self.get_argument('day')
            gid = self.get_argument('gid')
            res = web_getTick(gid, day)

        elif action == 'bkday':
            name = self.get_argument('name')
            day = self.get_argument('day')
            res = web_bkday(name, day)

        elif action == 'dayTable':
            res = web_getDayTable()

        callback = self.get_argument('callback')
        val = "%s(%s)"%(callback, res)
        self.write(val)


def fixData():
    red = getRedis()
    syms = red.keys("dayk:*")
    for sym in syms:
        recs = red.zrange(sym, 0, -1)
        for rec in recs:
            r = json.loads(rec)
            day = r[0]
            if not isinstance(day, int):
                r[0] = int(day)
                print sym, rec, " -> ", r
                red.zrem(sym, rec)
                red.zadd(sym, json.dumps(r), day)


def checkData():
    red = getRedis()
    days = red.zrange("dates", 0, -1)
    print days
    syms = red.keys("dayk:*")
    for sym in syms:
        zsp = 0
        for day in days:
            day = int(day)
            rec = red.zrangebyscore(sym, day, day)
            if len(rec) == 0:
                if zsp > 0:
                    new = [ day, zsp, zsp, zsp, zsp, 0, 0]
                    print sym, "None -> ", new
                    red.zadd(sym, json.dumps(new), day)
                #else:
                    #print sym, "None -> what ", day

            else:
                r = json.loads(rec[0])
                sp = r[4]
                if sp > 0 :
                    zsp = sp

                if r[6] == 0 and r[5] == 0 and r[1] == 0:
                    new = [ day, zsp, zsp, zsp, zsp, 0, 0 ]
                    print sym, r, " -> ", new
                    red.zrem(sym, rec[0])
                    red.zadd(sym, json.dumps(new), day)


settings = { "static_path": os.path.join(os.path.dirname(__file__), "static") }
application = tornado.web.Application( [(r"/do", MainHandler),(r"/daily", DailyJob),(r"/", Index),],**settings)
#application = tornado.web.Application( [(r"/", FakeHandler),],**settings)
application.add_handlers(r"^a\.twentyear.com$", [(r"/do", MainHandler),(r"/daily", DailyJob),(r"/", Index),])

if __name__ == "__main__":
    Port = 8080
    application.listen(Port)
    print "listen :", Port
    tornado.ioloop.IOLoop.instance().start()

    #makeMinArr()
    #doGetTick(601901, 20141127)
    #print web_getTick('600657', '20141125')
    #checkData()
    #fixData()

    #print web_getDayTable()
    #signal.signal(signal.SIGINT, onsignal_int)
    #getDataToday()
    #fillIndex()

    #getGidScore([20141126,20141125,20141124], "dayk:589")
    #makeBanKuaiRank(30)
    #daily()
    #web_bkrank()

    #days = red.lrange("dates", 0, -1)
    #for day in days:
    #    red.zadd("date", day, day)

    #red.delete("dates")
    #red.rename("date", "dates")


#index              sset, [ [day1, open, hight, low, close, vol, amount], [day2, open, hight, low, close, vol, amount], ... ]
#"dayk:3169"        sset, [ [day1, open, hight, low, close, vol, amount], [day2, open, hight, low, close, vol, amount], ... ]
#"tick:20141128:3169"    string
#"bk:new_jrhy"      set,  [gidA, gidB, .. ]
#"gp:3169"          set,  [bkA, bkB, ... ]
#names              hashs , include gid, bk
#dates              list , [20141126, 20141125, ...]

#"rank:20141111:new"
#"rank:20141111:gn"

#"rankbk:20141111:new_jrhy"
#"rankbk:20141111:gn_xsb"


#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.GetDateList?symbol=sh601336&num=60&page=1&sort=ticktime&asc=0&volume=40000&amount=0&type=0&day=
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=2014-11-27&symbol=sh601336
#http://finance.sina.com.cn/realstock/company/sh601336/jsvar.js
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date=2014-11-27&symbol=sh601336
#http://hq.sinajs.cn/rn=1417054674785&list=s_sz300268,s_sh000001,s_sz000001,s_sz002731,s_sh601137,s_sh601688,s_sz300087,s_sz002542,s_sz002084,s_sh600000,s_sh601515,s_sz002122,s_sh601788,s_sz300183,s_sz300028,s_sh601015,s_sz002488,s_sh603169,s_sz000050,s_sh601377,s_sh600030,s_sh601390,s_sh601901,s_sh600837,s_sh600832,s_sh601899,s_sh601186,s_sh600010,s_sh600755,s_sz000783,s_sh600016,s_sz000776,sh601336,rt_hk01336,RMBHKD,bk_
#http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num=9&symbol=sh601336&rn=1417054674948
