# eve
EVE online国服相关工具

本系统基于Python 3.6+开发，数据采用 https://www.fuzzwork.co.uk/dump/ 提供的MySQL数据。

## 提供接口

1. /api/search/blueprint?q=xxx  搜索蓝图
2. /api/search/reaction?q=xxx  搜索反应
3. /api/industry/blueprint/materials?id=xxx 根据指定typeID的蓝图给出制造相关的材料信息
