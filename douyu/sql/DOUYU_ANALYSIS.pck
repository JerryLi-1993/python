create or replace package DOUYU_ANALYSIS is

  -- Author  : JR
  -- Created : 2019/2/27 10:27:09
  -- Purpose : 斗鱼相关数据分析
  
  -- 执行
  PROCEDURE PRO_EXEC(I_DATE DATE);

  
end DOUYU_ANALYSIS;
/
create or replace package body DOUYU_ANALYSIS is

--更新日期
V_UPDATETIME VARCHAR2(64);

--错误信息
V_MSG VARCHAR2(1000);

---===========================================================================================
--  说明：记录存储过程名、调用者信息、类型、以及相应的信息
--  日期：2018-02-27
--  修改：JR

--查询表：-
--修改表：T_DOUYU_ANALYSIS_LOG
--============================================================================================
PROCEDURE PRO_DOUYU_ANALYSIS_LOG(I_MSG VARCHAR2) IS
PRAGMA AUTONOMOUS_TRANSACTION;
  V_PROC_NAME   VARCHAR2(128);
  V_OPERATOR    VARCHAR2(64);
  V_OWNER       VARCHAR2(64);
  V_NAME        VARCHAR2(64);
  V_LINENO      NUMBER;
  V_TYPE        VARCHAR2(64);
BEGIN
  OWA_UTIL.WHO_CALLED_ME(V_OWNER,V_NAME,V_LINENO,V_TYPE);
  V_PROC_NAME := V_OWNER||'.'||V_NAME||'.'||V_TYPE||'.'||V_LINENO;
  V_OPERATOR  := SYS_CONTEXT('USERENV','CURRENT_USER') ;
  INSERT INTO T_DOUYU_ANALYSIS_LOG(LOG_TIME,ORPERATOR,PROC_NAME,LOG_MSG)
          VALUES(SYSTIMESTAMP,V_OPERATOR,V_PROC_NAME,I_MSG);
  COMMIT;
END PRO_DOUYU_ANALYSIS_LOG;


---===========================================================================================
--  过程：每日各分类直播间总数以及总热度
--  参数：I_DATE 数据日期
--  日期：2018-02-27
--  修改：JR

--查询表：T_DOUYU_INFO
--修改表：T_DOUYU_CLASSIFY
--============================================================================================
PROCEDURE PRO_DOUYU_CLASSIFY(I_DATE DATE)
IS 
V_DATE DATE := I_DATE;  --数据日期
BEGIN
V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_DOUYU_CLASSIFY START,UPDATE TIME:'||V_UPDATETIME);

INSERT INTO T_DOUYU_CLASSIFY NOLOGGING
     SELECT TRUNC(V_DATE) AS DATE_TODAY,
            NVL(T.CLASSIFY_NAME,'-') AS CLASSIFY_NAME,
            NVL(T.CHANNEL_NAME,'-') AS CHANNEL_NAME,
            COUNT(1) AS SUM_USER,
            SUM(NVL(T.ROOM_HOT,0)) AS SUM_HOT,
            SYSDATE AS UP_DATE
       FROM T_DOUYU_INFO T
      WHERE T.DATE_TODAY = TRUNC(V_DATE)
        AND T.CHANNEL_NAME NOT IN ('心悦大咖秀')
   GROUP BY GROUPING SETS((),(T.CLASSIFY_NAME),(T.CLASSIFY_NAME,T.CHANNEL_NAME))
;
COMMIT;

V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_DOUYU_CLASSIFY INSERT COMMIT,UPDATE TIME:'||V_UPDATETIME);
EXCEPTION
  WHEN OTHERS THEN
    V_MSG := 'PRO_DOUYU_CLASSIFY---SQLERRM:'||SQLERRM;
    PRO_DOUYU_ANALYSIS_LOG(V_MSG);
    ROLLBACK;
END PRO_DOUYU_CLASSIFY;


---===========================================================================================
--  过程：每日各分类下主播的排行
--  参数：I_DATE_START 数据开始日期
--        I_DATE_END   数据结束日期
--  日期：2018-02-27
--  修改：JR

--查询表：T_DOUYU_INFO
--修改表：T_DOUYU_ROOM_RANK
--============================================================================================
PROCEDURE PRO_DOUYU_ROOM_RANK(I_DATE_START DATE,I_DATE_END DATE,I_DATE_TYPE VARCHAR2)
IS 
V_DATE_START DATE         := I_DATE_START;  --数据开始日期
V_DATE_END   DATE         := I_DATE_END;    --数据结束日期
V_DATE_TYPE  VARCHAR2(16) := I_DATE_TYPE;   --日期类型
BEGIN
V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_DOUYU_ROOM_RANK-'||V_DATE_TYPE||' START,UPDATE TIME:'||V_UPDATETIME);

INSERT INTO T_DOUYU_ROOM_RANK NOLOGGING
     SELECT TRUNC(V_DATE_START),TRUNC(V_DATE_END),V_DATE_TYPE,
            CLASSIFY_NAME,CLASS_RANK,ROOM_USER,SUM_HOT,SYSDATE AS UP_DATE
       FROM (
         SELECT T.CLASSIFY_NAME,
                RANK()OVER(PARTITION BY T.CLASSIFY_NAME ORDER BY SUM(T.ROOM_HOT) DESC) AS CLASS_RANK,
                T.ROOM_USER,
                SUM(T.ROOM_HOT) AS SUM_HOT
           FROM T_DOUYU_INFO T
          WHERE T.DATE_TODAY >= TRUNC(V_DATE_START)
            AND T.DATE_TODAY <= TRUNC(V_DATE_END)
            AND NVL(T.ROOM_HOT,0) <> 0
       GROUP BY T.CLASSIFY_NAME,T.ROOM_ID,T.ROOM_USER
     )TB
      WHERE TB.CLASS_RANK <= 10
;
COMMIT;

V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_DOUYU_ROOM_RANK-'||V_DATE_TYPE||' INSERT COMMIT,UPDATE TIME:'||V_UPDATETIME);
EXCEPTION
  WHEN OTHERS THEN
    V_MSG := 'PRO_DOUYU_ROOM_RANK-'||V_DATE_TYPE||'---SQLERRM:'||SQLERRM;
    PRO_DOUYU_ANALYSIS_LOG(V_MSG);
    ROLLBACK;
END PRO_DOUYU_ROOM_RANK;


---===========================================================================================
--  过程：执行过程
--  参数：I_DATE  数据日期
--  日期：2018-02-27
--  修改：JR

--查询表：-
--修改表：-
--============================================================================================
PROCEDURE PRO_EXEC(I_DATE DATE)
IS 
V_DATE        DATE  := I_DATE;         --数据日期
V_DATE_BEGIN  DATE  := I_DATE;         --数据开始日期
V_DATE_END    DATE  := I_DATE;         --数据结束日期
V_DATE_TYPE   VARCHAR2(16) := 'DAILY'; --日期类型
BEGIN
V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_EXEC START,UPDATE TIME:'||V_UPDATETIME);

--==================================================================
--1. 执行过程PRO_DOUYU_CLASSIFY：每日各分类直播间总数以及总热度
PRO_DOUYU_CLASSIFY(V_DATE);

--==================================================================
--2. 执行过程PRO_DOUYU_ROOM_RANK：每日各分类直播间总数以及总热度
     --I_DATE_TYPE 类型：
       --日：每天执行
       --周：每个星期一，执行上星期一到星期天的数据
       --月：每个月2号，执行上个月的数据
--每日
PRO_DOUYU_ROOM_RANK(V_DATE_BEGIN,V_DATE_END,V_DATE_TYPE);
--每周
IF TRIM(TO_CHAR(V_DATE,'day','NLS_DATE_LANGUAGE=AMERICAN')) = 'monday' THEN
  V_DATE_BEGIN := V_DATE - 7;  --上个星期一
  V_DATE_END   := V_DATE - 1;  --上个星期天
  V_DATE_TYPE  := 'WEEKLY';
  PRO_DOUYU_ROOM_RANK(V_DATE_BEGIN,V_DATE_END,V_DATE_TYPE);
END IF ;
--每月
IF TO_CHAR(V_DATE,'DD') = '02' THEN
  V_DATE_BEGIN := ADD_MONTHS(TRUNC(V_DATE),-1);           --上个月第一天
  V_DATE_END   := LAST_DAY(ADD_MONTHS(TRUNC(V_DATE),0));  --上个月最后一天
  V_DATE_TYPE  := 'MONTHLY';
  PRO_DOUYU_ROOM_RANK(V_DATE_BEGIN,V_DATE_END,V_DATE_TYPE);
END IF;

V_UPDATETIME := TO_CHAR(SYSTIMESTAMP, 'YYYY-MM-DD HH24:MI:SS.FF');
PRO_DOUYU_ANALYSIS_LOG('PRO_EXEC INSERT COMMIT,UPDATE TIME:'||V_UPDATETIME);
EXCEPTION
  WHEN OTHERS THEN
    V_MSG := 'PRO_EXEC---SQLERRM:'||SQLERRM;
    PRO_DOUYU_ANALYSIS_LOG(V_MSG);
    ROLLBACK;
END PRO_EXEC;

end DOUYU_ANALYSIS;
/
