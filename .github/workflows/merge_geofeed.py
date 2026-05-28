import os
import re
from datetime import datetime

DATA_DIR = "data"
PUBLIC_DIR = "public"
OUTPUT_FILE = os.path.join(PUBLIC_DIR, "geofeed.csv")

# 匹配标准 Geofeed 格式的正则
GEOFEED_REGEX = re.compile(r'^([0-9a-fA-F\.:]+/\d+)\s*,\s*([A-Z]{2})?\s*,\s*([A-Z0-9-]{2,6})?\s*,\s*([^,]*)?\s*,\s*([^,]*)?\s*$')

def validate_and_merge():
    # 结构: { "data/filename.csv": [ "line1", "line2", ... ] }
    source_mapped_data = {}
    
    if not os.path.exists(DATA_DIR):
        print(f"⚠️ 找不到 {DATA_DIR} 目录，请先创建它。")
        return

    # 1. 遍历并检查 data 目录下的所有 csv 文件
    for root, dirs, files in os.walk(DATA_DIR):
        # 排序文件名，确保每次合并的顺序一致
        for file in sorted(files):
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                # 统一使用正斜杠路径，如 data/hk-ips.csv
                relative_path = file_path.replace("\\", "/")
                print(f"🔍 正在检查文件: {relative_path}")
                
                file_lines = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        cleaned_line = line.strip()
                        # 跳过空行和已有的注释行
                        if not cleaned_line or cleaned_line.startswith('#'):
                            continue
                        
                        # 验证格式
                        if GEOFEED_REGEX.match(cleaned_line):
                            file_lines.append(cleaned_line)
                        else:
                            print(f"❌ 格式错误 [文件: {relative_path} | 行号: {line_num}]: {line.strip()}")
                            raise ValueError("Geofeed 格式不合规，构建停止！")
                
                if file_lines:
                    # 去重并排序该文件内的 IP
                    source_mapped_data[relative_path] = sorted(list(set(file_lines)))

    # 2. 确保 public 目录存在
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    
    # 3. 获取当前最新的 Commit 时间 (UTC 时间)
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    # 4. 写入带有“帽子”和“来源标签”的最终文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        # 写入你指定的固定帽子头部
        out_f.write("# BRICK Network Geofeed\n")
        out_f.write(f"# Last Commit: {current_time}\n")
        out_f.write("# Geofeed format: ip_prefix,country_code,region_code,city_name,postal_code\n\n")
        
        # 按照数据源文件逐个写入
        for source_file, ip_lines in source_mapped_data.items():
            out_f.write(f"# From: {source_file}\n")
            for line in ip_lines:
                out_f.write(line + '\n')
            out_f.write('\n') # 每个文件的数据块之间留一个空行，更美观
            
    print(f"✅ 成功合并数据，并已添加来源标记与时间戳到 {OUTPUT_FILE}")

if __name__ == "__main__":
    validate_and_merge()
