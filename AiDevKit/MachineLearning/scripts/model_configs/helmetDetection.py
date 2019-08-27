# ==============================================================================
# Copyright (c) Microsoft. All rights reserved.
#
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from easydict import EasyDict as edict

__BASE = edict()
cfg = __BASE

# Settings used in Model.register()
__BASE.MODEL_PATH = "MachineLearning/models/newHelmetDetection/"
__BASE.MODEL_NAME = "model.dlc"
__BASE.CONVERTED_MODEL_NAME = "model.dlc"
__BASE.MODEL_TAGS = {"Device": "peabody", "type": "mobilenetssd", "area": "iot", "version": "1.0"}
__BASE.MODEL_DESCRIPTION = "Helmet Detection"

# Settings used in Image.create())
__BASE.IMAGE_NAME = "helmetdetectionv1"

# Settings used in IotContainerImage.image_configuration()
__BASE.IMAGE_TAGS = ["mobilenetssd"]
__BASE.IMAGE_DESCRIPTION = "Helmet Detection module"

# Settings used in deployment.json
__BASE.MODULE_NAME = "Helmet_Detection"
