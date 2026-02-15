# Shoper (SHO) — Unit Economics

> Data: 2026-02-13
> Status: w trakcie budowy
> Metodologia: 5-krokowa analiza unit economics SaaS

---

## Baza danych — co wiemy

### Przychody (mln zł)

| Okres | Przychody | Zmiana r/r |
|---|---|---|
| 2023 | 152,6 | — |
| 2024 | 192,8 | +26% |
| Q1 2025 | 51,7 | +17% |
| Q2 2025 | ~54,0 | +16% |
| Q3 2025 | 52,9 | +12% |
| 9M 2025 | 158,3 | — |

### EBITDA skorygowana (mln zł)

| Okres | EBITDA skor. | Marża |
|---|---|---|
| 2023 | 50,6 | 33,2% |
| 2024 | 66,1 | 34,3% |
| Q1 2025 | 18,5 | 35,8% |
| Q2 2025 | ~19,5 | 36,2% |
| Q3 2025 | 19,4 | 36,7% |
| 9M 2025 | 57,4 | 36,3% |

### GMV (mld zł)

| Okres | GMV Sklepy | GMV Omnichannel | GMV Apilo (est.) |
|---|---|---|---|
| 2023 | 8,5 | ~9,5 | ~1,0 |
| 2024 | 10,7 | 14,5 | ~3,8 |
| Q4 2024 | 3,0 | 4,3 | ~1,3 |
| H1 2025 | ~5,8 (est.) | 9,0 | ~3,2 |
| Q2 2025 | 2,9 | 4,9 | ~2,0 |
| 9M 2025 | — | 14,5 | — |

### Kluczowe KPI

| Metryka | Wartość | Okres |
|---|---|---|
| Liczba e-sklepów (bezpośrednich) | ~20 000 | Q1 2025 |
| Klienci w ekosystemie (incl. Apilo) | 60 000+ | Q3 2025 |
| ARPU Standard | 4 700 PLN/rok | 2023 |
| ARPU Premium | 29 400 PLN/rok | 2023 |
| Take rate | 1,87% | H1 2025 |
| Take rate (historyczny) | 1,39% | 2021 |
| Udział w rynku platform | ~45% | IPO 2021 |

---

## Krok 1: Ekonomia jednego klienta

### Ile Shoper zarabia na jednym sklepie?

Liczymy implied ARPU (blended) = łączne przychody / liczba aktywnych sklepów:

```
2024: 192,8 mln zł / ~20 000 sklepów = ~9 640 PLN/rok na sklep
2023: 152,6 mln zł / ~20 000 sklepów = ~7 630 PLN/rok na sklep
```

**Uwaga:** Liczba sklepów (~20 000) to przybliżenie na Q1 2025. W 2023 mogła być nieco inna (w 2021 było 25 700, potem spadła po restrukturyzacji klientów home.pl). To wpływa na dokładność ARPU.

### Ile sklepów jest Premium?

Znamy ARPU Standard (4 700) i Premium (29 400) za 2023. Implied blended ARPU = 7 630.

```
Równanie: 4 700 × (1 - x) + 29 400 × x = 7 630
4 700 + 24 700x = 7 630
24 700x = 2 930
x = 11,9%
```

**~12% klientów to klienci Premium, generując ~47% przychodów z abonamentów.**

To kluczowy insight: niewielka grupa klientów Premium generuje niemal połowę przychodów abonamentowych. Każdy klient, który przechodzi ze Standard do Premium, to 6x wzrost ARPU bez kosztu akwizycji.

### Wzrost ARPU rok do roku

```
2023 → 2024: 7 630 → 9 640 PLN = +26%
```

Wzrost ARPU (+26%) = wzrost przychodów (+26%) przy stabilnej bazie klientów (~20 tys.). To oznacza, że wzrost Shopera w 2024 wynikał **głównie z wyciągania większej wartości z istniejących klientów** (wyższy take rate, więcej usług dodatkowych, migracja do Premium), a nie z pozyskiwania nowych.

To jest bardzo dobry sygnał — oznacza Net Revenue Retention > 100%.

---

## Krok 2: Monetyzacja — take rate

### Czym jest take rate w modelu Shoper?

Take rate = łączne przychody Shoper / GMV Sklepów

Obejmuje wszystko: abonament, prowizję od transakcji, płatności, logistykę, usługi dodatkowe.

### Trend take rate

| Rok | Take rate | Zmiana |
|---|---|---|
| 2021 | 1,39% | — |
| 2022 | ~1,50% (est.) | +0,11pp |
| 2023 | 1,80% (calc: 152,6M / 8,5mld) | +0,30pp |
| 2024 | 1,80% (calc: 192,8M / 10,7mld) | +0,00pp |
| H1 2025 | 1,87% | +0,07pp |

**Kalkulacja kontrolna:**
```
2023: 152,6 mln / 8 500 mln = 1,80% ✓
2024: 192,8 mln / 10 700 mln = 1,80% ✓
```

**Uwaga:** Take rate stabilizował się w 2024, ale znowu rośnie w 2025. To sugeruje, że nowe usługi (Apilo, płatności, AI) zaczynają zwiększać monetyzację.

### Benchmark: Shopify

Shopify ma take rate ~2,8% (2024). Shoper jest na 1,87%.

```
Potencjalna przestrzeń: 2,8% - 1,87% = 0,93pp
Gdyby take rate wzrósł do 2,5%: przychody przy GMV 10,7 mld = 267,5 mln vs obecne 192,8 mln
Dodatkowe przychody: +74,7 mln zł (+39%) — bez jednego nowego klienta
```

To jest potencjalna wartość ukryta w Shoperze. Ale UWAGA — Shopify działa na rynku US, gdzie e-commerce jest dojrzalszy, kupujący wydają więcej, i infrastruktura płatnicza jest bardziej zintegrowana. Nie można mechanicznie przenosić tego benchmarku.

---

## Krok 3: Retencja i LTV

### Czego nie wiemy (i dlaczego to ważne)

Shoper nie publikuje wprost dwóch kluczowych metryk:
- **Churn rate** — jaki % klientów odchodzi rocznie
- **Net Revenue Retention (NRR)** — czy istniejący klienci wydają rok do roku więcej

Ale możemy to wyestymować z danych, które mamy.

### Implikowana retencja (estimation)

Wiemy, że:
- Baza klientów jest stabilna (~20 000 sklepów) od ~2023
- Przychody rosną +26% r/r przy stabilnej bazie klientów
- ARPU rośnie z 7 630 do 9 640

Jeśli baza klientów jest stabilna, to: nowi klienci ≈ odchodzący klienci (churn).

**Typowy churn dla platform SaaS SMB:** 3-7% miesięcznie = 30-60% rocznie (!)

Ale to na rynku US, gdzie konkurencja jest brutalna. Na polskim rynku, przy 45% udziale Shoper i ograniczonej konkurencji, churn powinien być niższy. Szacuję: **15-25% rocznie** (1,5-2% miesięcznie).

### Implikowana Net Revenue Retention

```
NRR = (Przychody z istniejących klientów w roku N) / (Przychody z tych samych klientów w roku N-1)

Jeśli przychody +26% r/r przy stabilnej bazie:
NRR ≈ 126%
```

**NRR 126% oznacza: nawet gdyby Shoper nie pozyskał ani jednego nowego klienta, jego przychody rosłyby 26% rocznie** — bo istniejący klienci kupują więcej usług, płacą wyższy take rate, przechodzą na Premium.

Dla kontekstu: Shopify ma NRR ~110%. Najlepsze spółki SaaS (Snowflake, Datadog) mają 120-140%. Jeśli Shoper faktycznie ma ~126%, to wyjątkowa jakość.

**⚠️ ZASTRZEŻENIE:** To szacunek oparty na założeniu stabilnej bazy klientów. Jeśli baza klientów spadła (np. z 22 000 do 20 000), to NRR byłoby jeszcze wyższe. Jeśli wzrosła — niższe. Bez dokładnych danych o churnie to jest przybliżenie.

### LTV — Lifetime Value klienta

```
Scenariusz bazowy (churn 20%/rok, avg lifetime 5 lat):
- Roczny przychód na klienta: 9 640 PLN
- Marża EBITDA: 36%
- Roczny zysk na klienta: 9 640 × 0,36 = 3 470 PLN
- LTV = 3 470 × 5 lat = 17 350 PLN

Scenariusz optymistyczny (churn 15%/rok, avg lifetime 6,7 lat):
- LTV = 3 470 × 6,7 = 23 250 PLN

Scenariusz pesymistyczny (churn 30%/rok, avg lifetime 3,3 lat):
- LTV = 3 470 × 3,3 = 11 450 PLN
```

### LTV/CAC

Nie mamy bezpośrednich danych o CAC (koszt pozyskania klienta). Wiemy, że Shoper inwestuje ~40 mln zł/rok w rozwój produktu, ale to nie jest to samo co koszt pozyskania.

**⚠️ LUKA DANYCH:** Potrzebowalibyśmy danych o kosztach marketingu z raportu rocznego, żeby policzyć CAC. To wymaga PDF raportu rocznego.

---

## Krok 4: Marżowość i skalowalność

### Dźwignia operacyjna — czy marża rośnie?

| Okres | Marża EBITDA skor. | Trend |
|---|---|---|
| 2023 | 33,2% | — |
| 2024 | 34,3% | +1,1pp |
| Q1 2025 | 35,8% | +1,5pp |
| Q2 2025 | 36,2% | +0,4pp |
| Q3 2025 | 36,7% | +0,5pp |

**Marża rośnie kwartał po kwartale.** To potwierdza dźwignię operacyjną: przychody rosną szybciej niż koszty. Każdy dodatkowy złoty przychodu kosztuje Shopera mniej niż poprzedni.

### Implikowana struktura kosztów (2024)

```
Przychody:          192,8 mln zł
EBITDA (skor.):      66,1 mln zł
Koszty operacyjne:  126,7 mln zł (= 192,8 - 66,1)

Marża EBITDA:        34,3%
Koszty jako % rev:   65,7%
```

Główne kategorie kosztów SaaS:
- **Koszty pracownicze** (developerzy, support, sprzedaż) — prawdopodobnie 50-60% kosztów
- **Infrastruktura** (serwery, hosting) — 10-15%
- **Marketing i pozyskanie klientów** — 15-25%
- **Koszty transakcyjne** (prowizje od płatności) — 5-10%

**⚠️ LUKA DANYCH:** Dokładny podział kosztów wymaga raportu rocznego. To jest kluczowe do obliczenia CAC.

### Skalowanie: co się dzieje przy 2x przychodach?

W modelu SaaS koszty stałe (platforma, serwery, core team) nie rosną liniowo z przychodami. Jeśli Shoper podwoi przychody do ~400 mln:
- Koszty infrastruktury wzrosną może 30-40%
- Koszty supportu wzrosną, ale nie 2x (automatyzacja, AI)
- Koszty marketingu mogą rosnąć proporcjonalnie
- **Implikowana marża EBITDA przy 400 mln:** 40-45%

To jest potencjał, który rynek wycenia (lub nie wycenia).

---

## Krok 5: Złożenie modelu — co to wszystko razem znaczy?

### Podsumowanie unit economics Shoper

| Metryka | Wartość | Ocena |
|---|---|---|
| ARPU (blended) | 9 640 PLN/rok (2024) | 🟢 Rośnie +26% r/r |
| Take rate | 1,87% (H1'25) | 🟢 Rośnie, przestrzeń do 2,5%+ |
| NRR (implied) | ~126% | 🟢 Wyjątkowa jakość (jeśli potwierdzony) |
| LTV (bazowy) | ~17 350 PLN | 🟡 Zależy od churn, który nie znamy |
| Marża EBITDA | 36,7% (Q3'25) | 🟢 Rośnie, dźwignia operacyjna |
| Wzrost przychodów | +12-17% r/r (2025) | 🟢 Solidny, głównie organiczny |
| GMV Omnichannel | +43-55% r/r | 🟢 Apilo jako nowy motor wzrostu |
| Udział Premium | ~12% klientów | 🟡 Potencjał upsellingu |
| LTV/CAC | BRAK DANYCH | 🔴 Wymaga raportu rocznego |
| Churn | BRAK DANYCH | 🔴 Szacunek: 15-25%/rok |

### Co jest mocne?

1. **Rosnący take rate bez utraty klientów** — Shoper wyciąga coraz więcej z każdego sklepu, a baza nie spada. To dowód na pricing power.
2. **NRR prawdopodobnie >120%** — istniejący klienci wydają coraz więcej. To najlepsza metryka jakości SaaS.
3. **Dźwignia operacyjna działa** — marża EBITDA rośnie z 33% do 37% w 2 lata.
4. **Apilo jako nowe koło zamachowe** — GMV +175% r/r. Shoper staje się hubem omnichannel, nie tylko platformą sklepową.

### Co wymaga uwagi?

1. **Nie znamy churn** — to największa luka. Jeśli churn jest 30%+, LTV spada dramatycznie.
2. **Spowolnienie wzrostu przychodów** — z +26% (2024) do +12-17% (2025). Czy to normalizacja, czy sygnał ostrzegawczy?
3. **Zależność od cyber_Folks** — 49,9% udziałów, strategiczna współpraca. Ryzyko: co jeśli zmienią strategię?
4. **Brak danych o CAC** — nie wiemy, ile kosztuje pozyskanie klienta.

### Co trzeba uzupełnić z raportu rocznego PDF?

1. **Koszty marketingu / sprzedaży** → do obliczenia CAC
2. **Dokładna liczba klientów** (początek i koniec roku) → do obliczenia churn
3. **Segmentacja przychodów** (abonament vs prowizje vs usługi dodatkowe)
4. **Przepływy pieniężne** → FCF yield, capex structure
5. **Dane o kohortach** (jeśli ujawniane w prezentacjach)

---

## Źródła

- Szacunkowe wyniki 2024 — komunikat Shoper SA via PAP Biznes
- Wyniki Q1-Q3 2025 — komunikaty prasowe Shoper SA
- Dane IPO — prospekt emisyjny 2021
- Take rate trend — komunikaty kwartalne, Strefa Inwestorów
- Benchmark Shopify — publiczne dane spółki (NYSE: SHOP)
- [Shoper Q1 2025 — komunikat](https://investors.shoper.pl/serwis-prasowy/wyniki-finansowe-q1-2025---komunikat)
- [Shoper rekordowe wyniki 2024 — e-biznes.pl](https://e-biznes.pl/shoper-osiaga-rekordowe-wyniki-finansowe-w-2024-roku-145-mld-zl-wartosci-transakcji)
- [Shoper Q3 2025 — Stockwatch](https://www.stockwatch.pl/wiadomosci/shoper-zwiekszyl-zysk-netto-do-104-mln-zl-w-iii-kwartale-2025-r,akcje,360353)
- [Shoper GMV Q2 2025 — Strefa Inwestorów](https://strefainwestorow.pl/wiadomosci/20250902/rekordowe-gmv-shoper-i-wyzsza-rentownosc-w-drugim-kwartale-2025)
