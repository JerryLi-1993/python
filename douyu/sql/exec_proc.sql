--��Ļ���
SET SERVEROUTPUT ON 
--������ for test
--SET ECHO ON
--��ȡ����
DEFINE P_DATE=&1


BEGIN
  --ִ����ع���
  DOUYU_ANALYSIS.PRO_EXEC(TO_DATE('&P_DATE','YYYYMMDD'));
END;
/

EXIT
