# 04 · 源码阅读路线与关键检查点

## 跑一次，然后顺着参数往里读

执行 `python3 scripts/demo.py --k 5`。脚本先读 JSONL（每行一个请求），未显式指定测试集时走 `temporal_split`。训练请求构造一个 [Recommender](../../scripts/recommender.py)，之后两种候选协议、两种策略都复用这一个实例。因此四行里的差别主要来自候选池与排序方式，而不是重复训练得到不同权重。

在 `__init__` 里先注意三张表：训练曝光目录 `catalog`、训练点击次数 `pop`、用户点击过的去重集合 `histories`。某用户同一张笔记点三次，对热门计数贡献三次，但对 ItemCF 的这个用户共现只贡献一次。没被点击但有曝光的笔记可以进训练目录，热门计数默认为 0，也没有邻接分。

追到 `rank`：`candidates is None` 表示全训练目录，否则取传入候选。若需要过滤已看，用集合差去掉；打分用 `(-cf,-pop,id)`，所以相似度是首要键，热度只在相似度同分时决定，最后用 ID 保证稳定顺序。它没有将两个分数线性相加。这个细节很适合面试：如果一个候选只有 0.001 的协同分，另一个没有但很热门，当前代码仍把前者放前。

## 具体的断点与排查方法

| 现象 | 首先查 | 原因 |
|---|---|---|
| 某笔记同时出现在训练和测试候选 | 先对比 request_id 和时间 | 同一笔记跨时间是正常的，整条请求泄漏才不行 |
| 冷启动用户全返回热门 | 打印 history 和 sim 的键交集 | 无历史或历史全不在图中，所有相似分为 0 |
| 换候选协议后指标大涨 | 打印候选池大小和正例覆盖 | 日志候选已被旧策略筛选 |
| 输出无指标 | 检查 excluded_no_positive | 宏平均不能把无标签请求当模型全错 |
| 显式测试集仍高得反常 | 检查时间和特征联表时刻 | `--test` 入口只检查请求 ID 的交集与非空 |

如要确认一条请求的排名，手动打印 `history`、每个种子笔记的相似度字典、候选点击标签和排序结果。候选的点击标签只应在计算指标时使用。若有人提议把测试集点击笔记也加入历史，画出请求级时间线就能直接指出泄漏。

上游阅读顺序可从 Qilin 的样本构造、模型输入数据集、预测、评价依次追；先找 ID 是 raw 还是 indexed，再检查候选池是全库、采样还是日志内。不能把某个模型文件里的损失函数当作整个 benchmark。

先执行 `python3 scripts/fetch_references.py` 下载固定提交，路径对应 [SOURCES.md](../../SOURCES.md)。

| 路径 | 阅读问题 |
|---|---|
| Qilin `baselines/src/dataset_factory.py` | 历史、正例、负例如何构造？ |
| Qilin `baselines/src/evaluator.py` | 候选集是全库还是给定曝光？指标分母是什么？ |
| Qilin `baselines/config/recommendation_dpr_config.yaml` | 训练、评测的数据键与配置如何关联？ |
| Rednote `src/backend/offline/evaluation_contract.py` | 如何约束评测口径与输出？ |
| Rednote `src/backend/online/pipeline.py` | 召回、粗排、精排如何串联和降级？ |
| Rednote `src/recall/dssm_trainer.py` | 双塔损失、负例和向量导出在哪里？ |
| fun-rec `src/funrec/models/deepfm.py` | FM与DNN如何共享特征表示？ |

这些是固定提交的文件阅读入口，不是已验证的所有行为描述。先读数据，再读loss，最后读模型结构；数据泄漏不会因为换模型自动消失。

本仓库 `scripts/import_qilin.py` 将记录转成统一请求；`recommender.py` 仅从训练请求建立点击热门与ItemCF；`demo.py` 显式区分两种评价候选池。读完应能在纸上还原一条曝光如何变成一个正例和一条指标贡献。

源码任务：检查官方配置中的训练轮数、评测样本数、evaluate_type，修改为自己的资源预算，并记录修改。不能原封不动运行一个超大轮数后把进程还活着当作成功。

---
[返回首页](../../README.md) · [上一章](../03-architecture/README.md) · [下一章](../05-data-protocol/README.md)
