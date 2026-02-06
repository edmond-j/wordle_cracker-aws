import datetime
import boto3
import os
import json

def output_resutl(answer: str):
    s3 = boto3.client("s3")
    bucket = "wordlecracker-s3"
    key = "everyday_results.json"

    obj= s3.get_object(Bucket=bucket, Key=key)
    body = obj['Body'].read()
    if not body:
            data = []
    else:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
    # 文件内容不是有效 JSON，保险起见当作空列表处理
            data = []
    if not isinstance(data, list):
    # 防万一，兜底成空列表
        data = []
    today = datetime.date.today().isoformat()
    data = [item for item in data if item.get("date") != today]
    today.strip()
    data.append({"date": today, "answer": answer})
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data,ensure_ascii=False), ContentType="application/json")

today_answer={
    "answer": "showe",
    "date": "2024-06-15",
}

complex_answer={
    "answer": "crane",
    "date": ["2024-06-14", "2024-06-15"]
}

output_resutl("today_answer")
# print(today_answer)
# print(json.dumps(today_answer))
# print(today_answer['answer'])
# print(complex_answer)
# print(json.dumps(complex_answer))
# print(complex_answer['date'][0])
# output_resutl(json.dumps(today_answer))