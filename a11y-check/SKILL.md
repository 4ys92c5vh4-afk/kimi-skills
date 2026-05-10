---
name: a11y-check
description: Accessibility (a11y) enforcement for React/Next.js projects. Always activate when writing or reviewing frontend code to ensure aria-label, htmlFor, semantic HTML, color contrast, and keyboard navigation compliance.
---

# Accessibility Enforcement Rules

## Form Elements

- 所有 `<input>`, `<textarea>`, `<select>` 必须有以下之一：
  - 关联的 `<label htmlFor="id">`
  - `aria-label="描述"`
  - `aria-labelledby="label-id"`
- Ant Design 的 `Form.Item` 必须设置 `label` 或 `name`

```tsx
// ✅
<label htmlFor="email">邮箱</label>
<input id="email" type="email" />

// ✅
<input type="text" aria-label="搜索关键词" />

// ❌
<input type="text" placeholder="请输入" />
```

## Buttons & Interactive Elements

- 所有 `<button>` 必须有明确文本内容或 `aria-label`
- 图标按钮（只有图标的）必须加 `aria-label`

```tsx
// ✅
<button aria-label="关闭对话框">
  <CloseIcon />
</button>

// ✅
<button onClick={handleSave}>保存</button>

// ❌
<button onClick={handleDelete}>
  <DeleteIcon />
</button>
```

## Images

- 所有 `<img>` 必须有 `alt` 属性
- 装饰性图片用 `alt=""`

```tsx
// ✅
<img src="/logo.png" alt="生物芯片开放创新中心 Logo" />

// ✅ 装饰性
<img src="/divider.png" alt="" />

// ❌
<img src="/banner.png" />
```

## Color Contrast

- 正文文字与背景对比度 ≥ 4.5:1
- 大文字（18px+ 或 14px+ bold）对比度 ≥ 3:1
- 避免仅用颜色传达信息（如状态必须配合图标或文字）

## Semantic HTML

- 使用正确的语义标签：`<nav>`, `<main>`, `<section>`, `<article>`, `<header>`, `<footer>`
- 不要用 `<div>` 代替 `<button>` 做点击交互
- 表格使用 `<table>`, `<thead>`, `<tbody>`, `<th scope="col">`

## Focus Management

- 所有可交互元素必须可见焦点样式（outline 或 ring）
- Modal/Dialog 打开时焦点应进入对话框
- 焦点顺序遵循 DOM 顺序（避免正序混乱）

## Screen Reader Only Text

```tsx
// 仅对屏幕阅读器可见的辅助文本
<span className="sr-only">当前步骤 3/5</span>
```

Tailwind 的 `sr-only` 类：
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```
