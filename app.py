import boto3
import os
import logging

# 本地加载.env文件
# from dotenv import load_dotenv
# load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL"), force=True)
logger = logging.getLogger(__name__)


def read_words():
    s3 = boto3.client("s3")
    bucket = os.environ["dictionary_bucket"]
    key = os.environ["dictionary_file"]
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response["Body"].read().decode("utf-8")
    five_letter_words = []
    for line in file_content.splitlines():
        five_letter_words.append(line.strip())
    logger.info(f"total words: {len(five_letter_words)}")
    return five_letter_words


all_words = read_words()

pop_words = ["touch", "filer", "sandy"]
# "t","o","u","c","h","f","i","l","e","r","s","a","n","n","d","y"
must = []
absent = []
correct = []
present = []

import web_io


def is_absent_exist(word):
    exist = False
    if len(absent) == 0:
        return False
    else:
        for l in absent:
            if l in word:
                exist = True
                break
    return exist


# print("absent",is_absent_exist("girls"))


def is_wrong_in_position(word):
    exist = False
    if len(present) == 0:
        return False
    else:
        for l in present:
            if l["letter"] == word[l["pos"]]:
                exist = True
                break
    return exist


def is_correct_in_position(word):
    in_position = False
    if len(correct) == 0:
        return True
    else:
        for l in correct:
            if l["letter"] == word[l["pos"]]:
                in_position = True
            else:
                return False
    return in_position


def is_wrong_missing(word):
    if len(present) == 0:
        return False
    else:
        for l in present:
            if l["letter"] not in word:
                return True


def must_have(word):
    if len(must) == 0:
        return True
    else:
        for l in must:
            if l not in word:
                return False
    return True


def guess(words_list):
    n = 0
    candidates = []
    for word in words_list:
        if (
            not is_absent_exist(word)
            and not is_wrong_in_position(word)
            and not is_wrong_missing(word)
            and is_correct_in_position(word)
            # and must_have(word)
        ):
            candidates.append(word)
            # print(word)
            n += 1
    logger.info(f"possible answer: {n}")
    return candidates


def word_check(word, row):
    results = web_io.input(word, row)
    # results =['absent', 'absent', 'absent', 'present', 'absent']
    for j in range(0, 5):
        if results[j] == "absent":
            absent.append(word[j])
        elif results[j] == "correct":
            correct.append({"pos": j, "letter": word[j]})
        else:
            present.append({"pos": j, "letter": word[j]})


def lambda_handler(event, context):
    for i in range(0, 3):
        word_check(pop_words[i], i + 1)
    # 逻辑有问题
    candidates = guess(all_words)
    feedback: str
    for i in range(4, 7):
        if len(candidates) == 0:
            feedback = "no suitable word is found in the dictionary!"
            logger.warning(feedback)
            # 写入文件
            break
        elif len(candidates) == 1:
            feedback = f"the answer is: {candidates[0]}"
            logger.info(feedback)
            # 写入文件
            break
        else:
            logger.info(f"round {i}, candidates: {candidates}")
            word_check(candidates[0], i)
            candidates = guess(candidates)
            # 如果第五次结束后有2个选项，而第六次没提交正确的，那么屏幕上无法显示正确答案，但实际上程序知道了正确答案
            # 其实程序可以尝试无限多次，只要每次都重开浏览器

    return {"statusCode": 200, "body": feedback}


# if __name__ == "__main__":
#     lambda_handler(None, None)
