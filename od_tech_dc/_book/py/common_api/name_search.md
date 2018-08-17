# name_get

## 数据筛选
通常我们使用的数据筛选，可能是通过某一个字段A关联的字段范围，来控制B字段的取值，常见的方式就是
以添加compute字段的m2m辅助字段来限制B字段的取值范围。这样可能会因为辅助字段上存在_id或者_ids
的字段，而使得前台界面加载几十次对应的name_get而转圈。
替换方式，去掉辅助字段，在需要被限制字段的XML视图定义中加入相应的context，然后在相应的name_search方法中，
获取context，通过中间传入的参数进行数据获取判断后拼接domain，使得界面的值域被修正。
例如:
```xml
<field name="partner_id"
       options="{'no_create_edit':'1','no_create':'1','no_open':'1'}"
       attrs="{'required':[('partner_force_analytic','=',True)]}"
       context="{'display_name_and_code':True，'account_id':account_id}"/>
```

```python
@api.model
def name_search(self, name='', args=[], operator='ilike', limit=100):
    # 如果业务伙伴是通过科目上的业务伙伴核算限制范围的话 我们可以直接用name_search传入context值限制范围
    if self._context.has_key('account_id'):
        account_id = self._context.get('account_id')
        if account_id:
            domain = self._get_account_id_limit_domain(account_id)
            args += domain
        else:
            args = [('id', '=', -1)]

@api.model
def _get_account_id_limit_domain(self,account_id=None):
    # 通过科目上的业务伙伴限制domain值集
    account = self.env['account.account'].browse(account_id)
    supplier = False
    customer = False
    employee = False
    domain = ['|', ('parent_id', '=', False), ('is_company', '=', True)]
    if account and account.partner_force_analytic:
        for record in account.partner_force_analytic:
            if record.code == 'supplier':
                supplier = True
            if record.code == 'customer':
                customer = True
            if record.code == 'employee':
                employee = True
        # 科目上业务伙伴值集domain拼接
        domain += supplier and [('supplier', '=', True)] or [('supplier', '=', False)]
        domain += customer and [('customer', '=', True)] or [('customer', '=', False)]
        domain += supplier and [('employee', '=', True)] or [('employee', '=', False)]
        print domain
        return domain
```

[参考文章](https://blog.csdn.net/vnsoft/article/details/80834984)