from mes.product_result import  ProductResult
from burn_tool.kp_zfb.demo_get_available_device_count import csi_kp_get_available_device_count

class Postdata():
    last_huk = None
    def __init__(self,mes,cfg,huk,burn_result,pass_freq,fail_freq):
        self.mes = mes
        self.cfg = cfg
        self.burn_result = burn_result
        self.pass_freq = pass_freq
        self.fail_freq = fail_freq
        try:
            # 检查这次传入的 huk 是否与上一次的 huk 相等
            if Postdata.last_huk is not None and Postdata.last_huk == huk:
                print("第二次传入的huk与第一次相等,且不为空")
                if "COS烧入失败" in self.burn_result or "kr烧入失败" in self.burn_result:
                    self.burn_result = self.burn_result + "重新烧入"
            Postdata.last_huk = huk

            self.post()
        except Exception as e:
            print(e)

    def post(self):
        product_res = ProductResult(self.cfg)
        product_res.chip_id = Postdata.last_huk
        product_res.successCount = self.pass_freq
        product_res.failCount = self.fail_freq

        self.get_lisence_conut = csi_kp_get_available_device_count()
        product_res.lisence_available_count = self.get_lisence_conut
        # product_res.scrip_version = self.mes.getActiveOrder().scrip_version
        test_result = True if "烧入成功" in self.burn_result else False #
        data = product_res.getDownloadUpdate(res=test_result, false_info=self.burn_result)
        self.mes.postProductData(data=data)


