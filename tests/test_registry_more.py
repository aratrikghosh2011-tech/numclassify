"""Additional coverage for _registry.py functions not hit by other tests."""
import pytest
import numclassify as nc
from numclassify._registry import (
    _resolve,
    REGISTRY,
    find_in_range,
    find_all_in_range,
    find_any_in_range,
    most_special_in_range,
    count_properties,
    similar_numbers,
    print_properties,
)


class TestResolve:
    def test_resolve_with_string(self):
        func = _resolve("prime")
        assert callable(func)
        assert func(7) is True
        assert func(4) is False

    def test_resolve_with_callable(self):
        func = _resolve(lambda n: n > 0)
        assert callable(func)

    def test_resolve_with_bad_string_raises(self):
        with pytest.raises(KeyError):
            _resolve("nonexistent_type_xyz")

    def test_resolve_with_bad_type_raises(self):
        with pytest.raises(TypeError):
            _resolve(42)


class TestRangeFunctions:
    def test_find_in_range_with_string(self):
        result = find_in_range("prime", 1, 10)
        assert result == [2, 3, 5, 7]

    def test_find_in_range_with_callable(self):
        result = find_in_range(lambda n: n % 2 == 0, 1, 10)
        assert result == [2, 4, 6, 8, 10]

    def test_find_all_in_range(self):
        result = find_all_in_range(["prime", "fibonacci"], 1, 20)
        assert 2 in result
        assert 3 in result
        assert 5 in result
        assert 13 in result

    def test_find_any_in_range(self):
        result = find_any_in_range(["perfect", "prime"], 1, 10)
        assert 2 in result
        assert 3 in result
        assert 5 in result
        assert 6 in result  # perfect
        assert 7 in result

    def test_most_special_in_range(self):
        result = most_special_in_range(1, 100)
        assert isinstance(result, int)
        assert 1 <= result <= 100


class TestCountProperties:
    def test_count_properties(self):
        c = count_properties(6)
        assert isinstance(c, int)
        assert c > 0

    def test_count_properties_zero(self):
        c = count_properties(0)
        assert isinstance(c, int)


class TestSimilarNumbersEdgeCases:
    def test_similar_numbers_search_range_param(self):
        result = similar_numbers(6, search_range=20)
        assert isinstance(result, list)

    def test_similar_numbers_empty_for_unknown(self):
        # A number with very few properties might return empty
        result = similar_numbers(0, top_k=10)
        assert isinstance(result, list)

    def test_similar_numbers_sorted_ties(self):
        result = similar_numbers(28, top_k=3, search_range=50)
        if result:
            sims = [r['similarity'] for r in result]
            assert sims == sorted(sims, reverse=True)


class TestPrintProperties:
    def test_print_properties_runs(self, capsys):
        print_properties(6)
        captured = capsys.readouterr()
        assert '6' in captured.out
        assert 'TRUE' in captured.out or 'True' in captured.out

    def test_print_properties_empty(self, capsys):
        print_properties(0)
        captured = capsys.readouterr()
        assert '0' in captured.out
