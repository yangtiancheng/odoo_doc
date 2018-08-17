# 属性篇

## attrs(公共属性)
> invisible
:影藏组件。

> required
:组件必须有值。

> readonly
:组件只读不可编辑(onchange过来的值不会被保存，需要在create/write方法中加入到vals中，或者开发个性化readonly存储挂件，例如:readonly_by_pass)。

<p style="color:red">
如果后面的条件是类似domain形式的，那么[(A,'OP',B)]中，A是一个可选的字段，但是这个字段不能像py中的domain，它不能使用A.b这样的字段引用关系。
所以如果我们需要把这样的A.b字段在我们的模型中定义一个related字段，并把它放在xml中，这就是我们所谓的</p><B>辅助字段</B>。

## options(m2o关系字段属性)
> no_create_edit
:关系字段不允许在当前界面创建这个字段对应的模型记录。

> no_create
:不允许直接在当前界面创建字段对应的模型记录(从代码中看no_create_edit和no_create逻辑一样)。

> no_open
:不允许打开关系字段后面对应的单据。

<h5 style="color:red;">注意：最好用no_open:True/False，不要过度使用no_open:'0'/'1',经过测试['0' == '1' == True]</h5>

## options(o2m关系字段属性)
> no_edit_no_open
:关系字段不允许在当前界打开对应记录的form界面。

## 批量添加
> 1.batch_add(新开发js挂件非原生)

    直接在o2m的XML字段属性上挂载batch_add="true"即可。

> 2.ids_select

    这个比较复杂:
    1.首先在py文件的头行结构中，定义一个头字段ids_select,字段属性定义如下:
    ids_select = fields.Char(string='ids', help='This id is to get ids of multiple select of one2many')
    
    2.然后再XML的头部放入ids_select字段，可影藏，字段定义如下:
    <field name="ids_select" class="oe_o2mx" invisible="1" on_change="updateLines(ids_select,o2m_filed,context)"/>
    
    3.绑定对应的o2m字段，将挂件 widget="o2mx" 加到XML字段属性定义中。对应需o2m_filed的tree上要批量添加的主体字段(m2o_field)挂载 multiple_selection="true" 属性。
    
    4.对ids_select定义on_change的方法updateLines进行逻辑处理:
    - 通用结构:
        if not ids_select: return 0
        selected_ids = ids_select.split(',')
        if len(o2m_filed) == 1:
            change_line = False
            o2m_filed = self.o2m_filed.browse(o2m_filed[0][2])
        else:
            change_line = True
            o2m_filed = map(lambda x: x[2], filter(lambda x: x[2], o2m_filed))

        res = []
        old_value = []
        add_ids = []
        line_number = 0
        for line in o2m_filed:
            line_number += 1
            m2o_field = change_line and line['m2o_field'] or line.m2o_field.id
            old_value.append({
                'line_number':line_number,
                'm2o_field': m2o_field,
                'field1': field1,
                'field2': field2,
                'field3': field3,
                ...
            })
            add_ids.append(m2o_field)

        for id in selected_ids:
            line = self.env['selected_ids_model'].browse(int(id))
            if int(id) not in add_ids:
                line_number += 1
                res.append({
                    'line_number': line_number,
                    'm2o_field': line.m2o_field.id or False,
                    'field1': line.field1,
                    'field2': line.field2,
                    'field3': line.field3,
                    ...
                })
        if res:
            return {'value': {'invoice_detail_ids': old_value + res}}

    
    -

## Datas文件
>noupdate

```text
noupdate是加载在data标签块上的属性，如果noupdate="1",则对应data块中的record记录不会再被加载，或者说是不会被初始化值。
当然，如果data块上的noupdate="1"，在record块上还有一个forcecreate的属性，可以用来在data块是noupdate情况下，升级模块中如果
当前record记录没有被创建时，创建记录。
```