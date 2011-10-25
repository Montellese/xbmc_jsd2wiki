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
        if "result" in jsonObject:
            jsonObject = jsonObject["result"]
        if "methods" not in jsonObject:
            raise JsdSchemaError("\"methods\" is missing")
        if "types" not in jsonObject:
            raise JsdSchemaError("\"types\" is missing")
        if "notifications" not in jsonObject:
            raise JsdSchemaError("\"notifications\" is missing")
        
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
            wiki += JsdParser.__parseType(jsonObject["types"][typeName], None, 1, False)
            wiki += "\n"
            
        wiki += "\n"        
        wiki += WikiUtils.Heading("Notifications")
        
        namespace = ""
        notifications = list(jsonObject["notifications"].keys())
        notifications.sort()
        for notification in notifications:
            curNamespace = notification.partition(".")[0]
            
            if curNamespace != namespace:
                namespace = curNamespace
                wiki += WikiUtils.SubHeading(namespace)
                            
            wiki += WikiUtils.SubSubHeading(notification)
            wiki += JsdParser.__parseMethod(jsonObject["notifications"][notification])
            wiki += "\n"
        
        return wiki
    
    @staticmethod
    def __parseMethod(method):
        wiki = ""
        
        if "description" in method and len(method["description"]) > 0:
            wiki += method["description"]
            wiki += WikiUtils.NewLine()

        if "permission" in method:
            wiki += WikiUtils.Bold("Permissions:") + "\n"
            if isinstance(method["permission"], str):
                wiki += "* " + method["permission"] + "\n"
            else:
                for permission in method["permission"]:
                    wiki += "* " + permission + "\n"
        
        wiki += WikiUtils.Bold("Parameters:") + " "
        if "params" not in method or len(method["params"]) <= 0:
            wiki += "None\n"
            wiki += WikiUtils.NewLine()
        else:
            wiki += "\n"
            wiki += "<div style=\"margin-left: 20px; width: 60%; padding: 0px 5px 0px 5px; border-width: 1px; border-style: solid; border-color: #AAAAAA\">\n"
            for param in method["params"]:
                wiki += WikiUtils.NumberedListItem(JsdParser.__parseParam(param))
            wiki += "</div>\n"
               
        if "returns" in method:
            wiki += WikiUtils.Bold("Returns:") + " "
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
        elif returns is None:
            wiki += "null"
        elif "type" in returns and returns["type"] != "array" and returns["type"] != "object":
            wiki += WikiUtils.Italic(returns["type"])
        elif "$ref" in returns:
            wiki += WikiUtils.Italic(WikiUtils.SectionLink(returns["$ref"]))
        else:
            wiki += "\n<div style=\"margin-left: 20px; width: 60%; padding: 0px 5px 0px 5px; border-width: 1px; border-style: solid; border-color: #AAAAAA\">\n"
            wiki += JsdParser.__parseType(returns, None, 1, False)
            wiki += "\n</div>"
            
        wiki += "\n"
        return wiki
    
    @staticmethod
    def __parseType(type, name = None, level = 1, printDefault = True):
        wiki = ""

        if type is None:
            wiki += "null"
            return wiki
        
        if name is None and "extends" not in type:
            wiki += WikiUtils.Bold("Type:") + " "
        elif name is None and "extends" in type:
            wiki += WikiUtils.Bold("Extends:") + "\n"
        
        if "type" in type:
            if isinstance(type["type"], str):
                if type["type"] == "array" and "items" in type and "$ref" in type["items"]:
                    wiki += WikiUtils.Italic(WikiUtils.SectionLink(type["items"]["$ref"])) + "[]"
                else:
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
            else:
                wiki += WikiUtils.Italic("mixed")
        elif "$ref" in type:
            wiki += WikiUtils.Italic(WikiUtils.SectionLink(type["$ref"]))
        elif "extends" in type:
            if isinstance(type["extends"], str):
                wiki += WikiUtils.ListItem(WikiUtils.Italic(WikiUtils.SectionLink(type["extends"])))
            else:
                for extends in type["extends"]:
                    wiki += WikiUtils.ListItem(WikiUtils.Italic(WikiUtils.SectionLink(extends)))
        
        if name is not None:
            wiki += " "
            wiki += name

        if printDefault == True:
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
        
