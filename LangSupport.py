from re import compile as re_compile
from string import join as str_join

findall_gb   = re_compile('[\x81-\xff][\x00-\xff]|[^\x81-\xff]+').findall
findall_utf8 = re_compile('[\u2e80-\uffff]|[^\u2e80-\uffff]+').findall
sub_gb       = re_compile(
    '([\x81-\xff][\x00-\xff]) +(?=[\x81-\xff][\x00-\xff])').sub
sub_utf8     = re_compile('([\u2e80-\uffff]) +(?=[\u2e80-\uffff])').sub
sub_space    = re_compile(' +').sub

def remove_space(s):
    notFound = True
    ns = u''
    for i in s:
        if i == ' ' and notFound:
            notFound = False
        elif i == ' ' and not notFound:
            ns += i
            notFound = True
        else:
            ns += i
    return ns

LangSupport = type('LangSupport', (object, ),
        {'__init__': lambda self, encoding = 'ISO8859-1': self.__setattr__('_encoding', encoding),
         '__call__': lambda self, s: self.input(s),
         'input'   : lambda self, s: ' '.join(s),
         'output'  : lambda self, s: remove_space(s) } )

GBSupport = type('GBSupport', (LangSupport, ),
        {'input' : lambda self, s:
                str_join( findall_gb( type(s) == str and unicode(
                    s, self._encoding) or s ) ),
         'output': lambda self, s:
                sub_space(' ', sub_gb(r'\1', ( type(s) == str and unicode(s, 'UTF-8') or s ).encode(self._encoding) ) ) } )

UnicodeSupport = type('UnicodeSupport', (LangSupport, ),
        {'input' : lambda self, s:
                str_join( findall_utf8(
                    type(s) == str and unicode(s, self._encoding) or s ) ),
         'output': lambda self, s:
                sub_space(' ', sub_utf8(r'\1', ( type(s) == str and unicode(s, 'UTF-8') or s ).encode(self._encoding) ) ) } )
