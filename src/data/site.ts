// 站点全局配置：姓名、联系方式、Slogan、技能分组等
export interface Skill {
  name: string;
  level: string;
}

export interface SkillGroup {
  title: string;
  // 图标类型，由 Skills 组件映射为对应内联 SVG
  icon: 'chip' | 'ai' | 'tools' | 'web';
  skills: Skill[];
}

export const site = {
  name: '李鑫',
  role: '物联网 · 嵌入式 · AI',
  slogan: '一边焊板子，一边调模型；游走在硬件与 AI 的交界',
  lead: '物联网工程专业，专注嵌入式系统与大模型技术实践，喜欢动手落地工程。',
  about: '物联网工程专业，专注嵌入式系统与大模型技术实践。熟悉 STM32 单片机、传感器数据采集、物联网监测系统开发；同时学习大模型 SFT、LoRA 微调、数据集清洗与处理。主导过水产生态监测物联网项目，喜欢动手落地工程，闲暇爱好水族造景，目前正在备考研究生，持续沉淀技术。',
  email: 'sid0928@foxmail.com',
  emailObfuscated: 'sid0928 [at] foxmail.com',
  skillGroups: [
    {
      title: '嵌入式硬件',
      icon: 'chip',
      skills: [
        { name: 'STM32', level: '熟练' },
        { name: '51 单片机', level: '熟练' },
        { name: '传感器', level: '熟悉' },
        { name: '串口通信', level: '熟悉' },
        { name: '电路基础', level: '掌握' },
      ],
    },
    {
      title: 'AI 大模型',
      icon: 'ai',
      skills: [
        { name: 'Transformer', level: '了解' },
        { name: 'LoRA 微调', level: '实践' },
        { name: 'SFT', level: '实践' },
        { name: '数据集处理', level: '熟悉' },
        { name: 'Prompt 工程', level: '熟悉' },
      ],
    },
    {
      title: '开发工具',
      icon: 'tools',
      skills: [
        { name: 'Git', level: '熟练' },
        { name: 'VSCode', level: '熟练' },
        { name: 'Keil', level: '熟练' },
        { name: 'Python', level: '熟悉' },
        { name: 'Docker', level: '了解' },
      ],
    },
    {
      title: '前端基础',
      icon: 'web',
      skills: [
        { name: 'HTML', level: '熟悉' },
        { name: 'CSS', level: '熟悉' },
        { name: 'Tailwind CSS', level: '熟悉' },
        { name: 'JavaScript', level: '了解' },
      ],
    },
  ],
} as const;
