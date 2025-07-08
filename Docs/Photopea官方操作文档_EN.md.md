# `Photopea官方操作文档_EN.md` 文件注释

这份文档是 Photopea 官方提供的 API 操作指南，你可以把它想象成一本“Photopea API 的百科全书”或者“使用 Photopea 的高级秘籍”。它详细介绍了如何通过编程方式与 Photopea 进行交互，包括数据传输、环境配置、插件开发等。

## 主要内容概览：

### 1. `Passing data to Photopea` (向 Photopea 传递数据)

*   **比喻**: 就像“给 Photopea 喂食”或“发送指令”。这部分说明了如何通过 URL 的哈希参数向 Photopea 传递一个 JSON 配置对象，从而在 Photopea 启动时加载文件、资源、设置服务器参数、配置环境或执行脚本。
    *   **JSON 配置对象**: 详细解释了 `files` (文件)、`resources` (资源，如画笔、字体)、`server` (保存到服务器的配置)、`environment` (环境设置)、`apis` (第三方 API 密钥) 和 `script` (启动时执行的脚本) 等字段的用途。

### 2. `Saving to server` (保存到服务器)

*   **比喻**: 就像“Photopea 把完成的作品交给你”。这部分描述了当用户在 Photopea 中点击“保存”时，Photopea 如何将文档数据（包括 JSON 元数据和二进制文件）通过 HTTP POST 请求发送到你指定的服务器。还提供了 PHP 示例代码。

### 3. `Your Response` (你的响应)

*   **比喻**: 就像“你给 Photopea 的反馈”。这部分说明了你的服务器在接收到 Photopea 的保存请求后，可以返回一个 JSON 响应，其中包含 `message` (显示给用户的消息)、`script` (Photopea 内部执行的脚本) 和 `newSource` (更新文件源) 等参数。

### 4. `Cross-Origin Resource Sharing` (跨域资源共享)

*   **比喻**: 就像“不同网站之间的通行证”。这部分强调了为了让 Photopea 能够加载你服务器上的文件，你的服务器响应必须包含 `Access-Control-Allow-Origin: *` 头部，以解决跨域问题。

### 5. `Prices` (价格)

*   **比喻**: 就像“使用 Photopea API 的费用说明”。这部分说明了 Photopea API 的基本使用是免费的，但如果需要隐藏广告和使用“白标模式”（Whitelabel Mode），则需要购买分销商账户。

### 6. `Environment` (环境)

*   **比喻**: 就像“Photopea 的个性化设置”。这部分详细介绍了 `environment` 参数，通过它可以自定义 Photopea 编辑器的外观和行为，包括主题、语言、视图模式、工具显示、菜单结构、面板布局、短语替换、工具选项和自定义图标等。这使得你可以高度定制 Photopea 的用户体验。

### 7. `Tool options and menus` (工具选项和菜单)

*   **比喻**: 就像“工具箱里的工具说明书”。这部分提供了具体工具（如移动工具、魔棒工具）的选项和菜单配置示例，帮助你理解如何通过 `topt` 和 `tmnu` 参数来控制工具的行为。

### 8. `Tool IDs` (工具 ID)

*   **比喻**: 就像“Photopea 内部工具的编号”。这部分列出了 Photopea 中各种工具的唯一 ID，这些 ID 在配置 `showtools` 或 `topt`、`tmnu` 时会用到。

### 9. `Live Messaging` (实时消息)

*   **比喻**: 就像“Photopea 和你的网页之间的实时对话”。这部分详细介绍了如何通过 Web Messaging（`postMessage` 和 `addEventListener("message")`）在 Photopea 嵌入式窗口和外部环境（你的网页）之间进行双向通信，传输字符串（脚本）和 `ArrayBuffer`（二进制文件）。
    *   **获取数据**: 说明了如何使用 `app.activeDocument.saveToOE()` 和 `app.echoToOE()` 从 Photopea 中获取数据。
    *   **使用示例**: 提供了将 Photopea 作为“模块”进行批量处理、导出图层、生成名片等高级应用场景的设想。

### 10. `Example: Integrating with a custom storage` (示例：与自定义存储集成)

*   **比喻**: 就像“Photopea 和你的云盘无缝对接”。这部分提供了一个具体的例子，说明如何通过自定义 `File - Open` 和 `File - Save` 的行为，将 Photopea 与你自己的文件存储系统集成。

### 11. `Plugins` (插件)

*   **比喻**: 就像“为 Photopea 扩展功能”。这部分介绍了如何为 Photopea 创建和发布自定义插件。插件本质上是一个嵌入在 Photopea 内部的网页，可以通过 Live Messaging 与 Photopea 交互，实现更丰富的功能，如图片商店、字体画廊等。
    *   **发布插件**: 说明了如何将插件上传到 Photopea 的公共插件库。
    *   **图标 URL**: 提供了自定义插件图标的建议。

总而言之，这份文档是深入理解和利用 Photopea API 进行高级开发和定制的宝贵资源。