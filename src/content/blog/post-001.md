---
title: "STM32 串口调试踩坑记录"
date: "2026-10-20"
tags: ["STM32", "踩坑"]
summary: "整理 STM32 串口通信调试中遇到的波特率、中断与接线问题。"
---

在嵌入式开发里，串口是最常用也最容易踩坑的调试手段之一。这篇笔记记录我在 STM32 串口调试中遇到的一些典型问题。

## 波特率不匹配

波特率配置错误会导致乱码，常见原因包括：

- 外部晶振频率与代码配置不一致
- 时钟树配置（PLL 分频）算错

排查思路是先用示波器或逻辑分析仪确认实际波特率，再反向核对时钟配置。

## 中断与溢出

接收数据量大时容易触发 `ORE`（溢出错误）。关键是在中断里及时读取 `DR` 寄存器，或者改用 DMA 接收。

```c
// 串口接收中断处理示例
void USART1_IRQHandler(void)
{
    if (USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)
    {
        uint8_t ch = USART_ReceiveData(USART1);
        ring_buffer_push(&rx_buf, ch);
        USART_ClearITPendingBit(USART1, USART_IT_RXNE);
    }
}
```

## 接线注意

TTL 串口接线时 TX 接对方 RX、RX 接对方 TX，并且注意共地。
