from datetime import datetime, timezone

from src.generators.generate_batch import classify_session
from src.generators.session_generator import generate_session


class EventStore:

    def __init__(self):
        self._sessions = []

    def populate(self, num_sessions: int) -> list:
        for _ in range(num_sessions):
            self._sessions.append(
                generate_session()
            )

    def get_sessions(self) -> list:
        return self._sessions

    def get_sessions_since(self, timestamp) -> list:
        """
        Returns sessions that occured since the given timestamp
        :params timestamp: str, timestamp in ISO-format (YYYY-MM-DD HH:MM)
        :return list
        """
        sessions_since = []

        # Make sure timestamp is a datetime object
        if not isinstance(timestamp, datetime):
            timestamp = datetime.fromisoformat(timestamp)
            # print(f"Given timestamp converted to datetime object: {timestamp}")

        if timestamp.tzinfo is None:
            # Treat timezone-naive values as UTC.
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        assert isinstance(timestamp, datetime)

        for session in self._sessions:
            session_start_ts = datetime.fromisoformat(session["session_start_ts"])
            # print(f"Session start converted to datetime object: {session_start_ts}")
            if session_start_ts > timestamp:
                sessions_since.append(session)
        return sessions_since

    def count(self) -> int:
        return len(self._sessions)

    def clear(self) -> list:
        self._sessions = []

    def summary(self) -> str:
        summary = {
                "total_sessions": len(self._sessions),
                "browse_only": 0,
                "abandoned_cart": 0,
                "purchase": 0,
                "total_events": 0,
            }
        
        for session in self._sessions:
            outcome = classify_session(session)
            summary[outcome] += 1
            summary["total_events"] += len(session["events"])
        
        # Percent distributions
        browse_only = round(100 * summary['browse_only'] / summary['total_sessions'], 0)
        abandoned_carts = round(100 * summary['abandoned_cart'] / summary['total_sessions'], 0)
        purchases = round(100 * summary['purchase'] / summary['total_sessions'], 0)
        
        # Print summary report
        return f"""
        SUMMARY REPORT
        Total sessions: {summary['total_sessions']}
        Browse-only sessions ({browse_only}%): {summary['browse_only']}
        Abandoned-cart sessions ({abandoned_carts}%): {summary['abandoned_cart']}
        Purchase sessions ({purchases}%): {summary['purchase']}
        Total events: {summary['total_events']}"""


if __name__ == '__main__':
    from pprint import pprint
    store = EventStore()
    store.populate(num_sessions=100)
    pprint(store.get_sessions())
    print(f"Session counts: {store.count()}")
    store.summary_report()