-- =====================================
-- SelectionStage
-- =====================================

INSERT INTO selection_stages VALUES (0, '書類選考');
INSERT INTO selection_stages VALUES (1, '一次面接');
INSERT INTO selection_stages VALUES (2, '二次面接');
INSERT INTO selection_stages VALUES (3, '三次面接');
INSERT INTO selection_stages VALUES (4, '内定');
INSERT INTO selection_stages VALUES (5, '不採用');
INSERT INTO selection_stages VALUES (6, '辞退');

-- =====================================
-- Position
-- =====================================

INSERT INTO positions
(position_name, employment_type, description)
VALUES
('AIコンサルタント', 'インターン', '生成AIを活用した業務改善提案');

INSERT INTO positions
(position_name, employment_type, description)
VALUES
('ソフトウェアエンジニア', '新卒', 'Webアプリケーション開発');

INSERT INTO positions
(position_name, employment_type, description)
VALUES
('営業職', '中途', '法人営業');

INSERT INTO positions
(position_name, employment_type, description)
VALUES
('データサイエンティスト', '新卒', 'データ分析および機械学習');

-- =====================================
-- Recruiter
-- =====================================

INSERT INTO recruiters(name, department)
VALUES ('中村太郎', '経営企画');

INSERT INTO recruiters(name, department)
VALUES ('佐藤花子', '開発部');

INSERT INTO recruiters(name, department)
VALUES ('高橋健', '営業部');

-- =====================================
-- Skills
-- =====================================

INSERT INTO skills(skill_name) VALUES ('Python');
INSERT INTO skills(skill_name) VALUES ('Java');
INSERT INTO skills(skill_name) VALUES ('SQL');
INSERT INTO skills(skill_name) VALUES ('Salesforce');
INSERT INTO skills(skill_name) VALUES ('生成AI');
INSERT INTO skills(skill_name) VALUES ('機械学習');

-- =====================================
-- Candidates
-- =====================================

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('山田太郎','yamada@example.com','09011112222',
 '慶應義塾大学','理工学部',2027,20);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('鈴木花子','suzuki@example.com','09022223333',
 '東京大学','工学部',2027,NULL);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('佐々木健','sasaki@example.com','09033334444',
 '早稲田大学','創造理工学部',2026,NULL);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('高橋美咲','takahashi@example.com','09044445555',
 '東京工業大学','情報理工学院',2027,NULL);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('伊藤翔','ito@example.com','09055556666',
 '筑波大学','情報学群',2026,NULL);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('加藤彩','kato@example.com','09066667777',
 '大阪大学','基礎工学部',2027,10);

INSERT INTO candidates
(name,email,phone,university,faculty,graduation_year,available_hours_per_week)
VALUES
('田中翔','tanaka@example.com','09077778888',
 '東京理科大学','創域理工学部',2027,NULL);
-- =====================================
-- Candidate Skills
-- =====================================

INSERT INTO candidate_skills VALUES (1,1,4);
INSERT INTO candidate_skills VALUES (1,3,3);
INSERT INTO candidate_skills VALUES (1,5,5);

INSERT INTO candidate_skills VALUES (2,1,5);
INSERT INTO candidate_skills VALUES (2,6,4);

INSERT INTO candidate_skills VALUES (3,2,4);
INSERT INTO candidate_skills VALUES (3,3,5);

INSERT INTO candidate_skills VALUES (4,1,4);
INSERT INTO candidate_skills VALUES (4,2,3);
INSERT INTO candidate_skills VALUES (4,5,4);

INSERT INTO candidate_skills VALUES (5,3,5);
INSERT INTO candidate_skills VALUES (5,4,4);

INSERT INTO candidate_skills VALUES (6,1,2);
INSERT INTO candidate_skills VALUES (6,5,3);

INSERT INTO candidate_skills VALUES (7,1,4);
INSERT INTO candidate_skills VALUES (7,2,4);
INSERT INTO candidate_skills VALUES (7,3,3);
-- =====================================
-- Applications
-- =====================================

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(1,1,'2026-06-01',2026,1,'2026-07-01');

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(2,4,'2026-06-03',2026,2,'2026-07-05');

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(3,3,'2026-05-15',2026,4,NULL);

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(4,2,'2026-06-08',2026,0,'2026-06-28');

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(5,2,'2026-05-20',2026,5,NULL);

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(6,1,'2026-06-10',2026,6,NULL);

INSERT INTO applications
(candidate_id, position_id, application_date, recruitment_year,
 current_stage_id, next_interview_date)
VALUES
(7,2,'2026-06-15',2026,0,'2026-07-03');
-- =====================================
-- Interviews
-- =====================================

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(1, 1, 1, '2026-06-20 10:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(2, 1, 2, '2026-06-18 14:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(2, 2, 2, '2026-06-25 15:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(3, 1, 3, '2026-05-20 13:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(3, 2, 3, '2026-05-27 13:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(3, 3, 1, '2026-06-03 16:00:00', '通過');

INSERT INTO interviews
(application_id, stage_id, recruiter_id, interview_date, result)
VALUES
(5, 1, 2, '2026-05-28 11:00:00', '不合格');
-- =====================================
-- Evaluations
-- =====================================

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(1, 3, 5, 4,
 '生成AIへの関心が高く、コミュニケーション能力も良好であった。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(2, 5, 4, 4,
 '機械学習に関する知識が豊富であり、論理的な説明ができていた。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(3, 4, 4, 4,
 '技術力は十分であり、研究内容について深い理解が見られた。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(4, 3, 5, 4,
 '営業経験が豊富であり、対人コミュニケーション能力が高い。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(5, 3, 5, 4,
 '業界知識があり、顧客対応能力も高い。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(6, 4, 5, 5,
 'マネジメント経験もあり、即戦力として期待できる。');

INSERT INTO evaluations
(interview_id,
 technical_score,
 communication_score,
 overall_score,
 comment)
VALUES
(7, 2, 3, 2,
 '技術的な基礎知識が不足しており、今回の募集要件との適合性が低かった。');
