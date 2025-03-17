from extract_stats import extract_p_values, extract_confidence_intervals, extract_sample_sizes, extract_effect_sizes

def test_p_value_extraction():
    text = "The results showed a significant effect (p = 0.03)."
    p_values = extract_p_values(text)
    assert p_values == ["p = 0.03"]

def test_confidence_interval_extraction():
    text = "The 95% confidence interval was [1.2, 2.3]."
    cis = extract_confidence_intervals(text)
    assert cis == ["95% CI [1.2, 2.3]"]

def test_sample_size_extraction():
    text = "The sample size was N = 150."
    sample_sizes = extract_sample_sizes(text)
    assert sample_sizes == ["N = 150"]

def test_effect_size_extraction():
    text = "Cohen's d = 0.5 was observed."
    effect_sizes = extract_effect_sizes(text)
    assert effect_sizes == ["Cohen's d = 0.5"]
