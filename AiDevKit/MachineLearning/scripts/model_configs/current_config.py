# ==============================================================================
# Copyright (c) Microsoft. All rights reserved.
#
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

#Copy entire model config file text here for pre-configured model
from easydict import EasyDict as edict

__BASE = edict()
cfg = __BASE

# Settings used in Model.register()
__BASE.MODEL_PATH = MachineLearningmodelsModel Folder Name Here
__BASE.MODEL_NAME = Model Name Here
__BASE.CONVERTED_MODEL_NAME = Model Name Here
__BASE.MODEL_TAGS = {Device peabody, type mobilenetssd, area iot, version 1.0}
__BASE.MODEL_DESCRIPTION = Generic Description of Model Here

# Settings used in Image.create())
__BASE.IMAGE_NAME = Provide a Name for your image Here

# Settings used in IotContainerImage.image_configuration()
__BASE.IMAGE_TAGS = [mobilenetssd]
__BASE.IMAGE_DESCRIPTION = Provide Description of your Module Image here

# Settings used in deployment.json
__BASE.MODULE_NAME = Provide Module Name Here

# Settings used in SnpeConverter.convert_tf_model()
# In order to fill this in section, you will need to use Tensorboard to open your prebuilt tensorflow model
# You will then need to identify the Input_Node and Output_Node required for the specific model.

__BASE.MODEL_INPUT_NODE =
__BASE.MODEL_INPUT_DIMS =
__BASE.MODEL_OUTPUTS_NODES = []

# Settings used in SnpeConverter API (TensorFlow  Caffe)
__BASE.SNPECONVERTER_TYPE = TensorflowCaffee
