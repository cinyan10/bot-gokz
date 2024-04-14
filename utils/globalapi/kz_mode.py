import requests


def globalapi_check() -> bool:
    url = "https://kztimerglobal.com/api/v2.0/modes"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


def format_kzmode(mode) -> str | None:
    """return kz_timer, kz_simple or kz_vanilla"""
    if mode in ("v", "vnl", 0, "kz_vanilla"):
        return "kz_vanilla"
    elif mode in ("s", "skz", 1, "kz_simple"):
        return "kz_simple"
    elif mode in ("k", "kzt", 2, "kz_timer"):
        return "kz_timer"
    else:
        return None


def format_kzmode_simple(mode) -> str | None:
    """return kz_timer, kz_simple or kz_vanilla"""

    if mode in ("v", "vnl", 0, "kz_vanilla"):
        return "vnl"
    elif mode in ("s", "skz", 1, "kz_simple"):
        return "skz"
    elif mode in ("k", "kzt", 2, "kz_timer"):
        return "kzt"
    else:
        return None


def format_kzmode_num(mode) -> int | None:
    """return kz_timer, kz_simple or kz_vanilla"""

    if mode in ("v", "vnl", 0, "kz_vanilla"):
        return 0
    elif mode in ("s", "skz", 1, "kz_simple"):
        return 1
    elif mode in ("k", "kzt", 2, "kz_timer"):
        return 2
    else:
        return None


if __name__ == "__main__":
    rs = format_kzmode("SKZ")
    print(rs)
