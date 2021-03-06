import time
import random
from strgen import StringGenerator
import pandas as pd
from pandas import ExcelWriter
import xbridge_config

from interface import xbridge_rpc

TIME_DISTRIBUTION = []
ERROR_LOG = []
IS_SEQUENCE_TEST = False

VALID_DATA = 1
INVALID_DATA = 2
RANDOM_VALID_INVALID = 3

basic_garbage_list = ["", " ", "/", "\\", "//////////", "+", "-", "=", "*",
                        "{", "}", "{", "}", "(", ")", "[", "]", "{}", "()", "[]", "[[]]", "{{}}", "[{}]", "{[]}", ")(", "}{",
                        "<", ">", "<>", "<<", ">>", "<<>", "><",
                        ".", ";", "?", "-", ":", "!", "�", "%", "�", "�", "�", "�", "@", "|", "#", "^", "_",
                        "-----------", "%%%%%%%", "::::::::::", "^^^^^^^^", "<<<<<<<<<<<<<", ">>>>>>>>>>>>>",
                        "~&#'@$!%^.;?-", "yes", "no"
                     ]
current_basic_garbage_item = ""
                     
one_classes_list = ["[\\a]", "[\p]", "[\d]", "[\W]", "[\w]", "[\h]", "[\s]"]
two_classes_list = ["[\p\d]", "[\p\\a]", "[\p\h]", "[\s\d]", "[\s\\a]", "[\s\h]", "[\s\p]", "[\W\d]", "[\W\\a]", "[\W\h]",
                    "[\W\p]"]
three_classes_list = ['[\\a\d\W]', '[\a\d\h]', '[\a\d\s]', '[\\a\d\p]', '[\\a\d\W]']
four_classes_list = ['[\p\d\w\s]', '[\p\d\\a\h]', '[\p\d\\a\s]']
five_classes_list = ['[\p\d\W\w\h\\a]']

# Frequently used constants
fixed_negative_int = -10
fixed_positive_int = 10
fixed_positive_float = 10.2
fixed_negative_float = -10.2
fixed_small_positive_float = 0.00000000000000000000000000000000000000000000000000000001
fixed_large_positive_int = 9999999999999999999999999999999999999999999999999999999999999999
valid_random_positive_int = 0
invalid_random_positive_int = 0
valid_random_positive_float = 0
invalid_random_positive_float = 0

# Set for create_tx
c_src_Address = ""
c_dest_Address = ""
c_src_Token = ""
c_dest_Token = ""
source_nb = ""
dest_nb = ""
# set for accept_tx
a_random_tx_id = ""
a_src_Address = ""
a_dest_Address = ""
# set for any function that takes a txid as parameter
ca_random_tx_id = ""
# General purpose
valid_account_str = ""
invalid_account_str = ""
invalid_str_from_random_classes_1 = ""
invalid_str_from_random_classes_2 = ""
invalid_str_from_random_classes_3 = ""
invalid_str_from_random_classes_4 = ""

# CAUTION ! Be careful when changing this set, otherwise you may decrease entropy
# CAUTION ! Some items appear multiple times voluntarily: we want to increase their chances of being drawn during the random process
set_of_invalid_parameters = []

def update_set_of_invalid_parameters():
    global set_of_invalid_parameters
    set_of_invalid_parameters = ["", 0,
                    True, False,
                    invalid_str_from_random_classes_1,
                    invalid_str_from_random_classes_1,
                    invalid_str_from_random_classes_2,
                    invalid_str_from_random_classes_2,
                    invalid_str_from_random_classes_3,
                    invalid_str_from_random_classes_3,
                    invalid_str_from_random_classes_4,
                    invalid_str_from_random_classes_4,
                    current_basic_garbage_item,
                    current_basic_garbage_item,
                    invalid_random_positive_int,
                    invalid_random_positive_float,
                    -invalid_random_positive_int,
                    -invalid_random_positive_float,
                    valid_random_positive_float,
                    -valid_random_positive_float,
                    ]


def generate_new_set_of_data(data_nature=RANDOM_VALID_INVALID, char_min_size=1, char_max_size=12000):
    # Set for create_tx
    global c_src_Address
    global c_dest_Address
    global c_src_Token
    global c_dest_Token
    global source_nb
    global dest_nb
    # set for accept_tx
    global a_random_tx_id
    global a_src_Address
    global a_dest_Address
    # set for any function that takes a txid as parameter
    global ca_random_tx_id
    # General purpose
    global valid_account_str
    global invalid_account_str
    global valid_random_positive_int
    global invalid_random_positive_int
    global valid_random_positive_float
    global invalid_random_positive_float
    global current_basic_garbage_item
    global invalid_str_from_random_classes_1
    global invalid_str_from_random_classes_2
    global invalid_str_from_random_classes_3
    global invalid_str_from_random_classes_4
    invalid_str_from_random_classes_1 = generate_input_from_random_classes_combinations(1, 400)
    invalid_str_from_random_classes_2 = generate_input_from_random_classes_combinations(400, 1000)
    invalid_str_from_random_classes_3 = generate_input_from_random_classes_combinations(5000, 10000)
    invalid_str_from_random_classes_4 = generate_input_from_random_classes_combinations(10000, 12000)
    current_basic_garbage_item = random.choice(basic_garbage_list)
    valid_random_positive_int = generate_random_int(1, 1000)
    invalid_random_positive_int = generate_random_int(999999999999999999999, 9999999999999999999999999999999999999999999999999999)
    valid_random_positive_float = generate_random_number(1, 1000)
    invalid_random_positive_float = generate_random_number(999999999999999999999, 9999999999999999999999999999999999999999999999999999)
    if data_nature == RANDOM_VALID_INVALID:
        selected_data = random.choice([VALID_DATA, INVALID_DATA])
        generate_new_set_of_data(selected_data)
    if data_nature == INVALID_DATA:
        # Set for create_tx
        c_src_Address = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        c_dest_Address = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        c_src_Token = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        c_dest_Token = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        source_nb = generate_random_number(-999999999999999999999999999999999999999999999999999999999999999,
                                                         999999999999999999999999999999999999999999999999999999999999999)
        dest_nb = generate_random_number(-999999999999999999999999999999999999999999999999999999999999999,
                                                       999999999999999999999999999999999999999999999999999999999999999)
        # set for accept_tx
        a_random_tx_id = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        a_src_Address = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        a_dest_Address = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        # set for any function that takes a txid as parameter
        ca_random_tx_id = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
        # general purpose
        invalid_account_str = generate_input_from_random_classes_combinations(char_min_size, char_max_size)
    if data_nature == VALID_DATA:
        # Set for create_tx
        # c_src_Address = xbridge_rpc.rpc_connection.getnewaddress()
        # c_src_Address = generate_random_valid_address()
        c_src_Address = generate_valid_blocknet_address()
        c_dest_Address = generate_random_valid_address()
        c_src_Token = generate_random_valid_token()
        c_dest_Token = generate_random_valid_token()
        source_nb = generate_random_number(1, 1000)
        dest_nb = generate_random_number(1, 1000)
        a_random_tx_id = generate_random_valid_txid()
        # a_src_Address = xbridge_rpc.rpc_connection.getnewaddress()
        a_src_Address = generate_random_valid_address()
        # a_dest_Address = xbridge_rpc.rpc_connection.getnewaddress()
        a_dest_Address = generate_random_valid_address()
        # set for any function that takes a txid as parameter
        ca_random_tx_id = generate_random_valid_txid()
        valid_account_str = generate_random_valid_account_str()
    update_set_of_invalid_parameters()


def export_Full_Excel_Log():
    global TIME_DISTRIBUTION
    if len(TIME_DISTRIBUTION) == 0:
        return
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filepath_with_time = xbridge_config.get_conf_log_dir() + timestr + "_SEQUENCE_TESTS.xlsx"
    my_df = pd.DataFrame(TIME_DISTRIBUTION)
    # reorder the columns
    my_df = my_df[["version", "sequence", "API", "time"]]
    stat_df = my_df["time"].describe()
    writer = ExcelWriter(filepath_with_time)
    my_df.to_excel(writer, timestr)
    stat_df.to_excel(writer, 'Summary')
    try:
        writer.save()
        print("Created Excel Log:       %s" % filepath_with_time)
        print("Recorded:                %s logs" % str(len(TIME_DISTRIBUTION)))
        print("Max run time:            %s" % str(my_df["time"].max()))
    except:
        print("export_data - An error occured when creating: %s" % filepath_with_time)
    
# This function has been disabled
def export_data(filepath, list_to_export):
    return
    if len(list_to_export) == 0:
        return
    if not xbridge_config.should_log_Excel_files():
        return
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filepath_with_time = xbridge_config.get_conf_log_dir() + timestr + "_" + filepath
    my_df = pd.DataFrame(list_to_export)
    stat_df = my_df["time"].describe()
    writer = ExcelWriter(filepath_with_time)
    my_df.to_excel(writer, timestr)
    stat_df.to_excel(writer, 'Summary')
    try:
        writer.save()
        print("Created Excel Log: %s" % filepath_with_time)
    except:
        print("export_data - An error occured when creating: %s" % filepath_with_time)

def prepare_results_Summary():
    global ERROR_LOG
    if len(ERROR_LOG) == 0:
        return ""
    filtered_list = [itm for itm in ERROR_LOG if str(itm["group"])[0:1] != "<"]
    my_df = pd.DataFrame(filtered_list)
    # reorder the columns
    my_df = my_df[["group", "success", "failure", "error"]]
    aggregated_df = my_df.groupby(by=['group'])["success", "failure", "error"].sum()
    return aggregated_df
               
def generate_random_number(a, b):
    a = int(a * 100)
    b = int(b * 100)
    return float(random.randint(a, b)/100)

def generate_random_int(a, b):
    return int(random.randint(a, b))

def generate_valid_blocknet_address():
    xbridge_rpc.rpc_connection.keypoolrefill(1000)
    return xbridge_rpc.rpc_connection.getnewaddress()

def generate_random_valid_passphrase():
    template_str = '[a-zA-Z0-9]{1:7000}'
    return StringGenerator(template_str).render()

def generate_random_valid_address():
    template_str = '[\h]{30:70}'
    return StringGenerator(template_str).render()

def generate_random_valid_txid():
    nb_of_cars = 64
    template_str = '[a-zA-Z0-9]{' + str(nb_of_cars) + '}'
    return StringGenerator(template_str).render()
    
def generate_random_valid_token():
    nb_of_cars = 5
    template_str = '[A-Z]{' + str(nb_of_cars) + '}'
    return StringGenerator(template_str).render()    

def generate_random_valid_account_str():
    template_str = '[\h]{5:50}'
    return StringGenerator(template_str).render()

def generate_random_number_with_leading_zeros():
    template_str = '[0]{1:5000}&[\d]{1:5000}'
    return StringGenerator(template_str).render()    

def generate_input_from_random_classes_combinations(lower_bound, upper_bound):
    classes_list = ["\w", "\d", "\s", "\W", "\p", "\o", "\a"]
    # Sometimes, the picks will be of the same class, so combinations are from 1 to 7 combinations
    pick_1 = random.choice(classes_list)
    pick_2 = random.choice(classes_list)
    pick_3 = random.choice(classes_list)
    pick_4 = random.choice(classes_list)
    combined_picks = pick_1 + pick_2 + pick_3 + pick_4
    template_str = '[' + str(combined_picks) + ']{' + str(lower_bound) + ':' + str(upper_bound) + '}'
    return StringGenerator(template_str).render()
    
# Generate variable-size malformed data with whitespace + punctuation + digits
def generate_garbage_input(nb_of_cars):
    nb_of_cars = int(nb_of_cars)
    # return StringGenerator('[\w\d\W]{8}').render()
    template_str = '[\w\d\W]{' + str(nb_of_cars) + '}'
    return StringGenerator(template_str).render()
    
def generate_numeric_input(nb_of_digits):
    nb_of_digits = int(nb_of_digits)
    # return StringGenerator('[\w\d\W]{8}').render()
    template_str = '[\d]{' + str(nb_of_digits) + '}'
    return StringGenerator(template_str).render()
