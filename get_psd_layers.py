from psd_tools import PSDImage
import sys

def get_layer_types(psd_file_path, output_file_path):
    try:
        psd = PSDImage.open(psd_file_path)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(f"PSD文件: {psd_file_path}\n")
            for layer in psd.descendants():
                # 根据图层类型添加前缀，与Photopea保持一致
                prefix = ''
                if layer.kind == 'smartobject':
                    prefix = '[智能] '
                elif layer.kind == 'group':
                    prefix = '[分组] '
                elif layer.kind == 'type':
                    prefix = '[文字] '
                elif layer.kind == 'pixel':
                    prefix = '[图像] '
                elif layer.kind == 'shape':
                    prefix = '[形状] '
                
                f.write(f"{prefix}{layer.name}\n")
        print(f"图层信息已写入到 {output_file_path}")
    except Exception as e:
        print(f"处理PSD文件时发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python get_psd_layers.py <psd_file_path> <output_file_path>")
        sys.exit(1)
    
    psd_file = sys.argv[1]
    output_file = sys.argv[2]
    get_layer_types(psd_file, output_file)