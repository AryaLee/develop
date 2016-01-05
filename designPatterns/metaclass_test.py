import sys

class test(object):
    def __init__(self):
        self.father_name = self.__class__.__name__

    def operate(self):
        print 'test operate'

class test1(test):
    def operate(self):
        print 'test1 operate'


if __name__ == '__main__':

    #a = type('test1', (test,), {'name': 'hello'})
    #b = __import__('metaclass_test')
    print sys.modules[__name__].__dict__
    print sys.modules[__name__].__doc__
    print sys.modules[__name__].__name__

    a = getattr(sys.modules[__name__], 'test1')
    print a
    print a().father_name


####################################################################################################################
# type(string, father class tuple, attribute_dict) generate a class
# 
# 
####################################################################################################################
