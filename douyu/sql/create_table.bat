@echo off
::set path=D:\oracle\app\jr\product\11.2.0\dbhome_1\bin;D:\instantclient_11_2;
::set TNS_ADMIN=D:\instantclient_11_2\NETWORK\ADMIN
::set ORACLE_HOME=D:\instantclient_11_2
set NLS_LANG=SIMPLIFIED CHINESE_CHINA.ZHS16GBK
::set NLS_LANG=american_america.AL32UTF8

::��������(yyyymmdd)
set y=%date:~0,4%
set m=%date:~5,2%
set d=%date:~8,2%
set rq=%y%%m%%d%

::��ȡ·��,���û�д���,��ȡ��ǰ·��
set my_path=%1
if "%my_path%"=="" ( 
    set my_path=%cd%
)

::ִ��sql
sqlplus aaaa/bbbb@ORCL @%my_path%\create_table.sql %rq%

