from aiotsearch.tokenizers import tokenize_naive, tokenize_pymorphy


def test_tokenize_naive():
    assert tokenize_naive("Съешь еще этих мягких французских булок да выпей чаю") == {
        'съешь', 'еще', 'этих', 'мягких', 'французских', 'булок', 'да', 'выпей', 'чаю'
    }


def test_tokenize_pymorphy():
    assert tokenize_pymorphy("Съешь еще этих мягких французских булок да выпей чаю") == {
        'съесть', 'ещё', 'этот', 'мягкий', 'французский', 'булка', 'да', 'выпить', 'чай'
    }
