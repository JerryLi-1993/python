create or replace package COMMON is

  -- Author  : JR
  -- Created : 2019/2/26 22:29:20
  -- Purpose : 通用功能
  
  --添加表分区
  PROCEDURE ADD_PARTITIONS(P_TABLE VARCHAR2,P_DATE DATE);

end COMMON;
/
create or replace package body COMMON is

---===========================================================================================
--添加分区： 添加表分区(日期类型),分区名称形如：Pyyyymmdd，如果该分区存在，则不添加。
--    参数： P_TABLE  表名（不需要带用户名）
--           P_DATE   需添加的表分区日期
--    日期： 2018-02-27
--    修改： JR

--  查询表： USER_TAB_PARTITIONS
--  修改表： -
--============================================================================================
PROCEDURE ADD_PARTITIONS(P_TABLE VARCHAR2,P_DATE DATE) IS 
  V_PARTITIONNAME VARCHAR2(120);
  V_ISEXIT NUMBER DEFAULT 0;
  V_SQL VARCHAR2(3000);
  V_PARTITION_DATE VARCHAR2(20);
BEGIN
  V_PARTITIONNAME:='P'||TO_CHAR(P_DATE,'yyyymmdd');
  V_PARTITION_DATE:=TO_CHAR(P_DATE+1,'yyyy-mm-dd');
  
  --检查表是否存在
  SELECT COUNT(1) INTO V_ISEXIT FROM USER_TAB_PARTITIONS P 
   WHERE P.TABLE_NAME=P_TABLE
     AND P.PARTITION_NAME=V_PARTITIONNAME;
     
  IF V_ISEXIT = 0 THEN 
    V_SQL := 'alter table ' || P_TABLE || ' add partition ' || V_PARTITIONNAME ||
                  ' VALUES LESS THAN ( to_date(''' || V_PARTITION_DATE || ''',''yyyy-mm-dd'') ) ';
    EXECUTE IMMEDIATE V_SQL;
    --DBMS_OUTPUT.PUT_LINE(V_SQL);
  END IF;

END ADD_PARTITIONS;

end COMMON;
/
