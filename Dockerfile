FROM 715871776555.dkr.ecr.ap-southeast-2.amazonaws.com/lambda-python_chrome:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY . ${LAMBDA_TASK_ROOT}

# 用于消除错误：
# Message: session not created: probably user data directory is already in use, please specify a unique value for --user-data-dir argument, or don't use --user-data-
ENV HOME=/tmp
ENV XDG_CACHE_HOME=/tmp/.cache

# 确保 /tmp/.cache 存在并可写
RUN mkdir -p /tmp/.cache && chown root:root /tmp/.cache && chmod 1777 /tmp/.cache

CMD ["app.lambda_handler"]
