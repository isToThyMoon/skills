# 消息队列领域地图：来源与主张对应

- https://kafka.apache.org/40/design/design/#message-delivery-semantics  
  支持：发布持久性与消费处理保证是两个问题；Kafka 默认语义及事务/幂等能力有明确作用范围；写外部系统时 exactly-once 需要目标系统协作。用于收窄“exactly-once 等于端到端副作用一次”的说法。

- https://docs.oasis-open.org/amqp/core/v1.0/amqp-core-transport-v1.0.html#section-message-transfers  
  支持：AMQP settlement 时机可形成 at-most-once、at-least-once 等不同保证；at-least-once 可能因重发产生重复处理。用于确认确认时机、重复与丢失之间的关系。

- https://www.oasis-open.org/standard/amqp/  
  支持：AMQP 1.0 是 OASIS 标准，覆盖传输、消息、事务和安全等部分。用于区分开放协议规范与具体 Broker 产品行为。

- https://www.rabbitmq.com/docs/confirms  
  支持：publisher confirms 与 consumer acknowledgements 是相互独立、分别覆盖发布端和消费端的数据安全机制。用于纠正“有 ack 就端到端可靠”的笼统表达。

- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html  
  支持：消息在 visibility timeout 内暂时不可见，未完成删除后会再次可见；at-least-once 模型仍不能绝对排除重复；超时设置与处理时间、重试延迟存在取舍。用于补充托管队列的 lease/可见性模型。

- https://stripe.com/blog/idempotency  
  支持：网络中断会令操作结果不确定；稳定业务标识可让重试安全；指数退避与 jitter 可减少故障服务遭同步重试冲击。这是带实际实现背景的工程实践，不作为 Broker 协议保证。

- https://opentelemetry.io/docs/specs/semconv/messaging/messaging-metrics/  
  支持：消息客户端消费计数以及 messaging system、destination、consumer group、partition、error type 等通用遥测属性；页面也标示部分语义仍为 Development。用于可观测性分支，并限制“标准已经完全稳定”的主张。

- https://docs.oasis-open.org/amqp/core/v1.0/amqp-core-messaging-v1.0.html  
  支持：AMQP 消息 header 中 durable、ttl、delivery-count 的规范含义；delivery-count 可提示之前的不成功投递。用于校准“持久消息”“过期”“重复迹象”等术语，未据此推断所有产品实现完全一致。

## 明确证据缺口

本轮尝试检索公开事故材料，但未获得一份内容可直接核查、且专门对应消息丢失/重复处理的完整当事团队复盘。因此正文没有把教学模拟或通用反模式伪装成真实事故；进入具体产品与版本后，应继续补充真实事故复盘、部署架构和容量基线。
