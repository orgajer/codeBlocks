#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
修改日期        修改人        修改内容
2015-05-13    organo.xia     基础版本
"""

import traceback

class Step:
    def __init__(self, name='step'):
        self.name = name
        self.initStep()

    def total(self):
        return self._totalsteps

    def initStep(self):
        self.__step__ = []
        self.idx = 0
        self._totalsteps = 0

    def currentStepIde(self):
        idx = self.idx + 1
        return idx

    def register(self, func, jump=True):
        """
        para func: 按顺序注册的函数，每个函数返回值必须含有一个执行是否成功。
        para jump: 本次步骤执行完成后就否跳转到下个步骤。
        """
        assert(func)
        regfunc = (func, jump)
        self.__step__.append(regfunc)
        self._totalsteps += 1

    def _getJumpStatus(self):
        """
        Obtain jump to next step status.
        """
        func, jumpStatus = self.__step__[self.idx]
        return jumpStatus

    def _getCurExecFunc(self):
        """
        Obtain current execute function.
        """
        func, jumpStatus = self.__step__[self.idx]
        return func

    def reset(self):
        self.idx = 0

    def isFinalStep(self):
        return self.idx is self._totalsteps

    def executeOne(self, *args, **kwargs):
        """
        para *args: arguments
        para **kwargs: keyword argument
        """
        if self.isFinalStep():
            raise RuntimeError("Step Error", "The executeOne is run in last step, but you aren't reset it.")
        func = self._getCurExecFunc()
        try:
            result = func(*args, **kwargs)
            if result and len(result) >= 2:
                retBool = result[0]
                if retBool:
                    self.idx += 1
                else:
                    self.idx = 0
            else:
                self.idx += 1
            return result
        except:
            self.idx = 0
            info = traceback.format_exc()
            print info

    def execute(self, *args, **kwargs):
        """
        para *args: arguments
        para **kwargs: keyword argument
        """
        while not self.isFinalStep():
            self.executeOne(*args, **kwargs)
            if self._getJumpStatus():
                break


if __name__ == '__main__':
    def func(n="NonePara"):
        print "Hello, this is the %s function" % (n)
    def funcArgs(*args):
        para = ', '.join([str(x) for x in args])
        print para
    def funcKwargs(**kwargs):
        argsList = [(k, v) for k,v in kwargs.iteritems()]
        print str(argsList)
    
    step = Step()
    step.register(func)
    step.register(funcArgs)
    step.register(funcKwargs)

    # 单步执行程序
    for i in range(3):
        step.executeOne(i)
        step.executeOne('one', 'two', 'three', 'four')
        step.executeOne(a='One', b='Two', c='Three', d='Four')
        print 
        step.reset()

    # 自动跳转到下一步，直到执行结束或执行到跳转标志
    step.execute()
