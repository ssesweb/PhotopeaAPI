import json
import urllib.parse
import json
import os
import base64

class PhotopeaAPI:
    def __init__(self, base_url="https://www.photopea.com"):
        self.base_url = base_url
        self.current_document = None

    def open_psd_file(self, file_path_or_url: str):
        """打开 PSD 文件，支持本地文件路径或远程 URL"""
        file_to_load = file_path_or_url

        if os.path.exists(file_path_or_url):
            # 如果是本地文件路径，则读取文件内容并转换为 Data URI
            try:
                with open(file_path_or_url, "rb") as f:
                    file_content = f.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                # 根据文件扩展名判断 MIME 类型，这里只做简单判断，实际应用中可能需要更完善的 MIME 类型映射
                file_extension = os.path.splitext(file_path_or_url)[1].lower()
                if file_extension == ".psd":
                    mime_type = "image/vnd.adobe.photoshop"
                elif file_extension == ".png":
                    mime_type = "image/png"
                elif file_extension == ".jpg" or file_extension == ".jpeg":
                    mime_type = "image/jpeg"
                else:
                    mime_type = "application/octet-stream" # 默认二进制流
                
                file_to_load = f"data:{mime_type};base64,{encoded_content}"
                print(f"本地文件 {file_path_or_url} 已转换为 Data URI。")
            except Exception as e:
                print(f"读取本地文件 {file_path_or_url} 失败: {e}")
                return None
        elif not (file_path_or_url.startswith("http://") or file_path_or_url.startswith("https://")):
            print(f"警告: '{file_path_or_url}' 既不是有效的文件路径也不是有效的URL。")
            return None

        config = {
            "files": [file_to_load]
        }
        encoded_config = urllib.parse.quote(json.dumps(config))
        full_url = f"{self.base_url}#{encoded_config}"
        print(f"请在浏览器中打开此URL以打开PSD文件: {full_url}")
        # 在实际应用中，您可能需要嵌入一个iframe并监听postMessage事件
        # self.current_document = "some_identifier_for_the_opened_document"
        return full_url

    def _send_script(self, script: str):
        """通过 Live Messaging 发送脚本到 Photopea"""
        # 在实际应用中，这需要通过 postMessage 实现，这里仅为模拟输出
        print(f"发送 Photopea 脚本: {script}")

    def show_hide_layer(self, layer_name: str, visible: bool):
        """显示/隐藏图层"""
        # Photopea 脚本示例: app.activeDocument.layers.getByName("Layer1").visible = true;
        script = f"app.activeDocument.layers.getByName(\"{layer_name}\").visible = {str(visible).lower()};"
        self._send_script(script)

    # 待实现的其他功能
    def activate_layer(self, layer_name: str):
        """激活图层"""
        # Photopea 脚本示例: app.activeDocument.activeLayer = app.activeDocument.layers.getByName("Layer1");
        script = f"app.activeDocument.activeLayer = app.activeDocument.layers.getByName(\"{layer_name}\");"
        self._send_script(script)

    # 待实现的其他功能
    def modify_layer_text(self, layer_name: str, new_text: str):
        """修改图层文字""" 
        # Photopea 脚本示例: app.activeDocument.layers.getByName("LayerName").textItem.contents = "New Text";
        script = f"app.activeDocument.layers.getByName(\"{layer_name}\").textItem.contents = \"{new_text}\";"
        self._send_script(script)

    # 待实现的其他功能
    def replace_layer_image(self, layer_name: str, image_url: str):
        """替换图层图片"""
        # Photopea 脚本示例: app.activeDocument.layers.getByName("LayerName").replaceContents("image_data_url");
        # 注意: 实际应用中 image_url 需要是 Photopea 可访问的 URL 或 Data URI
        script = f"app.activeDocument.layers.getByName(\"{layer_name}\").replaceContents(\"{image_url}\");"
        self._send_script(script)

    # 待实现的其他功能
    def export_as_image(self, format: str = "png"):
        """导出为图片"""
        # Photopea 脚本示例: app.activeDocument.saveToOE("png");
        script = f"app.activeDocument.saveToOE(\"{format}\");"
        self._send_script(script)

    # 待实现的其他功能
    def close_psd_file(self):
        """关闭 PSD 文件"""
        # Photopea 脚本示例: app.activeDocument.close();
        script = "app.activeDocument.close();"
        self._send_script(script)

    # 待实现的其他功能
    def save_as_psd_file(self):
        """另存为 PSD 文件"""
        # Photopea 脚本示例: app.activeDocument.saveToOE("psd");
        script = "app.activeDocument.saveToOE(\"psd\");"
        self._send_script(script)

    # 待实现的其他功能
    def get_all_layer_names(self):
        """获取所有图层名"""
        # Photopea 脚本示例: var layerNames = []; app.activeDocument.layers.forEach(function(layer){ layerNames.push(layer.name); }); app.echoToOE(JSON.stringify(layerNames));
        script = "var layerNames = []; app.activeDocument.layers.forEach(function(layer){ layerNames.push(layer.name); }); app.echoToOE(JSON.stringify(layerNames));"
        self._send_script(script)
        # 注意: 实际应用中需要监听 Photopea 返回的 message 事件来获取图层名列表

    # 待实现的其他功能
    def get_layer_text(self, layer_name: str):
        """获取图层文字"""
        # Photopea 脚本示例: app.echoToOE(app.activeDocument.layers.getByName("LayerName").textItem.contents);
        script = f"app.echoToOE(app.activeDocument.layers.getByName(\"{layer_name}\").textItem.contents);"
        self._send_script(script)
        # 注意: 实际应用中需要监听 Photopea 返回的 message 事件来获取图层文字

    # 待实现的其他功能
    def set_text_layer_font(self, layer_name: str, font_name: str):
        """设置文字图层字体"""
        # Photopea 脚本示例: app.activeDocument.layers.getByName("LayerName").textItem.font = "FontName";
        script = f"app.activeDocument.layers.getByName(\"{layer_name}\").textItem.font = \"{font_name}\";"
        self._send_script(script)

    # 待实现的其他功能
    def get_layer_group(self, layer_name: str):
        """获取图层所属组"""
        # Photopea 脚本示例: app.echoToOE(app.activeDocument.layers.getByName("LayerName").parent.name);
        script = f"app.echoToOE(app.activeDocument.layers.getByName(\"{layer_name}\").parent.name);"
        self._send_script(script)
        # 注意: 实际应用中需要监听 Photopea 返回的 message 事件来获取图层组名

    # 待实现的其他功能
    def rename_layer(self, old_name: str, new_name: str):
        """重命名图层"""
        # Photopea 脚本示例: app.activeDocument.layers.getByName("OldName").name = "NewName";
        script = f"app.activeDocument.layers.getByName(\"{old_name}\").name = \"{new_name}\";"
        self._send_script(script)

    # 待实现的其他功能
    def content_aware_fill(self):
        """内容识别填充"""
        # Photopea 脚本示例: app.activeDocument.selection.contentAwareFill();
        script = "app.activeDocument.selection.contentAwareFill();"
        self._send_script(script)

    # 待实现的其他功能
    def modify_color_fill_layer(self, layer_name: str, color: str):
        """修改颜色填充图层"""
        # Photopea 脚本示例: var colorRef = new SolidColor(); colorRef.rgb.hexValue = "RRGGBB"; app.activeDocument.layers.getByName("LayerName").fillColor = colorRef;
        script = f"var colorRef = new SolidColor(); colorRef.rgb.hexValue = \"{color}\"; app.activeDocument.layers.getByName(\"{layer_name}\").fillColor = colorRef;"
        self._send_script(script)

    # 待实现的其他功能
    def set_shape_layer_stroke(self, layer_name: str, stroke_color: str, stroke_width: int):
        """设置形状图层描边"""
        # Photopea 脚本示例: var colorRef = new SolidColor(); colorRef.rgb.hexValue = "RRGGBB"; app.activeDocument.layers.getByName("LayerName").stroke = { enabled: true, color: colorRef, width: 10 };
        script = f"var colorRef = new SolidColor(); colorRef.rgb.hexValue = \"{stroke_color}\"; app.activeDocument.layers.getByName(\"{layer_name}\").stroke = {{ enabled: true, color: colorRef, width: {stroke_width} }};"
        self._send_script(script)

    # 待实现的其他功能
    def export_layer_as_png(self, layer_name: str):
        """导出图层为 PNG"""
        # Photopea 脚本示例: app.activeDocument.layers.getByName("LayerName").exportToOE("png");
        script = f"app.activeDocument.layers.getByName(\"{layer_name}\").exportToOE(\"png\");"
        self._send_script(script)

    # 待实现的其他功能

    # def add_image_layer(self, image_url: str):
    #     pass

    # def delete_layer(self, layer_name: str):
    #     pass

    # def get_layer_font_info(self, layer_name: str):
    #     pass

    # def activate_document(self, document_id):
    #     pass

    # def replace_frame(self, frame_id, new_content_url):
    #     pass

    # def artboard_slice(self):
    #     pass

    # def replace_layer_image_auto_scale(self, layer_name: str, image_url: str):
    #     pass

    # def set_text_layer_format(self, layer_name: str, format_options: dict):
    #     pass

if __name__ == "__main__":
    api = PhotopeaAPI()
    # 示例：打开一个远程PSD文件
    remote_psd_url = "https://customerscanvas.com/docs/cc/samples/text.psd"
    api.open_psd_file(remote_psd_url)

    # 示例：打开一个本地PSD文件
    # 请确保 'AMZ01.psd' 文件存在于 'c:\Download\01\PhotopeaAPI\' 目录下
    local_psd_path = "c:\\Download\\01\\PhotopeaAPI\\AMZ01.psd"
    api.open_psd_file(local_psd_path)