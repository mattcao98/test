import openai

import itchat_desktop as itchat

openai.api_key = "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"


def generate_text(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message.strip()


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg[0] == "#":
        return generate_text(msg[1:])


ccc = generate_text("你是谁")

print(ccc)

