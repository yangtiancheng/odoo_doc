# pdf报表

## PDF报表结构

- 一个XML数据配置文件
- 一个py文件

Odoo原生的报表通过HTML或者QWeb定义，可以通过Qweb控制流工具，使用wkhtmltopdf来注册pdf。
定义一个报表的主要需要定义1.报表 2.报表模板 3.可以个性化格式 4.可以客户化class来为报表的数据服务


## Report
1. 报表都需要定义一个 report_action：
    可以通过一个<report>标签来定义 report_action.格式定义：
    id - 是report_action的外部ID(ir_model_data可查)
    name(必输) - 数据库中的report_name 用于对应报表模板的外部ID
    file - 数据库中的report_file 与name相同
    string - PDF报表名称 action的下拉名称
    model(必输) - 报表放那个model的界面上
    report_type(必输) - 报表类型 目前我们认为它只有两种打印PDF的qweb-pdf、和打印HTML的qweb-html.
    report_name - 报表名称 输出报表的名字
    groups - 组权限控制 哪个对应的用户组能够触发报表操作
    attachment_use - bool(true/false) 如果设置成True则会将打印的报表以附件attachment的形式存储在系统的附件系统中，用于一次使用，需要测试。
    attachment - python逻辑赋值表达式，用来定义附件存储的文件名称 可使用一定的逻辑判断赋值。
    paperformat - 默认定义为公司下的纸张格式 如果有特殊需要可以自定义纸张格式。
    
```xml
<report
    id="account_invoices"
    model="account.invoice"
    string="Invoices"
    report_type="qweb-pdf"
    name="account.report_invoice"
    file="account.report_invoice"
    attachment_use="True"
    attachment="(object.state in ('open','paid')) and
        ('INV'+(object.number or '').replace('/','')+'.pdf')"
/>
```

## Report Template
1. 报表模板中call外部布局样式，它将添加默认的报表头和报表尾。PDF报表体江北包含在<div class='page'>标签中，template的外部id必须符合报表定义规则，从Qweb模板中，能够通过docs访问对象包含的所有字段。

2. 报表中有一些特定的变量:
    docs - 当前报表的记录集合(数据)
    doc_ids - 当前报表的记录集合的ids列表
    doc_model - docs包含的数据记录来源model
    time - 从python标准库中引用的time对象
    user - 打印报表的用户
    res_company - 当前打印报表用户对应公司
    如果需要访问其他模型的记录集，可以关注后续的客户话报表。
    
3. Translatable Templates(可翻译的模板)
如果需要根据业务伙伴的语言来打印对应语言格式的报表，需要定义两个模板。
- 主报表模板
- 可翻译的文件

可以在主报表模板中加入t-lang属性设置语言来直接调用翻译文件，如果需要对使用的字段等进行翻译，可以对字段附属的对象传入相应的context参数，使对象变的可翻译。
```text
如果没有想要翻译，最好不写，因为写入会重读记录，影响打印效率
```
```xml
<!-- Main template -->
<template id="report_saleorder">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="sale.report_saleorder_document" t-lang="doc.partner_id.lang"/>
        </t>
    </t>
</template>

<!-- Translatable template -->
<template id="report_saleorder_document">
    <!-- Re-browse of the record with the partner lang -->
    <t t-set="doc" t-value="doc.with_context({'lang':doc.partner_id.lang})" />
    <t t-call="web.external_layout">
        <div class="page">
            <div class="oe_structure"/>
            <div class="row">
                <div class="col-xs-6">
                    <strong t-if="doc.partner_shipping_id == doc.partner_invoice_id">Invoice and shipping address:</strong>
                    <strong t-if="doc.partner_shipping_id != doc.partner_invoice_id">Invoice address:</strong>
                    <div t-field="doc.partner_invoice_id" t-options="{&quot;no_marker&quot;: True}"/>
                <...>
            <div class="oe_structure"/>
        </div>
    </t>
</template>
```

解释一下:主报表模板调用附加context属性t-lang为doc.partner_id.lang 的翻译模板，这样就会被对应的语言渲染。这样的话，报表就会打印成对应业务伙伴语言的报表。如果只需要转换报表体内容而不动报表头/尾部分，可以：
```xml
<t t-call="web.external_layout" t-lang="en_US">
```


## Barcodes(条形码)
可以很方便的借助Qweb的语法将条形码嵌入到模板中
```xml
<img t-att-src="'/report/barcode/QR/%s' % 'My text in qr code'"/>
```
可以传递一些参数：
```xml
<img t-att-src="'/report/barcode/?
    type=%s&value=%s&width=%s&height=%s'%('QR', 'text', 200, 200)"/>
```

## Useful Remarks(有效的语法)
1. Report Template可以使用Twitter Bootstrap 和 FontAwesome类来渲染。
2. 本地CSS可以在Template中使用。
3. 可以通过继承主报表样式来插入到我们的css中。

```xml
<template id="report_saleorder_style" inherit_id="report.style">
  <xpath expr=".">
    <t>
      .example-css-class {
        background-color: red;
      }
    </t>
  </xpath>
</template>
```

## Paper Format(纸张格式)
报表格式是report.paperformat对象的记录，它们经常包括如下几个参数:
    name(必输) - 可标识样板格式的简要名称
    description - 对样板简短的介绍
    format - 预定义格式A0-A9 B0-B9 Legal Letter Tabloid... 默认是A4，如果定义了这个参数将无法使用个性化的格式。
    dpi - 输出的DPI 默认为90
    margin_top, margin_bottom, margin_left, margin_right - 边距大小默认单位mm
    page_height , page_width - 页面尺寸 默认单位mm
    orientation - Landscape 或者 Portrait
    header_line - 布尔值 是否显示头行
    header_spacing - 头空间 默认单位mm
    
```xml
<record id="paperformat_frenchcheck" model="report.paperformat">
    <field name="name">French Bank Check</field>
    <field name="default" eval="True"/>
    <field name="format">custom</field>
    <field name="page_height">80</field>
    <field name="page_width">175</field>
    <field name="orientation">Portrait</field>
    <field name="margin_top">3</field>
    <field name="margin_bottom">3</field>
    <field name="margin_left">3</field>
    <field name="margin_right">3</field>
    <field name="header_line" eval="False"/>
    <field name="header_spacing">3</field>
    <field name="dpi">80</field>
</record>
```

## 客户化报表
报表model有一个get_html方法，就是通过report.{module.report_name}来寻找客户化报表model，如果找到的话，将使用找到的这个类来调用Qweb引擎,否则就调用默认方法。如果希望客户化一个包含了各种项的报表模板，就可以定义这个model，重写render_html方法，并且在docargs列表中传递数据。

## 报表都可以在web页面上显示
可以通过例如:
http://<server-address>/report/html/sale.report_saleorder/38
http://<server-address>/report/pdf/sale.report_saleorder/38
如上方式访问html/pdf的报表


## Odoo11 PDF报表实例流程

### 1.创建一个ir.actions.report对象
```xml
<report
    string="界面打印下拉框处显示的文字"
    id="ir_model_data表中创建的数据记录name 其实就是外部id①"
    model="报表绑定的model 在哪个界面上显示"
    report_type="报表类别/qweb-pdf"
    name="hrp_asset.report_asset_transfer_application"
    file="hrp_asset.report_asset_transfer_application"
/>
```








































### XML文件中
1. 首先介绍一下XML文件中的基础格式:
```xml
<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
    </data>
</openerp>
```

2. 初始化一个report数据项:
```xml
<report
    string="界面打印下拉框处显示的文字"
    id="ir_model_data表中创建的数据记录name 其实就是外部id①"
    model="报表绑定的model 在哪个界面上显示"
    report_type="报表类别/qweb-pdf"
    name="hrp_asset.report_asset_transfer_application"
    file="hrp_asset.report_asset_transfer_application"
/>
```

3. 对report项绑定一个数据模板，paperformat_id来自于report.paperformat:
```xml
<record id="ir_model_data表中创建的数据记录name 其实就是外部id①" model="ir.actions.report.xml">
    <field name="paperformat_id" ref="hrp_base.paperformat_horizontal_A4"/>
</record>
```
注:这里的paperformat可以自行定义样式

