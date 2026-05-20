from app.languages import normalize_language, parse_query, resolve_target


def test_parse_query_no_prefix():
    assert parse_query("hello world") == (None, "hello world")


def test_parse_query_code_prefix():
    assert parse_query("fr: bonjour le monde") == ("French", "bonjour le monde")


def test_parse_query_name_prefix():
    assert parse_query("Spanish: good morning") == ("Spanish", "good morning")


def test_parse_query_unknown_prefix_is_not_a_prefix():
    # An ordinary colon must not be mistaken for a language override.
    assert parse_query("Note: buy milk") == (None, "Note: buy milk")


def test_parse_query_colon_in_body_preserved():
    target, body = parse_query("de: Zeit: 10:30 Uhr")
    assert target == "German"
    assert body == "Zeit: 10:30 Uhr"


def test_parse_query_prefix_only_no_body():
    assert parse_query("fr:") == (None, "fr:")


def test_parse_query_strips_surrounding_whitespace():
    assert parse_query("  ru :  привет  ") == ("Russian", "привет")


def test_parse_query_multiline_body():
    target, body = parse_query("ja: line one\nline two")
    assert target == "Japanese"
    assert body == "line one\nline two"


def test_normalize_language():
    assert normalize_language("FR") == "French"
    assert normalize_language("german") == "German"
    assert normalize_language("klingon") is None


def test_resolve_target_canonicalizes_known():
    assert resolve_target("es") == "Spanish"
    assert resolve_target("Russian") == "Russian"


def test_resolve_target_accepts_unknown_language():
    assert resolve_target("swahili") == "Swahili"
    assert resolve_target("brazilian portuguese") == "Brazilian Portuguese"


def test_resolve_target_rejects_garbage():
    assert resolve_target("123!!!") is None
    assert resolve_target("") is None
