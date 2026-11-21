# 06 · 轻量运行与真实数据接入

## 先读输出，再调参数

默认样例一共 120 条请求，通常会看到训练 84、测试 36、训练目录 16。四行分别对应目录热门、目录 ItemCF、日志热门、日志 ItemCF。先比较同一个 protocol 下的两种方法；不要拿目录的一个数字和日志的另一个数字得出提升。原始样例为展示指标故意生成，不代表线上效果。

```bash
python3 scripts/coverage_lab.py --k 5
```

该命令只核查可达上限和历史覆盖，目录大时也无需逐请求排列整个目录。若 toy 导入失败，先检查文件后缀、原始与索引 ID 字段配对、JSON 是否可解析。当前转换器拒绝覆盖已有输出；异常后输出可能是半成品，不要把它用于正式评测，换一个新路径重跑。验收真实样例以 [验证记录](../../experiments/VALIDATION.md) 的校验值和切分为准。

## 第一步：标准库demo

```bash
python3 scripts/demo.py
python3 -m unittest discover -s tests -v
```

Python 3.9+，不需GPU。120条原创合成请求只检查代码是否正确运行，不能作为业务指标。输出包含热门与ItemCF、训练目录全量召回和日志候选重排两种协议。

## 第二步：官方toy CSV

```bash
python3 scripts/fetch_references.py
python3 scripts/import_qilin.py vendor/Qilin/datasets/toy_data/csv/recommendation_toy.csv data/processed/qilin-toy.jsonl
python3 scripts/demo.py --data data/processed/qilin-toy.jsonl
```

toy文件名不保证规模很小。纯Python全目录排序在较大样例上较慢；先用小子集检查结构，再考虑向量化或稀疏实现。转换器拒绝覆盖输出文件，重复运行请使用新文件名。

## 第三步：正式数据

从数据页取得parquet并核实字段。安装pyarrow后对每个分片运行转换器，结构化索引字段用 `--indexed`；先检查有user_idx、request_idx及候选note_idx。按官方split分别合并，不混淆train/test。

```bash
python3 scripts/import_qilin.py data/raw/train.parquet data/processed/train.jsonl --indexed
python3 scripts/import_qilin.py data/raw/test.parquet data/processed/test.jsonl --indexed
python3 scripts/demo.py --data data/processed/train.jsonl --test data/processed/test.jsonl --k 10
```

train.parquet/test.parquet是本地命名示例，并非声称远端存在同名文件。完整parquet接入与训练未在交付环境验证。不要直接下载全部图片、模型和百万内容后再第一次检查字段。

---
[返回首页](../../README.md) · [上一章](../05-data-protocol/README.md) · [下一章](../07-recall/README.md)
