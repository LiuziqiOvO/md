import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


def convert_svg_to_pdf(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有 SVG 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".svg"):
            input_svg = os.path.join(input_folder, filename)
            output_pdf = os.path.join(output_folder, os.path.splitext(filename)[0] + '.pdf')

            # 转换 SVG 为 PDF
            try:
                drawing = svg2rlg(input_svg)
                renderPDF.drawToFile(drawing, output_pdf)
                print(f"Successfully converted {input_svg} to {output_pdf}")
            except Exception as e:
                print(f"Error converting {input_svg}: {e}")


# 使用示例
input_folder = './SVG'
output_folder = './fig'
convert_svg_to_pdf(input_folder, output_folder)
