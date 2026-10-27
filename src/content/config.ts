import { defineCollection, z } from 'astro:content';

// 博客集合：frontmatter 字段校验（title / date / tags / summary）
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.string()).default([]),
    summary: z.string(),
  }),
});

export const collections = { blog };
