![这里写图片描述](https://yum.postgresql.org/layout/images/hdr_left.png)
##安装

```
[root@master download]# wget https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-3.noarch.rpm
[root@master download]# yum localinstall pgdg-centos95-9.5-3.noarch.rpm 
[root@master download]# yum -y install postgresql95-server postgresql95-contrib
[root@master download]# /usr/pgsql-9.5/bin/postgresql95-setup initdb
[root@master download]# service postgresql-9.5 status
```

##初始登录

```
[root@master ~]# sudo groupadd postgresql
[root@master ~]# sudo useradd -g postgresql postgresql
[root@master ~]# sudo passwd postgres
[root@master ~]# su postgres
bash-4.2$ psql
psql (9.5.9)
输入 "help" 来获取帮助信息.

postgres=# \q
bash-4.2$ exit
[root@master learn-pgsql]# sudo -u postgres psql
psql (9.5.9)
输入 "help" 来获取帮助信息.

postgres=# ... ...
```
####抑或者

```
[root@master learn-pgsql]# psql -U root -d postgres
```

##运行脚本
####今有一个sql脚本文件：
```
[root@master learn-pgsql]# vi create_countries.sql
CREATE TABLE countries(
        country_code char(2) PRIMARY KEY,
        country_name text UNIQUE
);

```
####运行她
```
[root@master learn-pgsql]# sudo -u postgres psql
psql (9.5.9)
输入 "help" 来获取帮助信息.

postgres=# \i create_countries.sql 
CREATE TABLE
```

##未完待续


/usr/pgsql-9.5/bin/pg_config
/var/lib/pgsql/9.5/
 yum install postgresql-devel ----------------- /usr/include/libpq-fe.h //"cp /usr/include/libpq*.h somewhere/include"
 update pg_database set encoding = pg_char_to_encoding('GBK') where datname = 'oddsdata' ; //can change the encoding but cause to error;
 string.decode('utf-8').encode('utf-8') //use this to transfer the data in GBK and could written to psql;

docker run -d -i -t <imageID> /bin/bash;
docker rmi <imageID>;
docker attach <ContainerID>;
docker start  <ContainerID>;
docker commit <ContainerID> <NAME/VERSION>;
docker kill <ContainerID>;docker rm <ContainerID>;
docker rm $(  docker ps –a –f ancestor=hello-world )


docker pull sequenceiq/hadoop-docker:2.7.1
docker run -it sequenceiq/hadoop-docker:2.7.1 /etc/bootstrap.sh -bash
cd $HADOOP_PREFIX
# run the mapreduce
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.1.jar grep input output 'dfs[a-z.]+'
# check the output
bin/hdfs dfs -cat output/*


mvn archetype:generate -DgroupId=storm.blueprints -DartifactId=Chapter1 -DpackageName=storm.blueprints.chapter1.v1
mvn exec:java -Dexec.mainClass="com.vineetmanohar.module.Main"  

git config --global user.name oldinaction #用户名
git config --global user.email oldinaction@qq.com #邮箱
git remote add origin git@github.com:Luomin1993/soccerbet.git
git remote rm origin

git init
#只提交当前目录的test.html文件到本地git仓库（虽然文件在这个目录，但是如果不提交的话就不在本地的Git仓库，之后就不能和远程仓库进行数据交互）
git add test.html 
#就可以把所有内容添加到索引库中，注意后面有个点
git add . 
#提交索引库中的内容；-m是参数，表示注释内容，主要用来记录此次操作
git commit -m 
git push -u origin master
git push -u origin +master
