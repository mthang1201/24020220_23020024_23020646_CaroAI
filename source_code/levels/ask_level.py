# ---------------------------------------------------------------------------
# Ask level module
# ---------------------------------------------------------------------------

def _ask_board_size() -> int:
    """Prompt for board size; default 9."""
    raw = input(f"  Board size (default 9, min 9): ").strip()
    if not raw:
        return 9
    try:
        size = int(raw)
        if size < 9:
            print("  ⚠  Board size must be at least 9. Using 9.")
            return 9
        return size
    except ValueError:
        print("  ⚠  Invalid input. Using 9.")
        return 9
    
def _ask_depth(default: int, label: str = "AI") -> int:
    """Prompt for search depth with a warning for large values."""
    raw = input(f"  Search depth for {label} (default {default}): ").strip()
    if not raw:
        return default
    try:
        depth = int(raw)
        if depth <= 0:
            print(f"  ⚠  Depth must be positive. Using {default}.")
            return default
        if depth >= 5:
            print(f"  ⚠  Depth {depth} may be very slow on a 9x9 board. Continuing…")
        return depth
    except ValueError:
        print(f"  ⚠  Invalid input. Using {default}.")
        return default


def _ask_ui() -> str:
    """Prompt for UI choice; default console."""
    print("\n  Choose User Interface (UI):")
    print("    1  Console UI (Text-based)")
    print("    2  PyGame UI (Graphical GUI)")
    choice = input("  Your choice (default 1): ").strip() or "1"
    if choice == "2":
        return "pygame"
    return "console"


# Public API
def ask_board_size() -> int:
    return _ask_board_size()

def ask_depth(default: int, label: str = "AI") -> int:
    return _ask_depth(default, label)

def ask_ui() -> str:
    return _ask_ui()
