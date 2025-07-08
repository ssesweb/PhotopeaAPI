# `README.md` 文件注释

`README.md` 文件就像是这个 PhotopeaAPI 项目的“使用说明书”和“快速入门指南”。它告诉用户这个项目是什么、如何安装、如何使用以及提供了哪些功能。

```markdown
A JS-based wrapper for the [Photopea API](https://www.photopea.com/api/).

## Installation
The easiest way to install photopea.js is through a CDN.
```html
<script src="https://cdn.jsdelivr.net/npm/photopea@1.1.1/dist/photopea.min.js"></script>
```
You can also download [`photopea.min.js`](./dist/photopea.min.js) and host it yourself:
```html
<script src="./photopea.min.js"></script>
```
If you're using a Node framework, like Webpack, Rollup, or Vite, simply install with npm:
```bash
npm install photopea
```
You can then import the module in your code:
```js
import Photopea from "photopea";
```

## Usage
`Photopea` is a class with methods that can interact with any instance of Photopea.
### Constructors
For plugins, use window.parent as the Photopea content window:
```js
let pea = new Photopea(window.parent);
```
To create a new Photopea embed, use `Photopea.createEmbed`:
```js
Photopea.createEmbed(container).then(async (pea) => {
    // photopea initialized
    // pea is the new Photopea object
    // you can also use async/await:
    /*
    let pea = await Photopea.createEmbed(container);
    */
});
```
`container` is the parent DOM element and should be a `div` with a set width and height.
### Methods
These are methods for objects of the Photopea class, created with the constructors above. These are all Promises, so be sure to use `.then()` or `await`.
#### `async runScript(script)`
- `script` (string): the [script](https://www.photopea.com/learn/scripts) to run in Photopea.
- Returns: an array containing all of the scripts outputs, ending with `"done"`.
#### `async loadAsset(asset)`
- `asset` (ArrayBuffer): a buffer of the asset to load in Photopea.
- Returns: `[ "done" ]`.
#### `async openFromURL(url, asSmart=true)`
- `url` (string): The URL of the image/psd file to open.
- `asSmart` (boolean): whether to open the image as a layer. Set to `false` if you are opening an image or psd file in a new document.
- Returns: `[ "done" ]`.
#### `async exportImage(type="png")`
- `type` (string): export image filetype. Can be png or jpg.
- Returns: a Blob of the exported image. To get the image URL, use `URL.createObjectURL`.

## Demo
See [dist/test.html](./dist/test.html)
```

## 内容解释：

*   **项目简介**: “A JS-based wrapper for the [Photopea API](https://www.photopea.com/api/).”
    *   **比喻**: 就像项目的“一句话介绍”，告诉你这个项目是基于 JavaScript 的，并且是 Photopea API 的一个封装库。它提供了一个更方便的方式来使用 Photopea 的功能。

*   `## Installation` (安装)
    *   **比喻**: 就像“如何把这个工具带回家”。这部分说明了如何将 `photopea.js` 库集成到你的项目中。
    *   **通过 CDN**: “最简单的方式是通过 CDN 安装。”
        *   **比喻**: 就像“在线使用”，你不需要下载任何文件，直接在 HTML 中引用一个远程链接即可。这对于快速测试或简单的网页非常方便。
        *   `<script src="https://cdn.jsdelivr.net/npm/photopea@1.1.1/dist/photopea.min.js"></script>`: 这是 CDN 的引用方式。
    *   **本地托管**: “你也可以下载 `photopea.min.js` 并自己托管。”
        *   **比喻**: 就像“下载到本地使用”，你可以把库文件下载下来，放到自己的服务器上，然后从本地引用。这在某些网络受限或需要离线使用的场景下很有用。
        *   `<script src="./photopea.min.js"></script>`: 这是本地引用的方式。
    *   **通过 npm**: “如果你正在使用 Node 框架，比如 Webpack, Rollup, 或 Vite，只需通过 npm 安装。”
        *   **比喻**: 就像“专业工具箱的安装方式”，对于现代 JavaScript 项目，通常会使用包管理器（如 npm）来安装和管理依赖。这使得项目依赖清晰，易于管理和更新。
        *   `npm install photopea`: 这是安装命令。
        *   `import Photopea from "photopea";`: 这是在代码中导入模块的方式。

*   `## Usage` (使用)
    *   **比喻**: 就像“如何操作这个工具”。这部分详细说明了 `Photopea` 类及其方法的用法。
    *   `Photopea` 类: “`Photopea` 是一个类，其方法可以与 Photopea 的任何实例进行交互。”
        *   **比喻**: 就像一个“操作 Photopea 的控制器”，所有与 Photopea 的交互都通过这个类来完成。

*   `### Constructors` (构造函数)
    *   **比喻**: 就像“如何创建这个控制器”。这部分说明了如何获取 `Photopea` 类的实例。
    *   **用于插件**: “对于插件，使用 `window.parent` 作为 Photopea 内容窗口。”
        *   **比喻**: 如果你的代码是 Photopea 内部的一个插件，那么 Photopea 本身就是你的“父窗口”，你可以直接通过 `window.parent` 来获取 Photopea 的控制权。
        *   `let pea = new Photopea(window.parent);`: 插件的实例化方式。
    *   **创建新的 Photopea 嵌入**: “要创建一个新的 Photopea 嵌入，使用 `Photopea.createEmbed`。”
        *   **比喻**: 如果你想在自己的网页中嵌入 Photopea，就像“在你的网页里开辟一个 Photopea 工作区”，你需要使用这个静态方法来创建并初始化 Photopea 实例。
        *   `Photopea.createEmbed(container).then(async (pea) => { ... });`: 嵌入 Photopea 的示例代码。它返回一个 Promise，表示 Photopea 异步加载和初始化。
        *   `container`: 放置 Photopea 嵌入的 HTML 元素，通常是一个设置了宽度和高度的 `div`。

*   `### Methods` (方法)
    *   **比喻**: 就像“控制器上的各种按钮和功能”。这部分列出了 `Photopea` 实例可以调用的所有方法，它们都是异步的（返回 Promise）。
    *   `async runScript(script)`:
        *   **比喻**: 就像“向 Photopea 发送一段命令脚本”。你可以直接执行 Photopea 内部的 JavaScript 脚本，实现高级自动化操作。
        *   `script`: 要执行的脚本字符串。
        *   返回: 脚本的所有输出，以 `"done"` 结尾的数组。
    *   `async loadAsset(asset)`:
        *   **比喻**: 就像“把一个素材文件拖拽到 Photopea 里”。用于加载各种 Photopea 支持的素材（如画笔、字体、图片等）。
        *   `asset`: 素材的 `ArrayBuffer` 数据。
        *   返回: `[ "done" ]`。
    *   `async openFromURL(url, asSmart=true)`:
        *   **比喻**: 就像“从一个 URL 打开图片或 PSD 文件”。你可以指定一个图片的网址，Photopea 会自动加载并打开它。
        *   `url`: 图片/PSD 文件的 URL。
        *   `asSmart`: 是否作为智能对象打开（默认为 `true`）。
        *   返回: `[ "done" ]`。
    *   `async exportImage(type="png")`:
        *   **比喻**: 就像“把 Photopea 里的作品导出成图片”。用于将当前文档导出为 PNG 或 JPG 格式的图片。
        *   `type`: 导出类型，`"png"` 或 `"jpg"`。
        *   返回: 导出的图片 `Blob` 对象。你可以用 `URL.createObjectURL` 来获取图片的 URL。

*   `## Demo` (演示)
    *   **比喻**: 就像“一个可以亲手尝试的例子”。这部分指引用户查看 `dist/test.html` 文件，其中包含了如何使用这个库的实际演示。

总的来说，`README.md` 文件是用户了解和开始使用 PhotopeaAPI 库的第一个也是最重要的文档。