# `src/index.js` 文件注释

这个 `index.js` 文件是 PhotopeaAPI 库的核心，它定义了一个 `Photopea` 类，封装了与 Photopea 应用程序进行交互的各种方法。你可以把它想象成一个“遥控器”，通过它你可以控制 Photopea 里的各种功能。

```javascript
import terser from "@rollup/plugin-terser";

export default {
    input: "src/index.js",
    output: {
        file: "dist/photopea.min.js",
        format: "umd",
        name: "Photopea",
        plugins: [
            terser()
        ],
    },
};
```

## `Photopea` 类：

*   **比喻**: 就像 Photopea 应用程序的“代理人”或“操作员”，所有与 Photopea 的通信和操作都通过这个类来完成。

### 静态方法：

*   `static async createEmbed(parentElement, config)`
    *   **比喻**: 就像“建造一个 Photopea 工作台”。这个方法负责在你的网页中创建一个 `<iframe>` 元素，并在其中加载 Photopea 应用程序。你可以通过 `config` 参数来预设 Photopea 的一些初始设置，比如打开特定的文件或设置界面语言。
    *   `parentElement`: 你想把 Photopea 工作台放在哪个“房间”里（HTML 元素）。
    *   `config`: Photopea 的“装修方案”或“初始设置”，可以是 JavaScript 对象或 JSON 字符串。
    *   **工作原理**: 它会创建一个 `<iframe>`，设置样式，然后将 Photopea 的 URL 和配置作为参数加载到 `<iframe>` 中。它还会监听 Photopea 内部发出的“done”消息，确保 Photopea 完全加载并准备好交互后，才返回一个 `Photopea` 实例。

### 构造函数：

*   `constructor(contentWindow)`
    *   **比喻**: 就像“拿到 Photopea 工作台的控制权”。当你通过 `createEmbed` 创建了一个 Photopea 实例后，这个构造函数会用 `<iframe>` 的 `contentWindow`（Photopea 运行的那个窗口）来初始化 `Photopea` 对象，这样你就可以开始发送命令了。
    *   `contentWindow`: Photopea 应用程序运行的那个“窗口”对象。

### 实例方法：

*   `async runScript(script)`
    *   **比喻**: 就像“向 Photopea 发送指令脚本”。你可以把一段 JavaScript 代码作为字符串发送给 Photopea，让它在内部执行。这非常强大，因为 Photopea 内部有自己的 API（比如 `app.activeDocument`），你可以用它来自动化很多操作。
    *   `script`: 要在 Photopea 内部执行的 JavaScript 代码字符串。
    *   **工作原理**: 它会先暂停一小段时间（`_pause`），然后通过 `postMessage` 将脚本发送给 Photopea。同时，它会监听 Photopea 返回的消息，直到收到“done”为止，然后返回所有 Photopea 的输出。

*   `async loadAsset(asset)`
    *   **比喻**: 就像“把素材拖拽到 Photopea 里”。这个方法允许你加载各种 Photopea 支持的素材，比如画笔、字体、样式或图片等。你可以把一个 `ArrayBuffer` 格式的素材数据发送给 Photopea。
    *   `asset`: 要加载的素材数据，通常是 `ArrayBuffer` 类型。
    *   **工作原理**: 类似于 `runScript`，它通过 `postMessage` 发送素材数据，并等待 Photopea 返回“done”。

*   `async openFromURL(url, asSmart=true)`
    *   **比喻**: 就像“从网上打开一张图片到 Photopea”。你可以提供一个图片的 URL，Photopea 会自动从该 URL 加载图片。`asSmart` 参数决定是作为智能对象添加到当前文档，还是在新文档中打开。
    *   `url`: 图片的 URL。
    *   `asSmart`: 是否作为智能对象添加到当前文档（默认为 `true`）。
    *   **工作原理**: 它会先获取当前文档的图层或文档数量，然后发送 `app.open` 脚本命令来打开 URL。接着，它会等待图层或文档数量发生变化，以确认图片已成功加载。

*   `async exportImage(type="png")`
    *   **比喻**: 就像“把 Photopea 里的作品导出成图片”。这个方法允许你将当前 Photopea 文档导出为 PNG 或 JPG 格式的图片。它会返回一个 `Blob` 对象，你可以用它来显示图片或下载。
    *   `type`: 导出的图片格式，可以是 `"png"` 或 `"jpg"`（默认为 `"png"`）。
    *   **工作原理**: 它会发送 `app.activeDocument.saveToOE` 脚本命令来触发导出，并等待 Photopea 返回图片数据（`buffer`），然后将数据封装成 `Blob` 对象返回。

*   `async _pause(ms=10)`
    *   **比喻**: 这是一个“小憩”或“等待”的内部方法。它只是简单地暂停一小段时间（默认为 10 毫秒），以确保 Photopea 有足够的时间处理上一个命令，避免命令发送过快导致的问题。这是一个辅助方法，确保异步操作的顺序性。

总的来说，`src/index.js` 文件提供了一个高级抽象，让你能够方便地通过 JavaScript 代码来控制 Photopea 应用程序，实现自动化操作和集成。