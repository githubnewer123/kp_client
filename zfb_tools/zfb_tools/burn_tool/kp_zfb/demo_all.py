import os
SIM_HUK_VERIFY_ERROR = 5
import threading
from adapter_utils import is_secure_chip_for_alipay

def print(*a):
    pass

def thread_pressure(demo_all,thread_name,chip_type,module,license,huks):
    demo_all.thread_results[thread_name] = -100
    # demo_all.thread_results[thread_name] = 0
    # return 0
    for i in range(0,len(huks)):
        """Calling Linux KP simulation interface,pull"""
        ls_results, ls_cids = demo_all.pull_kr(chip_type, module,license, [huks[i]])
        if(not ls_results and len(ls_results) == 0):
            demo_all.thread_results[thread_name] = -1
            break

        """ Calling Linux KP simulation interface,Store kr """
        store_kr = demo_all.store_kr(chip_type, ls_cids[0], ls_results[0]["huk"], ls_results[0]["kr"])
        if(store_kr != 0):
            demo_all.thread_results[thread_name] = -2
            break
    
        """Calling Linux KP simulation interface,read kr """
        read_kr = demo_all.read_kr(chip_type, ls_results[0]["huk"])
        if(not read_kr):
            demo_all.thread_results[thread_name] = -3
            break
        
        """Calling Linux KP simulation interface,set kr to store different"""
        set_storage = demo_all.set_provision('Anitplay')
        if(set_storage != 0):
            demo_all.thread_results[thread_name] = -4
            break
    
        """Calling Linux KP simulation interface,burn kr """
        burn_kr = demo_all.burn_kr(chip_type, ls_results[0]["huk"], read_kr)
        if(burn_kr != 0):
            demo_all.thread_results[thread_name] = -5
            break
        
        """Calling Linux KP simulation interface,report kr """
        used = demo_all.report_kr(chip_type, ls_cids)
        if (used != 0):
            demo_all.thread_results[thread_name] = -6
            break
        
    if(demo_all.thread_results[thread_name] == -100):
        demo_all.thread_results[thread_name] = 0

class DemoAll:
    def __init__(self):
        self.thread_results = {}
    
    def read_wsl_output(self,output):
        try:
            start_str = "Start_of_operation"
            end_str = "End_of_operation"
            start = output.index(start_str)
            end = output.index(end_str)
            return eval(output[start + len(start_str):end])
        except:
            return None

    def make_sim_adapter_params(self,*a):
        if(len(a) <= 0):
            return ""
        
        args = ""
        for i in range(1,len(a)):
            data_type,input_type,content = a[i]
            args += " \"%s_%s_%s\""%(data_type,input_type,content)

        return "python3 sim_adapter.py %s%s"%(a[0],args)

    #pull拉取
    def pull_kr(self,chip_type,model,license,huks):
        #python3 demo_pull.py  pull test_type 2 HSC32I1 f072f920d28840f8bb9024733eaf84e0-f072f920d28840f8bb9024733eaf84e1 permission_smoke
        command = "python3 demo_pull.py pull %s %d %s %s %s"%(model,len(huks),chip_type,"-".join(huks),license)
        output = self.exec_python_wsl(command)
        result = self.read_wsl_output(output)
        if(not result or result["ret"] != 0):
            print("pull failed")
            return [],[]
        
        results = result["results"]
        cids = []
        for i in range(0,len(results)):
            cids.append(results[i]["cid"])
        print("pull ok")
        
        return results,cids
    
    #pull拉取
    def pull_kr_online(self,chip_type,product_id,private_key,huk):
        #python3 demo_pull.py  pull test_type 2 HSC32I1 f072f920d28840f8bb9024733eaf84e0-f072f920d28840f8bb9024733eaf84e1 permission_smoke
        command = "python3 pull_online.py pull \"%s\" \"%s\" \"%s\" \"%s\""%(chip_type,product_id,private_key,huk)
        output = self.exec_python_wsl(command)
        result = self.read_wsl_output(output)
        if(not result or result["ret"] != 0):
            print("pull failed")
            return [],[]
        
        results = result["results"]
        cids = []
        for i in range(0,len(results)):
            cids.append(results[i]["cid"])
        print("pull ok")
        
        return results,cids

    #report kr
    def report_kr(self,chip_type,cids):
        #python3 demo_pull.py  report f072f920d28840f8bb9024733eaf84e0 1 HSC32I1
        command = "python3 demo_pull.py report \"%s\" %d \"%s\""%("-".join(cids),1,chip_type)
        output = self.exec_python_wsl(command)
        results = self.read_wsl_output(output)
        if(not results):
            print("report all failed")
            return -1
        
        for i in range(0,len(cids)):
            if(results[cids[i]] == 1):
                print("cid:%s report success"%cids[i])
            else:
                print("cid:%s report failed"%cids[i])
                return -2
        
        return 0

    #report kr online
    def report_kr_online(self,product_id,private_key,chip_type,cids):
        #python3 pull_online.py report f072f920d28840f8bb9024733eaf84e0 1 HSC32I1
        command = "python3 pull_online.py report \"%s\" \"%s\" \"%s\" %d \"%s\""%(product_id,private_key,"-".join(cids),len(cids),chip_type)
        output = self.exec_python_wsl(command)
        results = self.read_wsl_output(output)
        if(not results):
            print("report all failed")
            return -1
        
        for i in range(0,len(cids)):
            if(results[cids[i]] == 1):
                print("cid:%s report success"%cids[i])
            else:
                print("cid:%s report failed"%cids[i])
                return -2
        
        return 0
    
    def burn_pressure_test(self,chip_type,module,license,total_count):
       command = "python3 sim_adapter.py test_burn_kr_pressure \"%s\" \"%s\" \"%s\" %d"%(chip_type,module,license,total_count)
       output = self.exec_python_wsl(command)
       print(command)
       print(output)
       try:
           output.index("'ret': 0")
           return 0
       except:
           return -1
       result = self.read_wsl_output(output)
       
    #    return result["ret"]
    
    def exec_python_wsl(self,wsl_command):
        # p_wsl = wsl_start()
        # wexpect_common(p_wsl, cmd='cd ~', exp='')
        # wexpect_common(p_wsl, cmd='cd /mnt/d/code/kp_test/kp_source/kp_unite/integrate/python', exp='')
        # wexpect_common(p_wsl, cmd=wsl_command', exp='success', full_log=True)
        # out = wsl_end(p_wsl)
        print(wsl_command)
        r = os.popen(wsl_command)

        info = r.readlines()
        out = ""
        for line in info:
            out += line
        return out

    #检查芯片是否支持
    def check_is_chip_support(self,chip_type):
        chip_list_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_supported_list",("string","out","")))
        chip_out = self.read_wsl_output(chip_list_out)
        if(chip_out["ret"] != 0):
            print("chip list fetch failed")
            return -1
        chip_list = chip_out["output"][0].split("|")
        if(chip_type in chip_list):
            print("chip support check ok")
        else:
            print("chip support check failed")
            return -2
        
        return 0

    #创建芯片池
    def create_chips(self,chip_type,chip_count):
        chip_list_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_create",("string","in",chip_type),("int","in",chip_count)))
        chip_out = self.read_wsl_output(chip_list_out)
        if(chip_out["ret"] != 0):
            print(chip_out)
            print("chips create failed")
            return -1
        print("create chips ok")
        return 0
    
    #x芯片池
    def destroy_chips(self,chip_type,chip_count):
        chip_list_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_destroy",("string","in",chip_type),("int","in",chip_count)))
        chip_out = self.read_wsl_output(chip_list_out)
        if(chip_out["ret"] != 0):
            print("chips destroy failed")
            return -1
        print("destroy chips ok")
        return 0
    #获取芯片huk
    def get_chip_huk(self,chip_type,huk_count):
        huks_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_get_huk",("string","in",chip_type),("string","out",""),("int","in",huk_count)))
        huk_output = self.read_wsl_output(huks_out)
        if(huk_output["ret"] != 0):
            print("chips huk get failed")
            return None
        
        print("chips huk get ok")
        return huk_output["output"][0].split("|")

    #store kr
    def store_kr(self,chip_type,cid,huk,kr):
        print(self.make_sim_adapter_params("sim_chip_store_kr",("string","in",chip_type),("string","in",huk),("string","in",cid),("string","in",kr)))
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_store_kr",("string","in",chip_type),("string","in",huk),("string","in",cid),("string","in",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print(kr_output)
            print("store kr failed")
            return -1
        
        print("store kr ok")
        return 0

    #read kr
    def read_kr(self,chip_type,huk):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_fetch_kr",("string","in",chip_type),("string","in",huk),("string","out","")))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            return None
        
        return kr_output["output"][0]

    #read_burned kr
    def read_burned_kr(self,chip_type,huk):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_read_burned_kr",("string","in",chip_type),("string","in",huk),("string","out","")))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            return None
        
        return kr_output["output"][0]

    def update_kr_key(self,chip_type,kr, key, value):
        update_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_kr_update_key",("string","in",chip_type),("string","out",kr),("string","in",key),("string","in",value)))
        update_output = self.read_wsl_output(update_out)
        if(update_output["ret"] != 0):
            print("update key failed")
            return None
        print("update key success")
        return update_output["output"][0]

    def update_key_auto(self,chip_type,kr,key):
        json_kr = self.dump_kr(chip_type,kr)
        if(not key in json_kr):
            return None

        update_value = ""
        if(key == "CREDENT_DATA"):
            update_value = "3"*(len(str(json_kr[key])) * 2)
            print(json_kr[key])
        elif(key == "CREDENT_LEN"):
            update_value = str(int(str(json_kr[key])) - 1)
        else:
            # update_value = "%X"%(int(str(json_kr[key]),16) + 1)
            update_dat1 = "F"*len(str(json_kr[key]))
            update_dat2 = "0"*len(str(json_kr[key]))
            if(update_dat1.lower() == str(json_kr[key]).lower()):
                update_value = update_dat2
            else:
                update_value = update_dat1
        updated_kr = self.update_kr_key(chip_type,kr,key,update_value)
        if(not updated_kr):
            return None

        print("key update auto success")
        return updated_kr

    def hsec_test_case_update_sad(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"SAD")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_head_hash(kr_read)
        if(ret == 0):
            return -4

        ret = self.hsec_verify_sad(kr_read)
        if(ret == 0):
            return -5

        print("test_case_update_sad ok")
        return 0
    
    def hsec_test_case_update_cid(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"CHIP_ID")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_head_hash(kr_read)
        if(ret == 0):
            return -4

        ret = self.hsec_verify_sad(kr_read)
        if(ret == 0):
            return -5

        print("hsec_test_case_update_cid ok")
        return 0

    def hsec_test_case_update_huk(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"HUK")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != SIM_HUK_VERIFY_ERROR:
            print("hsec_test_case_update_huk ret:%d"%ret)
            return -2

        print("hsec_test_case_update_huk ok")
        return 0

    def hsec_test_case_update_credent_len(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"CREDENT_LEN")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_credent_hash(kr_read)
        if(ret == 0):
            return -4

        print("hsec_test_case_update_credent_len ok")
        return 0

    def hsec_test_case_update_credent_hash(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"CREDENT_HASH")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_credent_hash(kr_read)
        if(ret == 0):
            return -4

        print("hsec_test_case_update_credent_hash ok")
        return 0

    def hsec_test_case_update_meta_hash(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"META_HEADER_HASH")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_head_hash(kr_read)
        if(ret == 0):
            return -4

        print("hsec_test_case_update_meta_hash ok")
        return 0

    def hsec_test_case_update_credent_content(self,chip_type,huk,kr):
        kr_updated = self.update_key_auto(chip_type,kr,"CREDENT_DATA")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.hsec_verify_credent_hash(kr_read)
        if(ret == 0):
            return -4

        print("hsec_test_case_update_credent_content ok")
        return 0
        

    def light_test_case_update_content(self,chip_type,huk,kr,usrkey2_skey, cvkey2_skey, rootckey_c, hash_rotpk, hash_debugpk):
        kr_updated = self.update_key_auto(chip_type,kr,"USRKEY2_SKEY")
        if(not kr_updated):
            return -1
        
        ret = self.burn_kr(chip_type,huk,kr_updated)
        if ret != 0:
            return -2

        kr_read = self.read_burned_kr(chip_type,huk)
        if not kr_read:
            return -3

        ret = self.light_verify_content(kr_read,usrkey2_skey, cvkey2_skey, rootckey_c, hash_rotpk, hash_debugpk)
        if(ret == 0):
            return -4

        print("light_test_case_update_content ok")
        return 0

    def get_sdk_version(self):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_get_lib_version",("string","out","")))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("get_sdk_version failed")
            return None
        
        print("get_sdk_version ok")
        return kr_output["output"][0]

    def burn_kr(self,chip_type,huk,kr):
        print(self.make_sim_adapter_params("sim_chip_burn_kr",("string","in",chip_type),("string","in",huk),("string","in",kr)))
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_chip_burn_kr",("string","in",chip_type),("string","in",huk),("string","in",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("burn kr failed")
            return kr_output["ret"]
        
        print("burn kr ok")
        return 0
    
    def set_provision(self,provision):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_set_provision_security_level",("string","in",provision)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("set_provision failed")
            return -1
        
        print("set_provision ok")
        return 0
    def hsec_verify_huk(self,kr,huk):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_huk_verify_hsec",("string","in",kr),("string","in",huk)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("hsec verify kr huk failed")
            return -1
        
        print("hsec verify kr huk ok")
        return 0

    def hsec_verify_sad(self,kr):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_sad_verify_hsec",("string","in",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("hsec verify kr sad failed")
            return -1
        
        print("hsec verify kr sad ok")
        return 0
    
    def hsec_verify_head_hash(self,kr):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_head_hash_verify_hsec",("string","in",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("hsec verify head hash failed")
            return -1
        
        print("hsec verify head hash ok")
        return 0

    def hsec_verify_credent_hash(self,kr):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_credent_hash_verify_hsec",("string","in",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("hsec verify credent hash failed")
            return -1
        
        print("hsec verify credent hash ok")
        return 0

    def hsec_verify_credent_data(self,kr,ecdh,model,product_type):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_credent_content_verify_hsec",("string","in",kr),("string","in",ecdh),("string","in",model),("string","in",product_type)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("hsec verify credent data failed")
            return -1
        
        print("hsec verify credent data ok")
        return 0
    
    def light_verify_content(self,kr,usrkey2_skey, cvkey2_skey, rootckey_c, hash_rotpk, hash_debugpk):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_content_verify_light",("string","in",kr),("string","in",usrkey2_skey),("string","in",cvkey2_skey),("string","in",rootckey_c),("string","in",hash_rotpk),("string","in",hash_debugpk)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("light verify content failed")
            return -1
        
        print("light verify content ok")
        return 0
        
    def dump_kr(self,chip_type,kr):
        print(self.make_sim_adapter_params("sim_kr_dump_key",("string","in",chip_type),("string","in",kr),("string","out","")))
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_kr_dump_key",("string","in",chip_type),("string","in",kr),("string","out","")))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("dump kr failed")
            return None
        
        print("dump kr ok")
        return eval(kr_output["output"][0])

    def encrypt_kr(self,chip_type,huk,kr):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_encrypt_kr",("string","in",chip_type),("string","in",huk),("string","out",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("encrypt kr failed")
            return None
        
        print("encrypt kr ok")
        return eval(kr_output["output"][0])

    def sign_kr(self,chip_type,huk,kr):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_sign_kr",("string","in",chip_type),("string","in",huk),("string","out",kr)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("sign kr failed")
            return None
        
        print("sign kr ok")
        return eval(kr_output["output"][0])
    

    def cm_kp_sim_burn_pressure_test(self, chip_type, module, license, count):
         command = "python3 sim_adapter.py test_burn_kr_pressure \"%s\" \"%s\" \"%s\" %d" % (
         chip_type, module, license, count)
         print('tttt111')
         print(command)
         output = self.exec_python_wsl(command)
         result = self.read_wsl_output(output)
         return result["ret"]
    
    def sim_burn_pressure_test(self, name, chip_type, module, licence, count):
        """P0 - 1 minutes - 2023-03-07 - wangdl"""
        """ Pressure test after continuous burning for 72 hours """
        startAt = time.time()
        burn = self.cm_kp_sim_burn_pressure_test(chip_type, module, licence, count)
        self.cus_assert(str(burn), '0', Cus_Assert.Equal, 'burn success ')
        print("thread %s burn  %s  time %d" % (name, str(burn), time.time() - startAt))

    def test_57004826_P0_Burning_pressure(self):
        for i in range(0, 2000):
            threads = []
            total_counts = 1000
            test_chip_type = "light"
            ret = self.burn_pressure_test(test_chip_type, 'xjttet111111', '', total_counts)
            if(ret != 0):
                print("exec error:%d"%ret)
                return
     
    def test_burn_kr_pressure(self,chip_type,module,license,total_count):
        threads = []
       
        test_total_threads = int(total_count / 10)
       
        for num in range(0, test_total_threads):
            if(self.create_chips(chip_type,int(total_count / test_total_threads)) != 0):
                return -2
            huks = self.get_chip_huk(chip_type, int(total_count / test_total_threads))
            if (not huks):
                return -200
            thread_pressure(self,str(0), chip_type, module, license, huks)
            ret = self.thread_results[str(0)]
            if(ret != 0):
                print("exec error :%d"%ret)
                return ret
            # t = threading.Thread(target=thread_pressure, args=(self,str(num), chip_type, module, license, huks))
            # threads.append(t)
            # t.start()
        # for t in threads:
        #     t.join()
        
        
        # for i in range(0,test_total_threads):
        #     ret = self.thread_results[str(i)]
        #     if(ret != 0):
        #         return ret
        
        return 0

    def test_case_SL2(self,chip_type,chip1,chip2):
        #read kr
        kr = self.read_kr(chip_type,chip1["huk"])
        if(not kr):
            print("read kr failed")
            return -1
        else:
            print("read kr success")

        # #sign kr
        # signed_kr = sign_kr(chip_type,chip1["huk"],kr)
        # if(not signed_kr):
        #     return -2

        # #encrypt kr
        # encrypted_kr = encrypt_kr(chip_type,chip1["huk"],signed_kr)
        # if(not encrypted_kr):
        #     return -3
        
        #burn kr
        ret = self.burn_kr(chip_type,chip2["huk"],encrypted_kr)
        if(ret == 0):
            print("burn kr success,expected failed")
            return -4

        return 0

    def test_case_SL3(self,chip_type,chip):
        #read kr
        kr = self.read_kr(chip_type,chip["huk"])
        if(not kr):
            print("read kr failed")
            return -1
        else:
            print("read kr success")

        #sign kr
        signed_kr = self.sign_kr(chip_type,chip["huk"],kr)
        if(not signed_kr):
            return -2

        #encrypt kr
        encrypted_kr = self.encrypt_kr(chip_type,chip["huk"],signed_kr)
        if(not encrypted_kr):
            return -3

        #decrypt kr
        decrypted_kr = self.encrypt_kr(chip_type,chip["huk"],encrypted_kr)
        if(not decrypted_kr):
            return -4

        decrypted_kr[1025] = 'FF'#modify data

        #encrypt kr
        encrypted_kr = self.encrypt_kr(chip_type,chip["huk"],decrypted_kr)
        if(not encrypted_kr):
            return -5

        #burn kr
        ret = self.burn_kr(chip_type,chip["huk"],encrypted_kr)
        if(ret == 0):
            print("burn kr success,expected failed")
            return -4

        return 0

    def read_hsm_license_count(self):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_hsm_read_license_count",("string","out","")))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("read_hsm_license_count failed")
            return None

        print("read_hsm_license_count ok")
        return kr_output["output"][0]

    def decrease_hsm_license_count(self):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_hsm_decrease_license_count",))
        kr_output = self.read_wsl_output(kr_out)
        return kr_output["ret"]

    def set_hsm_public_key(self,pem_path):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_hsm_set_public_key",("string","in",pem_path)))
        kr_output = self.read_wsl_output(kr_out)
        return kr_output["ret"]

    def exec_all(self,pull_model,pull_license,chip_type,chip_count,test_count):
        #get sdk version
        sdk_version = self.get_sdk_version()
        if( not sdk_version):
            return -1

        print("sdk version:%s"%sdk_version)

        #step1 检查芯片是否支持
        if(self.check_is_chip_support(chip_type) != 0):
            return -1

        #step2 创建芯片池
        if(self.create_chips(chip_type,chip_count) != 0):
            return -2

        #step3 获取huk
        huks = self.get_chip_huk(chip_type,test_count)
        if( not huks ):
            return -3

        # rtn = self.burn_pressure_test(chip_type,pull_model,pull_license,test_count)
        # return 0
        #step4 pull拉取
        pull_results,_ = self.pull_kr(chip_type,pull_model,pull_license,huks)
        if(not pull_results or len(pull_results) == 0):
            return -4

        #step5 report kp
        cids = []
        for i in range(0,len(pull_results)):
            cids.append(pull_results[i]["cid"])
        self.report_kr(chip_type,cids)

        for i in range(0,len(pull_results)):
            #store kr
            ret = self.store_kr(chip_type,pull_results[i]["cid"],pull_results[i]["huk"],pull_results[i]["kr"])
            if(ret != 0):
                print("store kr failed")
                return -1
            else:
                print("store kr success")
            
            #read kr
            kr = self.read_kr(chip_type,pull_results[i]["huk"])
            if(not kr):
                print("read kr failed")
                return -1
            else:
                print("read kr success")
            
            # #update key
            # self.update_key_auto(chip_type,kr,update_key)
            # updated_kr = self.update_kr_key(chip_type,kr,update_key,update_value)
            # if(not updated_kr):
            #     return -1

            #dump kr keys
            keys_json = self.dump_kr(chip_type,kr)
            if(not keys_json):
                return -1
            # if(keys_json[update_key] == update_value):
            #     print("key update read back matched")
            # else:
            #     print("key update read back not matched")
            #     return -1
            
            # #sign kr
            # signed_kr = self.sign_kr(chip_type,pull_results[i]["huk"],updated_kr)
            # if(not signed_kr):
            #     return -1

            # #encrypt kr
            # encrypted_kr = self.encrypt_kr(chip_type,pull_results[i]["huk"],signed_kr)
            # if(not encrypted_kr):
            #     return -1
            self.set_provision("Anitplay")
            if(is_secure_chip_for_alipay(chip_type)):
                self.hsec_verify_huk(kr,pull_results[i]["huk"])
                self.hsec_verify_sad(kr)
                self.hsec_verify_head_hash(kr)
                self.hsec_verify_credent_hash(kr)
                self.hsec_verify_credent_data(kr,"ECDH", "MOCK_MODEL","QZCRD")

                self.hsec_test_case_update_sad(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_cid(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_huk(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_credent_hash(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_credent_len(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_meta_hash(chip_type,pull_results[i]["huk"],kr)
                self.hsec_test_case_update_credent_content(chip_type,pull_results[i]["huk"],kr)
            else:
                # self.light_test_case_update_content(chip_type,pull_results[i]["huk"],kr,"2a64bfeaaba889f4", "08fa21f696c04345", "cc1192239de7a38ffd8f2d3d053fbb0680f5a0f887f90b33034ba98a81f18cca", "039ef0a18795310525ddc12a9c7eaf1e7450967bc9a22f4c6dd8d7efcae3bdcd", "032fee0a44200f69fdd1131bcfc239c3934f405d716faadfc702cf12650ddf68")                 
                self.light_verify_content(kr,"2a64bfeaaba889f4","08fa21f696c04345","cc1192239de7a38ffd8f2d3d053fbb0680f5a0f887f90b33034ba98a81f18cca","039ef0a18795310525ddc12a9c7eaf1e7450967bc9a22f4c6dd8d7efcae3bdcd","032fee0a44200f69fdd1131bcfc239c3934f405d716faadfc702cf12650ddf68")
            
            # self.burn_pressure_test(chip_type,pull_model,pull_license)
            # pro_list = ["Integrity","Encryption","Anitplay"]
            # #burn kr
            # for j in range(0,len(pro_list)):
            #     ret = self.set_provision(pro_list[j])
            #     if(ret != 0):
            #         return -2
            #     ret = self.burn_kr(chip_type,pull_results[i]["huk"],kr)
            #     if(ret != 0):
            #         return -1
        
        # self.test_case_SL2(chip_type,pull_results[0],pull_results[1])
        # self.test_case_SL3(chip_type,pull_results[0])

        return 0

    def generate_random(self,len):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_hsm_generate_random_data",("string","out",""),("int","in",len)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("generate_random failed")
            return None

        print("generate_random ok")
        return kr_output["output"][0]

    def burn_encrypted_firmware(self,firmware_path):
        kr_out = self.exec_python_wsl(self.make_sim_adapter_params("sim_burn_encrypted_firmware",("string","in",firmware_path)))
        kr_output = self.read_wsl_output(kr_out)
        if(kr_output["ret"] != 0):
            print("burn_encrypted_firmware failed")
            return False

        print("burn_encrypted_firmware ok")

        return 0

    def exec_all_online(self):
        product_id = "4153858429158494208"
        private_key = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAI0lwi6kTCSHzr6WRXtEvJIjuK6uKhjbWJ1g6NkxhIIErx4zo7w68lPmrWnKtqTUPwmEcFX3I6qOsaa58dRFP/lclT9v5Vwi74DmAACxX+Ig7qdY8q/NbdmLiKXbi6wWjdgNHCX1XnKxyno2EVZeULFSryRdCF/OahR8ILVkagZFAgMBAAECgYA2Bpbd/Xs7nFPxNVmhBj1bfprJGdb5LrQrgRV/VOnQTnStDb0FZlas8KW90Z65VphOT0gkT3Vyai3rkE7VHjCO83EYh0UipPUaMvc9mcut1WYnAOlr3mEI55nZlt9vd2ZST1bYTaExW/GYF1OgWPcSPNQBSBeBuiwyWpo7iBCqfQJBAL5l4k8AbC01QgrHWAFuEr57ges3UkwNbq2A1obn34p6OsMA7Pa6dsy2NqAvfjIV8JUs1ci1aDjdVw1wZFu2v0MCQQC9x7gTDJNbI+OkAZM8QSEmDhGb+l1lKPLgiIcEyHkxI6uZzEcvd8ZTaL4+alqXKqWYXpO6wmkuw0LzTPdwSDfXAkBYWlcmaf/JCsnWzqKcJ0QzeITVbhqWiDUv9nWWrMsjK41RKIDODcFLRdMbim55N40o7GFYfjYbDTt0VQ99L9SZAkEAhqUJGzLD5VjMLFMVxB0tSJOYuMJjut7XmqgiqykUmuGE4SRGqQ3gftMEjsHkLfYK8NTBGTLPb2cHvBiyQU5rlwJAfFXKxd6eHQX5xkf1Q2f0/RWRYmEuehYum+uStt5USyMlWs9bWpUvBK5k8noy3vcZNEFz59KNXIlAuvu4cjUDPw=="
        chip_type = "CV181x"

        #step1 检查芯片是否支持
        if(self.check_is_chip_support(chip_type) != 0):
            return -1

        #step2 创建芯片池
        if(self.create_chips(chip_type,1) != 0):
            return -2

        #step3 获取huk
        huks = self.get_chip_huk(chip_type,1)
        if( not huks ):
            return -3

        #step4 pull拉取
        pull_results,cids = self.pull_kr_online(chip_type,product_id,private_key,huks[0])
        if(not pull_results):
            return -4
        
        #step5 report kp
        cids = []
        for i in range(0,len(pull_results)):
            cids.append(pull_results[i]["cid"])
        self.report_kr_online(product_id,private_key,chip_type,cids)

        for i in range(0,len(pull_results)):
            #store kr
            ret = self.store_kr(chip_type,pull_results[i]["cid"],pull_results[i]["huk"],pull_results[i]["kr"])
            if(ret != 0):
                print("store kr failed")
                return -1
            else:
                print("store kr success")
            
            #read kr
            kr = self.read_kr(chip_type,pull_results[i]["huk"])
            if(not kr):
                print("read kr failed")
                return -1
            else:
                print("read kr success")
            
        #     # #update key
        #     # self.update_key_auto(chip_type,kr,update_key)
        #     # updated_kr = self.update_kr_key(chip_type,kr,update_key,update_value)
        #     # if(not updated_kr):
        #     #     return -1

            #dump kr keys
            keys_json = self.dump_kr(chip_type,kr)
            if(not keys_json):
                return -1
            print(keys_json)
        #     # if(keys_json[update_key] == update_value):
        #     #     print("key update read back matched")
        #     # else:
        #     #     print("key update read back not matched")
        #     #     return -1
            
        #     # #sign kr
        #     # signed_kr = self.sign_kr(chip_type,pull_results[i]["huk"],updated_kr)
        #     # if(not signed_kr):
        #     #     return -1

        #     # #encrypt kr
        #     # encrypted_kr = self.encrypt_kr(chip_type,pull_results[i]["huk"],signed_kr)
        #     # if(not encrypted_kr):
        #     #     return -1
        #     self.set_provision("Anitplay")
        #     if(chip_type == "HSC32I1"):
        #         self.hsec_verify_huk(kr,pull_results[i]["huk"])
        #         self.hsec_verify_sad(kr)
        #         self.hsec_verify_head_hash(kr)
        #         self.hsec_verify_credent_hash(kr)
        #         self.hsec_verify_credent_data(kr,"ECDH", "MOCK_MODEL","QZCRD")

        #         self.hsec_test_case_update_sad(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_cid(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_huk(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_credent_hash(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_credent_len(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_meta_hash(chip_type,pull_results[i]["huk"],kr)
        #         self.hsec_test_case_update_credent_content(chip_type,pull_results[i]["huk"],kr)
        #     else:
        #         self.light_test_case_update_content(chip_type,pull_results[i]["huk"],kr,"2a64bfeaaba889f4", "08fa21f696c04345", "cc1192239de7a38ffd8f2d3d053fbb0680f5a0f887f90b33034ba98a81f18cca", "039ef0a18795310525ddc12a9c7eaf1e7450967bc9a22f4c6dd8d7efcae3bdcd", "032fee0a44200f69fdd1131bcfc239c3934f405d716faadfc702cf12650ddf68")

        #     # pro_list = ["Integrity","Encryption","Anitplay"]
        #     # #burn kr
        #     # for j in range(0,len(pro_list)):
        #     #     ret = self.set_provision(pro_list[j])
        #     #     if(ret != 0):
        #     #         return -2
        #     #     ret = self.burn_kr(chip_type,pull_results[i]["huk"],kr)
        #     #     if(ret != 0):
        #     #         return -1

        # # self.test_case_SL2(chip_type,pull_results[0],pull_results[1])
        # # self.test_case_SL3(chip_type,pull_results[0])

        return 0
if __name__ == '__main__':
    print(DemoAll().exec_all("WP_Lx100","xjt_test123456","LX100",1,1))
