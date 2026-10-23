"""Thin in-process driver for Studium's MCP dispatcher (no stdio)."""
import json, sys
from pathlib import Path
from studium.mcp.server import dispatch, open_workspace

WS = Path.home()/'Developer/work/ws'

def session(book):
    root = WS/book
    return open_workspace(str(root), str(root/book))

_cache = {}
def call(book, name, **args):
    s = _cache.get(book) or session(book)
    _cache[book] = s
    out = dispatch(name, args, session=s)
    return out

def show(out, limit=4000):
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:limit])

if __name__ == '__main__':
    book, name = sys.argv[1], sys.argv[2]
    args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    show(call(book, name, **args), int(sys.argv[4]) if len(sys.argv) > 4 else 6000)
