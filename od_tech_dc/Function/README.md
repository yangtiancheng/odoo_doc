# 第四章 - 功能实现

## 基本功能

### report_xls.py

#### class report_xls(report_sxw)

- def render(self,wanted,col_specs,rowtype,render_space='empty')

```text
    参数解析：
    wanted: 来自wanted_list的预置列
    col_specs:参照specs[1:]，是用xls行模板方法的数据记录
    rowtype:选项'header'或者'data'
    render_space:如果没有特殊指定,是 调用空间+当地上下文集合 是dict字典数据类型
    
    方法解析：
    
```