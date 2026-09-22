# UI 地图来源与主张对应

- https://www.w3.org/TR/wcag/ — W3C 的 WCAG 2.2 规范；支持正文中“可访问性包含颜色、对比、重排、键盘、焦点、目标尺寸等分项成功准则，采用时需区分等级”的主张。
- https://www.w3.org/WAI/WCAG22/understanding/ — WCAG 2.2 Understanding 文档；用于确认上述成功准则的解释入口。该文档是说明材料，不是规范正文。
- https://design-system.service.gov.uk/components/ — GOV.UK Design System 的实际组件目录；支持“真实设计系统同时提供可复用组件、使用指导和代码示例”的主张。
- https://design-system.service.gov.uk/components/error-message/ — GOV.UK 错误消息组件指南；支持“错误应贴近字段、说明具体问题与修复方式，并保留已填内容”的案例与检查项。该做法属于 GOV.UK 场景，不宣称为所有产品唯一方案。
- https://design-system.service.gov.uk/get-started/focus-states/ — GOV.UK 焦点状态说明；支持“焦点状态帮助键盘等输入方式的用户识别当前交互对象，以及真实设计系统会给出焦点视觉规则”的主张。
- https://design-system.service.gov.uk/community/component-lifecycle-statuses/ — GOV.UK 组件生命周期；补充“设计系统组件有成熟度和演进状态，不能把组件库视为永恒不变的样式集合”的理解。本轮正文未据此提出强制要求。
- https://public-media.interaction-design.org/pdf/IDF-Course-Learning-Paths.pdf — Interaction Design Foundation 公开课程路径；其 UI Designer 入门范围同时列视觉模式、Gestalt/视觉知觉和动态网站可用性，用于交叉检查地图的主要分支。目录只支持范围，不证明具体设计效果。
- https://www.gov.uk/service-manual/design/form-structure — GOV.UK Service Manual 的实际表单结构指导；支持“一页一件事是政府服务的起点、是否合并需由用户研究决定”，使正文把 checklist 写成有条件建议，而非通用强制规则。
- https://baymard.com/blog/avoiding-repeat-form-errors — Baymard 结账可用性研究中的真实观察：经历错误后，部分参与者会为避免再次报错而填写不确定是否必要的信息。用于补充错误设计影响后续行为的失败机制；不可直接推出 SaaS 注册页的发生率或转化效果。
- https://baymard.com/blog/form-design — Baymard 电商表单研究汇总及实例；本记录只用它支持“消失标签妨碍纠错”的失败机制，不再将 `+` 邮箱实例归给此页。
- https://baymard.com/blog/validations-vs-warnings — Baymard 关于校验与警告的专项文章；页面正文明确记录邮箱校验器拒绝含 `+` 的合法地址，并称类似问题见于可用性测试及三个站点审计。用于支持“过严校验可能产生假阴性并阻挡合法输入”；迁移到 SaaS 注册页时只作为待检查机制，不推断发生率。
- https://baymard.com/research-articles/inline-form-validation — Baymard 多轮结账测试；支持“内联校验本身也可能因过早触发或修正后不消失而增加阻力”的边界，修正了“只要加校验就更好”的过度概括。

证据边界：真实失败/研究来自政府服务表单和电商结账，与教学 SaaS 注册页相邻但不相同。正文只迁移“值得检查的机制”，不迁移发生率、商业效果或具体布局结论。案例观察仍是模拟，没有声称方案提升注册率。
