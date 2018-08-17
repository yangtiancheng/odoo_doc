# onchange的动态domain

## Onchange函数可以返回一个字典

```text
    on_change in OpenERP has 3 possible values returned finally in a dictionary or a {} .
    
    1: The value dictionary i.e {field1:value1,field2:value2}
    
    2: The domain dictionary i.e {field1:domain1}
    
    3: The warning
    
    Syntax:
    
    res = {'value':{},'domain':{},'warning':'Warning Message'}
    According to your case add this to the return dictionary.
    
    {'domain':{'partner_id':[('customer','=',True)]}}
```
<h2 style="color:red;">
通过[1]我们可以改变界面上的数值,通过[2]我们可以改变界面取值的域(动态domain),通过[3]可以定义一个警告信息 
</h2>