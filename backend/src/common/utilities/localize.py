import json
import os

_cache: dict[str, dict] = {}


def localize(key: str, language: str = "en", **kwargs: str) -> str:
    if language not in _cache:
        path = os.path.join(os.path.dirname(__file__), f"../../assets/locales/{language}.json")
        try:
            with open(path) as f:
                _cache[language] = json.load(f)
        except FileNotFoundError:
            _cache[language] = _cache.get("en", {})
    value = _cache.get(language, {}).get(key, key)
    return value.format(**kwargs) if kwargs else value
