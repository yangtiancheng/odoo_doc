from inspect import currentframe, getargspec


class A:

    def func1(para1=1, context={'name': 'lixuanyuan'}, *args, **kwargs):
        return True


a = A()
funcx = a.func1
x = getargspec(funcx)
print 1
