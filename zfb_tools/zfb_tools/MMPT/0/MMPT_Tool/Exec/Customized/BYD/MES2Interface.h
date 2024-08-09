
#ifdef Data_API
#else
#define Data_API extern "C" _declspec(dllimport)
#endif

/************************************************************************************
������	Start
���ܣ�	��ָ����λ�á���SFCִ��Start����(CHECK������Ϣ)
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShoporder[]		Shoporder��������
		parOPERATION[]		OPERATION����վ��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻ط�1,����2��ʾ�Ѿ�������ǰ��վ
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Start (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	Complete
���ܣ�	��ָ����λ�á���SFCִ��Complete����
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShoporder[]		Shoporder��������
		parOPERATION[]		OPERATION����վ��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Complete (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	NC_Complete
���ܣ�	��ָ����λ�á���SFCִ��NC_Complete����
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShopOrder[]		����
		parOPERATION[]	OPERATION����վ��
		parNC_Tpye			��������
		parCOMMENTS[]		ע��
		parNC_CODE		�������
		parFailItem			������
		parFailValue		����ֵ
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int NC_Complete (char parSFC[], char parSITE[], char parShopOrder[], 
										char parOPERATION[],char parNC_Tpye[], char parCOMMENTS[], 
										char parNC_CODE[],char parFailItem[],char parFailValue[], char parUSER[], char parPASSWORD[], 
										char *retMessage);

/************************************************************************************
������	Split_Start
���ܣ�	��ָ����λ�á������л�ǰSFCִ��Start����(CHECK������Ϣ)
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShoporder[]		Shoporder��������
		parOPERATION[]		OPERATION����վ��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻ط�1,����2��ʾ�Ѿ�������ǰ��վ
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Split_Start (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	Split_Complete
���ܣ�	��ָ����λ�á���SFCִ��Complete����
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShoporder[]		Shoporder��������
		parOPERATION[]		OPERATION����վ��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Split_Complete (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	Split_NC_Complete
���ܣ�	��ָ����λ�á���SFCִ��NC_Complete����
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parShopOrder[]		����
		parOPERATION[]	OPERATION����վ��
		parNC_Tpye			��������
		parCOMMENTS[]		ע��
		parNC_CODE		�������
		parFailItem			������
		parFailValue		����ֵ
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Split_NC_Complete (char parSFC[], char parSITE[], char parShopOrder[], 
										char parOPERATION[],char parNC_Tpye[], char parCOMMENTS[], 
										char parNC_CODE[],char parFailItem[],char parFailValue[], char parUSER[], char parPASSWORD[], 
										char *retMessage);


/************************************************************************************
������	GetNumberbySFC
���ܣ�	ͨ��SFC������루��ͬ�ġ���Ŀ���ơ��͡������š����䲻ͬ���µĺ��룩
������
		parSFC[]			SFC
		parSITE[]			�����Ϻ�
		parSTORE[]			���������ơ����������꣬�˴�Ҳ�ɴ������꣩SN��IMEI1,IMEI2��BT��WIFI,KEYBOX, LUCKY,Battery
		parMODEL[]			��Ҫ����ĺ��������Ǹ���MODEL����
		parUSER[]			������Ա
		parPASSWORD[]		������Ա������
		*retMessage			���ص���Ϣ��IMEI:111111111111119;IMEI2:111111111111127��
							��SN:1234��
							��IMEI:1234��
							��IMEI2:1234��
							��BTAddress:1234��
							��Wifi:1234��
							��Battery:1234��
							��DEVICE:%s;KEY:%s;ID:%s;MAGIC:%s;CRC:%s��
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��  
************************************************************************************/
//*
Data_API int GetNumberbySFC (char parSFC[], char parSITE[], char parSTORE[], char parMODEL[], char parUSER[], char parPASSWORD[],char noQty[], char *retMessage);

/************************************************************************************
������	GetDatabyShoporder
���ܣ�	ͨ�����������Ŀ�͹������Զ�������
������
		parShopOrder			���������룩
		maxCount				����������������
		getSITE					��Ŀ�Ϻţ�������
		retMessage		���ص���Ϣ���Զ�������:�Զ�����ֵ;SN:111;��
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int GetDatabyShoporder(char parShopOrder[],char *maxCount,char *getSITE,char *retMessage);

/************************************************************************************
������	GetDatabyStationName
���ܣ�	�õ���վ���Զ�������
������
		parOPERATION[]		OPERATION����վ��
		parSITE[]			�����Ϻ�
		*retMessage		���ص���Ϣ
���أ�	�������1 �����򷵻�0 
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
Data_API int GetDatabyStationName(char parOPERATION[], char parSITE[],char *retMessage);

/************************************************************************************
������	SerializeSFC
���ܣ�	PSN ���л�Ϊ BSN
������
		parSITE[]			�����Ϻ�
		parSFC[]			SFC
		parNEWSFC[]			parNEWSFC ����SFC��sfc1;sfc2;sfc3
		parShoporder[]		Shoporder��������
		parOPERATION[]		OPERATION����վ��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ PASS
���أ�	return 1;
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
Data_API int SerializeSFC (char parSITE[], char parSFC[], char parNEWSFC[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	Data_Collect
���ܣ�	����Ҫ�ռ������ݷ���MES����������
������
		parSITE[]			�����Ϻ�
		parSFC[]			SFC
		parREPEATFlag		�����Ƿ���ظ�   
		parDC_REVISION		�����ռ���汾�� 
		parShopOrder		����
		parRESOURCE[]		��Դ             
		parOPERATION[]		�����ռ���վ��
		parDATA				�����ϵͳԤ����Ĺ�վ���ƣ����ݣ���ʽ��ֵ|ֵ|ֵ���� �Զ��幤վ���ƣ����ݣ���ʽ��NAME:VALUE;NAME:VALUE;NAME:VALUE��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int Data_Collect (char parSITE[], char parSFC[], char parREPEATFlag[], char parDC_REVISION[], char parShoporder[], char parRESOURCE[], char parOPERATION[], char parDATA[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
������	CreateNumberbySFC
���ã�	���� sendDataByPost()
		ȫ�ֱ��� pub_SecURL
		ȫ�ֱ��� pub_LOGON_INFO
���ܣ�	ͨ��SFC�������루��ͬ�ġ�SITE���͡�NUMBER_STORE��������ͬ���͵ĺ��룩
������
		parSFC			SFC
		parSITE			SITE
		parSTORE		���������ơ�
		parMODEL		��Ҫ����ĺ��������Ǹ���MODEL�������û�У��봫�����ַ���������
		parHOW			Ҫ�����ĺ�������
		parUSER			������Ա
		parPASSWORD		������Ա������
		retMessage		���ص���Ϣ��SFC:0902140001;MEID:111;AKEY1:222;AKEY2:333;BT:444��
���أ�	����ɹ��򷵻�true�����򷵻�false
���ߣ�	BYD �Ų� ��Ϣϵͳ�� ���� 2015��06��16��
************************************************************************************/

Data_API int CreateNumberbySFC (char parSFC[], char parShoporder[], char parSTORE[], char parMODEL[], char parHOW[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	QueryData_Collect
���ã�	���� sendDataByPost()
		ȫ�ֱ��� pub_SecURL
		ȫ�ֱ��� pub_LOGON_INFO
���ܣ�	��MES�в�ѯ֮ǰ�á�Data_Collect���ռ�����Ϣ��
������
		parSITE[]			�����Ϻ�
		parSFC[]			SFC
		parDC_GROUP		�����ռ�������
		parDC_REVISION	�����ռ���汾��
		parQueryDATA	��Ҫ��ѯ�����ݣ���ʽ��<���ݿ�����>:<ֵ>|<���ݿ�����>:<ֵ>|<���ݿ�����>:<ֵ>|...����
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�true�����򷵻�false
���ߣ�	BYD �Ų� ��Ϣϵͳ�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int QueryData_Collect (char parSITE[], char parSFC[], char parDC_GROUP[], char parDC_REVISION[], char *parQueryDATA, char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	GetDatabySFC
���ܣ�	��ȡָ��SFC����Ӧ�Ĺ������Զ�������
������
		parSFC[]			SFC
		parSITE[]			SITE
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/
//*
Data_API int GetDatabySFC (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	GetSFCInfo
���ܣ�	��ȡָ��SFC����Ӧ����Ϣ
������
		parSFC[]			SFC
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/

Data_API int GetSFCInfo (char parSFC[], char *retMessage);

Data_API bool BYDTD_COLLECT(char parstrSFC[],char parstrShoporder[],char parstrPF[],char parstrNCCode[],char parstrFailItem[],char parstrFailValue[],char *retMessage);

/************************************************************************************
������	BYDTD_COLLECT_TXT
���ܣ�	������־�ϴ� TXT ��
������
		parstrShoporder			������
		parTEST_FILE			TXT�ļ�·��
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/

Data_API bool BYDTD_COLLECT_TXT (char parstrShoporder[], char parTEST_FILE[], char *retMessage);

/************************************************************************************
������	BYDTD_COLLECT_XML
���ܣ�	������־�ϴ� XML ��
������
		parstrShoporder			������
		parTEST_CONT			XML�ļ�����
		parTEST_FILE			XML�ļ�·��
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2015��06��16��
************************************************************************************/

Data_API bool BYDTD_COLLECT_XML  (char parstrShoporder[], char parTEST_CONT[], char parTEST_FILE[], char *retMessage);

/************************************************************************************
������	MESinterface_GetServerDateTime_Link
���ܣ�	��ȡ������ʱ�� _ ���Զ��������ݿ�Ķ���
������
		parSITE[]			�����Ϻ�
		parFOTMAT		���ڸ�ʽ������yyyy-MM-dd HH:mm:ss��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ ������ɹ�����ô���ع����ţ�
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2011��06��17��
************************************************************************************/
//*
Data_API int MESinterface_GetServerDateTime_Link (char parSITE[], char parFOTMAT[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	GetServerDateTime_Link
���ܣ�	��ȡ������ʱ�� _ ���Զ��������ݿ�Ķ���
������
		parSITE[]			�����Ϻ�
		parFOTMAT		���ڸ�ʽ������yyyy-MM-dd HH:mm:ss��
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ ������ɹ�����ô���ع����ţ�
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2011��06��17��
************************************************************************************/
//*
Data_API int GetServerDateTime_Link (char parSITE[], char parFOTMAT[], char parUSER[], char parPASSWORD[], char *retMessage);

Data_API int MESinterface_GetSFCState (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);
Data_API int GetSFCState (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);


Data_API int GetCustomData(char parSFC[], char *retMessage);

/************************************************************************************
������	GetSFCKeybyStationName
���ܣ�	��ȡ��ǰ��վ��ǰ������Ҫ�󶨵�KEY��Ϣ
������
		parSFC[]			SFC
		parstrStationName[]			��վ����
		parstrShoporder[]			������
		parSITE[]			SITE
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2016��01��27��
************************************************************************************/
//*
Data_API int GetSFCKeybyStationName (char parSFC[],char parstrStationName[],char parstrShoporder[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
������	Getnumberinfo
���ܣ�	��ȡ���������Ϣ
������
		parNUMBER_STORE[]   �����
		parNUMBER[]			����
		parUSER[]			������Ա��MES�ʺţ�
		parPASSWORD[]		������Ա�����루MES�ʺ����룩
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� xlf 2016��09��06��
************************************************************************************/
//*
Data_API int Getnumberinfo (char parNUMBER_STORE[], char parNUMBER[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
������	GetNumberbySFCNew 3
���ܣ�	ͨ��SFC������루��ͬ�ġ���Ŀ���ơ��͡������š����䲻ͬ���µĺ��룩
������
		parSFC[]			SFC
		parShoporder[]		������
		parSTORE[]			���������ơ����������꣬�˴�Ҳ�ɴ������꣩SN��IMEI1,IMEI2��BT��WIFI,KEYBOX, LUCKY,Battery
		parNUMBER[]         ����
		parMODEL[]			��Ҫ����ĺ��������Ǹ���MODEL����
		parUSER[]			������Ա
		parPASSWORD[]		������Ա������
		*retMessage			���ص���Ϣ��IMEI:111111111111119;IMEI2:111111111111127��
							��SN:1234��
							��IMEI:1234��
							��IMEI2:1234��
							��BTAddress:1234��
							��Wifi:1234��
							��Battery:1234��
							��DEVICE:%s;KEY:%s;ID:%s;MAGIC:%s;CRC:%s��
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� xlf 2016��09��07��  
************************************************************************************/
Data_API int GetNumberbySFCNew (char parSFC[], char parShoporder[], char parSTORE[], char parNUMBER[], char parMODEL[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
������	ReworkToStation
���ܣ�	SFC������ĳ��վ
������
		parStation_NAME[]   ����Ŀ�Ĺ�վ
		parSFC[]		  SFC
		parREMARK[]		  ����ԭ��
		*retMessage		 ���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� Τ�ɺ� 2016��10��20��
************************************************************************************/
//*
Data_API int ReworkToStation (char parStation_NAME[], char parSFC[], char parREMARK[], char *retMessage);

/************************************************************************************
������	RemoveSFCKey
���ܣ�	�ؼ����Ͻ��
������
parStation_NAME[]   ����󶨹�վ������
parSFC[]		  SFC		����󶨵�SFC
parstrDataName[]		  ����ĸ��������ƣ��ɴ��գ���Ϊ��ǰ��վ���и�����
*retMessage		 ���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ���� 2017��03��08��
************************************************************************************/
//*
Data_API int RemoveSFCKey(char parStation_NAME[], char parSFC[], char parstrDataName[], char *retMessage);

Data_API bool StationJumpJudge(char sfc[],char parStationName[], char strTYPE[],char *refstrMessage);

/************************************************************************************
������	AddTestLogInfo
���ܣ�	����������־��Ϣ
������
		sfc[]		        SFC
		reslut[]            ���Խ�� 0ʧ�� 1�ɹ�
		testTime[]          ����ʱ�䣬��ʽ yyyy-MM-dd HH:mm:ss
		fullFileName[]      �ļ�����·��
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
************************************************************************************/
Data_API bool AddTestLogInfo(char sfc[],char reslut[], char testTime[],char fullFileName[],char *refstrMessage);

/************************************************************************************
������	ReplaceSfcSubKey
���ܣ�	�滻�ؼ�����������
������
parSFC[]		SFC		�滻�ؼ����������ϵ�SFC
parOldValue[]   �󶨵ľ�ֵ
parNewValue[]	�滻�����ֵ
parNewBydPn[]	�滻��������Ϻ�(��ѡ,Ϊ�ղ��޸��Ϻ�)
*retMessage		���صĴ���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��03��10��
************************************************************************************/
Data_API int ReplaceSfcSubKey(char parSFC[], char parOldValue[], char parNewValue[], char parNewBydPn[], char *retMessage);

/************************************************************************************
������	GetStationCheckConfig
���ܣ�	��ȡ��վУ��ȶ�������Ϣ�б�
������
parSFC[]		SFC		��ȡ��վУ��ȶ�������Ϣ�б��SFC
*retData		���صĹ�վУ��ȶ�������Ϣ�б���Ϣ����ʽ�ǣ��б�ĸ�����¼֮���ԡ�|���ָһ����¼�в�ͬ����Ϣ�ԡ�,��������
		���磺RULE:У�����,CHECK_TYPE:У������(0ɨ�����������ȶԣ�1ɨ�������ؼ����ϱȶԣ�2ɨ����������л�ǰ����ȶԣ�3ɨ��������Զ������ݱȶԣ�4ɨ�������ɨ�����ȶ�),PARAM1:����һ(0����⣬1�������ƣ�3�Զ�����������),PARAM2:������(0 Model��1�������ƣ�3�Զ�����������),PARAM3:������(0�������ƣ�1�������ƣ�3�Զ�����������),SCAN_COUNT:��Ҫɨ��Ĵ���(1��5),SCAN_MESSAGE:ɨ��ʱ��ʾ������(���������á�;���Ÿ���)|����
*retMessage		���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��03��10��
************************************************************************************/
Data_API int GetStationCheckConfig(char parSFC[], char *retData, char *retMessage);

#pragma region �Ż���Ľӿ�

/************************************************************************************
������	GetServerTime_New
���ܣ�	��ȡ������ʱ��
������
		*retServerTime	���ط�����ʱ��
		*retMessage		���ص���Ϣ ������ɹ�����ô���ع����ţ�
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int GetServerTime_New(char *retServerTime, char *retMessage);

/************************************************************************************
������	GetSFCInfo_New
���ܣ�	��ȡָ��SFC����Ӧ����Ϣ
������
		parSFC[]		SFC
		*retSFCInfo		����SFC��Ϣ����ʽΪ������1:ֵ1;����;����n:ֵn��
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int GetSFCInfo_New(char parSFC[], char *retSFCInfo, char *retMessage);

/************************************************************************************
������	GetStationCheckConfig_New
���ܣ�	��ȡ��վУ��ȶ�������Ϣ�б�
������
		parSFC[]				��ȡ��վУ��ȶ�������Ϣ�б��SFC
		*retCheckConfigData		���ع�վУ��ȶ�������Ϣ�б���ʽ�ǡ�RULE:У�����,CHECK_TYPE:У������,PARAM1:����һ,PARAM2:������,PARAM3:������,SCAN_COUNT:��Ҫɨ��Ĵ���(1��5),SCAN_MESSAGE:ɨ��ʱ��ʾ������|����|RULE:У�����,CHECK_TYPE:У������,PARAM1:����һ,PARAM2:������,PARAM3:������,SCAN_COUNT:��Ҫɨ��Ĵ���(1��5),SCAN_MESSAGE:ɨ��ʱ��ʾ�����ݡ�
		*retMessage				���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��26��
************************************************************************************/
Data_API int GetStationCheckConfig_New(char parSFC[], char *retCheckConfigData, char *retMessage);

/************************************************************************************
������	GetOnLineStationListByShoporder_New
���ܣ�	���ݹ�����ȡ���ڹ���·�ߵ����߹�վ��Ϣ�б�
������
		parShoporder[]	����
		*retStations	�������߹�վ��Ϣ�б���ʽ�ǡ�ID:��վID,NAME:��վ����|����|ID:��վID,NAME:��վ���ơ�
		*retMessage		���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��10��26��
************************************************************************************/
Data_API int GetOnLineStationListByShoporder_New(char parShoporder[], char *retStations, char *retMessage);

/************************************************************************************
������	GetCustomDatabyShoporder_New
���ܣ�	ͨ�����������Ŀ����Ʒ�������Ϻţ��͹������Զ�������
������
		*retCustomData		�ɹ�ʱ���ص��Զ������ݣ���ʽΪ�����ơ�ֵ������|����|���ơ�ֵ����������
		*retMessage			ʧ��ʱ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
��ע��	��������Ʒ�������Ϻţ�ID����ĿID��\cfg\mes_config.ini�ļ��е�Resource��PRODUCT_ID��PROJECT_ID�л�ȡ
************************************************************************************/
Data_API int GetCustomDatabyShoporder_New(char *retCustomData, char *retMessage);

/************************************************************************************
������	GetCustomDatabyProduct_New
���ܣ�	ͨ����Ʒ�������Ϻţ����Զ�������
������
		*retCustomData		�ɹ�ʱ���ص��Զ������ݣ���ʽΪ�����ơ�ֵ������|����|���ơ�ֵ����������
		*retMessage			ʧ��ʱ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��05��23��
��ע��	��Ʒ�������Ϻţ�ID��\cfg\mes_config.ini�ļ��е�PRODUCT_ID�л�ȡ
************************************************************************************/
Data_API int GetCustomDatabyProduct_New(char *retCustomData, char *retMessage);

/************************************************************************************
������	GetCustomDatabyStation_New
���ܣ�	��ȡ��վ�Զ�������
������
		*retCustomData		�ɹ�ʱ���ص��Զ������ݣ���ʽΪ�����ơ�ֵ������|����|���ơ�ֵ����������
		*retMessage			ʧ��ʱ���صĴ�����Ϣ
���أ�	�������1 �����򷵻�0 
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
��ע��	��վID��\cfg\mes_config.ini�ļ��е�StationID�л�ȡ
************************************************************************************/
Data_API int GetCustomDatabyStation_New(char *retCustomData, char *retMessage);

/************************************************************************************
������	GetCustomDatabySFC_New
���ܣ�	��ȡָ��SFC����Ӧ�Ĺ������Զ�������
������
		parSFC[]		SFC
		*retCustomData	�ɹ�ʱ���ص��Զ������ݣ���ʽΪ�����ơ�ֵ������|����|���ơ�ֵ����������
		*retMessage		ʧ��ʱ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
************************************************************************************/
Data_API int GetCustomDatabySFC_New(char parSFC[], char *retCustomData, char *retMessage);

/************************************************************************************
������	GetCustomData_New
���ܣ�	��ȡ�Զ�������(��վ����/����վSFC+��վ�Զ�������)
������
		parSFC[]			SFC
		*retCustomData		�ɹ�ʱ���ص��Զ������ݣ���ʽΪ�����ơ�ֵ������|����|���ơ�ֵ����������
		*retMessage			ʧ��ʱ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int GetCustomData_New(char parSFC[], char *retCustomData, char *retMessage);

/************************************************************************************
������	Start_New
���ܣ�	��ָ����λ�á���SFCִ��Start����(CHECK������Ϣ)
������
		parSFC[]			SFC
		parBoardCount[]		�ְ�����(��ѡ����ѡ��NULL)
		parWorkStation[]	��λ(��ѡ����ѡ��NULL)
		parLogOperation[]	�豸����������SMT����ţ���ѡ����ѡ��NULL)
		parLogResource[]	��Դ���ƣ��оߣ���ѡ����ѡ��NULL)
		parRemark[]			��ע(��ѡ����ѡ��NULL)
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
************************************************************************************/
Data_API int Start_New(char parSFC[], char parBoardCount[], char parWorkStation[], char parLogOperation[], char parLogResource[], char parRemark[], char *retMessage);

/************************************************************************************
������	Complete_New
���ܣ�	��ָ����λ�á���SFCִ��Complete����
������
		parSFC[]				SFC
		parBoardCount[]			�ְ�����(��ѡ����ѡ��NULL)
		parQualityBatchNum[]	��������(��ѡ����ѡ��NULL)
		parWorkStation[]		��λ(��ѡ����ѡ��NULL)
		parRemark[]				��ע(��ѡ����ѡ��NULL)
		*retMessage				���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
************************************************************************************/
Data_API int Complete_New(char parSFC[], char parBoardCount[], char parQualityBatchNum[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
������	NcComplete_New
���ܣ�	��ָ����λ�á���SFCִ��NC_Complete����
������
		parSFC[]			SFC
		parNcType[]			��������
		parNcCode[]			��������
		parNcContext[]		��������
		parFailItem[]		FAIL���ѡ����ѡ��NULL��
		parFailValue[]		FAILֵ����ѡ����ѡ��NULL��
		parBoardCount[]		�ְ�����(��ѡ����ѡ��NULL)
		parWorkStation[]	��λ����ѡ����ѡ��NULL��
		parLogOperation[]	�豸����������SMT����ţ���ѡ����ѡ��NULL��
		parLogResource[]	��Դ���ƣ��оߣ���ѡ����ѡ��NULL)
		parNcPlace[]		����λ��(��ѡ����ѡ��NULL)
		parCreateUser[]		����¼����(��ѡ����ѡ��NULL)
		parOldStationName[]	ԭ��վ����(��ѡ����ѡ��NULL)
		parRemark[]			��ע����ѡ����ѡ��NULL��
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��14��
************************************************************************************/
Data_API int NcComplete_New(char parSFC[], char parNcType[], char parNcCode[], char parNcContext[], char parFailItem[], char parFailValue[], char parBoardCount[]
	, char parWorkStation[], char parLogOperation[], char parLogResource[], char parNcPlace[], char parCreateUser[], char parOldStationName[], char parRemark[]
	, char *retMessage);

/************************************************************************************
������	SplitStart_New
���ܣ�	��ָ����λ�á���SFCִ��Start����(CHECK������Ϣ)
������
		parSFC[]			SFC
		parBoardCount[]		�ְ�����(��ѡ����ѡ��NULL)
		parLogOperation[]	�豸����������SMT����ţ���ѡ����ѡ��NULL)
		parLogResource[]	��Դ���ƣ��оߣ���ѡ����ѡ��NULL)
		parWorkStation[]	��λ(��ѡ����ѡ��NULL)
		parRemark[]			��ע(��ѡ����ѡ��NULL)
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��17��
************************************************************************************/
Data_API int SplitStart_New(char parSFC[], char parBoardCount[], char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
������	SplitComplete_New
���ܣ�	��ָ����λ�á���SFCִ��Complete����
������
		parSFC[]			SFC
		parBoardCount[]		�ְ�����(��ѡ����ѡ��NULL)
		parLogOperation[]	�豸����������SMT����ţ���ѡ����ѡ��NULL)
		parLogResource[]	��Դ���ƣ��оߣ���ѡ����ѡ��NULL)
		parWorkStation[]	��λ(��ѡ����ѡ��NULL)
		parRemark[]			��ע(��ѡ����ѡ��NULL)
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��17��
************************************************************************************/
Data_API int SplitComplete_New(char parSFC[], char parBoardCount[], char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
������	SplitNcComplete_New
���ܣ�	��ָ����λ�á���SFCִ��NcComplete����
������
		parSFC[]			SFC
		parNcType			��������
		parNcCode[]			��������
		parNcContext		��������
		parFailItem			FAIL���ѡ����ѡ��NULL��
		parFailValue		FAILֵ����ѡ����ѡ��NULL��
		parBoardCount[]		�ְ�����(��ѡ����ѡ��NULL)
		parLogOperation[]	�豸����������SMT����ţ���ѡ����ѡ��NULL��
		parLogResource[]	��Դ���ƣ��оߣ���ѡ����ѡ��NULL)
		parWorkStation[]	��λ����ѡ����ѡ��NULL��
		parRemark[]			��ע����ѡ����ѡ��NULL��
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��17��
************************************************************************************/
Data_API int SplitNcComplete_New(char parSFC[], char parNcTpye[], char parNcCode[], char parNcContext[], char parFailItem[], char parFailValue[], char parBoardCount[]
	, char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
������	CompleteToStation_New
���ܣ�	SFC��վ�ı�
������
		parSFC[]			SFC
		parStationID		���ĺ�Ĺ�վID
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��10��26��
************************************************************************************/
Data_API int CompleteToStation_New(char parSFC[], char parStationID[], char *retMessage);

/************************************************************************************
������	ChangeSfcStation_New
���ܣ�	�޸�SFC���ڹ�վ
������
		parSFC[]			SFC
		parNewStationID		�¹�վID
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��10��26��
************************************************************************************/
Data_API int ChangeSfcStation_New(char parSFC[], char parNewStationID[], char *retMessage);

/************************************************************************************
������	ChangeSfcShoporder_New
���ܣ�	�޸�SFC���ڹ���
������
		parSFC[]			SFC
		parNewSchedulingID	���Ų�ID
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��10��26��
************************************************************************************/
Data_API int ChangeSfcShoporder_New(char parSFC[], char parNewSchedulingID[], char *retMessage);

/************************************************************************************
������	Serializable_New
���ܣ�	PSN ���л�Ϊ BSN
������
		parSFC[]			PSN
		parNewSfcList[]		��SFC(BSN�б���ʽΪ��SFC1;SFC2;����;SFCn��)
		*retMessage			���ص���Ϣ PASS
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int Serializable_New(char parSFC[], char parNewSfcList[], char *retMessage);

/************************************************************************************
������	UnSerializable_New
���ܣ�	PSN �����л�
������
		parSFC[]			PSN
		*retMessage			���ص���Ϣ PASS
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��10��24��
************************************************************************************/
Data_API int UnSerializable_New(char parSFC[], char *retMessage);

/************************************************************************************
������	ReworkToStation_New
���ܣ�	SFC������ĳ��վ
������
		parSFC[]			SFC
		parStationID[]		����Ŀ�Ĺ�վID����ѡ����parStationName��ѡһ����ѡ��NULL��
		parStationName[]	����Ŀ�Ĺ�վ���ƣ���ѡ����parStationID��ѡһ����ѡ��NULL��
		parAction[]			������д��SFC��־��ACTION�ֶΣ�ֻ��ΪREWORK��REPAIR_OK����ѡ����ѡ��NULL��Ĭ��ΪREWORK)
		parSfcState[]		������SFC��״̬����ѡ����ѡ��NULL��Ĭ��ΪW��
		parRepairRework[]	�Ƿ�ά�޷���(true��ʾ��false��ʾ�񣬿�ѡ����ѡ��NULL��Ĭ��false)
		parRemark[]			����ԭ�򣨿�ѡ����ѡ��NULL��
		parPreStationID[]	����ǰһ��վID(��ѡ����ѡ��NULL)
		*retMessage			������Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��26��
************************************************************************************/
Data_API int ReworkToStation_New(char parSFC[], char parStationID[], char parStationName[], char parAction[], char parSfcState[], char parRepairRework[], char parRemark[]
	, char parPreStationID[], char *retMessage);

/************************************************************************************
������	SfcKeyCollect_New
���ܣ�	�ؼ������ռ�(��)
������
		parSFC[]			SFC
		parData[]			�ؼ���������(��ʽΪ������:ֵ:�����ظ��ɼ�������;����;����:ֵ:�����ظ��ɼ���������)
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��18��
************************************************************************************/
Data_API int SfcKeyCollect_New(char parSFC[], char parData[], char *retMessage);

/************************************************************************************
������	RemoveSFCKey
���ܣ�	�ؼ����Ͻ��
������
		parSFC[]			���ؼ����ϵ�SFC
		parStationName[]	��վ����(��ѡ����ѡ��NULL)
		parKeyName[]		�󶨲���(��ѡ����ѡ��NULL)
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��18��
************************************************************************************/
Data_API int RemoveSFCKey_New(char parSFC[], char parStationName[], char parKeyName[], char *retMessage);

/************************************************************************************
������	FindAccessoriesByIng_New
���ܣ�	����SFC��ѯ��󶨵Ĺؼ�����
������
		parSFC[]		SFC
		parShoporder[]	����(��ѡ����ѡ��NULL)
		parStation[]	��վ����(��ѡ����ѡ��NULL)
		*retSfcKeyData	����SFC�󶨵Ĺؼ��������ݣ���ʽΪ������:ֵ:����:BYD�Ϻ�|����|����:ֵ:����:BYD�Ϻš���
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��18��
************************************************************************************/
Data_API int FindAccessoriesByIng_New(char parSFC[], char parShoporder[], char parStation[], char *retSfcKeyData, char *retMessage);

/************************************************************************************
������	GetSfcsKeyBySfc_New
���ܣ�	��ȡSFC�������л�ǰ����SFC�󶨵Ĺؼ�����
������
		parSFC[]		���л����SFC
		*retSfcKeyData	����SFC�������л�ǰSFC�󶨵Ĺؼ����ϣ���ʽΪ��SFC:����:ֵ|����|SFC:����:ֵ��
		*retMessage		���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��05��13��
************************************************************************************/
Data_API int GetSfcsKeyBySfc_New(char parSFC[], char *retSfcKeyData, char *retMessage);

/************************************************************************************
������	ReplaceSfcSubKey_New
���ܣ�	�滻�ؼ�����������
������
		parSFC[]		�滻�ؼ����������ϵ�SFC
		parOldValue[]   �󶨵ľ�ֵ
		parNewValue[]	�滻�����ֵ
		parNewBydPn[]	�滻��������Ϻ�(��ѡ����ѡ��NULL)
		*retMessage		���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��18��
************************************************************************************/
Data_API int ReplaceSfcSubKey_New(char parSFC[], char parOldValue[], char parNewValue[], char parNewBydPn[], char *retMessage);

/************************************************************************************
������	GetKeypartConfig_New
���ܣ�	��ȡ��վ�ؼ����ϲɼ�����
������
		parSFC[]				SFC
		*retKeypartConfigData	���ع�վ�ؼ����ϲɼ����ã���ʽΪ��ID:����:����:�����ظ��ɼ�������:��ע:BYD�Ϻ�:SFC�Ƿ���Ҫ�깤(0��1��)|����|ID:����:����:�����ظ��ɼ�������:��ע:BYD�Ϻ�:SFC�Ƿ���Ҫ�깤(0��1��)��
		*retMessage				���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��26��
************************************************************************************/
Data_API int GetKeypartConfig_New(char parSFC[], char *retKeypartConfigData, char *retMessage);

/************************************************************************************
������	CreateNumbers_New
���ܣ�	������������
������
		parNumberStore[]	��������ơ����������꣬�˴�Ҳ�ɴ������꣩SN��IMEI1,IMEI2��BT��WIFI,KEYBOX, LUCKY,Battery
		parModel[]			��Ҫ����ĺ��������Ǹ���MODEL����(�������MODEL��ѡ����MODEL��ѡ����ѡ��NULL)
		parNum[]			�����ĺ�������(��ѡ��Ĭ��1����ѡ��NULL)
		parModuleID[]		ģ��ID(��ѡ����ѡ��NULL)
		parCustomStatus[]	�Զ���״̬(��ѡ����ѡ��NULL)
		parRemark[]			��ע(��ѡ����ѡ��NULL)
		*retNumberList		���غ�����Ϣ����ʽΪ����������1:����ֵ1;����;��������n:����ֵn|����|��������1:����ֵ1;����;��������n:����ֵn��
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int CreateNumbers_New(char parNumberStore[], char parModel[], char parNum[], char parModuleID[], char parCustomStatus[], char parRemark[], char *retNumberList
	, char *retMessage);

/************************************************************************************
������	CreateNumberBySfc_New
���ܣ�	ͨ��SFC��������
������
		parSFC[]			SFC
		parNumberStore[]	��������ơ����������꣬�˴�Ҳ�ɴ������꣩SN��IMEI1,IMEI2��BT��WIFI,KEYBOX, LUCKY,Battery
		parModel[]			��Ҫ����ĺ��������Ǹ���MODEL����(�������MODEL��ѡ����MODEL��ѡ����ѡ��NULL)
		parModuleID[]		ģ��ID(��ѡ����ѡ��NULL)
		parCustomStatus[]	�Զ���״̬(��ѡ����ѡ��NULL)
		parRemak[]			��ע(��ѡ����ѡ��NULL)
		*retNumber			���غ�����Ϣ����ʽΪ����������1:����ֵ1;����;��������n:����ֵn��
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int CreateNumberBySfc_New(char parSFC[], char parNumberStore[], char parModel[], char parModuleID[], char parCustomStatus[], char parRemak[], char *retNumber
	, char *retMessage);

/************************************************************************************
������	GetNumberBySfc_New
���ܣ�	ͨ��SFC�������
������
		parSFC[]			SFC
		parNumberStore[]	���������ơ����������꣬�˴�Ҳ�ɴ������꣩SN��IMEI1,IMEI2��BT��WIFI,KEYBOX, LUCKY,Battery
		parModel[]			��Ҫ����ĺ��������Ǹ���MODEL����(�������MODEL��ѡ����MODEL��ѡ����ѡ��NULL)
		parModuleID[]       ģ��ID(��ѡ����ѡ��NULL)
		parCustomStatus[]	�Զ���״̬(��ѡ����ѡ��NULL)
		parRemak[]			��ע(��ѡ����ѡ��NULL)
		*retNumber			���غ�����Ϣ����ʽΪ����������1:����ֵ1;����;��������n:����ֵn��
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int GetNumberBySfc_New (char parSFC[], char parNumberStore[], char parModel[], char parModuleID[], char parCustomStatus[], char parRemark[], char *retNumber
	, char *retMessage);

/************************************************************************************
������	GetNumberInfo_New
���ܣ�	��ȡ���������Ϣ
������
		parNumberStore[]	�����
		parNumber[]			����
		*retGroupNumbers	����������б���ʽΪ���������1:����ֵ1;����;�������n:����ֵn��
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API int GetNumberInfo_New(char parNumberStore[], char parNumber[], char *retNumberInfo, char *retMessage);

/************************************************************************************
������	GetNumberInfo2_New
���ܣ�	��ȡ���������Ϣ
������
		parNumberStore[]	�����
		parNumber[]			����
		*retNumberSfc		����numberSfc 
		*retGroupNumbers	����������б���ʽΪ���������1:����ֵ1;����;�������n:����ֵn��
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2018��11��21��
************************************************************************************/
Data_API int GetNumberInfo2_New(char parNumberStore[], char parNumber[], char *retNumberSfc, char *retNumberInfo, char *retMessage);

/************************************************************************************
������	GetNumberInfo3_New
���ܣ�	��ȡ���������Ϣ
������
		parNumberStore[]	�����
		parNumber[]			���� 
		*retNumberInfo		���غ�����Ϣ����ʽΪ��numberSfc:SFC;numberModel:MODEL;shoporder:����;status:״̬(0δʹ��,1��ʹ��,2:������);projectId:��ĿID;productId:��ƷID;numberLibraryId:�����ID;batchid:�ϴ����κ�;customStatus:�Զ���״̬��
		*retGroupNumbers	����������б���ʽΪ���������1:����ֵ1;����;�������n:����ֵn��
		*retMessage			���ص���Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2019��01��21��
************************************************************************************/
Data_API int GetNumberInfo3_New(char parNumberStore[], char parNumber[], char *retNumberInfo, char *retGroupNumbers, char *retMessage);

/************************************************************************************
������	TestDataCollect_New
���ܣ�	�������ݲɼ���main��sub����
������
		parSFC[]			��Ʒ�����к�SFC(��ѡ����ѡ��NULL)
		parTdsName[]		�������ݲɼ�������(��ѡ����ѡ��NULL)
		parFixtureNo[]		�о߱��(��ѡ����ѡ��NULL)
		parVersion[]		��������汾��(��ѡ����ѡ��NULL)
		parSwVersion[]      ��Ʒ������汾��(��ѡ����ѡ��NULL)
		parHwVersion[]		��Ʒ��Ӳ���汾��(��ѡ����ѡ��NULL)
		parTestResult[]		���Խ��(��ѡ����ѡ��NULL)
		parFailItem[]		������(��ѡ����ѡ��NULL)
		parFailValue[]		�������ֵ(��ѡ����ѡ��NULL)
		parNcCode[]			�������(��ѡ����ѡ��NULL)
		parElapseTime[]		����ʹ����ʱ(��ѡ����ѡ��NULL)
		parTestCount[]		���Դ���(��ѡ����ѡ��NULL)
		parTestDataList[]	���������б��б��ж�������á�|����������ѡ��������NULL��
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API bool TestDataCollect_New(char parSFC[], char parTdsName[], char parFixtureNo[], char parVersion[], char parSwVersion[], char parHwVersion[], char parTestResult[]
	, char parFailItem[], char parFailValue[], char parNcCode[], char parElapseTime[], char parTestCount[], char parTestDataList[], char *retMessage);

/************************************************************************************
������	TestDataCollect_TXT_New
���ܣ�	�������ݲɼ���main��sub����(TXT�������־)
������
		parTestFile			TXT�ļ�·��
		parTestCount[]		���Դ���(��ѡ����ѡ��NULL)
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API bool TestDataCollect_TXT_New(char parTestFile[], char parTestCount[], char *retMessage);

/************************************************************************************
������	TestDataCollect_XML_New
���ܣ�	�������ݲɼ���main��sub����(XML�������־)
������
		parTestFile[]		XML�ļ�·��
		parTestContent[]	XML�ļ�����
		parTestCount[]		���Դ���(��ѡ����ѡ��NULL)
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��04��20��
************************************************************************************/
Data_API bool TestDataCollect_XML_New(char TestFile[], char parTestContent[], char partTestCount[], char *retMessage);

/************************************************************************************
������	TestDataCollect2MainChild_New
���ܣ�	�������ݲɼ���main��child����
������
		parSFC[]			��Ʒ�����к�SFC(��ѡ����ѡ��NULL)
		parTdsName[]		�������ݲɼ�������(��ѡ����ѡ��NULL)
		parFixtureNo[]		�о߱��(��ѡ����ѡ��NULL)
		parVersion[]		��������汾��(��ѡ����ѡ��NULL)
		parSwVersion[]      ��Ʒ������汾��(��ѡ����ѡ��NULL)
		parHwVersion[]		��Ʒ��Ӳ���汾��(��ѡ����ѡ��NULL)
		parTestResult[]		���Խ��(��ѡ����ѡ��NULL)
		parFailItem[]		������(��ѡ����ѡ��NULL)
		parFailValue[]		�������ֵ(��ѡ����ѡ��NULL)
		parNcCode[]			�������(��ѡ����ѡ��NULL)
		parElapseTime[]		����ʹ����ʱ(��ѡ����ѡ��NULL)
		parTestCount[]		���Դ���(��ѡ����ѡ��NULL)
		parText[]			�ı����ݣ���ѡ��������NULL��
		parTestDataList[]	���������б���ʽΪ������;ֵ;���ֵ;��Сֵ;��׼ֵ;��λ;����ʱ��(yyyy-MM-dd HH:mm:ss);������;λ�ú�;���Խ���ʱ��;���Խ��;�������;PN;��ע;�ı�����
											|����|����;ֵ;���ֵ;��Сֵ;��׼ֵ;��λ;����ʱ��(yyyy-MM-dd HH:mm:ss);������;λ�ú�;���Խ���ʱ��;���Խ��;�������;PN;��ע;�ı����ݡ�
							����ѡ��������NULL��
		*retMessage			���صĴ�����Ϣ
		parContinue[]       �Ƿ�SNд�뱸�ݱ�1��ʾд�룬������ʾ��д��
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��07��27��
************************************************************************************/
Data_API bool TestDataCollect2MainChild_New(char parSFC[], char parTdsName[], char parFixtureNo[], char parVersion[], char parSwVersion[], char parHwVersion[], char parTestResult[]
	, char parFailItem[], char parFailValue[], char parNcCode[], char parElapseTime[], char parTestCount[], char parText[], char parTestDataList[], char parContinue[], char *retMessage);

/************************************************************************************
������	Binding_NEW
���ܣ�	����
������  parSFC[] ��Ʒ�����к�SFC
		parMultiple[] ���ϱ���
		parBoardCount[] �ְ���������ѡ�����null��
		*parCountInfo Ͷ�������Ϣ,��ʽ��IN_QTY:Ͷ������;OUT_QTY:��������;FAIL_QTY:��������;WASTE_QTY:��������;BINDING_QTY:��������
		*refstrMessage ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
�༭ʱ�䣺2018-3-28 HSX
*************************************************************************************/
Data_API bool Binding_NEW(char sfc[], char multiple[], char *countInfo, char *refstrMessage);

/************************************************************************************
������	CheckAllStationEquipment_New
���ܣ�	������й�վ�豸�Ƿ�����
������  *refstrMessage ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
�༭ʱ�䣺2018-3-29 HSX
*************************************************************************************/
Data_API bool CheckAllStationEquipment_New(char *refstrMessage);

/************************************************************************************
������	GetProjectEquipment_New
���ܣ�	��ȡ��Ŀ����վ����Ҫ���豸�嵥
������  parIsContinue[] ���豸�嵥Ϊ��ʱ�Ǳ����Ƿ��ؿգ�Ϊ0ʱ����
		*retData ���ص��豸��Ϣ����ʽ��PROJECT_ID:��ĿID;PROJECT_NAME:��Ŀ����;EQ_TYPE_ID:�豸����ID;EQ_TYPE_NAME:�豸��������;EQ_PROPERTY:�豸����;STATION_NAME:��վ����;PRODUCT_ID:��ƷID;PRODUCT_NAME:��Ʒ����|...
		*refstrMessage ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
�༭ʱ�䣺2018-3-29 HSX
*************************************************************************************/
Data_API bool GetProjectEquipment_New(char parIsContinue[], char *retData, char *refstrMessage);

/************************************************************************************
������	CheckEquipmentUseQty_New
���ܣ�	У���豸ʹ�ô���
������
		parSFC[]			SFC
		parEquipmentNo[]	�ʲ���Ż��豸���
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2018��08��09��
*************************************************************************************/
Data_API bool CheckEquipmentUseQty_New(char parSFC[], char parEquipmentNo[], char *retMessage);

/************************************************************************************
������	GetLineLossState_New
���ܣ�	��ȡ������״̬
������
		parFixture[]		�о߱��
		*retLineLossState	���ص�������״̬
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2019��01��21��
*************************************************************************************/
Data_API bool GetLineLossState_New(char parFixture[], char *retLineLossState, char *retMessage);

/************************************************************************************
������	AddLineLossCheck_New
���ܣ�	�����������¼
������
		parFixture[]	�о߱��
		parPcID[]		PC���
		parRfLine[]		��Ƶ�߱��
		parInstrument[]	�������
		parFilePath[]	����ļ���ַ
		*retMessage		���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2019��01��25��
*************************************************************************************/
Data_API bool AddLineLossCheck_New(char parFixture[], char parPcID[], char parRfLine[], char parInstrument[], char parFilePath[], char *retMessage);

/************************************************************************************
������	AddEquipmentInfoKeyList_New
���ܣ�	�豸��Ϣ�ɼ�
������  parEquNo[] �豸���(����)
		parEquType[] �豸����(����)
		char parSN[] ��ƷSN(ѡ����null)
		parLine[] ����(ѡ����null)
		parOperateName[] ������(ѡ�Ĭ��ȡ��¼ID�����������null)
		parOperateTime[] ����ʱ��(ѡ�Ĭ��ȡ���ýӿ�ʱ�䣬��ʽ��yyyy-MM-dd HH:mm:ss�����null)
		parKeys[] ���ϴ����Լ�ֵ�ԣ������ʽΪ��������1:ֵ1;����2:ֵ2...����
		*refstrMessage ��ʧ��ʱ���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
�༭ʱ�䣺2018-01-08 HSX
*************************************************************************************/
Data_API bool AddEquipmentInfoKeyList_New(char parEquNo[], char parEquType[], char parSN[], char parLine[], char parOperateName[], char parOperateTime[], char parKeys[], char* refstrMessage);

/************************************************************************************
������	ResetMesConfig_New
���ܣ�	��ȡ������վ��Ϣ��������\cfg\mes_config.ini�ļ�
������
		parShoporder[]	����
		parStation[]	��վ����
		*retMessage		���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2018��08��03��
************************************************************************************/
Data_API bool ResetMesConfig_New(char parShoporder[], char parStation[], char *retMessage);

/************************************************************************************
������	GetPanguTbOrderPpid_New
���ܣ�	��ȡ�̹�ORDER_PPID������
������
		ppid[]		        PPID,��SFC
		*retOrderPpidInfo   ����ORDERPPID��Ϣ,���ݸ�ʽ "(��1������)����1:ֵ1;.......����n:ֵn|(��2������)����1:ֵ1;.......����n:ֵn|......|(��n������)����1:ֵ1;.......����n:ֵn"
		*retMessage			���صĴ�����Ϣ
���أ�	����ɹ��򷵻�1�����򷵻�0
���ߣ�	BYD ������ҵȺִ�и��ܲð칫�� ��־�� 2017��05��24��
************************************************************************************/
Data_API bool GetPanguTbOrderPpid_New(char ppid[],char *retOrderPpidInfo, char *retMessage);

#pragma endregion �Ż���Ľӿ�
