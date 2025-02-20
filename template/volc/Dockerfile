FROM hashicorp/terraform:1.10.5

# 设置时区
ENV TZ=Asia/Shanghai

# 创建 Terraform 工作目录
WORKDIR /data/tmp

# 安装基础工具和 Python 依赖
RUN apk add --no-cache \
    python3-dev \
    py3-pip \
    build-base \
    wget \
    curl \
    git \
    unzip \
    libffi-dev \
    openssl-dev \
    && rm -rf /var/cache/apk/*

RUN curl -O -L https://github.com/volcengine/terraform-provider-volcengine/archive/refs/tags/v0.0.159.zip
RUN curl -O -L https://github.com/volcengine/terraform-provider-volcengine/releases/download/v0.0.159/terraform-provider-volcengine_0.0.159_linux_amd64.zip

RUN unzip v0.0.159.zip
RUN sh ./terraform-provider-volcengine-0.0.159/manual_install_tf.sh --version 0.0.159 --provider ./terraform-provider-volcengine_0.0.159_linux_amd64.zip

# 设置工作目录
WORKDIR /workspace
COPY ./requirements.txt ./requirements.txt
RUN python3 -m venv ./venv

ENV VIRTUAL_ENV_PROMPT=(venv)
ENV VIRTUAL_ENV=/workspace/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/bin/sh"]