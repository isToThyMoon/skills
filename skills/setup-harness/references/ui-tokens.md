# UI token

项目有界面时读。目标：之后改页面的 agent 只引用语义 token，整个界面保持一致。

token 分两层，各管一件事：

- **代码 token** 是实际来源，页面引用的就是它。
- **`DESIGN.md`** 用 `assets/DESIGN.template.md` 的格式（[Google DESIGN.md](https://github.com/google-labs-code/design.md)，还在 alpha），写清每个值的用途和设计风格，也让 agent 不用读代码就能理解视觉意图。

## 覆盖范围

字体、颜色、线条、间距、圆角、层级（阴影）、动效，加上写在 `DESIGN.md` 正文里的设计风格。

token 分原始值和语义两级：`blue-500` 是原始值，`color-accent`、`color-surface` 是语义。页面只引用语义，主题和暗色模式才能只改映射。

## 代码 token 放哪

用该技术栈惯用的主题机制，agent 才会自然地用它：

| 技术栈 | 落点 |
| --- | --- |
| Web（CSS） | CSS 变量 |
| Web（Tailwind） | 主题配置，v4 用 `@theme` |
| React Native | `theme.ts` 加 Provider 或 Unistyles 这类主题库 |
| SwiftUI | `Color`、`Font` 扩展和 spacing 常量，颜色放 Asset Catalog |
| Jetpack Compose | `MaterialTheme` 加自定义 `CompositionLocal` |
| Flutter | `ThemeData` 加 `ThemeExtension` |

新建多个代码库共用的视觉时，用 [DTCG](https://www.designtokens.org/) 格式的 JSON 作来源，再用 Style Dictionary 生成各端文件；生成的文件在开头注明"改来源，不改这里"。各端已有自己的 token 时不合并：`DESIGN.md` 写基准端的值，并列出各端的 token 文件和界面规范。

## 步骤

1. **定值。**
   - 已有 token：值保持不变，只核对类别覆盖，然后补 `DESIGN.md` 和检查；第 3 步已经是现状，跳过。
   - 已有界面、没有 token：统计现有代码里的颜色、字号、间距和圆角，按出现频率归并相近的值，写成 token。新 token 要能表达现有界面，这样之后的改动不会让风格突变。
   - 没有界面：问用户产品气质、参考产品、品牌色、明暗模式和信息密度，每项附推荐答案。风格由用户定。间距用固定的阶梯，字号用明确的层级，文字和背景的搭配满足 WCAG AA。
2. **写两层。** 写代码 token 和 `DESIGN.md`，并从 `AGENTS.md` 的"界面"一节链接过去。
3. **接入。** 在应用入口引入 token，让至少一个真实页面或组件用上它。已有页面保持原样，之后改到哪迁到哪，这样 diff 能审查，也不会一次改乱界面。
4. **加反馈。** 在检查入口里加一项，只看尚未提交的新增样式代码（`git diff HEAD` 的新增行，加上 `git ls-files -o --exclude-standard` 列出的新文件），发现硬编码的颜色或间距就报错，并写明该换成哪类 token。旧代码不受影响。技术栈有现成规则时用现成的（例如 `stylelint-declaration-strict-value`）。这项检查在不同技术栈上的准确度还没验证，误报多时收窄到颜色。
5. **校验。** 运行 `npx @google/design.md lint DESIGN.md`，修掉错误和对比度问题。npm 不可用时跳过，并写进报告。

## 完成条件

- 上面列出的类别都有 token，或在 `DESIGN.md` 里写明为什么这个项目不需要。
- 应用实际加载了代码 token，至少一个页面或组件引用它，启动后能看到效果。
- 故意加一个硬编码颜色时，检查入口会报错；撤掉后恢复通过。
- `npx @google/design.md lint DESIGN.md` 没有 error 和 `contrast-ratio` 警告，或已在报告里说明跳过原因。
