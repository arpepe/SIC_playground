import unittest

from app import app


class QuizAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('แบบทดสอบอาหาร street food ไทย', response.get_data(as_text=True))

    def test_answer_submission_updates_score(self):
        with self.client.session_transaction() as session:
            session.clear()
        response = self.client.post('/', data={'answer': 'ตลาดกลางคืน'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('คะแนน: 1/5', response.get_data(as_text=True))
        self.assertIn('ถูกต้อง', response.get_data(as_text=True))

    def test_low_score_shows_special_message(self):
        with self.client.session_transaction() as session:
            session['score'] = 0
            session['question_index'] = 4
        response = self.client.post('/', data={'answer': 'ไม่ถูก'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('คุณไม่ใช่แฟนพันธ์ุแท้อาหารไทย', response.get_data(as_text=True))

    def test_finished_quiz_does_not_crash_on_get(self):
        with self.client.session_transaction() as session:
            session['score'] = 5
            session['question_index'] = 5
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('จบแล้ว! คะแนนของคุณคือ 5/5', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
