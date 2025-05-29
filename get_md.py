import os
import re

base_dir = "clip"
output_md = "demo.md"

# 所有样本名（不带扩展名）
clean_dir = os.path.join(base_dir, "clean")
sample_names = sorted([
    os.path.splitext(f)[0]
    for f in os.listdir(clean_dir)
    if f.endswith(".flac")
])

# 获取 f-* 目录并按 B 排序（从 f-B-D 提取 B）
def extract_B(dir_name):
    match = re.match(r"f-(\d+)-\d+", dir_name)
    return int(match.group(1)) if match else float("inf")

f_dirs = sorted(
    [d for d in os.listdir(base_dir) if re.match(r"f-\d+-\d+", d)],
    key=extract_B
)

# 表头顺序：noisy, f-*, clean
version_dirs = ["noisy"] + f_dirs + ["clean"]

# 写 Markdown 表格
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# Speech Enhancement Demo\n\n")
    f.write("## Speech samples from our evaluation set\n\n")

    f.write('<table style="margin: 0 auto;">\n')
    f.write("  <thead>\n    <tr>\n")
    for version in version_dirs:
        f.write(f"      <th>{version}</th>\n")
    f.write("    </tr>\n  </thead>\n  <tbody>\n")

    for name in sample_names:
        f.write("    <tr>\n")
        for version in version_dirs:
            audio_path = f"{base_dir}/{version}/{name}.flac"
            image_path = f"{base_dir}/{version}/{name}.png"

            if os.path.exists(audio_path) and os.path.exists(image_path):
                f.write(
                    f'      <td style="text-align: center;">'
                    f'<img src="{image_path}" style="width:200px;"><br>'
                    f'<audio controls style="width:200px;"><source src="{audio_path}"></audio>'
                    f'</td>\n'
                )
            else:
                f.write("      <td>N/A</td>\n")
        f.write("    </tr>\n")

    f.write("  </tbody>\n</table>\n")
