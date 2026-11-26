import re

_TURKISH_MAP = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "Ç": "c",
        "Ğ": "g",
        "İ": "i",
        "Ö": "o",
        "Ş": "s",
        "Ü": "u",
    }
)


def slugify(text: str) -> str:
    """Turn a (Turkish) title into a URL-safe ASCII slug.

    Turkish characters are mapped before lowercasing: "İ".lower() yields "i"
    plus a combining dot, which would otherwise become a stray dash.
    """
    text = text.strip().translate(_TURKISH_MAP).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "makale"
