# 02 · 项目选择：Qilin主线与辅助资源

## 如何核对「参考工程说已复现」

先追四件事：数据是否来自公开 Qilin，训练和测试切分如何构造，候选来自全库、采样还是日志，指标按请求或用户如何聚合。若第三方 README 给出很高的 NDCG，却没写候选口径，先查评价入口；不要和自己的全目录召回直接比。Qilin 同时有搜索与推荐数据，文本 query 到笔记与无 query 的个性化推荐也要分开理解。

建议从官方数据和配置厘清输入，再用个人工程看怎样组织完整项目；fun-rec 的 MovieLens 实践可以迁移方法，但数据域与笔记不同，不能把它叫作同一任务复现。模型辅助阅读用 DeepCTR-Torch 比较公开实现；保留各自的版本并在简历里明确「参考」「接入」「复现」各自证据。

首选官方 [RED-Search/Qilin](https://github.com/RED-Search/Qilin) 数据与评测定义，结合 [Rednote-Qilin-Search-Rec-System](https://github.com/WBoxian/Rednote-Qilin-Search-Rec-System) 阅读工程链路。本仓库提供独立的轻量基线，让学习不被完整服务栈阻塞。

| 项目 | 选择理由 | 使用边界 |
|---|---|---|
| Qilin官方 | 真实笔记场景、请求与候选、官方baseline | 首先核对字段与协议 |
| Rednote-Qilin个人系统 | 多路召回到在线服务的工程示例 | 读源码，不直接继承作者指标 |
| fun-rec / 小麦书 | 算法解释与模型实现丰富 | 所查web_project是MovieLens电影案例 |
| DeepCTR-Torch | PyTorch排序模型参考 | 不是完整推荐系统 |
| KuaiRand | 多反馈与随机曝光实验 | 快手视频数据，作为扩展而非小红书数据 |

选择主线后只深入一条：热门/ItemCF → 双塔 → DeepFM或DIN → 重排。初期不同时复现DIEN、PLE、HSTU和生成式推荐。把模型串起来不等于建立了可信评测。

固定版本、来源和许可见 [SOURCES.md](../../SOURCES.md)。我们检查了当前仓库文件与官方样例；未完整部署第三方系统，未复现其报告指标。

---
[返回首页](../../README.md) · [上一章](../01-recsys-basics/README.md) · [下一章](../03-architecture/README.md)
