import os
import re

DATA_DIR = "data"
PUBLIC_DIR = "public"
OUTPUT_FILE = os.path.join(PUBLIC_DIR, "geofeed.csv")

# 简单的匹配正则：支持 IPv4/IPv6 CIDR，后面跟随 4 个逗号分隔的地理位置字段
# 例: 44.32.191.0/24,HK,,, 或 44.32.191.7/32,CN,CN-ZJ,Hangzhou,
GEOFEED_REGEX = re.compile(r'^([0-9a-fA-F\.:]+/\d+)\s*,\s*([A-Z]{2})?\s*,\s*([A-Z0-9-]{2,6})?\s*,\s*([^,]*)?\s*,\s*([^,]*)?\s*$')

def validate_and_merge():
    merged_lines = []
    
    if not os.path.exists(DATA_DIR):
        print(f"⚠️ 找不到 {DATA_DIR} 目录，请先创建它。")
        return

    # 遍历 data 目录下所有 csv 文件
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                print(f"🔍 正在检查文件: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        cleaned_line = line.strip()
                        # 跳过空行和注释行
                        if not cleaned_line or cleaned_line.startswith('#'):
                            continue
                        
                        # 验证格式
                        if GEOFEED_REGEX.match(cleaned_line):
                            merged_lines.append(cleaned_line)
                        else:
                            print(f"❌ 格式错误 [文件: {file} | 行号: {line_num}]: {line.strip()}")
                            raise ValueError("Geofeed 格式不合规，构建停止！")

    # 确保 public 目录存在
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    # 写入最终的合并文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        # 写入规范的头部注释（可选，符合 RFC 8805 标准）
        out_f.write("# Geofeed format: ip_prefix,country_code,region_code,city_name,postal_code\n")
        for line in sorted(list(set(merged_lines))):  # 去重并排序
            out_f.write(line + '\n')
            
    print(f"✅ 成功合并 {len(merged_lines)} 条合规记录到 {OUTPUT_FILE}")

if __name__ == "__main__":
    validate_and_merge()
