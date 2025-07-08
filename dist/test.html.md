# `dist/test.html` 文件注释

`dist/test.html` 文件就像一个“PhotopeaAPI 的演示舞台”。它展示了如何将 Photopea 嵌入到网页中，并使用 `Photopea` 类的方法来控制 Photopea 进行各种操作，比如运行脚本、打开图片、导出图像等。

```html
<html>
    <head>
        <script src="./photopea.min.js"></script>
    </head>
    <body>
        <div id="container" style="width: 800px; height: 400px;"></div>
        <script>
            let container = document.getElementById("container");
            Photopea.createEmbed(container).then(async (pea) => {
                let output = await pea.runScript(`
                    app.echoToOE("hello world");
                `);
                console.log(output)
                await pea.openFromURL("https://www.photopea.com/api/img2/pug.png", false);
                await pea.runScript(`app.activeDocument.activeLayer.blendMode = "lddg";`);
                await pea.openFromURL("https://www.photopea.com/api/img2/pug.png", true);
                await pea.runScript(`app.activeDocument.activeLayer.blendMode = "scrn";`);
                await pea.runScript(`app.activeDocument.activeLayer.translate(20, 20);`);
                output = await pea.runScript(`
                    app.echoToOE("hello world 2");
                `);
                console.log(output)
                let finalImage = await pea.exportImage();
                let img = new Image();
                img.src = URL.createObjectURL(finalImage);
                document.body.appendChild(img);
            });
        </script>
    </body>
</html>
```

## 代码解释：

*   `<html>`, `<head>`, `<body>`:
    *   **比喻**: 就像一个标准的“网页骨架”，定义了网页的基本结构。

*   `<script src="./photopea.min.js"></script>`:
    *   **比喻**: 就像“引入 PhotopeaAPI 这个工具包”。这行代码加载了 PhotopeaAPI 库，使得 `Photopea` 类及其方法可以在当前页面中使用。

*   `<div id="container" style="width: 800px; height: 400px;"></div>`:
    *   **比喻**: 就像在网页上“开辟一块画布”，这个 `div` 元素将作为 Photopea 嵌入式界面的容器。它被设置了固定的宽度和高度，以确保 Photopea 有足够的显示空间。

*   `<script>` 标签内的 JavaScript 代码:
    *   **比喻**: 这是“导演” Photopea 舞台表演的脚本。
    *   `let container = document.getElementById("container");`:
        *   获取之前定义的“画布”元素。
    *   `Photopea.createEmbed(container).then(async (pea) => { ... });`:
        *   **比喻**: 就像“在画布上启动 Photopea”。这是 PhotopeaAPI 的核心用法之一，它在 `container` 元素中创建并嵌入 Photopea 应用程序。`then` 方法确保在 Photopea 完全加载并准备好交互后，才执行后续的代码。`pea` 变量就是 Photopea 实例，通过它可以控制 Photopea。
    *   `let output = await pea.runScript(`app.echoToOE("hello world");`);`
        *   **比喻**: 就像“让 Photopea 说句话”。`runScript` 方法允许你向 Photopea 发送内部脚本命令。`app.echoToOE` 是 Photopea 内部的一个 API，用于将信息输出到外部环境（这里是浏览器的控制台）。
    *   `console.log(output)`:
        *   将 Photopea 的输出打印到浏览器的开发者控制台。
    *   `await pea.openFromURL("https://www.photopea.com/api/img2/pug.png", false);`
        *   **比喻**: 就像“在 Photopea 中打开一张新的图片”。这行代码从指定的 URL 加载一张图片，并将其作为新文档打开（`false` 表示不作为智能对象添加到当前文档）。
    *   `await pea.runScript(`app.activeDocument.activeLayer.blendMode = "lddg";`);`
        *   **比喻**: 就像“调整当前图层的混合模式”。这行代码通过 Photopea 内部脚本，将当前活动图层的混合模式设置为 `lddg`（线性减淡）。
    *   `await pea.openFromURL("https://www.photopea.com/api/img2/pug.png", true);`
        *   **比喻**: 就像“再打开一张图片，并添加到当前文档”。这次图片会作为智能对象添加到当前文档中。
    *   `await pea.runScript(`app.activeDocument.activeLayer.blendMode = "scrn";`);`
        *   **比喻**: 就像“再次调整当前图层的混合模式”。将当前活动图层的混合模式设置为 `scrn`（屏幕）。
    *   `await pea.runScript(`app.activeDocument.activeLayer.translate(20, 20);`);`
        *   **比喻**: 就像“移动当前图层”。将当前活动图层向右和向下各移动 20 像素。
    *   `output = await pea.runScript(`app.echoToOE("hello world 2");`);`
        *   再次执行一个脚本并打印输出。
    *   `let finalImage = await pea.exportImage();`
        *   **比喻**: 就像“把 Photopea 里的最终作品保存下来”。这行代码将 Photopea 中当前文档导出为图片（默认为 PNG 格式），并返回一个 `Blob` 对象。
    *   `let img = new Image(); img.src = URL.createObjectURL(finalImage); document.body.appendChild(img);`
        *   **比喻**: 就像“把导出的图片显示在网页上”。这几行代码创建了一个 `<img>` 元素，将导出的 `Blob` 对象转换为一个 URL，然后将图片显示在网页的 `body` 中。

总的来说，`dist/test.html` 是一个功能齐全的示例，它演示了如何利用 PhotopeaAPI 在网页中嵌入 Photopea，并通过 JavaScript 代码对其进行编程控制，实现自动化图像处理任务。