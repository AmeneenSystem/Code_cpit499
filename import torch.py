import torch

from IPython.display import Image, clear_output  # to display images
from utils.downloads import attempt_download 
from roboflow import Roboflow
rf = Roboflow(model_format="yolov5", notebook="roboflow-yolov5")

# clear_output()
print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

from roboflow import Roboflow
rf = Roboflow(api_key="ermtHXrdxS4YN2L8PXFs")
project = rf.workspace("ameneen").project("ameneen")
dataset = project.version(1).download("yolov5")

import yaml
with open(dataset.location + "/data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])