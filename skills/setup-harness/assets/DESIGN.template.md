---
name: {{项目名}}
colors:
  primary: "#0F172A"
  accent: "#0369A1"
  surface: "#FFFFFF"
  on-surface: "#0F172A"
  muted: "#64748B"
  border: "#E2E8F0"
  danger: "#B91C1C"
typography:
  heading:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  stroke-thin: 1px
  stroke-strong: 2px
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "{spacing.sm}"
---

## Overview

{{设计风格：产品气质、面向谁、整体感觉，以及它和同类产品的不同。上面的值是占位，按项目替换。}}

代码里的实际来源是 `{{代码 token 文件}}`。改值时两边同步，页面只引用语义 token。

## Colors

{{每个颜色的用途；什么时候用强调色。}}

## Typography

{{层级怎么用；正文和标题的字体搭配。}}

## Layout

{{间距节奏、栅格、页面密度。线条粗细用 `spacing.stroke-*`，线条颜色用 `colors.border`。}}

## Elevation & Depth

{{用阴影、边框还是背景色区分层级。}}

## Shapes

{{圆角的使用规则。}}

## Components

{{核心组件的状态：默认、悬停、按下、禁用、加载、空、错误。}}

## Do's and Don'ts

- {{这个产品特有的取舍，每条写"要怎样"以及原因。}}
