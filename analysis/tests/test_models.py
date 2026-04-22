import pytest


@pytest.mark.django_db
def test_analysis_factory_creates_analysis(analysis):
    assert analysis.id is not None
    assert analysis.name
    assert analysis.price is not None


@pytest.mark.django_db
def test_analysis_str_returns_name(analysis):
    assert str(analysis) == analysis.name