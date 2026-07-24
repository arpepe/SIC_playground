from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = 'sic-playground-secret'

QUESTIONS = [
    {
        'question': 'ข้าวเหนียวหมูปิ้งเป็นอาหาร street food ที่มักขายที่ไหน?',
        'choices': [
            {'label': '🌙 ตลาดกลางคืน', 'value': 'ตลาดกลางคืน'},
            {'label': '🏨 โรงแรมหรู', 'value': 'โรงแรมหรู'},
            {'label': '🍣 ร้านอาหารญี่ปุ่น', 'value': 'ร้านอาหารญี่ปุ่น'},
            {'label': '🛍️ ห้างสรรพสินค้า', 'value': 'ห้างสรรพสินค้า'},
        ],
        'answer': 'ตลาดกลางคืน',
    },
    {
        'question': 'อาหารไทยที่มีลักษณะเป็นเส้นและทอดกรอบคืออะไร?',
        'choices': [
            {'label': '🍜 ผัดไทย', 'value': 'ผัดไทย'},
            {'label': '🥢 ก๋วยเตี๋ยว', 'value': 'ก๋วยเตี๋ยว'},
            {'label': '🥩 หมูกรอบ', 'value': 'หมูกรอบ'},
            {'label': '🥭 ข้าวเหนียวมะม่วง', 'value': 'ข้าวเหนียวมะม่วง'},
        ],
        'answer': 'ผัดไทย',
    },
    {
        'question': 'สินค้าขายริมทางที่นิยมกินเล่นๆ ในไทยมักเรียกว่าอะไร?',
        'choices': [
            {'label': '🍜 street food', 'value': 'street food'},
            {'label': '🍰 dessert buffet', 'value': 'dessert buffet'},
            {'label': '🍣 sushi set', 'value': 'sushi set'},
            {'label': '🥗 salad bar', 'value': 'salad bar'},
        ],
        'answer': 'street food',
    },
    {
        'question': 'อาหารที่นิยมกินคู่กับน้ำพริกและผักสดคืออะไร?',
        'choices': [
            {'label': '🍜 บะหมี่เกี๊ยว', 'value': 'บะหมี่เกี๊ยว'},
            {'label': '🍚 ข้าวเหนียว', 'value': 'ข้าวเหนียว'},
            {'label': '🍗 ไก่ทอด', 'value': 'ไก่ทอด'},
            {'label': '🍣 ซูชิ', 'value': 'ซูชิ'},
        ],
        'answer': 'ข้าวเหนียว',
    },
    {
        'question': 'อาหารไทยที่นิยมรับประทานตอนเย็นริมทางและมักมีรสเผ็ดคืออะไร?',
        'choices': [
            {'label': '🍤 ต้มยำกุ้ง', 'value': 'ต้มยำกุ้ง'},
            {'label': '🍜 บะหมี่กรอบ', 'value': 'บะหมี่กรอบ'},
            {'label': '🥟 ปอเปี๊ยะทอด', 'value': 'ปอเปี๊ยะทอด'},
            {'label': '🍢 ลูกชิ้น', 'value': 'ลูกชิ้น'},
        ],
        'answer': 'ปอเปี๊ยะทอด',
    },
]

HTML = """
<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>แบบทดสอบอาหาร street food ไทย</title>
  <style>
    :root { color-scheme: light; }
    body {
      font-family: 'Segoe UI', Tahoma, sans-serif;
      margin: 0;
      background: linear-gradient(135deg, #fff7d6, #ffd6e7);
      color: #2f2a2a;
    }
    .app {
      max-width: 760px;
      margin: 0 auto;
      padding: 24px 16px 48px;
    }
    .card {
      background: #ffffff;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 12px 32px rgba(0,0,0,0.12);
    }
    h1 { font-size: 1.7rem; margin-top: 0; color: #c44b8c; }
    p { line-height: 1.6; }
    .score { font-weight: 700; color: #2563eb; margin-bottom: 16px; }
    .question { font-size: 1.15rem; font-weight: 700; margin: 12px 0; }
    .choices { display: grid; gap: 10px; margin: 16px 0; }
    button {
      border: 0;
      border-radius: 12px;
      padding: 12px 14px;
      font-size: 1rem;
      cursor: pointer;
      background: #f4f4f4;
      text-align: left;
    }
    button:hover { background: #e9f7ff; }
    .feedback { padding: 12px; border-radius: 12px; margin-top: 12px; }
    .correct { background: #e8f8ee; color: #166534; }
    .wrong { background: #fdecec; color: #b91c1c; }
    .result { margin-top: 16px; font-weight: 700; }
    .retry {
      margin-top: 16px;
      background: #ff8f3f;
      color: white;
      font-weight: 700;
      text-align: center;
    }
    @media (max-width: 600px) {
      .app { padding: 12px 10px 24px; }
      h1 { font-size: 1.4rem; }
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="card">
      <h1>แบบทดสอบอาหาร street food ไทย</h1>
      <p>ทดสอบความรู้เรื่องอาหาร street food ของไทยแบบสั้น ๆ เพื่อเตรียมสอบ</p>
      <div class="score">คะแนน: {{ score }}/{{ total }}</div>
      {% if finished %}
        <div class="result">จบแล้ว! คะแนนของคุณคือ {{ score }}/{{ total }}</div>
        <form method="post" action="/">
          <button class="retry" type="submit" name="retry" value="1">ลองทำใหม่</button>
        </form>
      {% else %}
        <div class="question">{{ current_question.question }}</div>
        <form method="post" action="/">
          <div class="choices">
            {% for choice in current_question.choices %}
              <button type="submit" name="answer" value="{{ choice.value }}">{{ choice.label }}</button>
            {% endfor %}
          </div>
        </form>
        {% if feedback %}
          <div class="feedback {% if feedback.correct %}correct{% else %}wrong{% endif %}">
            {{ feedback.message }}
          </div>
        {% endif %}
      {% endif %}
    </div>
  </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form.get('retry') == '1':
        session.clear()
        return render_template_string(
            HTML,
            score=0,
            total=len(QUESTIONS),
            finished=False,
            current_question=QUESTIONS[0],
            feedback=None,
        )

    score = session.get('score', 0)
    question_index = session.get('question_index', 0)

    if request.method == 'GET':
        return render_template_string(
            HTML,
            score=score,
            total=len(QUESTIONS),
            finished=False,
            current_question=QUESTIONS[question_index],
            feedback=None,
        )

    answer = request.form.get('answer')
    current_question = QUESTIONS[question_index]
    if answer == current_question['answer']:
        score += 1
        session['score'] = score
        feedback = {'correct': True, 'message': 'ถูกต้อง! คำตอบคือ ' + current_question['answer']}
    else:
        feedback = {'correct': False, 'message': 'ไม่ถูกต้องครับ คำตอบที่ถูกคือ ' + current_question['answer']}

    next_index = question_index + 1
    if next_index >= len(QUESTIONS):
        session['question_index'] = next_index
        return render_template_string(
            HTML,
            score=score,
            total=len(QUESTIONS),
            finished=True,
            current_question=None,
            feedback=None,
        )

    session['question_index'] = next_index
    return render_template_string(
        HTML,
        score=score,
        total=len(QUESTIONS),
        finished=False,
        current_question=QUESTIONS[next_index],
        feedback=feedback,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
