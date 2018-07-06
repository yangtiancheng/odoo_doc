# 基础设施

1. 发票产品根据供应商类别筛选,这里name_search方法中有代码context定义:
```python
        if self.env.context.get('vendor_category_ids', False) and self.env.context.get('vendor_category_ids', False)[0][2]:
            args += [('product_tmpl_id.product_top_categ_id.id','in',self.env.context.get('vendor_category_ids', False)[0][2])]
```
如果能够给模型传入供应商类别(m2m)上下文，则控制产品是这些供应商类别下。这里的product_top_categ_id是产品上产品类别的顶级视图类别。

