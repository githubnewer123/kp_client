#coding=utf-8
import datetime
import time
from ctypes import Structure
from ctypes import c_int, c_char_p, POINTER, c_ulong, c_uint,c_void_p,c_byte
from ctypes import cdll, CDLL,cast
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from base64 import b64encode
from adapter_utils import is_secure_chip_for_alipay

class KpLightKeyInfo(Structure):
    pass

KpLightKeyInfo._fields_ = [
    ('iType', c_int),#huk ,equals the huk when pull pass to interface
    ('iKeyLen', c_int),# chip id
    ('pKeyData', POINTER(c_byte)),# error msg
    ('pNext', POINTER(KpLightKeyInfo)),#next kp result,null if no more
]

class KpLightResult(Structure):
    pass

KpLightResult._fields_ = [
    ('pId', c_char_p),#huk ,equals the huk when pull pass to interface
    ('pCid', c_char_p),# chip id
    ('pDescribe', c_char_p),# error msg
    ('pKeyInfoHead', POINTER(KpLightKeyInfo)),#kp data 
    ('pNext', POINTER(KpLightResult)),#next kp result,null if no more
]


class KpHSecResult(Structure):
    pass

KpHSecResult._fields_ = [
    ('pHuk', c_char_p),#huk ,equals the huk when pull pass to interface
    ('pCid', c_char_p),# chip id
    ('pDescribe', c_char_p),# error msg
    ('pKpData', POINTER(c_byte)),#kp data 
    ('iKpDataLen', c_int),#kp data len
    ('iIsValidKp', c_int),#if kp is validate ,if ==0m means it is a invaldate kp
    ('pNext', POINTER(KpHSecResult)),#next kp result,null if no more
]


class KpResponse(Structure):
    _fields_ = [
        ('iCode', c_int),#kp server response code, if !=0 means error ocurs
        ('pMessage', c_char_p),#server error message
        ('chipType', c_byte * 32),#server error message
        ('pResultHead', c_void_p),#pull result list
    ]

PULL_CHIP_TYPE_HSEC = b"HSC32I1"
PULL_CHIP_TYPE_LIGHT = b"light"
PULL_CHIP_TYPE_WP_LX100 = b"WP_LX100"
PULL_CHIP_TYPE_DK_LX100 = b"DK_LX100"
PULL_CHIP_TYPE_CHIXIAO = "CV181x".encode("utf-8")
HOST = b"http://10.63.56.57"  # 拉取地址
HOST_ONLINE = b"http://dailyocc.aliyun-inc.test"
ONLINE_SIGN_PRIVATE_KEY = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIJ+WFkw982zrmEVb0U/rom6Cp46Z7Oji69zNcMJTc7DLRbV5+UAGSytk2uXkRygxEavzl9ozudx18RYJhyzgaiWOlCGJiJ57nTaGp0aqyUjwdQ/z8VOxkVM3XZPgn21PQzXLycp3c9qAn9uLXymM3RnRmKTfRmjb8GsN7ySjGqvAgMBAAECgYA5kWOIdYHczZfwXHRqKF3nhJuKklmNdmj5Teo50LDytkf9+wAClriEbU7L+GGcL5BnXse8b5BXqnF1vS2TG93my9JP/e4LoiHgkErbNYk5YrDR0gKLjG/aV0P1WDVKXl0oHOpvEgstJhCMs4McZrpmGi1XsTWn2yxb6q7MjYS3AQJBAOkOK21+0UZw+pzKPVcwp25HjEkPnz9RA1oRY/DH12pGCUD/fBmTIsQJ1DLiMjbBkH25kSuu38JDD056EllR+ZkCQQCPV0AC/skNr5ryRMv/OXk2Kp81VKRMatsINF8wl34GnNqN8lwvFdaScOxdS//4hcCYe80GyMMm1uw/VA5GrQOHAkEA5zaamTAW+ba+u+zc/HKVuZAcOqPYDt4V4Daem1P4gEPpjGWrvke+VxWVQ8IrpS1WZ5VB1D/TWIxlVCtBpwHwCQJAdXOEm++xRmmRiNoeXW72hw+9jLFiPst/1eUz6lj3huuXmZ/xMROv0iZ9RqUzhKvz9/3ZLanrXjPVOL7jQ74YmQJAOwEF5HQuaiJ2mWSs0Z0T8aXyjnX/xTO2PfFNS2TqOU40meqDUTaZRsKsDUyHTvp7UDd71VMZKrpQjh2hh/1cIQ=="
REPORT_PATH = b"/api/occ/kp/report"

#init apis
api = CDLL('./libkp_client.so')
api.sim_chip_create.argtypes = [c_char_p,c_int]
api.sim_chip_create.restype = c_int

api.sim_chip_get_huk.argtypes = [c_char_p,c_char_p,c_int]
api.sim_chip_get_huk.restype = c_int

api.sim_chip_destroy.argtypes = [c_char_p]
api.sim_chip_destroy.restype = c_int

api.sim_chip_store_kr.argtypes = [c_char_p,c_char_p,c_char_p,c_char_p]
api.sim_chip_store_kr.restype = c_int

api.sim_chip_fetch_kr.argtypes = [c_char_p,c_char_p,c_char_p]
api.sim_chip_fetch_kr.restype = c_int

api.sim_chip_burn_kr.argtypes = [c_char_p,c_char_p,c_char_p]
api.sim_chip_burn_kr.restype = c_int

api.sim_chip_read_burned_kr.argtypes = [c_char_p,c_char_p,c_char_p]
api.sim_chip_read_burned_kr.restype = c_int

api.sim_kr_dump_key.argtypes = [c_char_p, c_char_p,c_char_p]
api.sim_kr_dump_key.restype = c_int

api.sim_chip_kr_update_key.argtypes = [c_char_p, c_char_p,c_char_p,c_char_p]
api.sim_chip_kr_update_key.restype = c_int

api.sim_chip_supported_list.argtypes = [c_char_p]
api.sim_chip_supported_list.restype = c_int

api.sim_kr_huk_verify_hsec.argtypes = [c_char_p, c_char_p]
api.sim_kr_huk_verify_hsec.restype = c_int

api.sim_kr_head_hash_verify_hsec.argtypes = [c_char_p]
api.sim_kr_head_hash_verify_hsec.restype = c_int

api.sim_kr_credent_content_verify_hsec.argtypes = [c_char_p,c_char_p,c_char_p,c_char_p]
api.sim_kr_credent_content_verify_hsec.restype = c_int

api.sim_kr_credent_hash_verify_hsec.argtypes = [c_char_p]
api.sim_kr_credent_hash_verify_hsec.restype = c_int

api.sim_kr_sad_verify_hsec.argtypes = [c_char_p]
api.sim_kr_sad_verify_hsec.restype = c_int

api.sim_kr_content_verify_light.argtypes = [c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]
api.sim_kr_content_verify_light.restype = c_int

api.csi_kp_pullup_offline.argtypes = [c_char_p, c_char_p, c_int, c_char_p, POINTER(c_char_p),c_char_p]
api.csi_kp_pullup_offline.restype = POINTER(KpResponse)

api.csi_kp_pullup_online.argtypes = [c_char_p, c_char_p, c_int, c_char_p, c_char_p,c_char_p,c_char_p]
api.csi_kp_pullup_online.restype = POINTER(KpResponse)

api.sim_encrypt_kr.argtypes = [c_char_p, c_char_p, c_char_p]
api.sim_encrypt_kr.restype = c_int

api.sim_sign_kr.argtypes = [c_char_p, c_char_p, c_char_p]
api.sim_sign_kr.restype = c_int

api.sim_get_provision_security_level.argtypes = [c_char_p]
api.sim_get_provision_security_level.restype = c_int

api.csi_kp_releaseResult.argtypes = [POINTER(KpResponse)]

def get_huks(chip_type, count):
    huk = b'\0' * (33 * count)
    ret = api.sim_chip_get_huk(chip_type, huk,count)
    if(ret):
        print("sim_huk_get failed ret:%d"%ret)
        return None

    return huk.split(b"|")

def pull_kp(pull_model,pull_license,pull_count,chip_type, huks_set):
    if(is_secure_chip_for_alipay(chip_type)):
        PULL_BATCH_PATH = b"/api/occ/kp/getKpInfo"
    elif(chip_type == PULL_CHIP_TYPE_LIGHT):
        PULL_BATCH_PATH = b"/api/occ/kp/pull"
    else:
        return -1
    url = HOST + PULL_BATCH_PATH

    pullHuksArray = c_char_p * pull_count
    huks = pullHuksArray()
    for i in range(pull_count):
        huks[i] = huks_set[i]

    return api.csi_kp_pullup_offline(url, pull_model, pull_count, pull_license, huks,chip_type)#pull kp


def sign(signData,privatekey):
    private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + privatekey + "\n-----END RSA PRIVATE KEY-----"
    rsa_key = RSA.importKey(private_key)
    signer = pkcs1_15.new(rsa_key)
    digest = SHA256.new(signData.encode('utf8'))
    sign = b64encode(signer.sign(digest)).decode('utf8')
    return sign

def pull_kp_online(huk,product_id,private_key,chip_type):
    PULL_BATCH_PATH = b"/api/core/product/getHukInfo"
    url = HOST_ONLINE + PULL_BATCH_PATH
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    suffix = str(timestamp%100000)
    sign_data = sign(product_id.decode("utf-8") + str(timestamp) + suffix, private_key)

    return api.csi_kp_pullup_online(url, product_id, timestamp, suffix.encode("utf-8"), huk, sign_data.encode("utf-8"),chip_type)#pull kp

def get_kr_list(kr_list):
    try:
        start_str = "Start_of_operation"
        end_str = "End_of_operation"
        start = kr_list.index(start_str)
        end = kr_list.index(end_str)
        json_data = eval(kr_list[start + len(start_str):end])
        return json_data
    except:
        return None

def hsec_verify(read_burn_kr, huk):
    ret = api.sim_kr_huk_verify_hsec(read_burn_kr, huk)
    if(ret):
        print("sim_kr_huk_verify_hsec failed ret:%d"%ret)
        return -1

    ret = api.sim_kr_head_hash_verify_hsec(read_burn_kr)
    if(ret):
        print("sim_kr_head_hash_verify_hsec failed ret:%d"%ret)
        return -2
        
    ret = api.sim_kr_credent_content_verify_hsec(read_burn_kr,b"ECDH",b"MOCK_MODEL",b"QZCRD")
    if(ret):
        print("sim_kr_credent_content_verify_hsec failed ret:%d"%ret)
        return -3
    
    ret = api.sim_kr_credent_hash_verify_hsec(read_burn_kr)
    if(ret):
        print("sim_kr_credent_hash_verify_hsec failed ret:%d"%ret)
        return -4
        
    ret = api.sim_kr_sad_verify_hsec(read_burn_kr)
    if(ret):
        print("sim_kr_sad_verify_hsec failed ret:%d"%ret)
        return -5
    return 0

def light_verify(kr):
    CVKEY2_SKEY = b"08fa21f696c04345"
    USRKEY2_SKEY = b"2a64bfeaaba889f4"
    ROOTCKEY_C = b"cc1192239de7a38ffd8f2d3d053fbb0680f5a0f887f90b33034ba98a81f18cca"
    HASH_ROTPK = b"039ef0a18795310525ddc12a9c7eaf1e7450967bc9a22f4c6dd8d7efcae3bdcd"
    HASH_DEBUGPK = b"032fee0a44200f69fdd1131bcfc239c3934f405d716faadfc702cf12650ddf68"

    ret = api.sim_kr_content_verify_light(kr,USRKEY2_SKEY,CVKEY2_SKEY,ROOTCKEY_C,HASH_ROTPK,HASH_DEBUGPK)
    if(ret):
        print("sim_kr_content_verify_light failed ret:%d"%ret)
        return -9
    print("light_verify success")
    return 0

def test_kr_and_chip():
    kr_size_max = 1024 * 8
    chip_type = PULL_CHIP_TYPE_HSEC
    PULL_COUNT = 3
    
    ret = api.sim_chip_create(chip_type, PULL_COUNT)
    if(ret):
        print("sim_chip_create failed ret:%d"%ret)
        return -1

    huks = get_huks(chip_type, PULL_COUNT)
    if(huks == None):
        print("get huks failed")
        return -1
    
    kr_test = "Start_of_operation\r\n[{'cid': 'd0325c29eca94bdd9b45355ae3b5f3bd', 'huk': '00000000000000000000000000000000', 'kr': '496e44780300000004000100f4000000040020000000000080000000000d00103b00200000000000a0000000ffffffff3e00100000000000c0000000ffffffff5000240000000000d0000000ffffffff2602e54c4ef5329ae5b7b2a1ffeda660c3d8f78b0000000000000000000000000000000000000000000000000000000064303332356332396563613934626464396234353335356165336235663362646e7595da247e8db0ff461cf765fa7e1546044c1083ec0bd4236a60179cfb14eb000000000000000000000000000000001f0400002a5b34172ff533f79abd16ed58c16759dec793f54fb2cbbc660e8cfaee3a7ac30000000000000000000000007b22707269766174654b6579223a2234343064376133653433623436316266346361306230383635663766623836626337326161633137613332326432393734333835383237663832383563376135222c2273756363657373223a747275652c226465766963654365727469666963617465223a7b2263657274497373756572223a224f50454e415049222c22636f6d70616e79436f6465223a2232303231303033313330363837383534222c22646576696365496e666f726d6174696f6e223a7b22646576696365496d6569223a22646576696365496d6569222c226465766963654d6163223a226465766963654d6163222c22646576696365536e223a226430333235633239656361393462646439623435333535616533623566336264227d2c226578747261506172616d73223a7b226665617475726573223a5b22414e545f464f5252455354222c225452414e53504f5254222c225041594d454e54225d7d2c2270726f647563744d6f64656c223a224d4f434b5f4d4f44454c222c2270726f6475637454797065223a22515a435244222c227075626c69634b6579223a222d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d5c6e4d466b77457759484b6f5a497a6a3043415159494b6f5a497a6a304441516344516741457a714b5a4d326f6648364458496e34647a4b69574535336b346f4e505c6e586f336d43556a7044574163647539476e6f4d576d474b6b69794a643147574b632f717345486e42557658625a556271474963774e53686f2f673d3d5c6e2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d5c6e222c2273656375726974794e65676f74696174696f6e223a2245434448222c227369676e223a226345626c734d545a58744230445274577355564a777a6f67566c526c426c4c376b3074465148375836592b4d45307544357a466b765965484b796d7a5371646f55674267704d2f41675a5866696a744876336f63594a595737712f516233363157392f514230314e4e6d2b374c3653652b66746867767a5147664b52585949644d65675052646a304f7a522b2f416477774d50476458593349476a714155536e456a4d74756f5939666d304d74514546772f6a494f52556f38473864536b436b6a79546a6e6239786979796e7772434d4f737a362b377546324d693159454c5879526d31797a3450614b655274636859327973614f5434532f416d4936306f745541644a735a6a733577514b6a756d57686d4e73592b344c724572696b624b796b512b37417853743674322f53394a50387770707066364f6c38787a76554f46326f4f712f75775a2b4264753157716c36307a4170413d3d222c227369676e416c676f726974686d223a224241534536345f4f5645525f52534132303438222c22736e223a2232303233303230363139313333393233353438333436227d7d'}, {'cid': '85124ebc797348d4bb853dc66fcb3ef4', 'huk': '00000000000000000000000000000001', 'kr': '496e44780300000004000100f4000000040020000000000080000000000d00103b00200000000000a0000000ffffffff3e00100000000000c0000000ffffffff5000240000000000d0000000ffffffffb010fc606bc8ee2249122030c974d6800cc9c5a800000000000000000000000000000000000000000000000000000000383531323465626337393733343864346262383533646336366663623365663461eb1a87993e604e5d5f50a8740f8c174df6c1b7016aa0c2b9c692b50b3d6d19000000000000000000000000000000011f04000027efecfc8c3acec498ecfd54883bd3a480aa2e14e68e68bb6dcb72c53ab7dfff0000000000000000000000007b22707269766174654b6579223a2264383266383866613731303365393032626130633366616165633138326164356333613137656161373935663033353564656565373866323766653265633531222c2273756363657373223a747275652c226465766963654365727469666963617465223a7b2263657274497373756572223a224f50454e415049222c22636f6d70616e79436f6465223a2232303231303033313330363837383534222c22646576696365496e666f726d6174696f6e223a7b22646576696365496d6569223a22646576696365496d6569222c226465766963654d6163223a226465766963654d6163222c22646576696365536e223a223835313234656263373937333438643462623835336463363666636233656634227d2c226578747261506172616d73223a7b226665617475726573223a5b22414e545f464f5252455354222c225452414e53504f5254222c225041594d454e54225d7d2c2270726f647563744d6f64656c223a224d4f434b5f4d4f44454c222c2270726f6475637454797065223a22515a435244222c227075626c69634b6579223a222d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d5c6e4d466b77457759484b6f5a497a6a3043415159494b6f5a497a6a304441516344516741455979656c6352722f42364f49595963542f63546f4a62377a313834395c6e71757073317a464e7144597068574a79664c6a4d4330462f767a64745a49544e465232356f426667513932703637754377656f766369447957413d3d5c6e2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d5c6e222c2273656375726974794e65676f74696174696f6e223a2245434448222c227369676e223a226a514c5a694e423035782f6b5469374e436457712b2b795a6b6f5249666233484e7a615475344a3142464c4d695376386f447447477a4574434d755135713464672b69666b776e4f533774655a4b633059494c44643671644745693637783944772b4645387042692b79556c666c747a6f55455656646e5565356165666c326c2b4f68614b4c53755470326a35384837315a5a77676266634f4c6d42474441703462597a3476464e496f44666a6a485954576a66374d626273384270706a77386131713657334e53382f4c484f2b665736684e2b305752557a4477674a726344572b325968316d596e755978303147767968477a5a374e68334551523336646639615637794d3458715742494f2f5254626a7739745a554168366a53646145654d725670784c33707941326d6336446467506b7678426b7653572f7970664e77486e49334569713354727244382f7777346e307853413d3d222c227369676e416c676f726974686d223a224241534536345f4f5645525f52534132303438222c22736e223a2232303233303230363139313333393339373730303734227d7d'}]\r\nEnd_of_operation"
    #kr_test = "Start_of_operation\r\n[{'cid': 'fc0f34db9c3b4747b43f9f4904c831b5', 'huk': '00000000000000000000000000000000', 'kr': '496e447803000000080001003c0200000400200000000000c0000000000d00103200080000000000e0000000ffffffff3300080000000000e8000000ffffffff3400100000000000f0000000ffffffff360020000000000000010000ffffffff370020000000000020010000ffffffff390020000000000040010000ffffffff3a0020000000000060010000ffffffff427655c480c73dfb3b5b3540ddbf0ece8d4fb223000000000000000000000000000000000000000000000000000000006663306633346462396333623437343762343366396634393034633833316235fdeb3b3dc36d4e776b6d57a8a67f95eb9897768eee7608af3a303362cd83d3a5bdd005e101c1c0a6bb6ba61bbdb04610e4ee3fd306000f34698bf55d4c89b3aa3a4db9e3cd006c3bb303e429a31da4c208fb4d65cb0583284cd394c92c79e24a5fe0da726b99bd199a29771dc0f1563944b879811f38d292ba9a60799dc4f13160aee37d38549cb8c77fc3b9d87f493f44d6bc2e80a441eae6a6204d7157d8b0'}, {'cid': 'ec7e97fdde4d44139a4d585c72ad7a46', 'huk': '00000000000000000000000000000001', 'kr': '496e447803000000080001003c0200000400200000000000c0000000000d00103200080000000000e0000000ffffffff3300080000000000e8000000ffffffff3400100000000000f0000000ffffffff360020000000000000010000ffffffff370020000000000020010000ffffffff390020000000000040010000ffffffff3a0020000000000060010000ffffffffb67dd0e094ab4402174e5824de8696c34c138547000000000000000000000000000000000000000000000000000000006563376539376664646534643434313339613464353835633732616437613436fdeb3b3dc36d4e776b6d57a8a67f95eb240caeaee33692fe18b8c7bb91163ae0e9723852a78b746982a83101fc33938b9184f8b12404d9e57f144a10e29c562e3a4db9e3cd006c3bb303e429a31da4c208fb4d65cb0583284cd394c92c79e24a5fe0da726b99bd199a29771dc0f1563944b879811f38d292ba9a60799dc4f13160aee37d38549cb8c77fc3b9d87f493f44d6bc2e80a441eae6a6204d7157d8b0'}, {'cid': '936a9dd441b34c43a5481a33628a8c32', 'huk': '00000000000000000000000000000003', 'kr': '496e447803000000080001003c0200000400200000000000c0000000000d00103200080000000000e0000000ffffffff3300080000000000e8000000ffffffff3400100000000000f0000000ffffffff360020000000000000010000ffffffff370020000000000020010000ffffffff390020000000000040010000ffffffff3a0020000000000060010000ffffffff7dbb4772e74b851df806204c5d0f0dae65f1a7f0000000000000000000000000000000000000000000000000000000003933366139646434343162333463343361353438316133333632386138633332fdeb3b3dc36d4e776b6d57a8a67f95eb2ad257d957b252e7cffb4efc1ba6898f9fe826c259cc6a4a9095f4258d393027d7b58b34f0cc831ea390261fd69b3d073a4db9e3cd006c3bb303e429a31da4c208fb4d65cb0583284cd394c92c79e24a5fe0da726b99bd199a29771dc0f1563944b879811f38d292ba9a60799dc4f13160aee37d38549cb8c77fc3b9d87f493f44d6bc2e80a441eae6a6204d7157d8b0'}]\r\nEnd_of_operation"
    kr_list = get_kr_list(kr_test)
    # response = pull_kp(PULL_MODEL,PULL_LICENSE,PULL_COUNT,chip_type,huks)
    # if(response == None or response.contents.iCode != 0 or response.contents.pResultHead == None):
    #     print("pull_kp failed")
    #     api.csi_kp_releaseResult(response)
    #     return -2
    
    for i in range(0,len(kr_list)):
        ret = api.sim_chip_store_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),kr_list[i]["cid"].encode("utf-8"),kr_list[i]["kr"].encode("utf-8"))
        if(ret):
            print("sim_chip_store_kr failed ret:%d"%ret)
            return -3
        
        chip_kr = b'\0'*4096
        ret = api.sim_chip_fetch_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        if(ret):
            print("sim_chip_fetch_kr failed ret:%d"%ret)
            return -4
        # chip_kr = chip_kr.decode("utf-8").encode("utf-8")
        
        # ret = api.sim_sign_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        # if(ret):
        #     print("sim_sign_kr failed ret:%d"%ret)
        #     return -5

        # ret = api.sim_encrypt_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        # if(ret):
        #     print("sim_encrypt_kr failed ret:%d"%ret)
        #     return -5

        # ret = api.sim_decrypt_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        # if(ret):
        #     print("sim_decrypt_kr failed ret:%d"%ret)
        #     return -5

        # ret = api.sim_encrypt_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        # if(ret):
        #     print("sim_encrypt_kr failed ret:%d"%ret)
        #     return -5
    
        ret = api.sim_chip_burn_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),chip_kr)
        if(ret):
            print("sim_chip_burn_kr failed ret:%d"%ret)
            return -5
        
        # read_burn_kr = b'\0'*4096
        # ret = api.sim_chip_read_burned_kr(chip_type,kr_list[i]["huk"].encode("utf-8"),read_burn_kr)
        # if(ret):
        #     print("sim_chip_read_burned_kr failed ret:%d"%ret)
        #     return -6
    
        # ret = api.sim_chip_kr_update_key(chip_type,read_burn_kr,b"CREDENT_LEN",b"12")
        
        # if(ret):
        #     print("sim_chip_kr_update_key failed ret:%d"%ret)
        #     return -7

        # # if(chip_type == PULL_CHIP_TYPE_LIGHT):
        # #     light_verify(read_burn_kr)
        # # elif(chip_type == PULL_CHIP_TYPE_HSEC):
        # #     hsec_verify(read_burn_kr,kr_list[i]["huk"].encode("utf-8"))
        
  
        # json_out = b'\0'*10000
        # ret = api.sim_kr_dump_key(chip_type,read_burn_kr,json_out)
        # if(ret):
        #     print("sim_kr_dump_key failed ret:%d"%ret)
        #     return -6
        # print(json_out)
        
        # # print(json_out.decode("utf-8"))
        
    return 0

if __name__ == '__main__':
    # data1 = b"0"*256
    # ret = api.sim_chip_supported_list(data1)
    # print(data11)

    #     print("sim_chip_supported_list failed ret:%d"%ret)
    # api.test_rsa()
    # api.sim_set_provision_security_level(b"Anitplay")
    test_kr_and_chip()
    
    #pull_kp_online(b"0011223344556677",b"4134029307733413888",ONLINE_SIGN_PRIVATE_KEY,PULL_CHIP_TYPE_CHIXIAO)
