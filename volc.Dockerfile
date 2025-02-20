FROM hashicorp/terraform:1.10.5 AS builder

FROM debian:stable-slim AS runtime
# 设置时区
ENV TZ=Asia/Shanghai

COPY --from=builder /bin/terraform /bin/terraform

# 创建 Terraform 工作目录
WORKDIR /data/tmp

# 安装基础工具和 Python 依赖
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


RUN curl -O -L https://github.com/volcengine/terraform-provider-volcengine/archive/refs/tags/v0.0.159.zip
RUN curl -O -L https://github.com/volcengine/terraform-provider-volcengine/releases/download/v0.0.159/terraform-provider-volcengine_0.0.159_linux_amd64.zip

RUN unzip v0.0.159.zip
RUN bash ./terraform-provider-volcengine-0.0.159/manual_install_tf.sh --version 0.0.159 --provider ./terraform-provider-volcengine_0.0.159_linux_amd64.zip

# 设置工作目录
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN python3 -m venv ./venv

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]