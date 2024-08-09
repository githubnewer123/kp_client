from UI.product_main import Ui_ProductMainWindow
from view.product_main_view import ProductMainView
import common.utils as Utils
import sys,cgitb,logging,os,datetime,time


if __name__ == "__main__":
    cgitb.enable(format='text')
    log_path = "MMPT\\log\\app"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_list = os.listdir(log_path)
    if len(file_list) > 100:
        file_list.sort()
        for file in file_list[0:-100]:
            os.remove(os.path.join(log_path, file))

    logging.basicConfig(level=logging.INFO,
                        # filename="MMPT\\log\\app\\%s.log"%(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')),
                        format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        datefmt='%Y-%m-%d  %H:%M:%S %a')
    ProductMainView()