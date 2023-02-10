#!/usr/bin/env python3
# -*- coding =utf-8 -*-
# @Time：2023/2/7  10:38
# @Author ：Matt Cao
# @File：wxbot.py
# @Software：PyCharm
"""
gpt3.5 vs gpt3 : 复杂推理的能力、上下文学习能力、零样本能力
gpt3.5系列包括code-davinci-002，text-davinci-002，text-davinci-003，chatgpt；当前openai官方开放了除chatgpt以外模型的api接口。
注：官方目前未开放chatgpt的api接口，azure预计3月会接入chatgpt api；待官方后续发布chatgpt的api后，我们会尽快接入。
gpt3.5擅长的：生成类、改写类、理解类、总结归纳类，回复话术接近人类水平
gpt3.5不擅长的：2021年之后的知识（未加入训练）、判别信息真伪、事实类内容可能出错（因为回复内容接近人类水平，可以出现”一本正经的胡说八道“的令人混淆的情况）
gpt3.5系列模型对比：
code-davinci-002：代码理解、代码生成、代码补齐
text-davinci-003：上下文能力、零样本能力、翔实的内容
chatgpt：对话能力，建模对话历史的能力，增加对话信息量，拒绝模型知识范围之外的问题，更翔实的能力
回复翔实性、与人类对话的对齐能力：chatgpt>text-davinci-003>text-davinci-002
下游具体任务上的能力：code-davinci-002 > chatgpt & text-davinci-003

"""
import hashlib
import itchat_desktop as itchat


import requests
import time

hostqa = "https://gpt-api-test.hz.netease.com"
hostpro = "https://gpt-api.hz.netease.com"
api = "/api/v2/text/completion"

t = int(time.time())


def signkey():
    signvalue = "appId=2onljqammii7072snce270h3pn5fvc&nonce=1986&timestamp=" + str(
        t) + "&appkey=2l1c6tli4vhv2g9qaqsdled3bfc3gb1hce1o55ba3o51r"
    sign = hashlib.md5(signvalue.encode("utf-8")).hexdigest().upper()
    return sign


def aitext(prompt):
    sign = signkey()
    headers = {"nonce": "1986", "version": "v2", "appId": "2onljqammii7072snce270h3pn5fvc", "timestamp": str(t),
               "Content-Type": "application/json",
               "sign": sign}
    api = "/api/v2/text/completion"
    body = {
        "prompt": prompt,  # 用户补全的内容的提示,即想要做的内容
        "model": "text-davinci-003",  # text-davinci-003, code-davinci-002
        "maxTokens": 2048,  # 补全过程中最大数字最大不超过4096，一般支持
        "temperature": 0.7,  # 更高的值意味着模型将承担更多的风险。对于更有创意的应用程序，可以尝试0.9，对于有明确答案的应用程序
        "topP": 1,  # [0,1]的范围，决定了文本的创造性和多样性，值越小创造性越高，和temperature撘配使用
        "stop": None,  # 非必填,出现关键词终止
        "presencePenalty": 0,  # [-2.0,2.0] 正值减少后续相同输出的概率
        "frequencyPenalty": 0  # [-2.0,2.0] 正值减少后续相同输出的概率
    }

    url = hostqa + api
    response = requests.post(url=url, json=body, headers=headers)
    res = response.json()
    text = res.get("detail").get("choices")[0].get("text")
    text1 = text.replace("\n", "")
    return text1


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg.text.startswith("#"):
        return aitext(msg.text[1:])


if __name__ == "__main__":
    res =aitext("最近有哪几只股票会涨")
    print(res)


