
#ifdef Data_API
#else
#define Data_API extern "C" _declspec(dllimport)
#endif

/************************************************************************************
函数：	Start
功能：	对指定“位置”的SFC执行Start操作(CHECK流程信息)
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShoporder[]		Shoporder（工单）
		parOPERATION[]		OPERATION（工站）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回非1,返回2表示已经经过当前工站
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Start (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	Complete
功能：	对指定“位置”的SFC执行Complete操作
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShoporder[]		Shoporder（工单）
		parOPERATION[]		OPERATION（工站）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Complete (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	NC_Complete
功能：	对指定“位置”的SFC执行NC_Complete操作
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShopOrder[]		工单
		parOPERATION[]	OPERATION（工站）
		parNC_Tpye			错误类型
		parCOMMENTS[]		注释
		parNC_CODE		错误代码
		parFailItem			错误项
		parFailValue		错误值
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int NC_Complete (char parSFC[], char parSITE[], char parShopOrder[], 
										char parOPERATION[],char parNC_Tpye[], char parCOMMENTS[], 
										char parNC_CODE[],char parFailItem[],char parFailValue[], char parUSER[], char parPASSWORD[], 
										char *retMessage);

/************************************************************************************
函数：	Split_Start
功能：	对指定“位置”的序列化前SFC执行Start操作(CHECK流程信息)
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShoporder[]		Shoporder（工单）
		parOPERATION[]		OPERATION（工站）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回非1,返回2表示已经经过当前工站
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Split_Start (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	Split_Complete
功能：	对指定“位置”的SFC执行Complete操作
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShoporder[]		Shoporder（工单）
		parOPERATION[]		OPERATION（工站）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Split_Complete (char parSFC[], char parSITE[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	Split_NC_Complete
功能：	对指定“位置”的SFC执行NC_Complete操作
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parShopOrder[]		工单
		parOPERATION[]	OPERATION（工站）
		parNC_Tpye			错误类型
		parCOMMENTS[]		注释
		parNC_CODE		错误代码
		parFailItem			错误项
		parFailValue		错误值
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Split_NC_Complete (char parSFC[], char parSITE[], char parShopOrder[], 
										char parOPERATION[],char parNC_Tpye[], char parCOMMENTS[], 
										char parNC_CODE[],char parFailItem[],char parFailValue[], char parUSER[], char parPASSWORD[], 
										char *retMessage);


/************************************************************************************
函数：	GetNumberbySFC
功能：	通过SFC分配号码（不同的“项目名称”和“工单号”分配不同类新的号码）
参数：
		parSFC[]			SFC
		parSITE[]			订制料号
		parSTORE[]			号码库的名称。（若有网标，此处也可传入网标）SN，IMEI1,IMEI2，BT，WIFI,KEYBOX, LUCKY,Battery
		parMODEL[]			需要分配的号码属于那个“MODEL”。
		parUSER[]			操作人员
		parPASSWORD[]		操作人员的密码
		*retMessage			返回的消息（IMEI:111111111111119;IMEI2:111111111111127）
							（SN:1234）
							（IMEI:1234）
							（IMEI2:1234）
							（BTAddress:1234）
							（Wifi:1234）
							（Battery:1234）
							（DEVICE:%s;KEY:%s;ID:%s;MAGIC:%s;CRC:%s）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日  
************************************************************************************/
//*
Data_API int GetNumberbySFC (char parSFC[], char parSITE[], char parSTORE[], char parMODEL[], char parUSER[], char parPASSWORD[],char noQty[], char *retMessage);

/************************************************************************************
函数：	GetDatabyShoporder
功能：	通过工单获得项目和工单的自定义数据
参数：
		parShopOrder			工单（传入）
		maxCount				工单数量（传出）
		getSITE					项目料号（传出）
		retMessage		返回的消息（自定义名称:自定义数值;SN:111;）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int GetDatabyShoporder(char parShopOrder[],char *maxCount,char *getSITE,char *retMessage);

/************************************************************************************
函数：	GetDatabyStationName
功能：	得到工站的自定义数据
参数：
		parOPERATION[]		OPERATION（工站）
		parSITE[]			订制料号
		*retMessage		返回的消息
返回：	如果返回1 ，否则返回0 
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
Data_API int GetDatabyStationName(char parOPERATION[], char parSITE[],char *retMessage);

/************************************************************************************
函数：	SerializeSFC
功能：	PSN 序列化为 BSN
参数：
		parSITE[]			订制料号
		parSFC[]			SFC
		parNEWSFC[]			parNEWSFC （新SFC）sfc1;sfc2;sfc3
		parShoporder[]		Shoporder（工单）
		parOPERATION[]		OPERATION（工站）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息 PASS
返回：	return 1;
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
Data_API int SerializeSFC (char parSITE[], char parSFC[], char parNEWSFC[], char parShoporder[], char parOPERATION[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	Data_Collect
功能：	将需要收集的数据发往MES保存起来。
参数：
		parSITE[]			订制料号
		parSFC[]			SFC
		parREPEATFlag		数据是否可重复   
		parDC_REVISION		数据收集组版本号 
		parShopOrder		工单
		parRESOURCE[]		资源             
		parOPERATION[]		数据收集工站名
		parDATA				如果用系统预定义的工站名称：数据（格式“值|值|值”） 自定义工站名称：数据（格式“NAME:VALUE;NAME:VALUE;NAME:VALUE）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int Data_Collect (char parSITE[], char parSFC[], char parREPEATFlag[], char parDC_REVISION[], char parShoporder[], char parRESOURCE[], char parOPERATION[], char parDATA[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
函数：	CreateNumberbySFC
引用：	函数 sendDataByPost()
		全局变量 pub_SecURL
		全局变量 pub_LOGON_INFO
功能：	通过SFC创建号码（不同的“SITE”和“NUMBER_STORE”创建不同类型的号码）
参数：
		parSFC			SFC
		parSITE			SITE
		parSTORE		号码库的名称。
		parMODEL		需要分配的号码属于那个“MODEL”，如果没有，请传个空字符串过来。
		parHOW			要创建的号码数量
		parUSER			操作人员
		parPASSWORD		操作人员的密码
		retMessage		返回的消息（SFC:0902140001;MEID:111;AKEY1:222;AKEY2:333;BT:444）
返回：	如果成功则返回true，否则返回false
作者：	BYD 九部 信息系统部 杨霖 2015年06月16日
************************************************************************************/

Data_API int CreateNumberbySFC (char parSFC[], char parShoporder[], char parSTORE[], char parMODEL[], char parHOW[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	QueryData_Collect
引用：	函数 sendDataByPost()
		全局变量 pub_SecURL
		全局变量 pub_LOGON_INFO
功能：	从MES中查询之前用“Data_Collect”收集的信息。
参数：
		parSITE[]			订制料号
		parSFC[]			SFC
		parDC_GROUP		数据收集组名称
		parDC_REVISION	数据收集组版本号
		parQueryDATA	需要查询的数据（格式“<数据库列名>:<值>|<数据库列名>:<值>|<数据库列名>:<值>|...”）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回true，否则返回false
作者：	BYD 九部 信息系统部 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int QueryData_Collect (char parSITE[], char parSFC[], char parDC_GROUP[], char parDC_REVISION[], char *parQueryDATA, char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	GetDatabySFC
功能：	获取指定SFC所对应的工单的自定义数据
参数：
		parSFC[]			SFC
		parSITE[]			SITE
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/
//*
Data_API int GetDatabySFC (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	GetSFCInfo
功能：	获取指定SFC所对应的信息
参数：
		parSFC[]			SFC
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/

Data_API int GetSFCInfo (char parSFC[], char *retMessage);

Data_API bool BYDTD_COLLECT(char parstrSFC[],char parstrShoporder[],char parstrPF[],char parstrNCCode[],char parstrFailItem[],char parstrFailValue[],char *retMessage);

/************************************************************************************
函数：	BYDTD_COLLECT_TXT
功能：	测试日志上传 TXT 版
参数：
		parstrShoporder			工单号
		parTEST_FILE			TXT文件路径
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/

Data_API bool BYDTD_COLLECT_TXT (char parstrShoporder[], char parTEST_FILE[], char *retMessage);

/************************************************************************************
函数：	BYDTD_COLLECT_XML
功能：	测试日志上传 XML 版
参数：
		parstrShoporder			工单号
		parTEST_CONT			XML文件内容
		parTEST_FILE			XML文件路径
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2015年06月16日
************************************************************************************/

Data_API bool BYDTD_COLLECT_XML  (char parstrShoporder[], char parTEST_CONT[], char parTEST_FILE[], char *retMessage);

/************************************************************************************
函数：	MESinterface_GetServerDateTime_Link
功能：	获取服务器时间 _ 有自动连接数据库的动作
参数：
		parSITE[]			订制料号
		parFOTMAT		日期格式（例：yyyy-MM-dd HH:mm:ss）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息 （如果成功，那么返回工单号）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2011年06月17日
************************************************************************************/
//*
Data_API int MESinterface_GetServerDateTime_Link (char parSITE[], char parFOTMAT[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	GetServerDateTime_Link
功能：	获取服务器时间 _ 有自动连接数据库的动作
参数：
		parSITE[]			订制料号
		parFOTMAT		日期格式（例：yyyy-MM-dd HH:mm:ss）
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息 （如果成功，那么返回工单号）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2011年06月17日
************************************************************************************/
//*
Data_API int GetServerDateTime_Link (char parSITE[], char parFOTMAT[], char parUSER[], char parPASSWORD[], char *retMessage);

Data_API int MESinterface_GetSFCState (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);
Data_API int GetSFCState (char parSFC[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);


Data_API int GetCustomData(char parSFC[], char *retMessage);

/************************************************************************************
函数：	GetSFCKeybyStationName
功能：	获取当前工站当前工单需要绑定的KEY信息
参数：
		parSFC[]			SFC
		parstrStationName[]			工站名称
		parstrShoporder[]			工单号
		parSITE[]			SITE
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2016年01月27日
************************************************************************************/
//*
Data_API int GetSFCKeybyStationName (char parSFC[],char parstrStationName[],char parstrShoporder[], char parSITE[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
函数：	Getnumberinfo
功能：	获取号码相关信息
参数：
		parNUMBER_STORE[]   号码库
		parNUMBER[]			号码
		parUSER[]			操作人员（MES帐号）
		parPASSWORD[]		操作人员的密码（MES帐号密码）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 xlf 2016年09月06日
************************************************************************************/
//*
Data_API int Getnumberinfo (char parNUMBER_STORE[], char parNUMBER[], char parUSER[], char parPASSWORD[], char *retMessage);
/************************************************************************************
函数：	GetNumberbySFCNew 3
功能：	通过SFC分配号码（不同的“项目名称”和“工单号”分配不同类新的号码）
参数：
		parSFC[]			SFC
		parShoporder[]		工单号
		parSTORE[]			号码库的名称。（若有网标，此处也可传入网标）SN，IMEI1,IMEI2，BT，WIFI,KEYBOX, LUCKY,Battery
		parNUMBER[]         号码
		parMODEL[]			需要分配的号码属于那个“MODEL”。
		parUSER[]			操作人员
		parPASSWORD[]		操作人员的密码
		*retMessage			返回的消息（IMEI:111111111111119;IMEI2:111111111111127）
							（SN:1234）
							（IMEI:1234）
							（IMEI2:1234）
							（BTAddress:1234）
							（Wifi:1234）
							（Battery:1234）
							（DEVICE:%s;KEY:%s;ID:%s;MAGIC:%s;CRC:%s）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 xlf 2016年09月07日  
************************************************************************************/
Data_API int GetNumberbySFCNew (char parSFC[], char parShoporder[], char parSTORE[], char parNUMBER[], char parMODEL[], char parUSER[], char parPASSWORD[], char *retMessage);

/************************************************************************************
函数：	ReworkToStation
功能：	SFC返工到某工站
参数：
		parStation_NAME[]   返工目的工站
		parSFC[]		  SFC
		parREMARK[]		  返工原因
		*retMessage		 返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 韦成恒 2016年10月20日
************************************************************************************/
//*
Data_API int ReworkToStation (char parStation_NAME[], char parSFC[], char parREMARK[], char *retMessage);

/************************************************************************************
函数：	RemoveSFCKey
功能：	关键物料解绑
参数：
parStation_NAME[]   解除绑定工站的数据
parSFC[]		  SFC		解除绑定的SFC
parstrDataName[]		  解除的附件的名称（可传空，空为当前工站所有附件）
*retMessage		 返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 杨霖 2017年03月08日
************************************************************************************/
//*
Data_API int RemoveSFCKey(char parStation_NAME[], char parSFC[], char parstrDataName[], char *retMessage);

Data_API bool StationJumpJudge(char sfc[],char parStationName[], char strTYPE[],char *refstrMessage);

/************************************************************************************
函数：	AddTestLogInfo
功能：	新增测试日志信息
参数：
		sfc[]		        SFC
		reslut[]            测试结果 0失败 1成功
		testTime[]          测试时间，格式 yyyy-MM-dd HH:mm:ss
		fullFileName[]      文件绝对路径
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
************************************************************************************/
Data_API bool AddTestLogInfo(char sfc[],char reslut[], char testTime[],char fullFileName[],char *refstrMessage);

/************************************************************************************
函数：	ReplaceSfcSubKey
功能：	替换关键物料子物料
参数：
parSFC[]		SFC		替换关键物料子物料的SFC
parOldValue[]   绑定的旧值
parNewValue[]	替换后的新值
parNewBydPn[]	替换后的物料料号(可选,为空不修改料号)
*retMessage		返回的错消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年03月10日
************************************************************************************/
Data_API int ReplaceSfcSubKey(char parSFC[], char parOldValue[], char parNewValue[], char parNewBydPn[], char *retMessage);

/************************************************************************************
函数：	GetStationCheckConfig
功能：	获取工站校验比对配置信息列表
参数：
parSFC[]		SFC		获取工站校验比对配置信息列表的SFC
*retData		返回的工站校验比对配置信息列表信息，格式是：列表的各个记录之间以“|”分割，一条记录中不同的信息以“,”隔开。
		比如：RULE:校验规则,CHECK_TYPE:校验类型(0扫描号码与号码库比对，1扫描号码与关键物料比对，2扫描号码与序列化前号码比对，3扫描号码与自定义数据比对，4扫描号码与扫描号码比对),PARAM1:参数一(0号码库，1数据名称，3自定义数据名称),PARAM2:参数二(0 Model，1数据名称，3自定义数据名称),PARAM3:参数三(0号码名称，1数据名称，3自定义数据名称),SCAN_COUNT:需要扫描的次数(1～5),SCAN_MESSAGE:扫描时提示的内容(如果多个，用“;”号隔开)|……
*retMessage		返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年03月10日
************************************************************************************/
Data_API int GetStationCheckConfig(char parSFC[], char *retData, char *retMessage);

#pragma region 优化后的接口

/************************************************************************************
函数：	GetServerTime_New
功能：	获取服务器时间
参数：
		*retServerTime	返回服务器时间
		*retMessage		返回的消息 （如果成功，那么返回工单号）
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int GetServerTime_New(char *retServerTime, char *retMessage);

/************************************************************************************
函数：	GetSFCInfo_New
功能：	获取指定SFC所对应的信息
参数：
		parSFC[]		SFC
		*retSFCInfo		返回SFC信息，格式为“名称1:值1;……;名称n:值n”
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int GetSFCInfo_New(char parSFC[], char *retSFCInfo, char *retMessage);

/************************************************************************************
函数：	GetStationCheckConfig_New
功能：	获取工站校验比对配置信息列表
参数：
		parSFC[]				获取工站校验比对配置信息列表的SFC
		*retCheckConfigData		返回工站校验比对配置信息列表，格式是“RULE:校验规则,CHECK_TYPE:校验类型,PARAM1:参数一,PARAM2:参数二,PARAM3:参数三,SCAN_COUNT:需要扫描的次数(1～5),SCAN_MESSAGE:扫描时提示的内容|……|RULE:校验规则,CHECK_TYPE:校验类型,PARAM1:参数一,PARAM2:参数二,PARAM3:参数三,SCAN_COUNT:需要扫描的次数(1～5),SCAN_MESSAGE:扫描时提示的内容”
		*retMessage				返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月26日
************************************************************************************/
Data_API int GetStationCheckConfig_New(char parSFC[], char *retCheckConfigData, char *retMessage);

/************************************************************************************
函数：	GetOnLineStationListByShoporder_New
功能：	根据工单获取所在工艺路线的在线工站信息列表
参数：
		parShoporder[]	工单
		*retStations	返回在线工站信息列表，格式是“ID:工站ID,NAME:工站名称|……|ID:工站ID,NAME:工站名称”
		*retMessage		返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年10月26日
************************************************************************************/
Data_API int GetOnLineStationListByShoporder_New(char parShoporder[], char *retStations, char *retMessage);

/************************************************************************************
函数：	GetCustomDatabyShoporder_New
功能：	通过工单获得项目、产品（定制料号）和工单的自定义数据
参数：
		*retCustomData		成功时返回的自定义数据（格式为“名称≡值≡描述|……|名称≡值≡描述”）
		*retMessage			失败时返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
备注：	工单、产品（定制料号）ID、项目ID从\cfg\mes_config.ini文件中的Resource、PRODUCT_ID、PROJECT_ID中获取
************************************************************************************/
Data_API int GetCustomDatabyShoporder_New(char *retCustomData, char *retMessage);

/************************************************************************************
函数：	GetCustomDatabyProduct_New
功能：	通过产品（定制料号）的自定义数据
参数：
		*retCustomData		成功时返回的自定义数据（格式为“名称≡值≡描述|……|名称≡值≡描述”）
		*retMessage			失败时返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年05月23日
备注：	产品（定制料号）ID从\cfg\mes_config.ini文件中的PRODUCT_ID中获取
************************************************************************************/
Data_API int GetCustomDatabyProduct_New(char *retCustomData, char *retMessage);

/************************************************************************************
函数：	GetCustomDatabyStation_New
功能：	获取工站自定义数据
参数：
		*retCustomData		成功时返回的自定义数据（格式为“名称≡值≡描述|……|名称≡值≡描述”）
		*retMessage			失败时返回的错误信息
返回：	如果返回1 ，否则返回0 
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
备注：	工站ID从\cfg\mes_config.ini文件中的StationID中获取
************************************************************************************/
Data_API int GetCustomDatabyStation_New(char *retCustomData, char *retMessage);

/************************************************************************************
函数：	GetCustomDatabySFC_New
功能：	获取指定SFC所对应的工单的自定义数据
参数：
		parSFC[]		SFC
		*retCustomData	成功时返回的自定义数据（格式为“名称≡值≡描述|……|名称≡值≡描述”）
		*retMessage		失败时返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
************************************************************************************/
Data_API int GetCustomDatabySFC_New(char parSFC[], char *retCustomData, char *retMessage);

/************************************************************************************
函数：	GetCustomData_New
功能：	获取自定义数据(首站工单/非首站SFC+工站自定义数据)
参数：
		parSFC[]			SFC
		*retCustomData		成功时返回的自定义数据（格式为“名称≡值≡描述|……|名称≡值≡描述”）
		*retMessage			失败时返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int GetCustomData_New(char parSFC[], char *retCustomData, char *retMessage);

/************************************************************************************
函数：	Start_New
功能：	对指定“位置”的SFC执行Start操作(CHECK流程信息)
参数：
		parSFC[]			SFC
		parBoardCount[]		分板数量(可选，不选传NULL)
		parWorkStation[]	工位(可选，不选传NULL)
		parLogOperation[]	设备（电脑名或SMT机编号，可选，不选传NULL)
		parLogResource[]	资源名称（夹具，可选，不选传NULL)
		parRemark[]			备注(可选，不选传NULL)
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
************************************************************************************/
Data_API int Start_New(char parSFC[], char parBoardCount[], char parWorkStation[], char parLogOperation[], char parLogResource[], char parRemark[], char *retMessage);

/************************************************************************************
函数：	Complete_New
功能：	对指定“位置”的SFC执行Complete操作
参数：
		parSFC[]				SFC
		parBoardCount[]			分板数量(可选，不选传NULL)
		parQualityBatchNum[]	批次数量(可选，不选传NULL)
		parWorkStation[]		工位(可选，不选传NULL)
		parRemark[]				备注(可选，不选传NULL)
		*retMessage				返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
************************************************************************************/
Data_API int Complete_New(char parSFC[], char parBoardCount[], char parQualityBatchNum[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
函数：	NcComplete_New
功能：	对指定“位置”的SFC执行NC_Complete操作
参数：
		parSFC[]			SFC
		parNcType[]			不良类型
		parNcCode[]			不良代码
		parNcContext[]		不良描述
		parFailItem[]		FAIL项（可选，不选传NULL）
		parFailValue[]		FAIL值（可选，不选传NULL）
		parBoardCount[]		分板数量(可选，不选传NULL)
		parWorkStation[]	工位（可选，不选传NULL）
		parLogOperation[]	设备（电脑名或SMT机编号，可选，不选传NULL）
		parLogResource[]	资源名称（夹具，可选，不选传NULL)
		parNcPlace[]		不良位置(可选，不选传NULL)
		parCreateUser[]		不良录入人(可选，不选传NULL)
		parOldStationName[]	原工站名称(可选，不选传NULL)
		parRemark[]			备注（可选，不选传NULL）
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月14日
************************************************************************************/
Data_API int NcComplete_New(char parSFC[], char parNcType[], char parNcCode[], char parNcContext[], char parFailItem[], char parFailValue[], char parBoardCount[]
	, char parWorkStation[], char parLogOperation[], char parLogResource[], char parNcPlace[], char parCreateUser[], char parOldStationName[], char parRemark[]
	, char *retMessage);

/************************************************************************************
函数：	SplitStart_New
功能：	对指定“位置”的SFC执行Start操作(CHECK流程信息)
参数：
		parSFC[]			SFC
		parBoardCount[]		分板数量(可选，不选传NULL)
		parLogOperation[]	设备（电脑名或SMT机编号，可选，不选传NULL)
		parLogResource[]	资源名称（夹具，可选，不选传NULL)
		parWorkStation[]	工位(可选，不选传NULL)
		parRemark[]			备注(可选，不选传NULL)
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月17日
************************************************************************************/
Data_API int SplitStart_New(char parSFC[], char parBoardCount[], char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
函数：	SplitComplete_New
功能：	对指定“位置”的SFC执行Complete操作
参数：
		parSFC[]			SFC
		parBoardCount[]		分板数量(可选，不选传NULL)
		parLogOperation[]	设备（电脑名或SMT机编号，可选，不选传NULL)
		parLogResource[]	资源名称（夹具，可选，不选传NULL)
		parWorkStation[]	工位(可选，不选传NULL)
		parRemark[]			备注(可选，不选传NULL)
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月17日
************************************************************************************/
Data_API int SplitComplete_New(char parSFC[], char parBoardCount[], char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
函数：	SplitNcComplete_New
功能：	对指定“位置”的SFC执行NcComplete操作
参数：
		parSFC[]			SFC
		parNcType			不良类型
		parNcCode[]			不良代码
		parNcContext		不良描述
		parFailItem			FAIL项（可选，不选传NULL）
		parFailValue		FAIL值（可选，不选传NULL）
		parBoardCount[]		分板数量(可选，不选传NULL)
		parLogOperation[]	设备（电脑名或SMT机编号，可选，不选传NULL）
		parLogResource[]	资源名称（夹具，可选，不选传NULL)
		parWorkStation[]	工位（可选，不选传NULL）
		parRemark[]			备注（可选，不选传NULL）
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月17日
************************************************************************************/
Data_API int SplitNcComplete_New(char parSFC[], char parNcTpye[], char parNcCode[], char parNcContext[], char parFailItem[], char parFailValue[], char parBoardCount[]
	, char parLogOperation[], char parLogResource[], char parWorkStation[], char parRemark[], char *retMessage);

/************************************************************************************
函数：	CompleteToStation_New
功能：	SFC工站改变
参数：
		parSFC[]			SFC
		parStationID		更改后的工站ID
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年10月26日
************************************************************************************/
Data_API int CompleteToStation_New(char parSFC[], char parStationID[], char *retMessage);

/************************************************************************************
函数：	ChangeSfcStation_New
功能：	修改SFC所在工站
参数：
		parSFC[]			SFC
		parNewStationID		新工站ID
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年10月26日
************************************************************************************/
Data_API int ChangeSfcStation_New(char parSFC[], char parNewStationID[], char *retMessage);

/************************************************************************************
函数：	ChangeSfcShoporder_New
功能：	修改SFC所在工单
参数：
		parSFC[]			SFC
		parNewSchedulingID	新排产ID
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年10月26日
************************************************************************************/
Data_API int ChangeSfcShoporder_New(char parSFC[], char parNewSchedulingID[], char *retMessage);

/************************************************************************************
函数：	Serializable_New
功能：	PSN 序列化为 BSN
参数：
		parSFC[]			PSN
		parNewSfcList[]		新SFC(BSN列表，格式为“SFC1;SFC2;……;SFCn”)
		*retMessage			返回的消息 PASS
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int Serializable_New(char parSFC[], char parNewSfcList[], char *retMessage);

/************************************************************************************
函数：	UnSerializable_New
功能：	PSN 反序列化
参数：
		parSFC[]			PSN
		*retMessage			返回的消息 PASS
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年10月24日
************************************************************************************/
Data_API int UnSerializable_New(char parSFC[], char *retMessage);

/************************************************************************************
函数：	ReworkToStation_New
功能：	SFC返工到某工站
参数：
		parSFC[]			SFC
		parStationID[]		返工目的工站ID（可选，与parStationName二选一，不选传NULL）
		parStationName[]	返工目的工站名称（可选，与parStationID二选一，不选传NULL）
		parAction[]			操作（写入SFC日志的ACTION字段，只能为REWORK或REPAIR_OK，可选，不选传NULL，默认为REWORK)
		parSfcState[]		返工后SFC的状态（可选，不选传NULL，默认为W）
		parRepairRework[]	是否维修返工(true表示是false表示否，可选，不选传NULL，默认false)
		parRemark[]			返工原因（可选，不选传NULL）
		parPreStationID[]	返工前一工站ID(可选，不选传NULL)
		*retMessage			返回信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月26日
************************************************************************************/
Data_API int ReworkToStation_New(char parSFC[], char parStationID[], char parStationName[], char parAction[], char parSfcState[], char parRepairRework[], char parRemark[]
	, char parPreStationID[], char *retMessage);

/************************************************************************************
函数：	SfcKeyCollect_New
功能：	关键物料收集(绑定)
参数：
		parSFC[]			SFC
		parData[]			关键物料数据(格式为“名称:值:允许重复采集的数量;……;名称:值:允许重复采集的数量”)
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月18日
************************************************************************************/
Data_API int SfcKeyCollect_New(char parSFC[], char parData[], char *retMessage);

/************************************************************************************
函数：	RemoveSFCKey
功能：	关键物料解绑
参数：
		parSFC[]			解绑关键物料的SFC
		parStationName[]	工站名称(可选，不选传NULL)
		parKeyName[]		绑定参数(可选，不选传NULL)
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月18日
************************************************************************************/
Data_API int RemoveSFCKey_New(char parSFC[], char parStationName[], char parKeyName[], char *retMessage);

/************************************************************************************
函数：	FindAccessoriesByIng_New
功能：	根据SFC查询其绑定的关键物料
参数：
		parSFC[]		SFC
		parShoporder[]	工单(可选，不选传NULL)
		parStation[]	工站名称(可选，不选传NULL)
		*retSfcKeyData	返回SFC绑定的关键物料数据（格式为“名称:值:规则:BYD料号|……|名称:值:规则:BYD料号”）
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月18日
************************************************************************************/
Data_API int FindAccessoriesByIng_New(char parSFC[], char parShoporder[], char parStation[], char *retSfcKeyData, char *retMessage);

/************************************************************************************
函数：	GetSfcsKeyBySfc_New
功能：	获取SFC及其序列化前所有SFC绑定的关键物料
参数：
		parSFC[]		序列化后的SFC
		*retSfcKeyData	返回SFC及其序列化前SFC绑定的关键物料，格式为“SFC:名称:值|……|SFC:名称:值”
		*retMessage		返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年05月13日
************************************************************************************/
Data_API int GetSfcsKeyBySfc_New(char parSFC[], char *retSfcKeyData, char *retMessage);

/************************************************************************************
函数：	ReplaceSfcSubKey_New
功能：	替换关键物料子物料
参数：
		parSFC[]		替换关键物料子物料的SFC
		parOldValue[]   绑定的旧值
		parNewValue[]	替换后的新值
		parNewBydPn[]	替换后的物料料号(可选，不选传NULL)
		*retMessage		返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月18日
************************************************************************************/
Data_API int ReplaceSfcSubKey_New(char parSFC[], char parOldValue[], char parNewValue[], char parNewBydPn[], char *retMessage);

/************************************************************************************
函数：	GetKeypartConfig_New
功能：	获取工站关键物料采集配置
参数：
		parSFC[]				SFC
		*retKeypartConfigData	返回工站关键物料采集配置，格式为“ID:名称:规则:允许重复采集的数量:备注:BYD料号:SFC是否需要完工(0是1否)|……|ID:名称:规则:允许重复采集的数量:备注:BYD料号:SFC是否需要完工(0是1否)”
		*retMessage				返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月26日
************************************************************************************/
Data_API int GetKeypartConfig_New(char parSFC[], char *retKeypartConfigData, char *retMessage);

/************************************************************************************
函数：	CreateNumbers_New
功能：	批量创建号码
参数：
		parNumberStore[]	号码库名称。（若有网标，此处也可传入网标）SN，IMEI1,IMEI2，BT，WIFI,KEYBOX, LUCKY,Battery
		parModel[]			需要分配的号码属于那个“MODEL”。(号码库有MODEL必选，无MODEL不选，不选传NULL)
		parNum[]			创建的号码数量(可选，默认1，不选传NULL)
		parModuleID[]		模块ID(可选，不选传NULL)
		parCustomStatus[]	自定义状态(可选，不选传NULL)
		parRemark[]			备注(可选，不选传NULL)
		*retNumberList		返回号码信息，格式为“号码名称1:号码值1;……;号码名称n:号码值n|……|号码名称1:号码值1;……;号码名称n:号码值n”
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int CreateNumbers_New(char parNumberStore[], char parModel[], char parNum[], char parModuleID[], char parCustomStatus[], char parRemark[], char *retNumberList
	, char *retMessage);

/************************************************************************************
函数：	CreateNumberBySfc_New
功能：	通过SFC创建号码
参数：
		parSFC[]			SFC
		parNumberStore[]	号码库名称。（若有网标，此处也可传入网标）SN，IMEI1,IMEI2，BT，WIFI,KEYBOX, LUCKY,Battery
		parModel[]			需要分配的号码属于那个“MODEL”。(号码库有MODEL必选，无MODEL不选，不选传NULL)
		parModuleID[]		模块ID(可选，不选传NULL)
		parCustomStatus[]	自定义状态(可选，不选传NULL)
		parRemak[]			备注(可选，不选传NULL)
		*retNumber			返回号码信息，格式为“号码名称1:号码值1;……;号码名称n:号码值n”
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int CreateNumberBySfc_New(char parSFC[], char parNumberStore[], char parModel[], char parModuleID[], char parCustomStatus[], char parRemak[], char *retNumber
	, char *retMessage);

/************************************************************************************
函数：	GetNumberBySfc_New
功能：	通过SFC分配号码
参数：
		parSFC[]			SFC
		parNumberStore[]	号码库的名称。（若有网标，此处也可传入网标）SN，IMEI1,IMEI2，BT，WIFI,KEYBOX, LUCKY,Battery
		parModel[]			需要分配的号码属于那个“MODEL”。(号码库有MODEL必选，无MODEL不选，不选传NULL)
		parModuleID[]       模块ID(可选，不选传NULL)
		parCustomStatus[]	自定义状态(可选，不选传NULL)
		parRemak[]			备注(可选，不选传NULL)
		*retNumber			返回号码信息，格式为“号码名称1:号码值1;……;号码名称n:号码值n”
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int GetNumberBySfc_New (char parSFC[], char parNumberStore[], char parModel[], char parModuleID[], char parCustomStatus[], char parRemark[], char *retNumber
	, char *retMessage);

/************************************************************************************
函数：	GetNumberInfo_New
功能：	获取号码相关信息
参数：
		parNumberStore[]	号码库
		parNumber[]			号码
		*retGroupNumbers	返回组号码列表，格式为“号码标题1:号码值1;……;号码标题n:号码值n”
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API int GetNumberInfo_New(char parNumberStore[], char parNumber[], char *retNumberInfo, char *retMessage);

/************************************************************************************
函数：	GetNumberInfo2_New
功能：	获取号码相关信息
参数：
		parNumberStore[]	号码库
		parNumber[]			号码
		*retNumberSfc		返回numberSfc 
		*retGroupNumbers	返回组号码列表，格式为“号码标题1:号码值1;……;号码标题n:号码值n”
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2018年11月21日
************************************************************************************/
Data_API int GetNumberInfo2_New(char parNumberStore[], char parNumber[], char *retNumberSfc, char *retNumberInfo, char *retMessage);

/************************************************************************************
函数：	GetNumberInfo3_New
功能：	获取号码相关信息
参数：
		parNumberStore[]	号码库
		parNumber[]			号码 
		*retNumberInfo		返回号码信息，格式为“numberSfc:SFC;numberModel:MODEL;shoporder:工单;status:状态(0未使用,1已使用,2:已作废);projectId:项目ID;productId:产品ID;numberLibraryId:号码库ID;batchid:上传批次号;customStatus:自定义状态”
		*retGroupNumbers	返回组号码列表，格式为“号码标题1:号码值1;……;号码标题n:号码值n”
		*retMessage			返回的消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2019年01月21日
************************************************************************************/
Data_API int GetNumberInfo3_New(char parNumberStore[], char parNumber[], char *retNumberInfo, char *retGroupNumbers, char *retMessage);

/************************************************************************************
函数：	TestDataCollect_New
功能：	测试数据采集到main和sub表中
参数：
		parSFC[]			产品的序列号SFC(可选，不选传NULL)
		parTdsName[]		测试数据采集表名称(可选，不选传NULL)
		parFixtureNo[]		夹具编号(可选，不选传NULL)
		parVersion[]		测试软件版本号(可选，不选传NULL)
		parSwVersion[]      产品的软件版本号(可选，不选传NULL)
		parHwVersion[]		产品的硬件版本号(可选，不选传NULL)
		parTestResult[]		测试结果(可选，不选传NULL)
		parFailItem[]		错误项(可选，不选传NULL)
		parFailValue[]		错误项的值(可选，不选传NULL)
		parNcCode[]			错误代码(可选，不选传NULL)
		parElapseTime[]		测试使用用时(可选，不选传NULL)
		parTestCount[]		测试次数(可选，不选传NULL)
		parTestDataList[]	测试数据列表（列表中多个数据用“|”隔开，可选，不传填NULL）
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API bool TestDataCollect_New(char parSFC[], char parTdsName[], char parFixtureNo[], char parVersion[], char parSwVersion[], char parHwVersion[], char parTestResult[]
	, char parFailItem[], char parFailValue[], char parNcCode[], char parElapseTime[], char parTestCount[], char parTestDataList[], char *retMessage);

/************************************************************************************
函数：	TestDataCollect_TXT_New
功能：	测试数据采集到main和sub表中(TXT版测试日志)
参数：
		parTestFile			TXT文件路径
		parTestCount[]		测试次数(可选，不选传NULL)
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API bool TestDataCollect_TXT_New(char parTestFile[], char parTestCount[], char *retMessage);

/************************************************************************************
函数：	TestDataCollect_XML_New
功能：	测试数据采集到main和sub表中(XML版测试日志)
参数：
		parTestFile[]		XML文件路径
		parTestContent[]	XML文件内容
		parTestCount[]		测试次数(可选，不选传NULL)
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年04月20日
************************************************************************************/
Data_API bool TestDataCollect_XML_New(char TestFile[], char parTestContent[], char partTestCount[], char *retMessage);

/************************************************************************************
函数：	TestDataCollect2MainChild_New
功能：	测试数据采集到main和child表中
参数：
		parSFC[]			产品的序列号SFC(可选，不选传NULL)
		parTdsName[]		测试数据采集表名称(可选，不选传NULL)
		parFixtureNo[]		夹具编号(可选，不选传NULL)
		parVersion[]		测试软件版本号(可选，不选传NULL)
		parSwVersion[]      产品的软件版本号(可选，不选传NULL)
		parHwVersion[]		产品的硬件版本号(可选，不选传NULL)
		parTestResult[]		测试结果(可选，不选传NULL)
		parFailItem[]		错误项(可选，不选传NULL)
		parFailValue[]		错误项的值(可选，不选传NULL)
		parNcCode[]			错误代码(可选，不选传NULL)
		parElapseTime[]		测试使用用时(可选，不选传NULL)
		parTestCount[]		测试次数(可选，不选传NULL)
		parText[]			文本内容（可选，不传填NULL）
		parTestDataList[]	测试数据列表（格式为“名称;值;最大值;最小值;标准值;单位;测试时间(yyyy-MM-dd HH:mm:ss);测试人;位置号;测试结束时间;测试结果;错误代码;PN;备注;文本内容
											|……|名称;值;最大值;最小值;标准值;单位;测试时间(yyyy-MM-dd HH:mm:ss);测试人;位置号;测试结束时间;测试结果;错误代码;PN;备注;文本内容”
							，可选，不传填NULL）
		*retMessage			返回的错误消息
		parContinue[]       是否将SN写入备份表：1表示写入，其他表示不写入
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年07月27日
************************************************************************************/
Data_API bool TestDataCollect2MainChild_New(char parSFC[], char parTdsName[], char parFixtureNo[], char parVersion[], char parSwVersion[], char parHwVersion[], char parTestResult[]
	, char parFailItem[], char parFailValue[], char parNcCode[], char parElapseTime[], char parTestCount[], char parText[], char parTestDataList[], char parContinue[], char *retMessage);

/************************************************************************************
函数：	Binding_NEW
功能：	扣料
参数：  parSFC[] 产品的序列号SFC
		parMultiple[] 扣料倍数
		parBoardCount[] 分板数量（可选，不填传null）
		*parCountInfo 投入产出信息,格式：IN_QTY:投入数量;OUT_QTY:产出数量;FAIL_QTY:不良数量;WASTE_QTY:报废数量;BINDING_QTY:扣料数量
		*refstrMessage 返回的错误信息
返回：	如果成功则返回1，否则返回0
编辑时间：2018-3-28 HSX
*************************************************************************************/
Data_API bool Binding_NEW(char sfc[], char multiple[], char *countInfo, char *refstrMessage);

/************************************************************************************
函数：	CheckAllStationEquipment_New
功能：	检查所有工站设备是否上齐
参数：  *refstrMessage 返回的错误信息
返回：	如果成功则返回1，否则返回0
编辑时间：2018-3-29 HSX
*************************************************************************************/
Data_API bool CheckAllStationEquipment_New(char *refstrMessage);

/************************************************************************************
函数：	GetProjectEquipment_New
功能：	获取项目、工站所需要的设备清单
参数：  parIsContinue[] 当设备清单为空时是报错还是返回空，为0时报错
		*retData 返回的设备信息，格式：PROJECT_ID:项目ID;PROJECT_NAME:项目名称;EQ_TYPE_ID:设备类型ID;EQ_TYPE_NAME:设备类型名称;EQ_PROPERTY:设备属性;STATION_NAME:工站名称;PRODUCT_ID:产品ID;PRODUCT_NAME:产品名称|...
		*refstrMessage 返回的错误信息
返回：	如果成功则返回1，否则返回0
编辑时间：2018-3-29 HSX
*************************************************************************************/
Data_API bool GetProjectEquipment_New(char parIsContinue[], char *retData, char *refstrMessage);

/************************************************************************************
函数：	CheckEquipmentUseQty_New
功能：	校验设备使用次数
参数：
		parSFC[]			SFC
		parEquipmentNo[]	资产编号或设备编号
		*retMessage			返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2018年08月09日
*************************************************************************************/
Data_API bool CheckEquipmentUseQty_New(char parSFC[], char parEquipmentNo[], char *retMessage);

/************************************************************************************
函数：	GetLineLossState_New
功能：	获取线损点检状态
参数：
		parFixture[]		夹具编号
		*retLineLossState	返回的线损点检状态
		*retMessage			返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2019年01月21日
*************************************************************************************/
Data_API bool GetLineLossState_New(char parFixture[], char *retLineLossState, char *retMessage);

/************************************************************************************
函数：	AddLineLossCheck_New
功能：	增加线损点检记录
参数：
		parFixture[]	夹具编号
		parPcID[]		PC编号
		parRfLine[]		射频线编号
		parInstrument[]	仪器编号
		parFilePath[]	点检文件地址
		*retMessage		返回的错误信息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2019年01月25日
*************************************************************************************/
Data_API bool AddLineLossCheck_New(char parFixture[], char parPcID[], char parRfLine[], char parInstrument[], char parFilePath[], char *retMessage);

/************************************************************************************
函数：	AddEquipmentInfoKeyList_New
功能：	设备信息采集
参数：  parEquNo[] 设备编号(必填)
		parEquType[] 设备类型(必填)
		char parSN[] 产品SN(选填，不填传null)
		parLine[] 线体(选填，不填传null)
		parOperateName[] 操作人(选填，默认取登录ID人姓名，不填传null)
		parOperateTime[] 操作时间(选填，默认取调用接口时间，格式：yyyy-MM-dd HH:mm:ss，不填传null)
		parKeys[] 需上传属性键值对（必填，格式为：“名称1:值1;名称2:值2...”）
		*refstrMessage 当失败时返回的错误信息
返回：	如果成功则返回1，否则返回0
编辑时间：2018-01-08 HSX
*************************************************************************************/
Data_API bool AddEquipmentInfoKeyList_New(char parEquNo[], char parEquType[], char parSN[], char parLine[], char parOperateName[], char parOperateTime[], char parKeys[], char* refstrMessage);

/************************************************************************************
函数：	ResetMesConfig_New
功能：	获取工单工站信息，并重置\cfg\mes_config.ini文件
参数：
		parShoporder[]	工单
		parStation[]	工站名称
		*retMessage		返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2018年08月03日
************************************************************************************/
Data_API bool ResetMesConfig_New(char parShoporder[], char parStation[], char *retMessage);

/************************************************************************************
函数：	GetPanguTbOrderPpid_New
功能：	获取盘古ORDER_PPID表数据
参数：
		ppid[]		        PPID,即SFC
		*retOrderPpidInfo   返回ORDERPPID信息,数据格式 "(第1条数据)名称1:值1;.......名称n:值n|(第2条数据)名称1:值1;.......名称n:值n|......|(第n条数据)名称1:值1;.......名称n:值n"
		*retMessage			返回的错误消息
返回：	如果成功则返回1，否则返回0
作者：	BYD 电子事业群执行副总裁办公室 申志芳 2017年05月24日
************************************************************************************/
Data_API bool GetPanguTbOrderPpid_New(char ppid[],char *retOrderPpidInfo, char *retMessage);

#pragma endregion 优化后的接口
