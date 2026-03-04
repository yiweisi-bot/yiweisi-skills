-- ============================================
-- 自主学习系统 - 数据库架构
-- ============================================

-- 学习目标表
CREATE TABLE IF NOT EXISTS learning_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL DEFAULT 2,
    status TEXT NOT NULL DEFAULT 'pending',
    source TEXT,
    estimated_hours REAL,
    actual_hours REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    parent_id INTEGER,
    metadata TEXT,
    FOREIGN KEY (parent_id) REFERENCES learning_goals(id)
);

-- 学习任务表
CREATE TABLE IF NOT EXISTS learning_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 2,
    estimated_minutes INTEGER,
    actual_minutes INTEGER,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    result_summary TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE CASCADE
);

-- 学习会话表
CREATE TABLE IF NOT EXISTS learning_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_minutes INTEGER,
    tokens_used INTEGER DEFAULT 0,
    tokens_budget INTEGER,
    time_budget_minutes INTEGER,
    checkpoints TEXT,
    summary TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE CASCADE
);

-- 生成的技能表
CREATE TABLE IF NOT EXISTS generated_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    task_id INTEGER,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    parent_skill_id INTEGER,
    is_latest BOOLEAN DEFAULT 1,
    quality_score INTEGER,
    validation_status TEXT NOT NULL DEFAULT 'pending',
    tokens_used INTEGER DEFAULT 0,
    file_size_bytes INTEGER,
    word_count INTEGER,
    code_block_count INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP,
    validated_by TEXT,
    feedback TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE SET NULL,
    FOREIGN KEY (task_id) REFERENCES learning_tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (parent_skill_id) REFERENCES generated_skills(id) ON DELETE SET NULL
);

-- 待学习列表
CREATE TABLE IF NOT EXISTS learning_backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    source_goal_id INTEGER,
    source_session_id INTEGER,
    priority INTEGER NOT NULL DEFAULT 2,
    reason TEXT NOT NULL,
    saved_progress TEXT,
    tokens_already_used INTEGER DEFAULT 0,
    time_already_spent_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_attempted_at TIMESTAMP,
    attempt_count INTEGER DEFAULT 0,
    metadata TEXT,
    FOREIGN KEY (source_goal_id) REFERENCES learning_goals(id) ON DELETE SET NULL,
    FOREIGN KEY (source_session_id) REFERENCES learning_sessions(id) ON DELETE SET NULL
);

-- ============================================
-- 索引设计
-- ============================================

-- 学习目标索引
CREATE INDEX IF NOT EXISTS idx_goals_status ON learning_goals(status);
CREATE INDEX IF NOT EXISTS idx_goals_priority ON learning_goals(priority DESC);
CREATE INDEX IF NOT EXISTS idx_goals_created ON learning_goals(created_at DESC);

-- 学习任务索引
CREATE INDEX IF NOT EXISTS idx_tasks_goal_id ON learning_tasks(goal_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON learning_tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_created ON learning_tasks(created_at DESC);

-- 学习会话索引
CREATE INDEX IF NOT EXISTS idx_sessions_goal_id ON learning_sessions(goal_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON learning_sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON learning_sessions(started_at DESC);

-- 生成技能索引
CREATE INDEX IF NOT EXISTS idx_skills_goal_id ON generated_skills(goal_id);
CREATE INDEX IF NOT EXISTS idx_skills_validation ON generated_skills(validation_status);
CREATE INDEX IF NOT EXISTS idx_skills_created ON generated_skills(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_skills_latest ON generated_skills(is_latest) WHERE is_latest = 1;

-- 待学习列表索引
CREATE INDEX IF NOT EXISTS idx_backlog_priority ON learning_backlog(priority DESC);
CREATE INDEX IF NOT EXISTS idx_backlog_created ON learning_backlog(created_at DESC);
