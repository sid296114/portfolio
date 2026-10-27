---
title: "LoRA 微调入门笔记"
date: "2026-10-24"
tags: ["LoRA", "微调", "大模型"]
summary: "用通俗的方式梳理 LoRA 微调的基本原理与参数选择。"
---

LoRA（Low-Rank Adaptation）通过在权重矩阵旁并联低秩矩阵来实现轻量微调，训练时只更新新增的低秩参数，显存占用和训练成本都大幅下降。

## 核心思想

对于原始权重 `W`，LoRA 将其增量分解为两个低秩矩阵的乘积：

```
W' = W + ΔW = W + B · A
```

其中 `A` 和 `B` 的秩 `r` 远小于原始维度，因此参数量很小。

## 关键参数

- `r`（秩）：越大表达能力越强，但参数量也越大
- `alpha`：缩放系数，通常配合 `r` 一起调整
- `target_modules`：对哪些层注入 LoRA，一般选择注意力层的 `q`、`v` 投影

```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
)
```
