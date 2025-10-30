"""
Bezpieczne renderowanie Markdown z ochroną przed XSS
Wykorzystuje markdown + bleach do sanityzacji
"""

import markdown
import bleach
from markdown.extensions import codehilite, fenced_code, tables
import html

# Dozwolone tagi HTML po konwersji Markdown
ALLOWED_TAGS = [
    # Podstawowe formatowanie
    'p', 'br', 'hr',
    # Nagłówki
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    # Listy
    'ul', 'ol', 'li',
    # Formatowanie tekstu
    'strong', 'b', 'em', 'i', 'u', 'strike', 'del',
    # Linki i obrazy
    'a', 'img',
    # Tabele
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    # Kod
    'code', 'pre', 'blockquote',
    # Divs dla syntax highlighting
    'div', 'span'
]

# Dozwolone atrybuty dla tagów
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],
    'pre': ['class'],
    'div': ['class'],
    'span': ['class'],
    'table': ['class'],
    'th': ['align'],
    'td': ['align'],
}

# Dozwolone protokoły dla linków
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'ftp']

def sanitize_html(html_content):
    """
    Sanityzuje HTML usuwając potencjalnie niebezpieczne elementy
    """
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True  # Usuwa niedozwolone tagi zamiast escape'ować
    )

def safe_markdown_render(markdown_text):
    """
    Bezpiecznie renderuje Markdown do HTML z sanityzacją XSS
    """
    # Konfiguracja rozszerzeń Markdown
    extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists'
    ]
    
    # Konwersja Markdown -> HTML
    md = markdown.Markdown(extensions=extensions)
    html_content = md.convert(markdown_text)
    
    # Sanityzacja HTML
    safe_html = sanitize_html(html_content)
    
    return safe_html

# Przykłady testowe - bezpieczny Markdown
SAFE_MARKDOWN_EXAMPLES = """
# Nagłówek 1

## Nagłówek 2

**Pogrubiony tekst** i *kursywa*

### Lista:
- Element 1
- Element 2
- Element 3

### Numerowana lista:
1. Pierwszy
2. Drugi  
3. Trzeci

### Link:
[GitHub](https://github.com)

### Kod inline:
Użyj `print("Hello")` w Pythonie.

### Blok kodu:
```python
def hello():
    print("Hello, World!")
    return "success"
```

### Tabela:
| Nazwa | Wiek | Miasto |
|-------|------|--------|
| Anna  | 25   | Warszawa |
| Jan   | 30   | Kraków |

### Cytat:
> To jest cytat
> wieloliniowy

---

### Obraz:
![Python Logo](https://www.python.org/static/img/python-logo.png)
"""

# Przykłady NIEBEZPIECZNYCH prób XSS
MALICIOUS_EXAMPLES = [
    # JavaScript w różnych formach
    '<script>alert("XSS")</script>',
    '<img src="x" onerror="alert(\'XSS\')">',
    '<a href="javascript:alert(\'XSS\')">Click me</a>',
    '<iframe src="javascript:alert(\'XSS\')"></iframe>',
    
    # Ukryte w Markdown
    '[Click me](javascript:alert("XSS"))',
    '![Image](javascript:alert("XSS"))',
    '<img src="data:image/svg+xml;base64,PHN2ZyBvbmxvYWQ9YWxlcnQoMSk+">',
    
    # HTML injection
    '<div onclick="alert(\'XSS\')">Click me</div>',
    '<style>body{background:url("javascript:alert(\'XSS\')")}</style>',
    '<link rel="stylesheet" href="javascript:alert(\'XSS\')">',
    
    # Event handlers
    '<p onmouseover="alert(\'XSS\')">Hover me</p>',
    '<input onfocus="alert(\'XSS\')" autofocus>',
]

def test_xss_protection():
    """
    Testuje ochronę przed różnymi typami ataków XSS
    """
    print("=== TEST OCHRONY XSS ===\n")
    
    for i, malicious_code in enumerate(MALICIOUS_EXAMPLES, 1):
        print(f"Test {i}: {malicious_code[:50]}...")
        
        # Renderuj niebezpieczny kod
        rendered = safe_markdown_render(malicious_code)
        
        # Sprawdź czy zawiera javascript/script/on*
        is_safe = not any(dangerous in rendered.lower() for dangerous in 
                         ['javascript:', '<script', 'onerror=', 'onclick=', 'onload=', 'onmouseover='])
        
        print(f"Wynik: {rendered}")
        print(f"Bezpieczny: {'✅ TAK' if is_safe else '❌ NIE'}")
        print("-" * 50)

def demo_safe_rendering():
    """
    Demonstracja bezpiecznego renderowania
    """
    print("=== DEMO BEZPIECZNEGO RENDEROWANIA ===\n")
    
    rendered_html = safe_markdown_render(SAFE_MARKDOWN_EXAMPLES)
    
    print("Wejście (Markdown):")
    print(SAFE_MARKDOWN_EXAMPLES[:200] + "...")
    print("\n" + "="*50)
    print("Wyjście (HTML):")
    print(rendered_html[:500] + "...")
    
    # Zapisz do pliku HTML do podglądu
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bezpieczny Markdown</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        code {{ background: #f4f4f4; padding: 2px 4px; }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; }}
    </style>
</head>
<body>
    <h1>Demo bezpiecznego renderowania Markdown</h1>
    {rendered_html}
    
    <hr>
    <p><em>Ten HTML został wygenerowany z Markdown i przeszedł sanityzację XSS.</em></p>
</body>
</html>
"""
    
    with open('safe_markdown_demo.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"\n✅ Zapisano demo do: safe_markdown_demo.html")

def custom_sanitizer_example():
    """
    Przykład niestandardowej sanityzacji dla specjalnych przypadków
    """
    print("\n=== NIESTANDARDOWA SANITYZACJA ===\n")
    
    # Bardziej restrykcyjna konfiguracja (np. dla komentarzy)
    COMMENT_ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'code', 'blockquote']
    COMMENT_ALLOWED_ATTRIBUTES = {}
    
    def sanitize_comment(markdown_text):
        md = markdown.Markdown(extensions=['markdown.extensions.nl2br'])
        html_content = md.convert(markdown_text)
        
        return bleach.clean(
            html_content,
            tags=COMMENT_ALLOWED_TAGS,
            attributes=COMMENT_ALLOWED_ATTRIBUTES,
            protocols=[],
            strip=True
        )
    
    comment_markdown = """
# To zostanie usunięte
**To zostanie** ale *to też*
[Link zostanie usunięty](http://example.com)
`kod zostanie`
"""
    
    result = sanitize_comment(comment_markdown)
    print("Markdown dla komentarza:")
    print(comment_markdown)
    print("\nPo restrykcyjnej sanityzacji:")
    print(result)

if __name__ == "__main__":
    # Sprawdź czy wymagane pakiety są zainstalowane
    try:
        import markdown
        import bleach
    except ImportError as e:
        print(f"❌ Brak wymaganego pakietu: {e}")
        print("Zainstaluj: pip install markdown bleach")
        exit(1)
    
    print("🔒 BEZPIECZNE RENDEROWANIE MARKDOWN Z OCHRONĄ XSS")
    print("=" * 60)
    
    # Uruchom testy
    demo_safe_rendering()
    test_xss_protection()
    custom_sanitizer_example()
    
    print("\n✅ Wszystkie testy zakończone!")
    print("📄 Sprawdź plik 'safe_markdown_demo.html' w przeglądarce")
