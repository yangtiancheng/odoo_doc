# API

## 
```python
def one(method):
    """ Decorate a record-style method where ``self`` is expected to be a
        singleton instance. The decorated method automatically loops on records,
        and makes a list with the results. In case the method is decorated with
        :func:`returns`, it concatenates the resulting instances. Such a
        method::

            @api.one
            def method(self, args):
                return self.name

        may be called in both record and traditional styles, like::

            # recs = model.browse(cr, uid, ids, context)
            names = recs.method(args)

            names = model.method(cr, uid, ids, args, context=context)

        .. deprecated:: 9.0

            :func:`~.one` often makes the code less clear and behaves in ways
            developers and readers may not expect.

            It is strongly recommended to use :func:`~.multi` and either
            iterate on the ``self`` recordset or ensure that the recordset
            is a single record with :meth:`~openerp.models.Model.ensure_one`.
    """
    split = get_context_split(method)
    downgrade = get_downgrade(method)
    aggregate = get_aggregate(method)
    
    def old_api(self, cr, uid, ids, *args, **kwargs):
        context, args, kwargs = split(args, kwargs)
        recs = self.browse(cr, uid, ids, context)
        result = new_api(recs, *args, **kwargs)
        return downgrade(result)
    
    def new_api(self, *args, **kwargs):
        result = [method(rec, *args, **kwargs) for rec in self]
        return aggregate(self, result)
    
    return make_wrapper(one, method, old_api, new_api)


def get_context_split(method):
    """ Return a function ``split`` that extracts the context from a pair of
        positional and keyword arguments::

            context, args, kwargs = split(args, kwargs)
    """
    pos = len(getargspec(method).args) - 1

    def split(args, kwargs):
        if pos < len(args):
            return args[pos], args[:pos], kwargs
        else:
            return kwargs.pop('context', None), args, kwargs

    return split
    
def getargspec(func):
    """Get the names and default values of a function's arguments.

    A tuple of four things is returned: (args, varargs, varkw, defaults).
    'args' is a list of the argument names (it may contain nested lists).
    'varargs' and 'varkw' are the names of the * and ** arguments or None.
    'defaults' is an n-tuple of the default values of the last n arguments.
    """

    if ismethod(func):
        func = func.im_func
    if not isfunction(func):
        raise TypeError('{!r} is not a Python function'.format(func))
    args, varargs, varkw = getargs(func.func_code)
    return ArgSpec(args, varargs, varkw, func.func_defaults)
```