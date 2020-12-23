import pytest

from autofmu.utils import slugify


@pytest.mark.parametrize(
    "given,expected,unicode",
    (
        ("Hello, World!", "hello-world", False),
        ("spam & eggs", "spam-eggs", False),
        (" multiple---dash and  space ", "multiple-dash-and-space", False),
        ("\t whitespace-in-value \n", "whitespace-in-value", False),
        ("underscore_in-value", "underscore_in-value", False),
        ("__strip__underscore-value___", "strip__underscore-value", False),
        ("--strip-dash-value---", "strip-dash-value", False),
        ("__strip-mixed-value---", "strip-mixed-value", False),
        ("_ -strip-mixed-value _-", "strip-mixed-value", False),
        ("spam & ıçüş", "spam-ıçüş", True),
        ("foo ıç bar", "foo-ıç-bar", True),
        ("    foo ıç bar", "foo-ıç-bar", True),
        ("你好", "你好", True),
        ("İstanbul", "istanbul", True),
    ),
)
def test_slugify(given: str, expected: str, unicode: bool):
    assert slugify(given, allow_unicode=unicode) == expected
