# Ticker to Thesis — Investment Research Workspace

## Właściciel
Michał — początkujący inwestor indywidualny, uczący się systematycznego podejścia do inwestowania.

## Cel workspace'a
System do zarządzania procesem inwestycyjnym: od typowania spółek (screening), przez głęboką analizę (ticker-to-thesis), po tracking portfela i monitoring pozycji.

## Profil inwestycyjny
- **Horyzont:** długoterminowy (lata)
- **Rynki:** głównie GPW, z globalną dywersyfikacją przez ETF-y
- **Broker:** XTB (konta: IKZE, IKE, zwykłe)
- **Styl:** inwestowanie w wartość z elementami growth; preferuje ETF-y na szerokie indeksy + selektywne pozycje indywidualne
- **Poziom wiedzy:** początkujący — uczy się fundamentów (P/E, DCF, analiza bilansowa); materiały edukacyjne w `learning/`

## Struktura workspace'a

```
ticker-to-thesis/
├── CLAUDE.md                      # ten plik — kontekst workspace'a
├── GPW_rekomendacje_2026.md       # screening: top picks analityków na GPW 2026
├── NEU_memo_PL.md                 # memo inwestycyjne Neuca (po polsku)
├── NEU_przewodnik_inwestora.md    # przewodnik inwestora Neuca
├── analyses/                      # głębokie analizy spółek
│   └── BDX-2026-02-08/           # Budimex — pełna analiza 6-lens
├── portfolio/                     # tracking portfela
│   ├── portfolio.md              # aktualny stan pozycji — czytelny opis (IKZE/IKE/zwykłe)
│   ├── portfolio.csv             # pozycje jako dane — do parsowania, sumowania, skryptów
│   ├── watchlist.md              # monitoring: target prices, kill conditions, katalizatory
│   └── watchlist.csv             # kandydaci + obserwowane — ustrukturyzowane dane
├── learning/                      # notatki edukacyjne
│   └── 01-fundamentals.md        # podstawy inwestowania
├── scripts/                       # narzędzia
│   ├── pdf-to-md.py              # konwersja PDF→markdown
│   └── pdf-to-png.py             # konwersja PDF→PNG
└── .claude/skills/
    └── ticker-to-thesis/          # skill do generowania memo inwestycyjnych
```

## Aktualne pozycje (stan: 2026-02-12)
- **IKZE:** ETF-y US hedgowane (Nasdaq-100, S&P 500, Semiconductor VanEck)
- **IKE:** ETF-y PL (mWIG40TR, sWIG80TR) + US Healthcare + Obligacje 6M
- **Zwykłe:** Neuca (NEU.PL) — 11 akcji @ 784,09 PLN + gotówka ~9 159 PLN
- **Łącznie:** ~62 790 PLN, z czego ~18% gotówka

## Spółki z głęboką analizą
- **Neuca (NEU)** — LONG, fair value 920-960 PLN, strefa wejścia 720-774 PLN, pozycja w portfelu
- **Budimex (BDX)** — HOLD z pozytywnym nastawieniem, jakościowy kompaunder ale wyceniony wysoko

## Workflow

1. **Screening** → `GPW_rekomendacje_2026.md` + własne screeny → kandydaci trafiają do `portfolio/watchlist.md`
2. **Analiza** → skill `ticker-to-thesis` generuje memo w `analyses/{TICKER}-{YYYY-MM-DD}/`
3. **Decyzja** → jeśli kupujesz, dodajesz pozycję do `portfolio/portfolio.md` i monitoring do `watchlist.md`
4. **Monitoring** → co 2 tygodnie przegląd `watchlist.md` — sprawdzaj kill conditions, katalizatory, ceny

## Pipeline / do zrobienia
- Kolejne analizy ticker-to-thesis: LPP, Dino, Żabka, Benefit Systems (priorytet z watchlisty)
- Screener ilościowy: skrypt do ściągania wskaźników z Biznesradar/Stooq
- Automatyczne alerty cenowe (integracja z API?)

## Konwencje
- Analizy idą do `analyses/{TICKER}-{YYYY-MM-DD}/`
- Memo inwestycyjne pisane przez skill ticker-to-thesis (6-lens multi-agent pipeline)
- Portfolio aktualizowane w `portfolio/portfolio.md`
- Notatki edukacyjne w `learning/` z numeracją (01-, 02-, ...)
- Język: polski dla notatek i memo, angielski w kodzie i nazwach plików
