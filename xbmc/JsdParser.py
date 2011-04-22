'''
Created on 21.04.2011

@author: Montellese
'''

import json
from xbmc.WikiUtils import *

class JsdTypeError(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message

class JsdSchemaError(Exception):
    def __init__(self, message):
        self.message = message

class JsdParser(object):
    @staticmethod
    def Convert(jsonSchema):
        jsonObject = json.loads(jsonSchema)
        if "methods" not in jsonObject:
            raise JsdSchemaError("\"methods\" is missing")
        if "types" not in jsonObject:
            raise JsdSchemaError("\"types\" is missing")
        
        wiki = WikiUtils.Heading("Methods")
        
        namespace = ""
        methods = list(jsonObject["methods"].keys())
        methods.sort()
        for methodName in methods:
            curNamespace = methodName.partition(".")[0]
            
            if curNamespace != namespace:
                namespace = curNamespace
                wiki += WikiUtils.SubHeading(namespace)
                            
            wiki += WikiUtils.SubSubHeading(methodName)
            wiki += JsdParser.__parseMethod(jsonObject["methods"][methodName])
        
        wiki += "\n"
        wiki += WikiUtils.Heading("Global types")
            
        namespace = ""
        types = list(jsonObject["types"].keys())
        types.sort()
        for typeName in types:
            curNamespace = typeName.partition(".")[0]
            
            if curNamespace != namespace:
                namespace = curNamespace
                wiki += WikiUtils.SubHeading(namespace)
                            
            wiki += WikiUtils.SubSubHeading(typeName)
            wiki += JsdParser.__parseType(jsonObject["types"][typeName])
            wiki += "\n"
        
        return wiki
    
    @staticmethod
    def __parseMethod(method):
        wiki = ""
        
        if "description" in method and len(method["description"]) > 0:
            wiki += method["description"]
            wiki += WikiUtils.NewLine()
        
        wiki += WikiUtils.Bold("Permission:") + " "
        wiki += method["permission"]
        wiki += WikiUtils.NewLine()
        
        wiki += WikiUtils.Bold("Parameters:") + " "
        if "params" not in method or len(method["params"]) <= 0:
            wiki += "None\n"
            wiki += WikiUtils.NewLine()
        else:
            wiki += "\n"
            for param in method["params"]:
                wiki += WikiUtils.NumberedListItem(JsdParser.__parseParam(param))
               
        wiki += WikiUtils.Bold("Returns: ")
        wiki += JsdParser.__parseReturn(method["returns"])
        
        return wiki
    
    @staticmethod
    def __parseParam(param):
        return JsdParser.__parseType(param, param["name"])
    
    @staticmethod
    def __parseReturn(returns):
        wiki = ""
        if isinstance(returns, str):
            wiki += WikiUtils.Italic(returns) + "\n"
        else:
            wiki += WikiUtils.NewLine()
            wiki += JsdParser.__parseType(returns)
            
        wiki += "\n"
        return wiki
    
    @staticmethod
    def __parseType(type, name = None, level = 1):
        wiki = ""
        
        if name is None:
            wiki += WikiUtils.Bold("Type:") + " "
        
        if "type" in type:
            wiki += WikiUtils.Italic(type["type"])
            
            if type["type"] == "array" and ("minItems" in type or "maxItems" in type):
                wiki += "["
                if "minItems" in type:
                    wiki += str(type["minItems"]) + ".."

                if "maxItems" in type:
                    wiki += str(type["maxItems"])
                elif "minItems" in type:
                    wiki += "X"
                wiki += "]"
        elif "$ref" in type:
            wiki += WikiUtils.Italic(WikiUtils.SectionLink(type["$ref"]))
        
        if name is not None:
            wiki += " "
            wiki += name
        
        if name is None:
            wiki += WikiUtils.NewLine()
            wiki += WikiUtils.Bold("Optional:") + " "
            
        if "required" not in type or type["required"] == False:
            if name is None:
                wiki += "true"
                
            if "default" in type and not isinstance(type["default"], list) and not isinstance(type["default"], dict):
                if name is None:
                    wiki += WikiUtils.NewLine()
                    wiki += WikiUtils.Bold("Default:") + " "
                else:
                    wiki += " = "
                
                if isinstance(type["default"], str):
                    wiki += "\"%s\"" % type["default"]
                elif type["default"] is not None:
                    wiki += str(type["default"])
                else:
                    wiki += "null"
            
            if name is not None:
                wiki = "[ %s ]" % wiki
        elif name is None:
            wiki += "false"
            
        if "properties" in type:
            wiki += WikiUtils.NewLine()
            wiki += WikiUtils.Bold("Properties:") + "\n"
            
            for property in type["properties"]:
                wiki += WikiUtils.ListItem(JsdParser.__parseType(type["properties"][property], property, level + 1), level)
        
        return wiki
        