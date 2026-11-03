# 账户 API 同步适配器

此目录与桌面程序独立分发，不随桌面安装包预装或自动下载。用户自行取得可信配置，在设置的数据源中预览并导入 JSON，随后显式选择账户、核对请求域名、输入只读凭证并验证。配置中禁止填写 API Key、Secret 或 Passphrase。

当前提供 `providers/binance-spot/adapter.json`，覆盖现有 Spot 只读成交、账户与辅助历史、账户订阅和估值能力。此处不声明 OKX 已接入；通用运行时已用另一种认证协议测试 HMAC-SHA256 Base64、ISO8601、请求头签名及 Passphrase，后续可添加外部适配器。合约、保证金、统一账户余额和手续费符号不能直接当作现货语义。

JSON `config.schemaVersion` 为 2。`adapter` 包含 namespace、HTTPS origin、只读 operations、auth、权限验证、分页与可选 stream。operations 的键是运行时标准能力（`/fills`、`/account` 等），path 是上游实际路径；parameters 可以重命名标准查询参数，值 `-` 表示不发送。response 提供字段路径、对象、数组、枚举、精确标量转换和 productPaths 十进制乘积；不执行脚本。资金事件响应需要映射到标准来源记录，并保留 pending、钱包与金额语义不确定性；不能用映射把未知事实声明为已确认。

权限读取先拒绝未知权限字段，再归一化为 `read`、`ipRestricted` 和 `permissionWrites` 指定的布尔字段。读取成功不等于密钥只读。请求仅 GET；WebSocket 只订阅账户事件，事件只触发 REST 补采，不直接入账。

`fixtures/` 是纯合成响应，不包含真实账户和凭证；当前作为时间、权限、账户、目录、成交的离线契约验证。资金事件、限流、WSS 和估值的运行时回归位于桌面服务测试中。未使用真实账户验证，不代表数据许可或地区合规确认。

验证配置：`python3 scripts/validate.py`。联动桌面运行时：在桌面仓执行 `EXCHANGE_ADAPTER_CATALOG=/absolute/path/exchange-api-providers go test ./backend/services/exchange_import -run TestExternalAdapterFixtureContract`。

## Schema 与分页

`schema.json` 提供 JSON 编辑器结构提示；最终权限、目的地、执行上限与必备能力由桌面运行时严格验证。不要把仅通过 JSON Schema 当成可连接的证明。

`auth.prehash` 是有限 token 序列，可使用 `$query`、`$timestamp`、`$method`、`$requestPath`、`$body`；`auth.headers` 只能引用 `$apiKey`、`$signature`、`$timestamp`、`$passphrase`，不能放真实凭据或表达式。`passphraseRequired` 控制额外输入及后端验证。

`pagination` 明确 `cursorParameter`、`cursorMode`（`inclusive_numeric` / `exclusive`）和 `direction`（`ascending` / `descending`）；必须和上游文档核对，不允许仅靠排序响应推断覆盖。签名后的实际 requestPath 包含已编码查询字符串。`operations.*.success` 可声明 HTTP 200 响应中的业务成功码，`errorPath` 与 `errors` 把上游错误映射为通用错误，远端原文不返回到客户端日志。

权限映射和 Spot 财务模型只接受明确可证实语义。返佣、合约头寸、不同钱包/统一账户以及不能证明 gross/net 的资金来源，需要独立能力或保留未证实，不自动转换成完成流水。
