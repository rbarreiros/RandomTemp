#
# Cura Random temperature post processing script
# Author:   Rui Barreiros
# Date:     27/12/2023
#
# Description: Ultimaker Cura post processing plugin to randomize temperature each layer
# 

from ..Script import Script
from UM.Application import Application
from UM.Logger import Logger
from random import randrange, seed

__version__ = '0.1'

class RandomTemp(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "RandomTemp",
            "key": "RandomTemp",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "minTemp":
                {
                    "label": "Minimum Temperature",
                    "description": "Minimum allowed random temperature",
                    "type": "int",
                    "default_value": 190,
                    "minimum_value": 150,
                    "maximum_values": 350,
                    "minimum_value_warning": 160,
                    "maximum_value_warning": 300
                },
                "maxTemp":
                {
                    "label": "Maximum Temperature",
                    "description": "Maximum allowed random temperature",
                    "type": "int",
                    "default_value": 210,
                    "minimum_value": 150,
                    "maximum_values": 350,
                    "minimum_value_warning": 160,
                    "maximum_value_warning": 300
                },
                "stepsTemp":
                {
                    "label": "Temperature steps",
                    "description": "Temperature step changes each layer",
                    "type": "int",
                    "default_value": 5,
                    "minimum_value": 1,
                    "maximum_values": 20,
                    "minimum_value_warning": 1,
                    "maximum_value_warning": 15
                },
                "layerStartOffset":
                {
                    "label": "Layer Start Offset",
                    "description": "At which layer should we start randomizing?",
                    "type": "int",
                    "default_value": 2,
                    "minimum_value": 0,
                    "maximum_values": 10000,
                    "maximum_value_warning": 1000
                },
                "layerEndOffset":
                {
                    "label": "Layer End Offset",
                    "description": "At which layer offset should we stop (max layer - offset)",
                    "type": "int",
                    "minimum_value": 0,
                    "maximum_values": 10000
                }
            }
        }"""
    
    def execute(self, data):

        minTemp = self.getSettingValueByKey("minTemp")
        maxTemp = self.getSettingValueByKey("maxTemp")
        stepsTemp = self.getSettingValueByKey("stepsTemp")
        layerStart = self.getSettingValueByKey("layerStartOffset") + 2
        layerEnd = self.getSettingValueByKey("layerEndOffset")

        seed()

        lastTemp = maxTemp
        lastLayer = len(data) - 2

        for layer in data:
            layer_idx = data.index(layer)

            lines = layer.split("\n")
            for line in lines:
                if line.startswith(";LAYER:"):
                    line_idx = lines.index(line)

                    if (layer_idx >= layerStart) and (layer_idx <= (lastLayer - layerEnd)):
                        topTemp = maxTemp
                        botTemp = minTemp

                        if lastTemp + stepsTemp >= maxTemp:
                            topTemp = maxTemp - stepsTemp
                        if lastTemp - stepsTemp <= minTemp:
                            botTemp = minTemp + stepsTemp

                        randTemp = randrange(botTemp, topTemp, stepsTemp)

                        if (botTemp != topTemp) and (lastTemp == randTemp):
                            randTemp = randrange(botTemp, topTemp, stepsTemp)

                        lastTemp = randTemp

                        lines.insert(line_idx + 1, ";TYPE:RANDOM TEMP")
                        lines.insert(line_idx + 2, f"M104 S{str(randTemp)}")
            
            res = "\n".join(lines)
            data[layer_idx] = res

        return data
