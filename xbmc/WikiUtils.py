'''
Created on 21.04.2011

@author: Montellese
'''

class WikiUtils(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def __xHeading(level, text):
        if level < 0:
            level = 0
            
        extra = level * "="
        return "==%s%s%s==\n" % (extra, text, extra)

    @staticmethod
    def Heading(text):
        return WikiUtils.__xHeading(0, text)
    
    @staticmethod
    def SubHeading(text):
        return WikiUtils.__xHeading(1, text)
    
    @staticmethod
    def SubSubHeading(text):
        return WikiUtils.__xHeading(2, text)
    
    @staticmethod
    def Bold(text):
        return "'''%s'''" % text
    
    @staticmethod
    def Italic(text):
        return "''%s''" % text
    
    @staticmethod
    def HorizontalLine():
        return "----"
    
    @staticmethod
    def NewLine():
        return "<br />\n"
    
    @staticmethod
    def Indent(level = 1):
        if level < 1:
            level = 1
        return level * ":"
    
    @staticmethod
    def ListItem(text, level = 1):
        if level < 1:
            level = 1
        return level * "*" + text + "\n"
    
    @staticmethod
    def NumberedListItem(text, level = 1):
        if level < 1:
            level = 1
        return level * "#" + text + "\n"
    
    @staticmethod
    def Code(language, code):
        return "<syntaxhighlight lang=\"%s\">%s</syntaxhighlight>" % (language, code)
    
    @staticmethod
    def Link(url, text):
        return "[%s %s]" % (url, text)
    
    @staticmethod
    def InternalLink(page):
        return "[[%s]]" % page
    
    @staticmethod
    def SectionLink(section):
        return "[[#%s|%s]]" % (section, section)