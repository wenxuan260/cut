import base64

def image_to_base64(image_path, output_file):
    # 打开图像文件并读取其二进制数据
    with open(image_path, 'rb') as image_file:
        # 读取文件内容并进行base64编码
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 将编码后的base64字符串写入输出文件
    with open(output_file, 'w') as output:
        output.write(encoded_string)
    print(f"Base64 编码已保存到 {output_file}")

# 传入原图文件路径和输出文件路径
image_path = 'Test.png'  # 你的图片文件路径
output_file = 'Test.txt'  # 保存base64的文件路径

image_to_base64(image_path, output_file)
