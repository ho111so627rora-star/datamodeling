import sqlite3

from flask import Flask, abort, flash, g, redirect, render_template, request, url_for


app = Flask(__name__)
app.config.update(SECRET_KEY="development-key-change-on-server", DATABASE="recruitment.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_one(sql, values=()):
    row = get_db().execute(sql, values).fetchone()
    if row is None:
        abort(404)
    return row


def form_options():
    db = get_db()
    return {
        "positions": db.execute("SELECT * FROM positions ORDER BY position_name").fetchall(),
        "stages": db.execute("SELECT * FROM selection_stages ORDER BY stage_id").fetchall(),
        "recruiters": db.execute("SELECT * FROM recruiters ORDER BY name").fetchall(),
    }


def required(values, labels):
    errors = []
    for key, label in labels.items():
        if not str(values.get(key, "")).strip():
            errors.append(f"{label}は必須です。")
    return errors


@app.route("/")
def dashboard():
    db = get_db()
    summary = db.execute(
        """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN current_stage_id BETWEEN 0 AND 3 THEN 1 ELSE 0 END) AS active,
               SUM(CASE WHEN current_stage_id = 4 THEN 1 ELSE 0 END) AS offers,
               SUM(CASE WHEN current_stage_id = 5 THEN 1 ELSE 0 END) AS rejected
        FROM applications
        """
    ).fetchone()
    candidate_count = db.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    stage_counts = db.execute(
        """
        SELECT s.stage_name, COUNT(a.application_id) AS count
        FROM selection_stages s
        LEFT JOIN applications a ON a.current_stage_id = s.stage_id
        GROUP BY s.stage_id, s.stage_name
        ORDER BY s.stage_id
        """
    ).fetchall()
    upcoming = db.execute(
        """
        SELECT a.application_id, c.name, p.position_name, a.next_interview_date
        FROM applications a
        JOIN candidates c ON c.candidate_id = a.candidate_id
        JOIN positions p ON p.position_id = a.position_id
        WHERE a.next_interview_date IS NOT NULL
        ORDER BY a.next_interview_date
        LIMIT 8
        """
    ).fetchall()
    return render_template("dashboard.html", summary=summary,
                           candidate_count=candidate_count,
                           stage_counts=stage_counts, upcoming=upcoming)


@app.route("/candidates")
def candidates():
    keyword = request.args.get("keyword", "").strip()
    stage_id = request.args.get("stage_id", "").strip()
    recruitment_year = request.args.get("recruitment_year", "").strip()
    sql = """
        SELECT a.application_id, c.candidate_id, c.name, c.university,
               p.position_name, a.recruitment_year, s.stage_name,
               a.next_interview_date
        FROM applications a
        JOIN candidates c ON c.candidate_id = a.candidate_id
        JOIN positions p ON p.position_id = a.position_id
        JOIN selection_stages s ON s.stage_id = a.current_stage_id
        WHERE 1 = 1
    """
    params = []
    if keyword:
        sql += " AND (c.name LIKE ? OR c.university LIKE ? OR p.position_name LIKE ?)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    if stage_id:
        sql += " AND a.current_stage_id = ?"
        params.append(stage_id)
    if recruitment_year:
        sql += " AND a.recruitment_year = ?"
        params.append(recruitment_year)
    sql += " ORDER BY a.recruitment_year DESC, c.name"
    rows = get_db().execute(sql, params).fetchall()
    stages = get_db().execute("SELECT * FROM selection_stages ORDER BY stage_id").fetchall()
    return render_template("candidates.html", rows=rows, stages=stages,
                           keyword=keyword, stage_id=stage_id,
                           recruitment_year=recruitment_year)


@app.route("/candidates/<int:candidate_id>")
def candidate_detail(candidate_id):
    db = get_db()
    candidate = query_one("SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,))
    skills = db.execute(
        """SELECT s.skill_name, cs.skill_level FROM candidate_skills cs
           JOIN skills s ON s.skill_id = cs.skill_id
           WHERE cs.candidate_id = ? ORDER BY s.skill_name""", (candidate_id,)
    ).fetchall()
    applications = db.execute(
        """SELECT a.*, p.position_name, s.stage_name FROM applications a
           JOIN positions p ON p.position_id = a.position_id
           JOIN selection_stages s ON s.stage_id = a.current_stage_id
           WHERE a.candidate_id = ? ORDER BY a.recruitment_year DESC, a.application_date DESC""",
        (candidate_id,)
    ).fetchall()
    interviews = db.execute(
        """SELECT i.*, a.recruitment_year, s.stage_name, r.name AS recruiter_name,
                  e.technical_score, e.communication_score, e.overall_score, e.comment
           FROM interviews i
           JOIN applications a ON a.application_id = i.application_id
           JOIN selection_stages s ON s.stage_id = i.stage_id
           JOIN recruiters r ON r.recruiter_id = i.recruiter_id
           LEFT JOIN evaluations e ON e.interview_id = i.interview_id
           WHERE a.candidate_id = ? ORDER BY i.interview_date DESC""", (candidate_id,)
    ).fetchall()
    return render_template("candidate_detail.html", candidate=candidate,
                           skills=skills, applications=applications, interviews=interviews)


@app.route("/candidates/new", methods=("GET", "POST"))
def candidate_new():
    if request.method == "POST":
        errors = required(request.form, {"name": "氏名", "email": "メールアドレス"})
        graduation_year = request.form.get("graduation_year", "").strip()
        hours = request.form.get("available_hours_per_week", "").strip()
        try:
            graduation_year = int(graduation_year) if graduation_year else None
            hours = int(hours) if hours else None
            if hours is not None and not 0 <= hours <= 168:
                errors.append("稼働可能時間は0～168で入力してください。")
        except ValueError:
            errors.append("卒業年度と稼働可能時間は整数で入力してください。")
        if not errors:
            try:
                cursor = get_db().execute(
                    """INSERT INTO candidates
                       (name, email, phone, university, faculty, graduation_year, available_hours_per_week)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (request.form["name"].strip(), request.form["email"].strip(),
                     request.form.get("phone", "").strip() or None,
                     request.form.get("university", "").strip() or None,
                     request.form.get("faculty", "").strip() or None,
                     graduation_year, hours)
                )
                get_db().commit()
                flash("候補者を登録しました。", "success")
                return redirect(url_for("candidate_detail", candidate_id=cursor.lastrowid))
            except sqlite3.IntegrityError:
                get_db().rollback()
                errors.append("このメールアドレスは既に登録されています。")
        for error in errors:
            flash(error, "error")
    return render_template("candidate_form.html")


@app.route("/candidates/<int:candidate_id>/edit", methods=("GET", "POST"))
def candidate_edit(candidate_id):
    candidate = query_one("SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,))
    if request.method == "POST":
        errors = required(request.form, {"name": "氏名", "email": "メールアドレス"})
        try:
            graduation_year = int(request.form["graduation_year"]) if request.form.get("graduation_year") else None
            hours = int(request.form["available_hours_per_week"]) if request.form.get("available_hours_per_week") else None
        except ValueError:
            graduation_year, hours = None, None
            errors.append("卒業年度と稼働可能時間は整数で入力してください。")
        if not errors:
            try:
                get_db().execute(
                    """UPDATE candidates SET name=?, email=?, phone=?, university=?, faculty=?,
                       graduation_year=?, available_hours_per_week=? WHERE candidate_id=?""",
                    (request.form["name"].strip(), request.form["email"].strip(),
                     request.form.get("phone") or None, request.form.get("university") or None,
                     request.form.get("faculty") or None, graduation_year, hours, candidate_id)
                )
                get_db().commit()
                flash("候補者情報を更新しました。", "success")
                return redirect(url_for("candidate_detail", candidate_id=candidate_id))
            except sqlite3.IntegrityError:
                get_db().rollback()
                errors.append("このメールアドレスは既に登録されています。")
        for error in errors:
            flash(error, "error")
    return render_template("candidate_form.html", candidate=candidate)


@app.route("/candidates/<int:candidate_id>/applications/new", methods=("GET", "POST"))
def application_new(candidate_id):
    candidate = query_one("SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,))
    options = form_options()
    if request.method == "POST":
        errors = required(request.form, {"position_id": "職種", "application_date": "応募日",
                                         "recruitment_year": "採用年度", "current_stage_id": "選考ステージ"})
        try:
            year = int(request.form.get("recruitment_year", ""))
            if not 2000 <= year <= 2100:
                errors.append("採用年度は2000～2100で入力してください。")
        except ValueError:
            year = None
            errors.append("採用年度は整数で入力してください。")
        if not errors:
            try:
                get_db().execute(
                    """INSERT INTO applications
                       (candidate_id, position_id, application_date, recruitment_year,
                        current_stage_id, next_interview_date) VALUES (?, ?, ?, ?, ?, ?)""",
                    (candidate_id, request.form["position_id"], request.form["application_date"], year,
                     request.form["current_stage_id"], request.form.get("next_interview_date") or None)
                )
                get_db().commit()
                flash("応募を登録しました。", "success")
                return redirect(url_for("candidate_detail", candidate_id=candidate_id))
            except sqlite3.IntegrityError:
                get_db().rollback()
                errors.append("同じ候補者・職種・採用年度の応募が既に存在します。")
        for error in errors:
            flash(error, "error")
    return render_template("application_form.html", candidate=candidate, options=options,
                           today=get_db().execute("SELECT date('now')").fetchone()[0])


@app.route("/applications/<int:application_id>/edit", methods=("GET", "POST"))
def application_edit(application_id):
    application = query_one("SELECT * FROM applications WHERE application_id = ?", (application_id,))
    candidate = query_one("SELECT * FROM candidates WHERE candidate_id = ?", (application["candidate_id"],))
    options = form_options()
    if request.method == "POST":
        errors = required(request.form, {"position_id": "職種", "application_date": "応募日",
                                         "recruitment_year": "採用年度", "current_stage_id": "選考ステージ"})
        try:
            year = int(request.form.get("recruitment_year", ""))
        except ValueError:
            year = None
            errors.append("採用年度は整数で入力してください。")
        if not errors:
            try:
                get_db().execute(
                    """UPDATE applications SET position_id=?, application_date=?, recruitment_year=?,
                       current_stage_id=?, next_interview_date=? WHERE application_id=?""",
                    (request.form["position_id"], request.form["application_date"], year,
                     request.form["current_stage_id"], request.form.get("next_interview_date") or None,
                     application_id)
                )
                get_db().commit()
                flash("応募情報を更新しました。", "success")
                return redirect(url_for("candidate_detail", candidate_id=application["candidate_id"]))
            except sqlite3.IntegrityError:
                get_db().rollback()
                errors.append("同じ候補者・職種・採用年度の応募が既に存在します。")
        for error in errors:
            flash(error, "error")
    return render_template("application_form.html", candidate=candidate,
                           application=application, options=options)


@app.post("/applications/<int:application_id>/delete")
def application_delete(application_id):
    application = query_one("SELECT * FROM applications WHERE application_id = ?", (application_id,))
    db = get_db()
    try:
        db.execute("BEGIN")
        db.execute("DELETE FROM evaluations WHERE interview_id IN (SELECT interview_id FROM interviews WHERE application_id = ?)", (application_id,))
        db.execute("DELETE FROM interviews WHERE application_id = ?", (application_id,))
        db.execute("DELETE FROM applications WHERE application_id = ?", (application_id,))
        db.commit()
        flash("応募と関連する面接・評価を削除しました。", "success")
    except sqlite3.Error:
        db.rollback()
        flash("削除に失敗しました。", "error")
    return redirect(url_for("candidate_detail", candidate_id=application["candidate_id"]))


@app.route("/applications/<int:application_id>/interviews/new", methods=("GET", "POST"))
def interview_new(application_id):
    application = query_one(
        """SELECT a.*, c.name, c.candidate_id, p.position_name FROM applications a
           JOIN candidates c ON c.candidate_id=a.candidate_id
           JOIN positions p ON p.position_id=a.position_id WHERE a.application_id=?""", (application_id,)
    )
    options = form_options()
    if request.method == "POST":
        errors = required(request.form, {"stage_id": "面接ステージ", "recruiter_id": "担当者",
                                         "interview_date": "面接日時", "result": "結果"})
        scores = {}
        for key, label in (("technical_score", "技術点"), ("communication_score", "対話点"),
                           ("overall_score", "総合点")):
            try:
                scores[key] = int(request.form.get(key, ""))
                if not 1 <= scores[key] <= 5:
                    errors.append(f"{label}は1～5で入力してください。")
            except ValueError:
                errors.append(f"{label}は1～5の整数で入力してください。")
        if not errors:
            db = get_db()
            try:
                db.execute("BEGIN")
                cursor = db.execute(
                    """INSERT INTO interviews (application_id, stage_id, recruiter_id, interview_date, result)
                       VALUES (?, ?, ?, ?, ?)""",
                    (application_id, request.form["stage_id"], request.form["recruiter_id"],
                     request.form["interview_date"], request.form["result"].strip())
                )
                db.execute(
                    """INSERT INTO evaluations
                       (interview_id, technical_score, communication_score, overall_score, comment)
                       VALUES (?, ?, ?, ?, ?)""",
                    (cursor.lastrowid, scores["technical_score"], scores["communication_score"],
                     scores["overall_score"], request.form.get("comment", "").strip() or None)
                )
                db.commit()
                flash("面接と評価を登録しました。", "success")
                return redirect(url_for("candidate_detail", candidate_id=application["candidate_id"]))
            except sqlite3.Error:
                db.rollback()
                errors.append("面接と評価の登録に失敗しました。")
        for error in errors:
            flash(error, "error")
    return render_template("interview_form.html", application=application, options=options)


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", message="指定されたデータが見つかりません。"), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", message="サーバー内部でエラーが発生しました。"), 500


if __name__ == "__main__":
    app.run(debug=True)
