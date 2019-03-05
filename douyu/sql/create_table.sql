--屏幕输出
SET SERVEROUTPUT ON 
--输出语句 for test
--SET ECHO ON
--获取日期
DEFINE P_DATE=&1


DECLARE
  --sql字符串
  SQL_STR VARCHAR2(2000);
  --用户是否存在，默认为否(0)
  EXISTS_USER NUMBER := 0;
  --表是否存在，默认为否(0)
  EXISTS_TABLE NUMBER := 0;
BEGIN
  --==========================================================================================
  --==========================================================================================
  --查看用户是否存在
  EXISTS_USER := 0;
  SELECT COUNT(1) INTO EXISTS_USER 
    FROM ALL_USERS
   WHERE USERNAME = 'PY_USER';
  
  --用户不存在则创建并授权
  IF EXISTS_USER = 0 THEN
      --创建用户
      EXECUTE IMMEDIATE 'create user py_user identified by py1234567';
      --授予用户创建SESSION的权限，即登陆权限，允许用户登录数据库
      EXECUTE IMMEDIATE 'grant create session to py_user';
      --授予用户使用表空间的权限
      EXECUTE IMMEDIATE 'grant unlimited tablespace to py_user';
      --授权:增删查改
      EXECUTE IMMEDIATE 'grant create any table to py_user';
      EXECUTE IMMEDIATE 'grant drop any table to py_user';
      EXECUTE IMMEDIATE 'grant insert any table to py_user';
      EXECUTE IMMEDIATE 'grant update any table to py_user';
      --授权，包、函数、存储过程
      EXECUTE IMMEDIATE 'grant create any procedure to py_user';
      EXECUTE IMMEDIATE 'grant execute any procedure to py_user';
  END IF;
  
  --==========================================================================================
  --==========================================================================================

  --查看表是否存在
  EXISTS_TABLE := 0;
  SELECT COUNT(1) INTO EXISTS_TABLE
    FROM ALL_TABLES
   WHERE OWNER='PY_USER'
     AND TABLE_NAME = 'T_DOUYU_INFO';
   
  --建分区表：按日期分区，建立在py_user下
  IF EXISTS_TABLE = 0 THEN
    SQL_STR := '
      CREATE TABLE PY_USER.T_DOUYU_INFO(
        DATE_TODAY     DATE,
        ROOM_ID        VARCHAR2(400),
        CLASSIFY_NAME  VARCHAR2(256),
        CHANNEL_NAME   VARCHAR2(256),
        ROOM_NAME      VARCHAR2(256),
        ROOM_URL       VARCHAR2(256),
        ROOM_USER      VARCHAR2(256),
        ROOM_HOT       NUMBER,
        DATE_TIME      DATE
      )
      NOLOGGING
      PARTITION BY RANGE(DATE_TODAY)
      (
        PARTITION P20190226 VALUES LESS THAN (TO_DATE(''2019-02-27 00:00:00'',''YYYY-MM-DD HH24:MI:SS'')),
        PARTITION P20190227 VALUES LESS THAN (TO_DATE(''2019-02-28 00:00:00'',''YYYY-MM-DD HH24:MI:SS''))
      )';
      EXECUTE IMMEDIATE SQL_STR;

      EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_INFO IS ''斗鱼直播热度数据''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.DATE_TODAY IS ''日期''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_ID IS ''直播间ID''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.CLASSIFY_NAME IS ''直播间所属分类''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.CHANNEL_NAME IS ''直播间所属频道''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_NAME IS ''直播间名称''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_URL IS ''直播间url''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_USER IS ''直播间主播名称''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_HOT IS ''直播间热度''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.DATE_TIME IS ''插入时间''';
  END IF;
  
  --创建表当前分区
  PY_USER.COMMON.ADD_PARTITIONS('T_DOUYU_INFO',TO_DATE('&P_DATE','YYYYMMDD'));
  
  --==========================================================================================
  --==========================================================================================
  --创建package-DOUYU_ANALYSIS的日志表
  EXISTS_TABLE := 0;
  SELECT COUNT(1) INTO EXISTS_TABLE
    FROM ALL_TABLES
   WHERE OWNER='PY_USER'
     AND TABLE_NAME = 'T_DOUYU_ANALYSIS_LOG';
     
  IF EXISTS_TABLE = 0 THEN
    SQL_STR := '
      CREATE TABLE PY_USER.T_DOUYU_ANALYSIS_LOG(
      LOG_TIME     TIMESTAMP,
      ORPERATOR    VARCHAR2(64),
      PROC_NAME    VARCHAR2(64),
      LOG_MSG      VARCHAR2(1000)
      )';
    EXECUTE IMMEDIATE SQL_STR;  
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_ANALYSIS_LOG IS ''斗鱼相关数据DOUYU_ANALYSIS日志表''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.LOG_TIME IS ''日志记录时间''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.ORPERATOR IS ''执行者''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.PROC_NAME IS ''存储过程名''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.LOG_MSG IS ''日志信息''';
  END IF;

  --==========================================================================================
  --==========================================================================================
  --创建热度分类表
  EXISTS_TABLE := 0;
  SELECT COUNT(1) INTO EXISTS_TABLE
    FROM ALL_TABLES
   WHERE OWNER='PY_USER'
     AND TABLE_NAME = 'T_DOUYU_CLASSIFY';
     
  IF EXISTS_TABLE = 0 THEN
    SQL_STR := '
      CREATE TABLE PY_USER.T_DOUYU_CLASSIFY(
      DATE_TODAY    DATE,
      CLASSIFY_NAME VARCHAR2(256),
      CHANNEL_NAME  VARCHAR2(256),
      SUM_USER      NUMBER,
      SUM_HOT       NUMBER,
      UP_DATE       DATE
      )';
    EXECUTE IMMEDIATE SQL_STR;
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_CLASSIFY IS ''各分类直播间总数以及总热度''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.DATE_TODAY IS ''日期''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.CLASSIFY_NAME IS ''分类名称''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.CHANNEL_NAME IS ''频道名称''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.SUM_USER IS ''总主播数''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.SUM_HOT IS ''总认读''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.UP_DATE IS ''数据插入时间''';
  END IF;
  
  --==========================================================================================
  --==========================================================================================
  --各频道下主播排行表
  EXISTS_TABLE := 0;
  SELECT COUNT(1) INTO EXISTS_TABLE
    FROM ALL_TABLES
   WHERE OWNER='PY_USER'
     AND TABLE_NAME = 'T_DOUYU_ROOM_RANK';
     
  IF EXISTS_TABLE = 0 THEN
    SQL_STR := '
      CREATE TABLE PY_USER.T_DOUYU_ROOM_RANK(
      DATE_START    DATE,
      DATE_END      DATE,
      DATE_TYPE     VARCHAR2(16),
      CLASSIFY_NAME VARCHAR2(256),
      CLASS_RANK    NUMBER,
      ROOM_USER     VARCHAR2(256),
      SUM_HOT       NUMBER,
      UP_DATE       DATE
      )';
    EXECUTE IMMEDIATE SQL_STR;
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_ROOM_RANK IS ''各频道下主播排行(前10)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_START IS ''开始日期(闭区间)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_END IS ''结束日期(闭区间)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_TYPE IS ''日期类型(日/周/月)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.CLASSIFY_NAME IS ''频道名称''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.CLASS_RANK IS ''直播间在该分类的热度排行''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.ROOM_USER IS ''主播名称''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.SUM_HOT IS ''总热度''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.UP_DATE IS ''数据插入时间''';
  END IF;
  
END;
/

EXIT
