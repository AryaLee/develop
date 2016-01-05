from types import *
# import sys ##sys.modules[__name__] ....info

class strategyPattern(object):
    def __init__(self, strategy_module = '__main__'):
        self.strategy_module = strategy_module
        self.strategy = None

    def get_strategy(self, strategy_name):
        strategy = self._get_class(strategy_name)
        if self.strategy:
            del self.strategy

        self.strategy = strategy()

    def operate(self):
        self.strategy.operate()

    def _get_class(self, class_name):
        module = __import__(self.strategy_module)
        return getattr(module, class_name)

class firstStrategy(object):
    def operate(self):
        print self.__class__.__name__

class secondStrategy(object):
    def operate(self):
        print self.__class__.__name__


if __name__ == '__main__':
    strategy_module_name = '__main__'

    test = strategyPattern(strategy_module_name)
    test.get_strategy('firstStrategy')
    test.operate()
    print test.strategy

    test.get_strategy('secondStrategy')
    test.operate()
    print test.strategy_last


