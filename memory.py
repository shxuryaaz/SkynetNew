from collections import defaultdict

_sessions = defaultdict(list)

def get_history(session_id):
    return _sessions[session_id]

def add_message(session_id, role, content):
    _sessions[session_id].append({"role": role, "content": content})

def reset_session(session_id):
    _sessions[session_id] = [] 