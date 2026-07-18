import os
import shutil
import sqlite3
import tempfile
import unittest
from contextlib import closing

from app import app


class RecruitmentAppTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.database = os.path.join(self.temp_dir, "test.db")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), "recruitment.db"), self.database)
        app.config.update(TESTING=True, DATABASE=self.database, SECRET_KEY="test")
        self.client = app.test_client()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def csrf_token(self):
        self.client.get("/")
        with self.client.session_transaction() as session:
            return session["csrf_token"]

    def test_pages_and_crud_flow(self):
        for path in ("/", "/candidates", "/candidates/1", "/candidates/new",
                     "/candidates/1/applications/new", "/applications/1/edit",
                     "/applications/1/interviews/new"):
            self.assertEqual(self.client.get(path).status_code, 200, path)

        response = self.client.post("/candidates/new", data={
            "csrf_token": self.csrf_token(),
            "name": "テスト候補者", "email": "test@example.com", "phone": "",
            "university": "テスト大学", "faculty": "情報学部",
            "graduation_year": "2028", "available_hours_per_week": "20",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("テスト候補者".encode(), response.data)

        with closing(sqlite3.connect(self.database)) as db:
            candidate_id = db.execute(
                "SELECT candidate_id FROM candidates WHERE email='test@example.com'"
            ).fetchone()[0]

        response = self.client.post(f"/candidates/{candidate_id}/applications/new", data={
            "csrf_token": self.csrf_token(),
            "position_id": "1", "application_date": "2027-06-01",
            "recruitment_year": "2027", "current_stage_id": "0",
            "next_interview_date": "2027-06-20T10:00",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("2027".encode(), response.data)

        with closing(sqlite3.connect(self.database)) as db:
            application_id = db.execute(
                "SELECT application_id FROM applications WHERE candidate_id=?", (candidate_id,)
            ).fetchone()[0]

        response = self.client.post(f"/applications/{application_id}/interviews/new", data={
            "csrf_token": self.csrf_token(),
            "stage_id": "1", "recruiter_id": "1",
            "interview_date": "2027-06-20T10:00", "result": "通過",
            "technical_score": "4", "communication_score": "5",
            "overall_score": "4", "comment": "テスト評価",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("テスト評価".encode(), response.data)

        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute(
                "SELECT current_stage_id FROM applications WHERE application_id=?", (application_id,)
            ).fetchone()[0], 2)

        response = self.client.post(
            f"/applications/{application_id}/delete",
            data={"csrf_token": self.csrf_token()}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertEqual(db.execute(
                "SELECT COUNT(*) FROM applications WHERE application_id=?", (application_id,)
            ).fetchone()[0], 0)

    def test_validation_security_and_not_found(self):
        response = self.client.post("/candidates/new", data={
            "csrf_token": self.csrf_token(), "name": "", "email": ""
        })
        self.assertIn("氏名は必須です".encode(), response.data)
        response = self.client.post("/candidates/new", data={
            "csrf_token": self.csrf_token(), "name": "不正メール", "email": "invalid"
        })
        self.assertIn("メールアドレスの形式が正しくありません".encode(), response.data)
        self.assertEqual(self.client.post("/candidates/new", data={}).status_code, 400)
        self.assertEqual(self.client.get("/candidates/99999").status_code, 404)

        response = self.client.get("/applications/3/interviews/new", follow_redirects=True)
        self.assertIn("選考が終了している応募には面接を登録できません".encode(), response.data)

        response = self.client.post("/applications/1/edit", data={
            "csrf_token": self.csrf_token(), "position_id": "1",
            "application_date": "2026-06-01", "recruitment_year": "2026",
            "current_stage_id": "4", "next_interview_date": "2026-08-01T10:00",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with closing(sqlite3.connect(self.database)) as db:
            self.assertIsNone(db.execute(
                "SELECT next_interview_date FROM applications WHERE application_id=1"
            ).fetchone()[0])


if __name__ == "__main__":
    unittest.main()
