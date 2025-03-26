import starchivator
from datetime import datetime, timedelta, date
import json
from json import load
import os
import sys
import base64
import random
from model import TDateTime
from model.logger import logger

def working(config="src/config.json", header_text="StarPack____"):
    BLOCK_NUMBER = 3
    config = load(open(config_path, "r"))
    file_paths = config["Paths"]
    file_paths["DefaultPath_out_dat"] = os.path.join(file_dir, "out.dat")
    file_paths["DefaultPath_x_dat"] = os.path.join(file_dir, "x.dat")
    file_paths["DefaultPath_out_0"] = os.path.join(file_dir, "out.0")
    file_paths["DefaultPath_out_1"] = os.path.join(file_dir, "out.1")
    file_paths["DefaultPath_arc_folder"] = os.path.join(file_dir, "arc\\")
    headers = config["HeaderTexts"]
    log_config = config["Logs"]
    current_time = datetime(1, 1, 1)
    special_buffer_signal = 0
    current_parameter_index = 0
    current_values = {
        i: {
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\xff",
            "Status": False,
        }
        for i in range(200000)
    }
    logger.set_log_config(log_config)
    array_of_buffered_parameters = {}
    old_total_number_of_values= 0
    while True:
        (
        current_values,
        array_of_buffered_parameters,
        current_time,
        special_buffer_signal,
        current_parameter_index,
        old_total_number_of_values
    ) = starchivator.do_archivation_iteration(
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            file_paths,
            headers,
            BLOCK_NUMBER, old_total_number_of_values
        )



def work_cycle(config):
    BLOCK_NUMBER = 3
    config = load(open(config_path, "r"))
    file_paths = config["Paths"]
    headers = config["HeaderTexts"]
    log_config = config["Logs"]
    current_time = datetime(1, 1, 1)
    special_buffer_signal = 0
    current_parameter_index = 0
    current_values = {
        i: {
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\xff",
        }
        for i in range(200000)
    }
    logger.set_log_config(log_config)
    array_of_buffered_parameters = {}
    while True:
        (
        current_values,
        array_of_buffered_parameters,
        current_time,
        special_buffer_signal,
        current_parameter_index,
    ) = starchivator.do_archivation_iteration(
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            file_paths,
            headers,
            BLOCK_NUMBER
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        config = json.load(open(path, "r"))
    else:
        config_path="config.json"
        config = json.load(open(config_path, "r"))
    syncingTiming = open("model/DateTimeMain.py", "r")
    syncingTimingData = [line for line in syncingTiming]
    if syncingTimingData[32].split(" ")[-1].replace("\n","") == "None":
        syncingTiming.close()
        with open ("model/DateTimeMain.py", 'r') as fileForSyncTiming:
            old_data = fileForSyncTiming.read()
        sync = date.today().strftime("%d-%m-%Y") 
        syncing = old_data.replace('#data = None', "#data = "+str(sync))
        with open ("model/DateTimeMain.py", 'w') as fileForSyncTiming:
            fileForSyncTiming.write(syncing)
        working(config=config)
    else:
        def processData(end_time, start_time, BlockN, lenBlocks):
            data = bytearray(random.getrandbits(8) for _ in range(1024))
            base64Encoded = base64.b64encode(data).decode()
            data[:] = base64Encoded.encode()
            return {
                'maxAfterProcessing': max(data),
                'processingTime': end_time - start_time
            }
        start_time = date.today()
        end_time = date.today()
        timerArch = timedelta(days=60) + datetime.strptime(str(syncingTimingData[32].split(" ")[-1].replace("\n","")), "%d-%m-%Y") 
        currentTimer = datetime.now()
        if currentTimer > timerArch:
            try:
                TDateTime.syncTiming()
            except:
                print("Syncing Exception(02). Sync Failed. Contact Developer")
        else:
            working(config=config)