import pytest
from hypothesis import given, strategies as st

from simplified_canonical_path import simplify_path


def reference_normalize(path: str) -> str:
    components: list[str] = []

    for component in path.split("/"):
        if component in ("", "."):
            continue
        if component == "..":
            components = components[:-1]
        else:
            components += [component]

    return "/" + "/".join(components)


path_component = st.one_of(
    st.just(""),
    st.just("."),
    st.just(".."),
    st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.",
        min_size=1,
        max_size=10,
    ).filter(lambda component: component not in {".", ".."}),
)


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/", "/"),
        ("//", "/"),
        ("////", "/"),
        ("/home/", "/home"),
        ("/home//foo/", "/home/foo"),
        ("/a/./b/./c/", "/a/b/c"),
        ("/home/user/Documents/../Pictures", "/home/user/Pictures"),
        ("/../", "/"),
        ("/a/../../b", "/b"),
        ("/a/b/c/../../../d", "/d"),
        ("/.../a/../b/c/../d/./", "/.../b/d"),
        ("/....", "/...."),
        ("/a_1/../b.2//c_3", "/b.2/c_3"),
    ],
)
def test_simplify_path(path: str, expected: str) -> None:
    assert simplify_path(path) == expected


@given(st.lists(path_component, max_size=50))
def test_simplify_path_matches_reference_normalizer(components: list[str]) -> None:
    path = "/" + "/".join(components)

    assert simplify_path(path) == reference_normalize(path)


@given(st.lists(path_component, max_size=50))
def test_simplify_path_returns_canonical_path(components: list[str]) -> None:
    result = simplify_path("/" + "/".join(components))
    result_components = result.split("/")[1:]

    assert result.startswith("/")
    assert "//" not in result
    assert result == "/" or not result.endswith("/")
    assert "." not in result_components
    assert ".." not in result_components
    assert simplify_path(result) == result
