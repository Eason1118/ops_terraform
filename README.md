# ops_terraform

## 项目简介
**该项目核心目的是解决资源交付，并不建议使用TF做已有的资源变更操作**

`ops_terraform` 是一个用于渲染 Terraform 配置文件的工具，基于 Jinja2 模板和 YAML 参数文件，使得 Terraform 配置的管理更加灵活和可维护。

## 目录结构
```
ops_terraform/
├── README.md            # 项目说明文档
├── render.py            # 渲染 Jinja2 模板的 Python 脚本
├── template/            # 存放 Jinja2 模板文件
│   ├── gcp_vm.tf.j2     # GCP 虚拟机 Terraform 配置模板
│   ├── tx_db.tf.j2      # 腾讯云数据库 Terraform 配置模板
│   └── tx_vm.tf.j2      # 腾讯云虚拟机 Terraform 配置模板
└── values/              # 存放 YAML 配置文件
    ├── gcp_vm.yaml      # GCP 虚拟机参数文件
    ├── tx_db.yaml       # 腾讯云数据库参数文件
    └── tx_vm.yaml       # 腾讯云虚拟机参数文件
```

## 安装依赖
本项目依赖 Python 及 Jinja2 库，请确保你的环境已安装。

```bash
pip install jinja2 pyyaml
```

## 使用方法
1. **编辑参数文件**  
   在 `values/` 目录下，根据需要修改对应的 YAML 参数文件。

2. **执行渲染脚本**  
   运行 `render.py` 生成 Terraform 配置文件。

   ```bash
   python render.py -t template/tx_vm.tf.j2 -f <tx-vm-values-1.yaml> -f <tx-vm-values-2.yaml> -o main.tf
   ```

3. **检查生成的 Terraform 配置**  
   渲染后，生成的 `.tf` 文件可用于 Terraform 部署。

4. **应用 Terraform 配置**  
   运行 Terraform 命令进行资源管理：

   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

## 示例
例如，执行 `render.py` 可能会生成 `main.tf`，内容如下：
```hcl
resource "google_compute_instance" "instance" {
  name         = "example-instance"
  machine_type = "e2-medium"
  zone         = "us-central1-a"
}
```

## 贡献指南
如果你有优化建议或新需求，欢迎提交 PR 或 Issue！

