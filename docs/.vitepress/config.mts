import { defineConfig } from 'vitepress'
import sidebarGen from './sidebar.gen'

// ============================================================
// 站点配置：想改站名、导航、栏目，只动这一个文件
// sidebar（左侧目录树）由 tools/import_notes.py 导入笔记后
// 自动重写 sidebar.gen.ts，不需要手动维护
// ============================================================

const SECTIONS = [
  { key: 'daily', label: '每日笔记' },
  { key: 'java', label: 'Java' },
  { key: 'bigdata', label: '大数据' },
  { key: 'python-ai', label: 'Python 与 AI' },
  { key: 'governance', label: '数据治理' },
  { key: 'methodology', label: '学习方法论' },
  { key: 'weekly', label: '学习周记' },
]

// 把每个栏目的 sidebar 配置挂到对应路径前缀下
const sidebar: Record<string, any> = {}
for (const s of SECTIONS) {
  sidebar[`/${s.key}/`] = (sidebarGen as any)[s.key] ?? []
}

export default defineConfig({
  lang: 'zh-CN',
  // 部署在 https://<用户名>.github.io/zxblog/ 子路径，base 必须与仓库名一致，
  // 否则线上样式与链接全部 404（本地 dev 路径也会变成 /zxblog/ 前缀）
  base: '/zxblog/',
  title: 'sunzz 的学习笔记',
  description: '个人学习博客：Java、大数据、Python 与 AI、数据治理的学习笔记与每周复盘',
  head: [['meta', { name: 'generator', content: 'VitePress' }]],

  // 本地全文搜索：零依赖零费用，中文可用
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      ...SECTIONS.map((s) => ({
        text: s.label,
        link: `/${s.key}/`,
        activeMatch: `/${s.key}/`,
      })),
      { text: '关于', link: '/about/' },
    ],
    sidebar,
    search: { provider: 'local' },
    outline: { label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到亮色模式',
    darkModeSwitchTitle: '切换到暗色模式',
  },

  // 从 git 提交时间取"最后更新"，所以每次发内容要记得 commit
  lastUpdated: true,
})
