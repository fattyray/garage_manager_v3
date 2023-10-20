import pymysql
def dbinit():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()

    cursor.execute("""create table if not exists user(
        userid integer primary key AUTO_INCREMENT,
        username varchar(255) not null ,
        sex varchar(10) check ( sex='m' or sex='f' or sex='M' or sex='F'),
        age int check ( age>0 and age<120),
        address varchar(1024)
    )""")

    cursor.execute("""
    create table if not exists car(
        carid integer primary key AUTO_INCREMENT,
        carplate varchar(255) not null ,
        cartype varchar(1024),
        userid integer,
        foreign key (userid) references user(userid)
    )
    """)

    cursor.execute("""
    create table if not exists cartype(
        cartype varchar(1024) not null ,
        ishigh bool not null
    )
    
    """)


    cursor.execute("""
    create table if not exists account(
        userid integer primary key ,
        balance float,
        isvip bool
    )
    
    """)

    cursor.execute("""
    create table if not exists ingarage(
        carid integer primary key ,
        isin bool,
        inouttime datetime,
        entrance varchar(1024),
        garageid integer not null 
    )
    
    """)

    cursor.execute("""
    create table if not exists garage(
       garageid integer primary key  auto_increment,
       viproom integer,
       normroom integer,
       price float
    )
    """)

    #如果没有的话需创建视图

    # cursor.execute("""
    #
    # create view allowed as
    # select carid,carplate,car.cartype,ishigh
    # from car,cartype
    # where car.cartype=cartype.cartype;
    # """)

    # cursor.execute("""
    #
    # create view useraccount as
    # select user.userid,username,balance,isvip,carid
    # from user,account,car
    # where user.userid=account.userid and car.userid=user.userid
    # """)

    # cursor.execute("""
    #
    #   create view parking_fee as
    # select car.carid,carplate,garage.garageid,((TIMESTAMPDIFF(MINUTE,inouttime,current_timestamp())*garage.price )/60.0)as fee
    # from car,ingarage,garage
    # where car.carid=ingarage.carid and ingarage.garageid=garage.garageid
    #     """)
    db.close()
#
# dbinit()

def createuser(username,usersex,userage,address):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    sql="insert into user( username, sex, age, address) values ('{0}','{1}',{2},'{3}');".format(username,usersex,userage,address)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

# 测试
# createuser("admin",'m',23,'广州市番禺区')

def createcar(carplate,cartype,userid):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    try:
        # 执行sql语句
        sql="insert into car( carplate, cartype, userid)  values ('{0}','{1}',{2});".format(carplate,cartype,userid)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
# createcar("粤·TNT385","东风日产天籁",1)

def createcartype(cartype,ishigh):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    try:
        # 执行sql语句
        if ishigh:
            ishigh="true"
        else:
            ishigh="false"
        sql="insert into cartype(cartype, ishigh) values ('{0}',{1});".format(cartype,ishigh)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

# createcartype("东风日产天籁",True)

def createaccount(userid,balance,isvip):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    try:
        # 执行sql语句
        if isvip:
            isvip = "true"
        else:
            isvip = "false"
        sql="insert into account(userid, balance, isvip) values ({0},{1},{2}); ".format(userid,balance,isvip)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()
# createaccount(1,200.0,False)


def createingarage(carid,isin,entrance,garageid):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    try:
        # 执行sql语句
        if isin:
            isin = "true"
        else:
            isin = "false"
        sql="insert into ingarage(carid, isin, inouttime, entrance, garageid) values ({0},{1},current_timestamp(),'{2}',{3}); ".format(carid,isin,entrance,garageid)
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

# createingarage(1,True,"entrance1",1)


def creategarage(viproom,normroom,price):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    sql="insert into garage( viproom, normroom, price) VALUES ({0},{1},{2});".format(viproom,normroom,price)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

# creategarage(400,600,0.4)
def hasowner(name):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    sql="select userid from  user where username='{0}'; ".format(name)
    cursor.execute(sql)
    l=cursor.fetchall()
    if len(l)>0:
        return True
    else:
        return False


def getowner(name):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    sql="select userid from  user where username='{0}'; ".format(name)
    cursor.execute(sql)
    result=cursor.fetchone()
    return result[0]

# getowner("admin")

def hascartype(name):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    sql="select * from  cartype where cartype='{0}'; ".format(name)
    cursor.execute(sql)
    result=cursor.fetchall()
    print(result)
    return len(result)

# print(hascartype("东风日产天籁"))

def getbalance(userid):

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute(" select balance from account where userid = {0};".format(userid))
    ans=cursor.fetchone()
    return ans[0]
def addbalance(userid,add):

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute(" select balance from account where userid = {0};".format(userid))
    ans=cursor.fetchone()
    cursor.execute(" update account set balance={1} where userid = {0};".format(userid,( ans[0]+add)))
    db.commit()
    db.close()

def setvip(userid):

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute(" update account set isvip=true where userid = {0};".format(userid))
    db.commit()
    db.close()


def hasvip(userid):

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='2222',
                         database='myproject')
    cursor = db.cursor()
    cursor.execute("select isvip from account where userid = {0};".format(userid))
    ans = cursor.fetchall()
    db.close()
    if len(ans)<1:
        return 0
    else:
        return ans[0][0]


# print(hasvip(6))
# print(getbalance(1))