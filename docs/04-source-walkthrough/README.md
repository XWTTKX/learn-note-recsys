# 04 · 源码阅读路线与关键检查点

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
