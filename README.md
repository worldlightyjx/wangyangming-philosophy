# 王阳明全集 · 文白对照交互版

这是一个将《王阳明全集》整理为**可检索、可按卷浏览、支持文言 / 白话 / 对照切换**的本地网页项目。

当前项目已经完成：

- 基于 PDF 提取整书原文
- 按卷切分为前端可加载的数据文件
- 生成整书导航与全文搜索
- 已补入《传习录》上、中、下三卷的新版白话释义

## 项目目标

将《王阳明全集》制作成一个适合阅读和继续整理的本地代码仓库：

- **原文整书接入**
- **逐卷逐段文白对照**
- **交互式网页阅读**
- **后续可持续补写白话释义**

需要特别说明的是：

1. 古文原文可直接使用。
2. 现代白话译文不能直接照搬现成版本，因此本项目中的白话部分采用**重新撰写的释义**。

## 当前入口

- 主入口：`index.html`
- 兼容入口：`王阳明全集-文白对照.html`（会自动跳转到 `index.html`）

本地双击 `index.html` 即可阅读；部署到 GitHub Pages 时也会默认使用这个入口。

## 目录结构

```text
.
├── README.md
├── index.html                    # GitHub Pages / 本地主入口
├── 王阳明全集-文白对照.html      # 兼容旧链接的跳转页
├── 王阳明全集.pdf                # 当前使用的 PDF 文件
├── data/
│   ├── book-index.js            # 全书卷索引
│   ├── raw-pages.json           # PDF 提取后的分页原始文本
│   ├── volumes/                 # 40 卷原文数据
│   └── baihua/                  # 按卷侧载的白话释义
├── scripts/
│   └── generate_book_data.py    # PDF -> 分卷数据脚本
└── 其他中间文件/调试文件
```

## 数据说明

### `data/volumes/`

这里存放整书原文分卷数据。目前共 **40 卷**，前端按需加载。

每个文件格式大致为：

```js
window.BOOK_VOLUMES["juan01-cxl-shang"] = {
  id: "...",
  title: "...",
  blocks: [
    { type: "para", wen: "原文", bai: "", page: 70 }
  ]
};
```

### `data/baihua/`

这里存放按卷补写的白话释义，不直接改写原文卷文件，而是以“侧载覆盖”的方式接入页面。

当前已完成：

- `juan01-cxl-shang.js`
- `juan02-cxl-zhong.js`
- `juan03-cxl-xia.js`

也就是《传习录》上、中、下三卷。

## 使用方式

### 1. 打开网页

直接双击或在浏览器中打开：

```text
index.html
```

如果仍从旧文件名打开：

```text
王阳明全集-文白对照.html
```

页面也会自动跳转到 `index.html`。

### 1.1 GitHub Pages 部署

如果仓库地址是：

```text
https://github.com/worldlightyjx/wangyangming-philosophy
```

那么启用仓库 Pages 后，默认访问地址会是：

```text
https://worldlightyjx.github.io/wangyangming-philosophy/
```

### 2. 页面功能

- 左侧按册 / 按卷导航
- 顶部切换：
  - 文言
  - 白话
  - 对照
- 全书全文搜索
- 白话按卷逐步补入，补完即显示

## 开发工作流

### 1. 从 PDF 生成原文卷数据

脚本：

```bash
python3 scripts/generate_book_data.py
```

用途：

- 读取 PDF
- 提取分页文字
- 按卷切分
- 输出到 `data/volumes/`
- 生成 `data/book-index.js`

> 注意：`scripts/generate_book_data.py` 里当前写死了 PDF 文件名。如果你更换 PDF 文件，需要同步修改脚本中的 `PDF_PATH`。

### 2. 补写白话

白话不是写回 `data/volumes/`，而是新增到：

```text
data/baihua/<volume-id>.js
```

格式为：

```js
window.BOOK_BAIHUA = window.BOOK_BAIHUA || {};
window.BOOK_BAIHUA["juan01-cxl-shang"] = {
  blocks: [
    "对应第 1 段的白话释义",
    "对应第 2 段的白话释义"
  ]
};
```

要求：

- 顺序必须和对应卷的 `blocks` 一一对应
- 数量必须完全一致
- 白话尽量贴近原文，保留问答、转折、比喻和论证层次

## 当前进度

### 已完成

- 整书 PDF 原文提取
- 40 卷原文数据生成
- 网页按卷加载与全文搜索
- 《传习录》上、中、下三卷白话重写

### 未完成

- 文录、别录、外集、续编、年谱等其余卷的白话释义
- 进一步提升部分卷的逐句细译程度

## 适合继续扩展的方向

- 继续补完其余 37 卷白话
- 增加章节定位 / 段落锚点
- 增加卷内目录或标题索引
- 增加搜索结果跳转高亮
- 增加构建脚本或本地静态服务器说明

## 备注

本项目更适合当作一个**持续整理中的数字人文 / 古籍阅读工程**，而不是一次性完成的静态成品。当前仓库已经具备完整骨架，后续主要工作集中在白话释义质量与覆盖范围的持续完善。
