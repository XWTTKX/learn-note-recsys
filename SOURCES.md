# 来源与版本

核对日期：2026-11-17。以下SHA通过git取得；资料按固定版本组织，不依赖搜索摘要中的星数或指标。

| 来源 | 固定版本 | 用途 | 许可核对 |
|---|---|---|---|
| [bcefghj/learn-nanobot](https://github.com/bcefghj/learn-nanobot) | [740d041a52e1](https://github.com/bcefghj/learn-nanobot/tree/740d041a52e1d50499aabc70ec5bd6ae592737d0) | 结构参考；未复制正文 | MIT |
| [RED-Search/Qilin](https://github.com/RED-Search/Qilin) | [299c02667e1d](https://github.com/RED-Search/Qilin/tree/299c02667e1dc98dd8e62aa5e13a8e04a9d0363b) | 官方数据、配置与评价源码 | README声称MIT，但所查根目录未见LICENSE；数据卡标注Apache-2.0 |
| [WBoxian/Rednote-Qilin-Search-Rec-System](https://github.com/WBoxian/Rednote-Qilin-Search-Rec-System) | [763764e8ab99](https://github.com/WBoxian/Rednote-Qilin-Search-Rec-System/tree/763764e8ab99410098439e2f57158227a7ce18f2) | 第三方完整工程阅读 | MIT |
| [datawhalechina/fun-rec](https://github.com/datawhalechina/fun-rec) | [5f7bd84d4403](https://github.com/datawhalechina/fun-rec/tree/5f7bd84d4403b5f92b6bedbd31e3984ef00a4572) | 模型原理与实现补充 | README声明CC BY-NC-SA 4.0；不复制正文或实现 |
| [shenweichen/DeepCTR-Torch](https://github.com/shenweichen/DeepCTR-Torch) | [9eccef78e581](https://github.com/shenweichen/DeepCTR-Torch/tree/9eccef78e5810c61d6a04ddc7d96279e3db9c970) | PyTorch排序模型补充 | Apache-2.0 |

## 原创与引用边界

本仓库教程、轻量基线、样例和测试为本项目编写；参考仓库以链接和固定版本阅读路线引用。没有将上游完整实现改名后冒充原创。第三方代码、数据、图片和权重的许可不随本仓库MIT许可改变。

## 调研方法与限制

已检查仓库README、文件树与部分核心源码。未对第三方完整系统做部署验证。主分支、README报告和搜索缓存可能互相不一致，比较结果须重新核对提交、配置、数据和候选池。

官方数据入口：[THUIR/Qilin](https://huggingface.co/datasets/THUIR/Qilin)；论文：[Qilin](https://arxiv.org/abs/2503.00501)。数据页标注Apache-2.0，仍需按实际下载版本保存许可与引用。此仓库只含原创合成请求，不重新分发Qilin日志。

补充：[KuaiRand](https://kuairand.com/)。它来自快手，不是小红书数据。当前主线已有Qilin，不必为了项目名把视频或电影数据改称小红书数据。

fun-rec的书名“小麦书”不代表其web_project是小红书推荐复刻；已读版本明确使用MovieLens-1M。Rednote-Qilin是个人工程，不代表官方生产架构。
