"""Remove dead FASHION STORE controls from templates/base.html.
Run from the project root: python fix_fashion_store.py
A .bak backup is created before the first change.
"""
from pathlib import Path
import re

path = Path('templates/base.html')
if not path.is_file():
    raise SystemExit('Не знайдено templates/base.html. Запустіть скрипт у папці з manage.py.')
original = path.read_text(encoding='utf-8')
s = original
patterns = [
    r'\s*<button\s+class="icon-button"\s+type="button"\s+aria-label="Пошук">.*?</button>',
    r'\s*<a\s+class="icon-button"\s+href="#"\s+aria-label="Обране">.*?</a>',
    r'\s*<a\s+class="icon-button cart-button"\s+href="#"\s+aria-label="Кошик">.*?</a>',
    r'\s*<a\s+href="#">Аксесуари</a>',
]
for pattern in patterns:
    s = re.sub(pattern, '', s, count=1, flags=re.S)
# Replace only the dead informational/footer links; do not touch functional navigation.
s = s.replace('<a href="#">Новинки</a>', '<p>Одяг, взуття та аксесуари</p>')
s = s.replace('<a href="#">Одяг</a>', '')
s = s.replace('<a href="#">Взуття</a>', '')
s = s.replace('<a href="#">Аксесуари</a>', '')
s = s.replace('<a href="#">Про магазин</a>', '<p>Навчальний демонстраційний проєкт</p>')
s = s.replace('<a href="#">Доставка та оплата</a>', '')
s = s.replace('<a href="#">Повернення</a>', '')
s = s.replace('<a href="#">Контакти</a>', '')
if s == original:
    raise SystemExit('Змін немає: перевірте, чи не було ці елементи видалено раніше.')
backup = path.with_suffix('.html.bak')
if not backup.exists():
    backup.write_text(original, encoding='utf-8')
path.write_text(s, encoding='utf-8')
print('Готово: неактивні елементи приховано. Резервна копія:', backup)
print('Перевірте сайт у браузері та виконайте python manage.py test.')
