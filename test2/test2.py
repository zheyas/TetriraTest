import pytest
from unittest.mock import patch, Mock
from collections import Counter

from solution import get_animals_by_letter, write_csv, write_russian_csv, RUSSIAN_LETTERS

# Для примера - подставной HTML-запрос с "животными"
HTML_PAGE_1 = '''
<div id="mw-pages">
    <ul>
        <li>Акула</li>
        <li>Бобр</li>
        <li>Барсук</li>
    </ul>
    <a href="/wiki/Категория:Животные_по_алфавиту?pagefrom=Б" title="Следующая страница">Следующая страница</a>
</div>
'''

HTML_PAGE_2 = '''
<div id="mw-pages">
    <ul>
        <li>Бурундук</li>
        <li>Верблюд</li>
    </ul>
</div>
'''

def mock_requests_get(url, *args, **kwargs):
    m = Mock()
    if "pagefrom=Б" in url:
        m.content = HTML_PAGE_2.encode('utf-8')
    else:
        m.content = HTML_PAGE_1.encode('utf-8')
    return m

@patch('solution.requests.get', side_effect=mock_requests_get)
def test_get_animals_by_letter(mock_get):
    result = get_animals_by_letter()
    # Проверяем, что посчитал буквы правильно
    expected = Counter({'А':1, 'Б':3, 'В':1})
    assert result == expected

def test_write_csv(tmp_path):
    counts = Counter({'А':2, 'Б':1})
    filename = tmp_path/"test.csv"
    write_csv(counts, filename)
    content = filename.read_text(encoding='utf-8')
    assert "А,2" in content and "Б,1" in content

def test_write_russian_csv(tmp_path):
    counts = Counter({'Ш': 3, 'Ё': 4, 'А': 2, 'Я': 5})
    filename = tmp_path/"rus.csv"
    write_russian_csv(counts, filename)
    content = filename.read_text(encoding='utf-8')
    for let in ('Ш','Ё','А','Я'):
        assert let in content
