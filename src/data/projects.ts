// 项目数据：新增项目只需在数组末尾追加一条
export interface Project {
  id: string;
  name: string;
  description: string;
  thumbnail: string;
  tags: string[];
  detail: string;
}

export const projects: Project[] = [
  {
    id: 'proj-001',
    name: '水产养殖环境监测物联网系统',
    description: '基于 STM32 与多种传感器，实现水温、溶氧、pH 等水质指标的实时采集与远程监测。',
    thumbnail: '/assets/projects/proj-001.svg',
    tags: ['STM32', '传感器', '物联网'],
    detail:
      '主导设计并实现一套水产养殖环境监测系统：以 STM32 为控制核心，集成水温、溶解氧、pH 等传感器，通过串口与通信模块上报数据；服务端对采集数据进行存储与阈值告警，帮助养殖户及时发现水质异常。项目覆盖嵌入式开发、传感器采集、通信协议与上位机展示等环节。',
  },
  {
    id: 'proj-002',
    name: '大模型 LoRA 微调实验',
    description: '使用 LoRA 对开源大模型进行领域微调，包含数据集清洗、训练与评估的完整流程。',
    thumbnail: '/assets/projects/proj-002.svg',
    tags: ['LoRA', '微调', '数据集'],
    detail:
      '围绕领域问答场景，完成数据集清洗、格式对齐与 LoRA 微调实验，对比微调前后效果并记录踩坑经验。（占位示例，待补充完整技术方案与成果）',
  },
];
