# 17 · 资料索引与阅读顺序

## 按你卡住的阶段选资料

1. 数据和口径：读 [Qilin 论文](https://arxiv.org/abs/2503.00501)，从数据切分、候选和任务定义三处记笔记。再回到 toy，亲自核对转换后的第一条请求、数据规模和时间边界。
2. 共现与召回：从仓库的 ItemCF 手算例子开始，再读固定版本的 fun-rec，比较相似度权重、图构建与候选预算。
3. 排序与序列：读 [DeepFM](https://arxiv.org/abs/1703.04247) 和 [DIN](https://arxiv.org/abs/1706.06978)，分别回答「二阶项怎么省掉两两计算」和「为什么候选不同就要重算历史表示」。

阅读完成后的验收是能自己重画模块输入输出、写出损失和提出一个可验证的反例。将数据、论文、代码和作者报告的指标分别记录；详细版本在[来源表](../../SOURCES.md)。

1. [Qilin官方仓库](https://github.com/RED-Search/Qilin)、[论文](https://arxiv.org/abs/2503.00501)、[数据页](https://huggingface.co/datasets/THUIR/Qilin)：先理解任务与数据。
2. [Rednote-Qilin个人系统](https://github.com/WBoxian/Rednote-Qilin-Search-Rec-System)：沿数据、召回、评测、服务逐步读。
3. [fun-rec](https://github.com/datawhalechina/fun-rec)：补协同过滤、DeepFM、DIN与多任务基础。
4. [DeepCTR-Torch](https://github.com/shenweichen/DeepCTR-Torch)：选择PyTorch排序实现对照。
5. [DeepFM论文](https://arxiv.org/abs/1703.04247)、[DIN论文](https://arxiv.org/abs/1706.06978)：理解具体目标和输入。
6. [KuaiRand](https://kuairand.com/)：扩展多反馈与随机曝光研究；Pure版本历史不完整，不当作完整序列日志。

论文阅读记录四项：任务定义、样本与损失、评价协议、适用假设。每看一个模型，回答它比现有基线多解决了什么问题，以及需要付出什么成本。

最新主分支内容可能变化，本仓库源码入口以[SOURCES.md](../../SOURCES.md)的固定提交为准。读懂与运行成功是两件事，运行成功与复现论文指标又是两件事。

---
[返回首页](../../README.md) · [上一章](../16-star/README.md)
