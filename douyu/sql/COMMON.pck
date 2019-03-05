create or replace package COMMON is

  -- Author  : JR
  -- Created : 2019/2/26 22:29:20
  -- Purpose : ͨ�ù���
  
  --��ӱ����
  PROCEDURE ADD_PARTITIONS(P_TABLE VARCHAR2,P_DATE DATE);

end COMMON;
/
create or replace package body COMMON is

---===========================================================================================
--��ӷ����� ��ӱ����(��������),�����������磺Pyyyymmdd������÷������ڣ�����ӡ�
--    ������ P_TABLE  ����������Ҫ���û�����
--           P_DATE   ����ӵı��������
--    ���ڣ� 2018-02-27
--    �޸ģ� JR

--  ��ѯ�� USER_TAB_PARTITIONS
--  �޸ı� -
--============================================================================================
PROCEDURE ADD_PARTITIONS(P_TABLE VARCHAR2,P_DATE DATE) IS 
  V_PARTITIONNAME VARCHAR2(120);
  V_ISEXIT NUMBER DEFAULT 0;
  V_SQL VARCHAR2(3000);
  V_PARTITION_DATE VARCHAR2(20);
BEGIN
  V_PARTITIONNAME:='P'||TO_CHAR(P_DATE,'yyyymmdd');
  V_PARTITION_DATE:=TO_CHAR(P_DATE+1,'yyyy-mm-dd');
  
  --�����Ƿ����
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
