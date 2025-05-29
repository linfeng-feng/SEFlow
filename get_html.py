import os
import re

base_dirs = ["clip", "noise", "reverb", "packet", "complex"]
output_html = "index.html"

# 获取 f-* 目录并按 B 排序（从 f-B-D 提取 B）
def extract_B(dir_name):
    match = re.match(r"f-(\d+)-\d+", dir_name)
    return int(match.group(1)) if match else float("inf")

# 写 HTML 页面
with open(output_html, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n")
    f.write("  <meta charset=\"UTF-8\">\n")
    f.write("  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
    f.write("  <title>Speech Enhancement Demo</title>\n")
    f.write("  <style>\n")
    f.write("    body { font-family: Arial, sans-serif; margin: 40px; }\n")
    f.write("    h1 { text-align: center; }\n")
    f.write("    h2 { margin-top: 50px; }\n")
    f.write("    table { margin: 0 auto; border-collapse: collapse; }\n")
    f.write("    th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }\n")
    f.write("    img { width: 200px; }\n")
    f.write("    audio { width: 200px; }\n")
    f.write("  </style>\n")
    f.write("</head>\n<body>\n")

    # Title and abstract
    f.write("  <h1>Speech Enhancement via Multi-condition Modeling</h1>\n")
    f.write("  <p style='max-width: 800px; margin: 0 auto; text-align: justify;'>\n")
    f.write("    This page demonstrates the speech enhancement performance of our model under various types of degradations including clipping, noise, reverberation, packet loss, and complex distortions. Each section below shows the corresponding samples for comparison.\n")
    f.write("  </p>\n")

    for base_dir in base_dirs:
        f.write(f"<h2>{base_dir.capitalize()} Corruption</h2>\n")

        clean_dir = os.path.join(base_dir, "clean")
        if not os.path.exists(clean_dir):
            continue

        sample_names = sorted([
            os.path.splitext(f)[0]
            for f in os.listdir(clean_dir)
            if f.endswith(".flac")
        ])

        f_dirs = sorted(
            [d for d in os.listdir(base_dir) if re.match(r"f-\d+-\d+", d)],
            key=extract_B
        )

        version_dirs = ["noisy"] + f_dirs + ["clean"]

        f.write("  <table>\n")
        f.write("    <thead>\n      <tr>\n")
        for version in version_dirs:
            f.write(f"        <th>{version}</th>\n")
        f.write("      </tr>\n    </thead>\n    <tbody>\n")

        for name in sample_names:
            f.write("      <tr>\n")
            for version in version_dirs:
                audio_path = f"{base_dir}/{version}/{name}.flac"
                image_path = f"{base_dir}/{version}/{name}.png"

                if os.path.exists(audio_path) and os.path.exists(image_path):
                    f.write(
                        f'        <td>'
                        f'<img src="{image_path}"><br>'
                        f'<audio controls><source src="{audio_path}" type="audio/flac"></audio>'
                        f'</td>\n'
                    )
                else:
                    f.write("        <td>N/A</td>\n")
            f.write("      </tr>\n")

        f.write("    </tbody>\n  </table>\n")

    f.write("</body>\n</html>\n")
