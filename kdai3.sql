CREATE TABLE selection_stages (
    stage_id INTEGER PRIMARY KEY,
    stage_name TEXT NOT NULL
);
CREATE TABLE candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    university TEXT,
    faculty TEXT,
    graduation_year INTEGER,
    available_hours_per_week INTEGER
);
CREATE TABLE positions (
    position_id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_name TEXT NOT NULL,
    employment_type TEXT NOT NULL,
    description TEXT
);
CREATE TABLE recruiters (
    recruiter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT
);
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL UNIQUE
);
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,

    candidate_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL,

    application_date DATE NOT NULL,

    recruitment_year INTEGER NOT NULL,

    current_stage_id INTEGER NOT NULL,

    next_interview_date DATETIME,

    UNIQUE (candidate_id, position_id, recruitment_year),

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id),

    FOREIGN KEY (position_id)
        REFERENCES positions(position_id),

    FOREIGN KEY (current_stage_id)
        REFERENCES selection_stages(stage_id)
);
CREATE TABLE interviews (
    interview_id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_id INTEGER NOT NULL,
    stage_id INTEGER NOT NULL,
    recruiter_id INTEGER NOT NULL,

    interview_date DATETIME,

    result TEXT,

    FOREIGN KEY (application_id)
        REFERENCES applications(application_id),

    FOREIGN KEY (stage_id)
        REFERENCES selection_stages(stage_id),

    FOREIGN KEY (recruiter_id)
        REFERENCES recruiters(recruiter_id)
);
CREATE TABLE evaluations (
    evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,

    interview_id INTEGER NOT NULL UNIQUE,

    technical_score INTEGER,
    communication_score INTEGER,
    overall_score INTEGER,

    comment TEXT,

    FOREIGN KEY (interview_id)
        REFERENCES interviews(interview_id)
);
CREATE TABLE candidate_skills (
    candidate_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,

    skill_level INTEGER,

    PRIMARY KEY (candidate_id, skill_id),

    FOREIGN KEY (candidate_id)
        REFERENCES candidates(candidate_id),

    FOREIGN KEY (skill_id)
        REFERENCES skills(skill_id)
);
