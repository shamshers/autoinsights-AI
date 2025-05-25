import datetime
from threading import Lock

class HistoryService:
    def __init__(self):
        self._store = {}  # analysis_id -> analysis result dict
        self._counter = 0
        self._lock = Lock()

    def save(self, result: dict, user: str = "guest") -> int:
        with self._lock:
            self._counter += 1
            analysis_id = self._counter
            result["timestamp"] = datetime.datetime.now().isoformat()
            result["user"] = user
            self._store[analysis_id] = result
            return analysis_id

    def get(self, analysis_id: int):
        return self._store.get(analysis_id)

    def all(self):
        return self._store.copy()

# Singleton instance
history_service = HistoryService()
