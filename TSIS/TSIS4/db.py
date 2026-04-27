"""PostgreSQL persistence layer using psycopg2.

Tables:
    players(id SERIAL PK, username VARCHAR(50) UNIQUE NOT NULL)
    game_sessions(id SERIAL PK, player_id FK -> players(id),
                  score INT, level_reached INT,
                  played_at TIMESTAMP DEFAULT NOW())

Connection settings come from environment variables, falling back to
typical local-dev defaults. Override with:
    PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
or a single DATABASE_URL.
"""
import os

try:
    import psycopg2
    import psycopg2.extras
except ImportError:  # pragma: no cover
    psycopg2 = None


class Database:
    def __init__(self):
        self.conn = None
        self.error = None
        self._connect()
        if self.conn:
            self._ensure_schema()

    # ---------- connection ----------

    def _connect(self):
        if psycopg2 is None:
            self.error = "psycopg2 not installed (pip install psycopg2-binary)"
            return
        try:
            url = os.getenv("DATABASE_URL")
            if url:
                self.conn = psycopg2.connect(url)
            else:
                self.conn = psycopg2.connect(
                    host=os.getenv("PGHOST", "localhost"),
                    port=int(os.getenv("PGPORT", "5432")),
                    user=os.getenv("PGUSER", "postgres"),
                    password=os.getenv("PGPASSWORD", "dinok120!"),
                    dbname=os.getenv("PGDATABASE", "snake_game"),
                )
            self.conn.autocommit = True
        except Exception as e:  # noqa: BLE001
            self.error = f"DB connect failed: {e}"
            self.conn = None

    def _ensure_schema(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id       SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id            SERIAL PRIMARY KEY,
                        player_id     INTEGER REFERENCES players(id) ON DELETE CASCADE,
                        score         INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at     TIMESTAMP DEFAULT NOW()
                    );
                """)
        except Exception as e:  # noqa: BLE001
            self.error = f"DB schema init failed: {e}"

    @property
    def available(self):
        return self.conn is not None

    # ---------- API ----------

    def get_or_create_player(self, username):
        if not self.available:
            return None
        username = (username or "").strip()[:50]
        if not username:
            return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM players WHERE username = %s",
                            (username,))
                row = cur.fetchone()
                if row:
                    return row[0]
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) RETURNING id",
                    (username,),
                )
                return cur.fetchone()[0]
        except Exception as e:  # noqa: BLE001
            self.error = f"get_or_create_player failed: {e}"
            return None

    def save_session(self, username, score, level_reached):
        if not self.available:
            return False
        pid = self.get_or_create_player(username)
        if pid is None:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO game_sessions (player_id, score, level_reached)
                       VALUES (%s, %s, %s)""",
                    (pid, int(score), int(level_reached)),
                )
            return True
        except Exception as e:  # noqa: BLE001
            self.error = f"save_session failed: {e}"
            return False

    def personal_best(self, username):
        if not self.available:
            return 0
        pid = self.get_or_create_player(username)
        if pid is None:
            return 0
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """SELECT COALESCE(MAX(score), 0)
                       FROM game_sessions WHERE player_id = %s""",
                    (pid,),
                )
                return int(cur.fetchone()[0])
        except Exception as e:  # noqa: BLE001
            self.error = f"personal_best failed: {e}"
            return 0

    def top_scores(self, limit=10):
        if not self.available:
            return []
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """SELECT p.username, gs.score, gs.level_reached, gs.played_at
                       FROM game_sessions gs
                       JOIN players p ON p.id = gs.player_id
                       ORDER BY gs.score DESC, gs.played_at ASC
                       LIMIT %s""",
                    (limit,),
                )
                rows = cur.fetchall()
                return [
                    {
                        "username":      r[0],
                        "score":         int(r[1]),
                        "level_reached": int(r[2]),
                        "played_at":     r[3],
                    }
                    for r in rows
                ]
        except Exception as e:  # noqa: BLE001
            self.error = f"top_scores failed: {e}"
            return []

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except Exception:  # noqa: BLE001
                pass
            self.conn = None
