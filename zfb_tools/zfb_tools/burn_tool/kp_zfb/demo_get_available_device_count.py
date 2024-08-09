import time
from ctypes import Structure
from ctypes import c_int, c_char_p, POINTER, c_ulong, c_uint,c_void_p,c_byte
from ctypes import cdll, CDLL,cast
import configparser
import sys
import os

def csi_kp_get_available_device_count():
   try:
      api = CDLL('./libkp_client.so')
      api.csi_kp_get_available_device_count.argtypes = [c_char_p,c_char_p,c_char_p,c_char_p]
      api.csi_kp_get_available_device_count.restype = c_int
      # 创建 ConfigParser 对象
      path = os.getcwd()
      config = configparser.ConfigParser()
      config_file = path + '/cfg/lisence_cfg.ini'
      if not os.path.exists(config_file):
         raise FileNotFoundError(f"配置文件 '{config_file}' 不存在")
      # 读取配置文件
      config.read(config_file)
      pull_model = config.get('settings', 'pull_model')  # 获得产品类型
      license = config.get('settings', 'license')  # 获得产品类型
      url=b"http://10.1.100.66:28080/api/occ/kp/getAvailableCount"# 服务器地址
      product = pull_model.encode('utf-8') #  要查询的许可证名称，请按照实际许可证名称填写
      if license != None:
         license = license.encode('utf-8')
      # product=b"TRANSIT_ZX9660_SE" #  要查询的许可证名称，请按照实际许可证名称填写
      # TRANSIT_ZX9660_SE
      # PAYMENT_ZX9660_SE
      chip_type=b"ZX9660"
      res_count = api.csi_kp_get_available_device_count(url,product, license,chip_type)
      if res_count < 0:
         print('cis kp_get_available_device_count failed')
         return res_count
      else:
         print('license The remaining quantity is:',res_count)
         return res_count
   except Exception as e:
      print(e)
