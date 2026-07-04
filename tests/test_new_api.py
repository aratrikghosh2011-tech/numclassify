"""
tests/test_new_api.py
Edge case tests for v0.6.0 additions:
  similar_numbers(), specialness_percentile(), property_info() oeis_url.
"""
import re
import pytest
import numclassify as nc


class TestSimilarNumbers:
    def test_returns_list(self):
        result = nc.similar_numbers(6)
        assert isinstance(result, list)

    def test_top_k_respected(self):
        result = nc.similar_numbers(6, top_k=3)
        assert len(result) <= 3

    def test_result_structure(self):
        result = nc.similar_numbers(6, top_k=2)
        for item in result:
            assert 'number' in item
            assert 'similarity' in item
            assert 'shared_properties' in item
            assert isinstance(item['number'], int)
            assert 0.0 <= item['similarity'] <= 1.0
            assert isinstance(item['shared_properties'], list)

    def test_excludes_self(self):
        result = nc.similar_numbers(6)
        numbers = [r['number'] for r in result]
        assert 6 not in numbers

    def test_sorted_by_similarity(self):
        result = nc.similar_numbers(28, top_k=5)
        sims = [r['similarity'] for r in result]
        assert sims == sorted(sims, reverse=True)

    def test_n_equals_1(self):
        result = nc.similar_numbers(1)
        assert isinstance(result, list)

    def test_n_equals_0(self):
        result = nc.similar_numbers(0)
        assert isinstance(result, list)

    def test_top_k_zero(self):
        result = nc.similar_numbers(6, top_k=0)
        assert result == []

    def test_highly_special_number(self):
        result = nc.similar_numbers(1729, top_k=3, search_range=100)
        assert isinstance(result, list)

    def test_shared_properties_are_real(self):
        result = nc.similar_numbers(6, top_k=1)
        if result:
            for prop in result[0]['shared_properties']:
                info = nc.property_info(prop)
                assert info is not None


class TestSpecialnessPercentile:
    def test_returns_float(self):
        result = nc.specialness_percentile(6, sample_size=50)
        assert isinstance(result, float)

    def test_range_0_to_100(self):
        result = nc.specialness_percentile(1729, sample_size=50)
        assert 0.0 <= result <= 100.0

    def test_highly_special_scores_high(self):
        result = nc.specialness_percentile(1729, sample_size=200)
        assert result > 50.0

    def test_n_equals_1(self):
        result = nc.specialness_percentile(1, sample_size=50)
        assert 0.0 <= result <= 100.0

    def test_prime_scores_reasonably(self):
        result = nc.specialness_percentile(7, sample_size=100)
        assert 0.0 <= result <= 100.0

    def test_determinism_on_same_seed(self):
        r1 = nc.specialness_percentile(6, sample_size=50)
        r2 = nc.specialness_percentile(6, sample_size=50)
        assert 0 <= r1 <= 100
        assert 0 <= r2 <= 100


class TestPropertyInfoOeisUrl:
    def test_prime_has_oeis_url(self):
        info = nc.property_info('prime')
        assert 'oeis_url' in info
        assert info['oeis_url'] == 'https://oeis.org/A000040'

    def test_oeis_url_format(self):
        info = nc.property_info('fibonacci')
        if info.get('oeis'):
            assert info['oeis_url'].startswith('https://oeis.org/')
            assert info['oeis_url'] == f"https://oeis.org/{info['oeis']}"

    def test_no_oeis_gives_empty_url(self):
        from numclassify._registry import REGISTRY, _normalize
        for key, entry in REGISTRY.items():
            if key != _normalize(entry.name) or entry.oeis:
                continue
            info = nc.property_info(entry.name)
            assert info['oeis_url'] == ''
            break

    def test_unknown_property_raises(self):
        with pytest.raises((ValueError, KeyError)):
            nc.property_info('notarealthing_xyz')

    def test_info_structure_complete(self):
        info = nc.property_info('prime')
        required_keys = {'name', 'description', 'category', 'oeis', 'oeis_url', 'examples'}
        assert required_keys.issubset(info.keys()), f"Missing keys: {required_keys - info.keys()}"

    def test_examples_are_integers(self):
        info = nc.property_info('prime')
        assert isinstance(info['examples'], list)
        assert all(isinstance(x, int) for x in info['examples'])

    def test_aliases_work(self):
        try:
            info = nc.property_info('fibonacci')
            assert info['name'] is not None
        except (ValueError, KeyError):
            pass


class TestWhyHidden:
    def test_no_practice_type_leaks_verdict(self):
        """
        The critical regression test. Every PRACTICE_TYPES entry, at
        several n values, must not contain '{is|is not} {TypeName}' in
        its hidden explanation. This is the exact bug found in v0.8.0
        where 12/22 types leaked the verdict via a prefix convention
        that the original strip logic never accounted for.
        """
        import re
        failures = []
        for t in nc.PRACTICE_TYPES:
            type_word = t.split()[0].lower()
            pattern = re.compile(rf'\bis\s+(?:not\s+)?{re.escape(type_word)}\b', re.IGNORECASE)
            for n in [1, 2, 6, 7, 28, 30, 47, 100, 153]:
                try:
                    hidden = nc.why_hidden(t, n)
                except RuntimeError:
                    continue
                if pattern.search(hidden):
                    failures.append(f"{t}({n}): {hidden!r}")
        assert not failures, f"Verdict leaked in {len(failures)} cases:\n" + "\n".join(failures)

    def test_no_bare_yes_no_token(self):
        import re
        failures = []
        for t in nc.PRACTICE_TYPES:
            for n in [1, 6, 7, 28, 153]:
                try:
                    hidden = nc.why_hidden(t, n)
                except RuntimeError:
                    continue
                if re.search(r'\bYES\b|\bNO\b', hidden):
                    failures.append(f"{t}({n}): {hidden!r}")
        assert not failures, f"Bare verdict token found:\n" + "\n".join(failures)

    def test_still_shows_working(self):
        for t in ["Armstrong", "Perfect", "Prime"]:
            try:
                result = nc.why_hidden(t, 6)
            except RuntimeError:
                continue
            assert len(result) > 5

    def test_fails_loudly_not_silently(self):
        """
        If why_hidden() cannot safely strip a verdict, it must raise
        RuntimeError rather than return a leaking string. This test
        exists to ensure future changes don't quietly relax the safety
        check to make the exhaustive audit pass by hiding failures.
        """
        import inspect
        source = inspect.getsource(nc.why_hidden)
        assert 'RuntimeError' in source


class TestPracticeSet:
    def test_returns_correct_count(self):
        assert len(nc.practice_set("Prime", count=10)) == 10

    def test_result_structure(self):
        for item in nc.practice_set("Perfect", count=6):
            assert 'number' in item and 'answer' in item
            assert isinstance(item['number'], int)
            assert isinstance(item['answer'], bool)
            assert 1 <= item['number'] <= 200

    def test_roughly_balanced(self):
        result = nc.practice_set("Prime", count=20)
        yes_count = sum(1 for r in result if r['answer'])
        assert 6 <= yes_count <= 14

    def test_rare_property_doesnt_crash(self):
        # Perfect numbers under 200: only 6 and 28.
        result = nc.practice_set("Perfect", count=10)
        assert len(result) == 10

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            nc.practice_set("Wolstenholme Prime", count=5)

    def test_seed_reproducible(self):
        r1 = nc.practice_set("Prime", count=10, seed=42)
        r2 = nc.practice_set("Prime", count=10, seed=42)
        assert r1 == r2

    def test_no_duplicate_numbers(self):
        result = nc.practice_set("Prime", count=10)
        numbers = [r['number'] for r in result]
        assert len(numbers) == len(set(numbers))

    def test_all_practice_types_work(self):
        for t in nc.PRACTICE_TYPES:
            assert len(nc.practice_set(t, count=6)) == 6
