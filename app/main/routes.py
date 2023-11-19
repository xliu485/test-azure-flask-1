from app.main import bp
from flask import render_template, request
from flask_login import login_required, current_user
from openai import OpenAI
import os

# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# 为了使程序跑起来，这里把这句注释掉，这样它就不尝试用从系统里找这个环境变量了。
# 实际使用时需要你自己在OpenAI搞一个key，加载系统变量里。当然你也可以在这里
# 直接填上，即硬编码，但显然不推荐

@bp.route('/')
@login_required
def index():
    global messages
    messages=[
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital app that gives a short general solution."},
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital app that recommends a suitable online hospital department webpage in my app to the customer."},
        {"role": "system", "content": "You are an intelligent assistant for a pet online hospital which its departments are general, dental, orthopedic and surgery."}
    ]
    return render_template('index.html', name=current_user.name)

@bp.route("/get", methods=["POST"])
@login_required
def chat():
    msg = request.form["msg"]
    return get_Chat_response(msg)

def get_Chat_response(text):
    if text:
        messages.append({"role": "user", "content": text})
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.5
        )

        reply = completion.choices[0].message.content
        messages.extend([{"role": "assistant", "content": text}, {"role": "assistant", "content": reply}])
        # print(messages)
        return reply

@bp.route('/about')
@login_required
def about():
    return render_template('About.html')
