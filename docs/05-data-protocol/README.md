# 05 · Qilin字段、数据划分与泄漏防护

数据入口是 [THUIR/Qilin](https://huggingface.co/datasets/THUIR/Qilin)，包含推荐请求、历史和候选反馈。数据许可与上游代码许可分别记录；不把原始日志或笔记内容打包上传自己的GitHub。

## 已检查的样例CSV

`recent_clicked_note_ids` 与 `rec_result_details` 是可解析JSON；同文件的某些 `*_idxs`/`*_with_idx` 单元格呈NumPy风格字符串，不能直接json.loads。适配器默认使用成对的原始ID字段，绝不混用原始ID历史和整数索引候选。

统一输出为 `request_id,user,timestamp,history,candidates[{id,click}]`。同请求同笔记多次曝光暂按max(click)合并，时间取最早曝光；这是教学协议，会丢失位置与重复曝光信息。正式逐曝光CTR实验必须保留原始曝光键和时间。

## 防泄漏清单

1. 按请求或会话划分，不能把同一请求的不同候选随机分到train/test。
2. 历史来自请求前，不从“用户全部点击”反推测试历史。
3. 热门、共现、统计特征只用训练期；跨时间窗口统计须保存截止时间。
4. 验证集调参，测试集不做负例挖掘或超参选择。
5. 发布时间、曝光后互动统计、未来点击不能当请求时可知特征。

默认demo对样例按请求最早时间做70/30切分，不拆相同时间戳。该划分不是官方benchmark协议，且不保证会话完全隔离；正式复现保留官方split并额外审计会话交集。`--test`支持显式训练/测试输入，但仅检查request_id重叠，不会自动验证全部历史时间。

---
[返回首页](../../README.md) · [上一章](../04-source-walkthrough/README.md) · [下一章](../06-quickstart/README.md)
