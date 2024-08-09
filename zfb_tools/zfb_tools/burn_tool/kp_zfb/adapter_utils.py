def read_wsl_output(output):
    try:
        start_str = "Start_of_operation"
        end_str = "End_of_operation"
        start = output.index(start_str)
        end = output.index(end_str)
        return eval(output[start + len(start_str):end])
    except:
        return None

def make_sim_adapter_params(*a):
    if(len(a) <= 0):
        return ""

    args = ""
    for i in range(1,len(a)):
        data_type,input_type,content = a[i]
        args += " %s_%s_%s"%(data_type,input_type,content)

    return "python3 sim_adapter.py %s%s"%(a[0],args)

def is_secure_chip_for_alipay(chip_type):
    if(type(chip_type) is str):
        chip_type = chip_type.encode("utf-8")

    return chip_type == b"HSC32I1" or chip_type == b"WP_LX100" or chip_type == b"DK_LX100" or chip_type == b"ZX9660" or chip_type == b"CIU98"
