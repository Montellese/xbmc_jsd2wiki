'''
Created on 21.04.2011

@author: Montellese
'''

import sys
import xbmc

def main(argv):
    length = len(argv)
    if length < 1:
        argv.append("../introspect.jsd")
    if length < 2:
        argv.append("../wiki.txt")
        '''print("Usage: jsd2wiki jsonSchemaFile outputFile")
        return -1'''
    
    input = None
    output = None
    try:
        input = open(argv[0], "r")
        jsonSchema = ""
        for line in input:
            jsonSchema += line
            
        output = open(argv[1], "w")
        output.write(xbmc.JsdParser.Convert(jsonSchema))
    except IOError as e:
        print("Error while reading the given file: %s" % argv[0])
    except xbmc.JsdSchemaError as e:
        print("Error in the given json schema: %s" % e.message)
    except xbmc.JsdTypeError as e:
        print("Error while parsing a json schema type named %s: %s" % (e.name, e.message))
    finally:
        if output is not None:
            output.close()
        if input is not None:
            input.close()
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
