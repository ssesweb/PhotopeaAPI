# `rollup.config.mjs` 文件注释

想象一下，`rollup.config.mjs` 文件就像一个“工厂的生产线蓝图”。它告诉 Rollup 这个打包工具，如何把你的源代码（原材料）加工成最终可以交付的产品（打包后的 JavaScript 文件）。

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

## 配置项解释：

*   `import terser from "@rollup/plugin-terser";`
    *   **比喻**: 就像在工厂蓝图的开头，你声明了你需要使用哪些“特殊工具”。这里引入了 `terser` 插件，它是一个用于压缩和混淆代码的工具，能让最终产品更小、更高效。

*   `export default { ... };`
    *   **比喻**: 这是整个生产线蓝图的“总指挥部”，所有的生产指令都包含在这里面。

*   `input: "src/index.js"`
    *   **比喻**: 就像生产线的“原材料入口”，它告诉 Rollup 从哪个文件开始读取你的源代码。这里是 `src/index.js`，它是 PhotopeaAPI 库的入口文件。

*   `output: { ... }`
    *   **比喻**: 就像生产线的“产品出货区”，这里定义了最终产品的各种属性和如何输出。
    *   `file: "dist/photopea.min.js"`
        *   **比喻**: 就像最终产品的“存放位置和文件名”。它告诉 Rollup 打包后的文件应该叫什么名字，并放在哪个目录下。这里是 `dist` 目录下的 `photopea.min.js`，通常 `min` 表示是压缩过的版本。
    *   `format: "umd"`
        *   **比喻**: 就像产品的“包装格式”。UMD (Universal Module Definition) 是一种通用的模块格式，它能让你的库在多种环境下都能被使用，无论是浏览器、Node.js 还是其他模块加载器，都像一个“万能插头”。
    *   `name: "Photopea"`
        *   **比喻**: 就像产品在全局环境中的“品牌名称”。当你的库在浏览器中被加载时，它会创建一个名为 `Photopea` 的全局变量，其他代码可以通过 `Photopea` 来访问你的库。
    *   `plugins: [ terser() ]`
        *   **比喻**: 就像生产线上的“加工机器”。这里使用了 `terser()` 插件，它会在打包过程中对代码进行压缩和优化，去除不必要的空格、注释，缩短变量名等，从而减小文件大小，提高加载和运行效率。

总的来说，`rollup.config.mjs` 文件是构建 PhotopeaAPI 库的关键配置，它确保了源代码能够被正确地打包、优化，并以通用的格式发布，以便在各种环境中高效使用。