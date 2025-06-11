import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter

BASE_URL = "https://ru.wikipedia.org"
START_URL = BASE_URL + "/wiki/Категория:Животные_по_алфавиту"
RUSSIAN_LETTERS = [chr(i) for i in range(ord('А'), ord('Я')+1)] + ['Ё']

def get_animals_by_letter():
    current_url = START_URL
    letter_counts = Counter()

    while True:
        resp = requests.get(current_url)
        soup = BeautifulSoup(resp.content, "html.parser")
        content_div = soup.find('div', {'id': 'mw-pages'})
        if not content_div:
            break
        ul_tags = content_div.find_all('ul')
        for ul in ul_tags:
            for li in ul.find_all('li'):
                beast = li.get_text().strip()
                if beast:
                    first_letter = beast[0].upper()
                    letter_counts[first_letter] += 1
        next_link = content_div.find('a', string="Следующая страница")
        if next_link:
            current_url = BASE_URL + next_link['href']
        else:
            break
    return letter_counts

def write_csv(counts, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter, count in sorted(counts.items()):
            writer.writerow([letter, count])

def write_russian_csv(counts, filename='russian_beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in RUSSIAN_LETTERS:
            if letter in counts:
                writer.writerow([letter, counts[letter]])

if __name__ == "__main__":
    counts = get_animals_by_letter()
    write_csv(counts)
    write_russian_csv(counts)
    print("Готово! Созданы beasts.csv и russian_beasts.csv")
