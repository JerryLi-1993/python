--��Ļ���
SET SERVEROUTPUT ON 
--������ for test
--SET ECHO ON
--��ȡ����
DEFINE P_DATE=&1


DECLARE
  --sql�ַ���
  SQL_STR VARCHAR2(2000);
  --�û��Ƿ���ڣ�Ĭ��Ϊ��(0)
  EXISTS_USER NUMBER := 0;
  --���Ƿ���ڣ�Ĭ��Ϊ��(0)
  EXISTS_TABLE NUMBER := 0;
BEGIN
  --==========================================================================================
  --==========================================================================================
  --�鿴�û��Ƿ����
  EXISTS_USER := 0;
  SELECT COUNT(1) INTO EXISTS_USER 
    FROM ALL_USERS
   WHERE USERNAME = 'PY_USER';
  
  --�û��������򴴽�����Ȩ
  IF EXISTS_USER = 0 THEN
      --�����û�
      EXECUTE IMMEDIATE 'create user py_user identified by py1234567';
      --�����û�����SESSION��Ȩ�ޣ�����½Ȩ�ޣ������û���¼���ݿ�
      EXECUTE IMMEDIATE 'grant create session to py_user';
      --�����û�ʹ�ñ�ռ��Ȩ��
      EXECUTE IMMEDIATE 'grant unlimited tablespace to py_user';
      --��Ȩ:��ɾ���
      EXECUTE IMMEDIATE 'grant create any table to py_user';
      EXECUTE IMMEDIATE 'grant drop any table to py_user';
      EXECUTE IMMEDIATE 'grant insert any table to py_user';
      EXECUTE IMMEDIATE 'grant update any table to py_user';
      --��Ȩ�������������洢����
      EXECUTE IMMEDIATE 'grant create any procedure to py_user';
      EXECUTE IMMEDIATE 'grant execute any procedure to py_user';
  END IF;
  
  --==========================================================================================
  --==========================================================================================

  --�鿴���Ƿ����
  EXISTS_TABLE := 0;
  SELECT COUNT(1) INTO EXISTS_TABLE
    FROM ALL_TABLES
   WHERE OWNER='PY_USER'
     AND TABLE_NAME = 'T_DOUYU_INFO';
   
  --�������������ڷ�����������py_user��
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

      EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_INFO IS ''����ֱ���ȶ�����''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.DATE_TODAY IS ''����''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_ID IS ''ֱ����ID''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.CLASSIFY_NAME IS ''ֱ������������''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.CHANNEL_NAME IS ''ֱ��������Ƶ��''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_NAME IS ''ֱ��������''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_URL IS ''ֱ����url''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_USER IS ''ֱ������������''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.ROOM_HOT IS ''ֱ�����ȶ�''';
      EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_INFO.DATE_TIME IS ''����ʱ��''';
  END IF;
  
  --������ǰ����
  PY_USER.COMMON.ADD_PARTITIONS('T_DOUYU_INFO',TO_DATE('&P_DATE','YYYYMMDD'));
  
  --==========================================================================================
  --==========================================================================================
  --����package-DOUYU_ANALYSIS����־��
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
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_ANALYSIS_LOG IS ''�����������DOUYU_ANALYSIS��־��''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.LOG_TIME IS ''��־��¼ʱ��''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.ORPERATOR IS ''ִ����''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.PROC_NAME IS ''�洢������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ANALYSIS_LOG.LOG_MSG IS ''��־��Ϣ''';
  END IF;

  --==========================================================================================
  --==========================================================================================
  --�����ȶȷ����
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
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_CLASSIFY IS ''������ֱ���������Լ����ȶ�''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.DATE_TODAY IS ''����''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.CLASSIFY_NAME IS ''��������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.CHANNEL_NAME IS ''Ƶ������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.SUM_USER IS ''��������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.SUM_HOT IS ''���϶�''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_CLASSIFY.UP_DATE IS ''���ݲ���ʱ��''';
  END IF;
  
  --==========================================================================================
  --==========================================================================================
  --��Ƶ�����������б�
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
    
    EXECUTE IMMEDIATE 'COMMENT ON TABLE PY_USER.T_DOUYU_ROOM_RANK IS ''��Ƶ������������(ǰ10)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_START IS ''��ʼ����(������)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_END IS ''��������(������)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.DATE_TYPE IS ''��������(��/��/��)''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.CLASSIFY_NAME IS ''Ƶ������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.CLASS_RANK IS ''ֱ�����ڸ÷�����ȶ�����''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.ROOM_USER IS ''��������''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.SUM_HOT IS ''���ȶ�''';
    EXECUTE IMMEDIATE 'COMMENT ON COLUMN PY_USER.T_DOUYU_ROOM_RANK.UP_DATE IS ''���ݲ���ʱ��''';
  END IF;
  
END;
/

EXIT
