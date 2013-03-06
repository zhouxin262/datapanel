Requirements:
------------
    sudo apt-get install python-setuptools
    sudo easy_install -U distribute
    sudo apt-get install python-dev
    sudo apt-get install libmysql++-dev
    sudo easy_install mysql-python
    sudo easy_install django
    sudo easy_install flup

    sudo apt-get install uwsgi
    sudo apt-get install uwsgi-plugin-python
    mysql
    python 2.7
    django 1.4
    pyyaml
    python-memcached
    south

How to Use:
------------
注册并建立项目，在设置中找到token。在要统计的页面html中加入：

    <script type="text/javascript" src="http://www.ezaiai.com/js/{{your_token_here}}/" charset="utf-8"></script>
    <script type="text/javascript">
    jx.push('index',{});
    </script>

---
* jx.push中第一个参数是动作名称，例如: index, goods, flow...
* 建立项目中url必须填写正确，只有来自该域名下的数据才会被采集


How to migrate DB:
------------
强烈建议用服务器上的数据库，如果不是最新的，我可以备份给你

---

    1. install south
    2. syncdb - 以后都不用再syncdb了
    3. new app:
        ./manage.py schemamigration appname --initial
        ./manage.py migrate appname
    4. changed model:
        ./manage.py schemamigration appname --auto
        ./manage.py migrate appname
    5. 多机搞起时 fake 十分重要，不解释

---


Using js lib:
------------
    jquery
    jquery.dataTables
    jquery.flot


Using flash Plugins:
------------
    FusionCharts


