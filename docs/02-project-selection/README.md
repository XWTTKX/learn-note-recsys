# 02 · 项目选择：Qilin主线与辅助资源

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
