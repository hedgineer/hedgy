import hedgy

def test_classifier_is_list():
    
    results = hedgy.classifier.generate_classifier_prompts("classifier_prompts.json")
    assert type(results) == list

def test_classifier_has_correct_roles():
    
    results = hedgy.classifier.generate_classifier_prompts("classifier_prompts.json")
    roles = {i['role'] for i in results}

    for i in roles:
        assert i in ('system', 'user', 'assistant') 