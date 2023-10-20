import pymysql
def CanEnter(carplate):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select  ishigh from allowed where carplate='{0}'".format(carplate))
    s=cursor.fetchall()
    print(s)
    db.close()
    if len(s)==0:
        return False
    if s[0]==0:
        return True
    else:
        return True


#
print(CanEnter("桂C·GT009"))

def GetCarId(carplate):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select carid from car where carplate='{0}';".format(carplate))
    s=cursor.fetchone()
    db.close()
    if len(s)==0:
        return 0
    else:
        return s[0]

def GetUserId(carplate):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select userid from car where carplate='{0}';".format(carplate))
    s = cursor.fetchone()
    db.close()
    if len(s) == 0:
        return 0
    else:
        return s[0]
def isin(carplate,garageid):
    ids = GetCarId(carplate)
    if ids==0:
        return False
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select * from ingarage where  carid={0} and garageid = {1};".format(ids, garageid))
    s = cursor.fetchall()
    if len(s) == 0:
        return False
    else:
        return True

def Enter(carplate,entrances,garageid):
    if not CanEnter(carplate):
        return "Failed"
    ids=GetCarId(carplate)
    if ids==0:
        return "Failed"
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select * from ingarage where  carid={0} and garageid = {1};".format(ids,garageid))
    s=cursor.fetchall()
    if len(s)==0:
        #说明该车库之前没有该车的入库信息,说明现在是进
        import db_use
        db_use.createingarage(ids,True,entrances,garageid)

    else:
        #说明之前该车辆有在入口处进行识别但没有实际的进入，应当清除该车之前的在该停车场id下的记录然后在入内
        cursor = cursor.execute("delete from ingarage where carid = {0} and garageid = {1};".format(ids,garageid))
        db.commit()
        db.close()
    return "Success"

# Enter("京A·128F8","西门",1)
def Leave(carplate,garageid):
    ids = GetCarId(carplate)
    if ids == 0:
        return "Failed"
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select * from ingarage where  carid={0} and garageid={1};".format(ids,garageid))
    s = cursor.fetchone()
    if len(s)==0:
        return "Failed"
    else:
        cursor.execute("select isvip from useraccount where carid={0}".format(ids))
        isvip=cursor.fetchone()[0]
        print(isvip)
        if isvip:
            cursor.execute("delete from ingarage where carid={0} and garageid={1}".format(ids,garageid))
            db.commit()
            db.close()
            return 0
        else:
            cursor.execute("select fee from parking_fee where carid={0} and garageid={1} ".format(ids,garageid))
            ss=cursor.fetchone()[0]
            print(ss)
            cursor.execute("delete from ingarage where carid={0} and garageid={1}".format(ids, garageid))
            db.commit()
            db.close()
            return ss

# Leave("粤·TNT385",1)

def isfull(garageid):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='20021110wcr',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select count(isin) from ingarage where garageid={0} ;".format(garageid))
    s=cursor.fetchone()[0];
    # print(s)
    cursor.execute("select garage.viproom+garage.normroom from garage where garageid={0};".format(garageid))
    x=cursor.fetchone()[0];
    # print(x)
    return s>=x

isfull(1)