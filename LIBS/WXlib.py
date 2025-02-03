import os
import re
from dotenv import load_dotenv

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models import get_model_specs
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes


class WX:
    def __init__(self):
        # load environmental variables
        load_dotenv()
        # set authentication credentials
        self.WX_KEY = os.getenv('WX_KEY')
        self.WX_API = os.getenv('WX_API')
        self.WX_PRJ = os.getenv('WX_PRJ')

        # checking environmental variables 
        if (self.WX_KEY == None) or (self.WX_API == None) or (self.WX_PRJ == None):
            print(f"Set the all required environmental variables: WX_KEY, WX_API and WX_PRJ first! Quitting. Exit code 1")
            quit(1)
         
        # set model default parameters
        self.defaultModelParams = {
                "decoding_method": "greedy",
                "max_new_tokens": 2048,
                "min_new_tokens": 0,
                "stop_sequences": [],
                "repetition_penalty": 1
        }
        # set default model id
        self.defaultModelID = 'meta-llama/llama-3-3-70b-instruct'
        # instantiate LLM model with default values
        self.wxInstModel(modelID=self.defaultModelID, modelParams=self.defaultModelParams)
        return
    
    def wxGetAllModelsSpecs(self):
        try:
            self.models = get_model_specs(self.WX_API)['resources']
        except Exception as e:
            print(f"The WX_API = {self.WX_API} has invalid value! Quitting. Exit code 2")
            quit(2)
        return self.models

    def wxListAllModelIDs(self):
        self.wxGetAllModelsSpecs()
        retVal = []
        for model in self.models:
            retVal.append(model['model_id'])
        return retVal
    
    def wxGetModelSpecs(self, modelID):
        self.wxGetAllModelsSpecs()
        retVal = {}
        for model in self.models:
            if (model['model_id'] == modelID):
                retVal = model
        return retVal

    def wxGetModelParamNames(self):
        retVal = [
            { "name": "decoding_method",    "type": "str",   "values": "'sample' || 'greedy'"},
            { "name": "temperature",        "type": "float", "values": ">=0 && <=2"},
            { "name": "top_p",              "type": "float", "values": ">=0 && <=1"},
            { "name": "top_k",              "type": "int",   "values": ">=1 && <=100"},
            { "name": "random_seed",        "type": "int",   "values": ">0 && <=10^19"},
            { "name": "repetition_penalty", "type": "float", "values": ">=0 && <=2 "},
            { "name": "min_new_tokens",     "type": "int",   "values": ">=0 && <=max tokens supported by LLM"},
            { "name": "max_new_tokens",     "type": "int",   "values": ">=min tokens && max tokens supported by LLM"},
            { "name": "stop_sequences",     "type": "list",  "values": "any list of strings"}
        ]
        return retVal 

    def wxInstModel(self, modelID=None, modelParams=None):
        credentials = { 
            "url"    : self.WX_API, 
            "apikey" : self.WX_KEY
        }
        if (modelID == None):
            modelID = self.defaultModelID
        if (modelParams == None):
            modelParams = self.defaultModelParams
        model = Model( modelID, credentials, modelParams, self.WX_PRJ )
        self.wxModel = model
        return model

    def wxGenText(self, promptTemplate, promptVariables):
        prompt = promptTemplate
        for varName, varValue in promptVariables.items():
            prompt = re.sub("{{" + varName + "}}", varValue, prompt)

        llmResponse = self.wxModel.generate_text( prompt ).strip()
        return llmResponse

if __name__ == "__main__":
    quit(0)