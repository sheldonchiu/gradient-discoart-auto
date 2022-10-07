import os
import os.path as osp
import sys
import utils
import torch
from discoart import create, load_config, save_config

os.environ['DISCOART_OPTOUT_CLOUD_BACKUP'] = "1"
os.environ['DISCOART_DISABLE_IPYTHON']="1" 

basePath = os.environ.get('DISCOART_OUTPUT_DIR', "/storage/discoart")
os.environ['DISCOART_OUTPUT_DIR'] = basePath

remoteDir = os.environ.get('S3_REMOTE_DIR', "")

bucketName = os.environ.get('S3_BUCKET_NAME', "discoart")

configFilePath = os.environ.get('DISCOART_CONFIG_FILE_S3', None)
if configFilePath is None:
    sys.exti(0)

if __name__ == '__main__':
    # Get config from S3
    os.system("rm -f *.yml")
    configFile = utils.getConfig(bucketName, configFilePath)
    config = load_config(configFile)

    # Upload the new config to S3 for recording the name_docarray
    text = list(osp.splitext(osp.basename(configFile)))
    text[0] = f"{text[0]}-return"
    newName = ''.join(text)
    save_config(config, newName)
    utils.save(bucketName, osp.join(osp.dirname(configFilePath), newName), newName)

    observer = utils.start_watching(bucketName=bucketName, outputPath=basePath, remoteDir)
    da = create(**config)
