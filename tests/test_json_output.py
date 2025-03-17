import json
from extract_stats import save_to_json

def test_json_output():
    data = {
        "p_values": ["p = 0.05"],
        "confidence_intervals": ["95% CI [1.2, 2.3]"],
        "sample_sizes": ["N = 100"],
        "effect_sizes": ["Cohen's d = 0.5"]
    }
    json_path = "tests/output.json"
    save_to_json(data, json_path)
    with open(json_path, "r") as f:
        loaded_data = json.load(f)
    assert loaded_data == data
