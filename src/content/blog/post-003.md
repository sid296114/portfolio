---
title: "传感器数据采集与滤波"
date: "2026-10-26"
tags: ["传感器", "嵌入式"]
summary: "介绍常见传感器数据抖动的原因与滑动平均滤波的实现。"
---

模拟传感器采集的数据经常伴随噪声与抖动，直接使用会影响系统的稳定性。这篇笔记整理常用的数据平滑方法。

## 抖动来源

- 电源纹波与电磁干扰
- ADC 采样精度与参考电压波动
- 传感器本身的漂移

## 滑动平均滤波

滑动平均实现简单、效果明显，适合大多数温度、水质等缓变信号。

```c
#define N 8

float moving_average(float new_sample)
{
    static float buf[N] = {0};
    static int idx = 0;
    float sum = 0;

    buf[idx] = new_sample;
    idx = (idx + 1) % N;

    for (int i = 0; i < N; i++)
        sum += buf[i];

    return sum / N;
}
```

对于突变信号（如液位、流量），可以结合中值滤波或一阶低通滤波来兼顾响应速度与稳定性。
