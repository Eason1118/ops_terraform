import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

def load_yaml(files):
    """ 读取多个 YAML 配置文件，并进行合并（后面的配置覆盖前面的）。 """
    merged_config = {}
    for file in files:
        with open(file, "r") as f:
            config = yaml.safe_load(f) or {}
            merged_config.update(config)  # 后加载的配置覆盖前面相同的 key
    return merged_config

def apply_overrides(config, overrides):
    """ 解析 --set 传入的 key=value，并更新 config """
    for override in overrides:
        keys, value = override.split("=", 1)
        keys = keys.split(".")  # 允许嵌套键，如 cvm.instance.name
        sub_config = config
        for key in keys[:-1]:
            sub_config = sub_config.setdefault(key, {})  # 确保中间字典存在
        sub_config[keys[-1]] = yaml.safe_load(value)  # 尝试解析为正确的类型（数字、布尔等）

def render_template(config, template_file, output_file):
    """ 渲染 Jinja2 模板并生成 Terraform 配置文件 """
    env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    rendered_tf = template.render(config)

    with open(output_file, "w") as file:
        file.write(rendered_tf)

    print(f"Terraform 配置文件 {output_file} 已生成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用 Jinja2 渲染 Terraform 模板")
    parser.add_argument("-f", "--files", nargs="+", required=True, help="指定一个或多个 YAML 配置文件")
    parser.add_argument("-t", "--template", default="template.tf.j2", help="Jinja2 模板文件 (默认: template.tf.j2)")
    parser.add_argument("-o", "--output", default="main.tf", help="输出 Terraform 文件 (默认: main.tf)")
    parser.add_argument("--set", nargs="*", default=[], help="动态设置 YAML 配置中的值 (格式: key=value)")

    args = parser.parse_args()
    
    # 读取并合并 YAML 配置文件
    config = load_yaml(args.files)
    
    # 应用 --set 传入的参数
    apply_overrides(config, args.set)
    
    # 渲染 Terraform 模板
    render_template(config, args.template, args.output)
