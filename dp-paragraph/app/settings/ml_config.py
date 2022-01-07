import configparser


cfg = configparser.ConfigParser()
cfg.read('./environment.ini')


ML = cfg["ml"]

MODEL_PATH = ML['model_path']

CLASS_MAPPING = {'paragraph': 0, 'bg': 1}

NUM_FEATURE = 1024
BBOX_THRESHOLD = 0.8
OVERLAP_THRESS = 0.5

HORIZONTAL_FLIPS = False
VERTICAL_FLIPS = False
ROT_90 = False
NUM_ROIS=32
NETWORK = 'resnet50'  