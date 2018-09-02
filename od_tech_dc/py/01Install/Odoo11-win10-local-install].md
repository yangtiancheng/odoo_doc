# Odoo10安装

## Odoo11 - Windows - Install

1.获取github源码，([github地址](https://github.com/odoo/odoo))


2.通过clone获取v10源代码
git clone https://www.github.com/odoo/odoo --depth 1 --branch 10.0 --single-branch odoo10

3. 安装底层应用依赖资源：
```text
1.安装python环境
这里我们使用annacoda3(https://www.anaconda.com/download/#windows)，由于odoo10以上版本需要使用python3.x，所以我们使用conda指令创建python3.6虚拟环境
    'conda create -n py3od11 python=3.6'
2. 配置环境变量path(和python的一样 只不过需要配置的时创建的虚拟环境的路径 例如:D:\Anaconda3\envs\py3od11 和 D:\Anaconda3\envs\py3od11\Script)
3. python改名 
    例如虚拟环境路径中：D:\Anaconda3\envs\py3od11
    python.exe -> python36.ext
pythonw.exe -> pythonw36.ext

    
4. 安装基础必要插件
     python36 -m pip install [package_name]
        Package_name包有如下:
        pypiwin32 
        
        Pillow-3.4.2-cp36-cp36m-win_amd64.whl 
        
        gevent-1.2.2-cp36-cp36m-win_amd64.whl 
        
        lxml-3.8.0-cp36-cp36m-win_amd64.whl 
        
        psutil-5.3.1-cp36-cp36m-win_amd64.whl 
        
        psycopg2-2.7.3-cp36-cp36m-win_amd64.whl 
        
        pyldap-2.4.37-cp36-cp36m-win_amd64.whl 
        
        reportlab-3.4.0-cp36-cp36m-win_amd64.whl
        
5. 安装odoo必要插件
    切换到odoo目录下，你会发现有一个requirements.txt的文件，我们安装它内部的插件:
    python36 -m pip install -r requirements.txt
    python36 -m pip install -U werkzeug
```

4. 安装必要的pdf打印插件 [下载wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)

5. 下载一个postgresql的navicat数据库管理软件.

6. 下载并安装postgres10.
对应pg的端口请配置好 例如(端口：5432 密码：123456)
[Postgres下载路径](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

7.在navicat中连接postgresql数据库.


8.在数据库中创建一个拥有createdb权限的用户 例如：user:odoo pwd:odoo 



9. 启动服务
通过CMD切换到odoo的文件目录下，执行命令 python36 odoo-bin -s 
这样会在odoo的文件目录下生成一个odoo.conf的配置文件，我们只需要对文件进行配置修改.

10. 安装完成运行时发现缺少一些关系包 虽然这些在requirements.txt包含，但是估计批量没安装成功 我们手动安装一下
python36 -m pip install 包名

如：PyPDF2 passlib python-dateutil pywin32 PyYAML Pillow jinja2 html2text num2words等，运行时报错缺什么就装什么

11. 为了启动能够连接到对应的数据库，我们需要修改对应的odoo.conf文件
例如我修改后的配置文件:
```text
[options]
addons_path = D:\odoo11plus\odoo\odoo\addons,D:\odoo11plus\odoo\addons
admin_passwd = handhand
csv_internal_sep = ,
data_dir = D:\odoo11plus\data_dir
db_host = localhost
db_maxconn = 64
db_name = False
db_password = odoo
db_port = 5432
db_sslmode = prefer
db_template = template1
db_user = odoo
demo = {}
email_from = False
geoip_database = /usr/share/GeoIP/GeoLite2-City.mmdb
http_enable = True
http_interface = 
http_port = 8069
import_partial = 
limit_memory_hard = None
limit_memory_soft = None
limit_request = None
limit_time_cpu = None
limit_time_real = None
limit_time_real_cron = None
list_db = True
log_db = False
log_db_level = warning
log_handler = :INFO
log_level = info
logfile = False
logrotate = False
longpolling_port = 8072
max_cron_threads = 2
osv_memory_age_limit = 1.0
osv_memory_count_limit = False
pg_path = C:\Program Files\PostgreSQL\10\bin
pidfile = False
proxy_mode = False
reportgz = False
server_wide_modules = web
smtp_password = False
smtp_port = 25
smtp_server = localhost
smtp_ssl = False
smtp_user = False
syslog = False
test_commit = False
test_enable = False
test_file = False
test_report_directory = False
translate_modules = ['all']
unaccent = False
without_demo = False
workers = None
```
必须配置的有: admin_passwd、db_host、db_port、db_user、db_password、pg_path 其他的按情况配置.

12.为了工程化操作，我们可以在pycharm中直接创建一个启动项:

之后我们只需要在pycharm选择对应的启动服务，点击运行 就可以使用odoo服务了。

前台创建数据库并登入:


后记：
写的粗糙，后期继续细化，另外如果把python的应用放到docker镜像中，在本地使用postgresql10的数据库服务，那样的开发应该是最适合的，以后补充。