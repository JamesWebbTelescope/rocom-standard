import os

_DEFAULT_RELATIVE = "illegal.json"

def _resolve_registry_path() -> str:
    """Resolve registry path — works both locally and inside Docker."""
    candidates = [
        # Environment variable (for container deployments)
        os.path.join(os.environ.get('ROCOM_SPECS_DIR', '')),
        # Inside Docker container (specs volume → standards submodule)
        "/app/illegal.json",
        # Local dev from repo root
        _DEFAULT_RELATIVE,
        os.path.join(os.path.expanduser("~"), "Rocom", "illegal.json"),
    ]
    # Walk up from this module to find specs/
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(10):
        candidate = os.path.join(current, _DEFAULT_RELATIVE)
        candidates.append(candidate)
        current = os.path.dirname(current)

    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        f"Cannot find {_DEFAULT_RELATIVE}. Searched: {candidates}"
    )

if __name__ == "__main__":
   path = _resolve_registry_path()
   print("Found path: " + f"{path}")