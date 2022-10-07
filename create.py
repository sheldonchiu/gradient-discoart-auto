import os
import sys
import utils
import torch
from discoart import create, load_config, save_config

os.environ['DISCOART_OPTOUT_CLOUD_BACKUP'] = "1"
os.environ['DISCOART_DISABLE_IPYTHON']="1" 

basePath = os.environ.get('DISCOART_OUTPUT_DIR', "/storage/discoart")
os.environ['DISCOART_OUTPUT_DIR'] = basePath

bucketName = os.environ.get('S3_BUCKET_NAME', "discoart")

configFilePath = os.environ.get('DISCOART_CONFIG_FILE_S3', None)
if configFilePath is None:
    sys.exti(0)
configFile = utils.getConfig(bucketName, configFilePath)
# configFile = "test.yaml"
config = load_config(configFile)

observer = utils.start_watching(basePath=basePath, bucketName=bucketName)

da = create(**config)
