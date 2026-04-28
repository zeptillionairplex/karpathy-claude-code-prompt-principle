# 12 — Font Pairing (decision-first)

## Why this exists

`04-typography-and-color.md` § 1–3 은 "Inter only 회피" 만 명시하지만 페어
링 결정 절차가 없다. "Pretendard + Fraunces" 같은 KR+Latin 페어를 어떤
근거로 골랐는지 docs 안에 없으면 다음 mock 도 동일 페어를 답습한다. 본 doc
은 페어링 결정의 **3 rules → matrix → fallback stack** 흐름을 박는다.

**결정 = which pair → matrix lookup**. 결과 = `font-family` 한 줄. 이 doc
은 결정 자체가 doc 의 § 2 (3 rules) 다음에 § 3 (Latin matrix) → § 4 (KR+Latin
matrix) 순서로 펼쳐진다 (Architect #2 fix — which-rule column 의무).

## When to use

- 새 프로젝트의 폰트 결정
- 기존 단일 폰트에 display 또는 mono 추가 검토
- KR+Latin 다국어 페어 결정
- Variable font 도입 검토
- fallback stack 최적화

## How to use

1. § 1 결정트리로 single vs pair 분기.
2. § 2 의 3 rules 체크 — 위반 시 페어 reject.
3. § 3 또는 § 4 매트릭스에서 페어 lookup. 없으면 § 2 rules 로 ad-hoc 검증
   후 매트릭스에 등록.
4. § 5 variable font / § 6 fluid type / § 7 fallback / § 8 loading 선택.

---

## § 1. Pairing decision tree

```
프로젝트 시작
  │
  ├─ 단일 super-family 로 충분? (Inter / Geist / Pretendard 100–900 모두 사용)
  │     │
  │     ├─ Yes → § 5 Variable font 활용 + § 7 fallback stack 만 결정 → 끝
  │     │       (Anti-pattern #8 회피: 200 또는 800/900 weight 가 ≥ 1 등장)
  │     │
  │     └─ No  → 페어링 필요 → § 2
  │
  └─ 다국어 (KR / JP / CJK) 포함?
        │
        ├─ Yes → § 4 KR+Latin matrix
        │
        └─ No  → § 3 Latin matrix
```

**Single-family 권장 사례:** Inter / Geist / Pretendard / Manrope 처럼
weight 100–900 + italic + variable axis 가 모두 갖춰진 super-family. 페어
없이 hierarchy 가 충분 — Vercel/Stripe 가 이 경로.

**Pair 필요 사례:** display 가 본문과 다른 voice 를 요구하는 에디토리얼,
serif 의 heritage 가 brand identity 인 경우, 또는 mono 가 코드/숫자에
필요한 dev 도구.

---

## § 2. Pairing 규칙 (3 rules)

### Rule 1 — Voice contrast

display 와 body 가 **음성** 이 달라야. 같은 voice 면 페어가 무용 — 단일
폰트 + weight 차이로 충분.

| Voice 카테고리 | 예 | 짝 |
|---|---|---|
| Geometric sans | Geist, Futura, Avenir | ↔ Humanist sans / Serif |
| Humanist sans | Inter, Fira Sans, Source Sans | ↔ Geometric sans / Serif |
| Modern serif | Playfair, Bodoni | ↔ Sans (geometric/humanist) |
| Old-style serif | Garamond, Caslon, Source Serif | ↔ Sans (humanist) |
| Slab serif | Roboto Slab, Fraunces (slab axis) | ↔ Sans / Mono |
| Mono | JetBrains Mono, Geist Mono | ↔ Sans (보통 within same super-family) |

### Rule 2 — x-height matching

두 폰트의 x-height 비율 차이 ≤ 5%. 그 이상이면 baseline 어긋남, 같은 줄
안에서 한 폰트가 "위로 떠 있는" 느낌.

```text
x-height ratio = (소문자 'x' 의 높이) / (cap height)
Inter: 0.524
Pretendard: 0.520 (Hangul 기준 x-height equivalent)
Fraunces: 0.510
Playfair Display: 0.460 (gap 12% — 매칭 안 됨)
Source Serif: 0.500 (Inter 와 gap 5% — 경계선)
```

검증 도구: [Fontpair x-height visualizer](https://www.fontpair.co/) 또는
[Wakamai Fondue](https://wakamaifondue.com/) (font 메타 분석).

### Rule 3 — Weight contrast

display = 700–900, body = 400–500. 차이 ≥ 300 weight points. 차이가
< 200 이면 위계 부족, > 500 이면 unbalanced.

```css
h1 { font-family: "Fraunces"; font-weight: 900; }
body { font-family: "Inter"; font-weight: 400; }
/* gap 500 — 균형 안 잡힘. body 를 500 으로 올리거나 h1 을 700 으로. */

h1 { font-family: "Fraunces"; font-weight: 700; }
body { font-family: "Inter"; font-weight: 400; }
/* gap 300 — 정확. */
```

---

## § 3. Latin pairing matrix (12 페어)

| # | Display | Body | x-height ratio | weight gap | use case | which-rule | Source |
|---|---|---|---|---|---|---|---|
| L-1 | Fraunces | Inter | 0.510 / 0.524 (gap 2.7%) | 700/400 | 에디토리얼, 빈티지/heritage SaaS | Rule 1+2+3 ✓ | Vercel Geist 풍 |
| L-2 | Playfair Display | Source Sans | 0.460 / 0.510 (gap 9.8%) | 900/400 | 럭셔리, 매거진 | Rule 1+3 ✓ / Rule 2 borderline | Fontpair |
| L-3 | Lora | Lato | 0.485 / 0.510 (gap 5.0%) | 700/400 | 콘텐츠 블로그, 에세이 | Rule 1+2+3 ✓ | Google Fonts pairings |
| L-4 | Space Grotesk | IBM Plex Sans | 0.522 / 0.516 (gap 1.2%) | 700/400 | 테크/dev 도구 | Rule 1+2+3 ✓ | Awwwards 다수 |
| L-5 | Geist | Geist Mono | 동일 super-family | 700/400 | dev tool, 코드/숫자 강조 | Rule 1 (mono+sans) | Vercel |
| L-6 | Inter Tight | Inter | 동일 super-family | 800/400 | 미니멀 SaaS | Rule 3 (tight=display variant) | Stripe |
| L-7 | Cormorant Garamond | Work Sans | 0.480 / 0.510 (gap 6.3%) | 700/400 | 부티크, fashion | Rule 1+3 ✓ / Rule 2 borderline | Fontpair |
| L-8 | DM Serif Display | DM Sans | 동일 super-family | 700/400 | consumer brand | Rule 1+2+3 ✓ | Google Fonts |
| L-9 | Fraunces (opsz 144) | Fraunces (opsz 9) | 동일 폰트, opsz 차이 | 900/400 | 미니멀, 단일 폰트 | Rule 1 (opsz axis) | Fraunces variable |
| L-10 | JetBrains Mono | Inter Tight | 0.530 / 0.522 (gap 1.5%) | 700/400 | 코드 우선 dev | Rule 1+2+3 ✓ | JetBrains 자체 |
| L-11 | Roboto Slab | Roboto | 0.520 / 0.528 (gap 1.5%) | 900/400 | Material 정통 | Rule 1+2+3 ✓ | Material 3 |
| L-12 | EB Garamond | Source Sans Pro | 0.490 / 0.510 (gap 4.0%) | 700/400 | 학술, 출판 | Rule 1+2+3 ✓ | Adobe Fonts |

**검증법:** 새 페어를 매트릭스에 추가 시 (1) Rule 1 voice 대비 명시 (2)
x-height ratio 측정값 (3) weight gap (4) which-rule 4-tuple 모두 채울 것.

---

## § 4. Korean + Latin pairing matrix

KR display + Latin body, KR body + Latin display 양방향. KR 폰트의
Latin 글리프 품질이 결정 요인.

| # | KR | Latin | 방향 | x-height match | use case | KR baseline 처리 |
|---|---|---|---|---|---|---|
| K-1 | Pretendard | Inter | both as body | 0.520 / 0.524 (gap 0.8%) | 가장 안전한 default. SaaS, 콘텐츠. | Pretendard 단독으로 충분 — Latin fallback |
| K-2 | Pretendard | Fraunces | KR body + Latin display (italic) | 0.520 / 0.510 (gap 1.9%) | 빈티지/heritage 톤. 본 repo: `anti-ai-design-test.html` (koa pedals), `anti-ai-design-test.v2.html` (Apple MacBook) | display 만 Fraunces, body 는 Pretendard. line-height +0.1. weight: italic 500 (display) vs 400 (body). |
| K-3 | Noto Sans KR | Roboto | both as body | 0.516 / 0.528 (gap 2.3%) | Material 정통 KR, gov / 공공 | font-size-adjust: 0.52 권장 |
| K-4 | Spoqa Han Sans | Inter | both as body | 0.510 / 0.524 (gap 2.7%) | legacy 미디어, 기사 | line-height 1.7 |
| K-5 | Sandoll Gothic Neo | Source Sans | both as body | — | 상업 KR 브랜드 (유료) | 라이선스 별도 — 본 doc 의 default 아님 |
| K-6 | Pretendard | Geist | both as body | 0.520 / 0.522 (gap 0.4%) | dev tool KR localization | 코드는 Geist Mono 사용 |
| K-7 | Noto Serif KR | EB Garamond | both as display/serif | — | 출판, 학술 KR | h1/h2 만 serif, body 는 별도 sans |
| K-8 | Pretendard | DM Serif Display | KR body + Latin display | — | consumer brand KR | display 만 serif |

**KR baseline 처리 디테일:**

- `font-size-adjust: 0.5` — KR 와 Latin 의 x-height 를 강제로 매칭 (Latin
  fallback 시 baseline 어긋남 방지).
- `line-height` — KR body 1.7, Latin body 1.6 (KR 가 0.1 더 큼).
- `word-break: keep-all` + `line-break: strict`.
- `text-spacing: ideograph-alpha ideograph-numeric` — CJK/Latin 혼재 시
  자동 spacing.

**Source:** [Pretendard 공식](https://github.com/orioncactus/pretendard),
[Naver Typography](https://naver.github.io/fontface/typography.html).

---

## § 5. Variable font 활용

### 핵심 axis

| Axis | 효과 | 예시 폰트 |
|---|---|---|
| `wght` | weight 100–900 연속 | Inter, Pretendard, Geist |
| `opsz` | optical sizing — 9pt 본문 vs 144pt 디스플레이 자동 변형 | Fraunces, Source Serif |
| `wdth` | width — compressed 75% ~ extended 125% | Roboto Flex, Inter Tight |
| `slnt` | slant — italic 대신 기울기만 | Inter |
| `GRAD` | grade — 두께 미세 조정 (luminance 보정) | Roboto Flex |

**Payload:** 정적 weight 9개 (9 × 80KB ≈ 720KB) → Variable woff2 (wght 1×110KB,
wght+opsz 1×180KB). 1/4 payload + `font-variation-settings: "wght" 550;` 같은
임의 weight 도 가능.

```css
@font-face {
  font-family: "Inter Var";
  src: url("/fonts/inter.var.woff2") format("woff2-variations");
  font-weight: 100 900;          /* 범위 선언 */
  font-display: swap;
}

h1 { font-variation-settings: "wght" 880; }
.lede { font-variation-settings: "wght" 280; }
```

`font-optical-sizing: auto` — opsz axis 가 있는 폰트면 size 에 따라 자동
변형. Fraunces 9pt 와 144pt 가 다른 글리프로 표시.

---

## § 6. Fluid type — clamp() + container query

### clamp() 계산식

```css
font-size: clamp(min, preferred, max);
/* 기본 형태: min + (max-min) × (vw - min-vw) / (max-vw - min-vw) */

h1 { font-size: clamp(2rem, 1.5rem + 2vw, 3.5rem); }
/*    320px 화면: 2rem (32px)
      768px 화면: ≈ 2.4rem
      1440px 화면: 3.5rem (56px) */
```

도구: [Utopia.fyi](https://utopia.fyi/type/calculator) — viewport range +
type scale 입력 → clamp() 식 자동 생성.

### Container query 진입

`cq` 단위로 **컴포넌트 단위 fluid type** 가능 (viewport 와 무관):

```css
.card {
  container-type: inline-size;
}
.card h2 {
  font-size: clamp(1rem, 4cqi, 2rem);   /* card 너비 기반 */
}
```

`cqi` (container query inline size) — 카드가 좁은 사이드바에 들어가도 적절
크기.

**Source:** [Utopia.fyi — Type Calculator](https://utopia.fyi/type/calculator),
[MDN — Container queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries).

---

## § 7. Fallback stack 설계

### System fallback (KR 포함)

```css
body {
  font-family:
    "Pretendard Variable", "Pretendard",
    -apple-system, BlinkMacSystemFont,
    "Apple SD Gothic Neo",
    system-ui, "Segoe UI", Roboto,
    "Noto Sans KR", "Malgun Gothic",
    sans-serif;
}
```

순서 이유: 각 OS 의 최선 매치가 앞쪽. macOS/iOS → `-apple-system` →
`Apple SD Gothic Neo`. Windows → `Segoe UI` → `Malgun Gothic`. Android →
`Roboto` → `Noto Sans KR`. 마지막 generic `sans-serif` 가 안전망.

### `size-adjust` / `ascent-override` 로 CLS 방지

```css
@font-face {
  font-family: "Pretendard fallback";
  src: local("Apple SD Gothic Neo"), local("Malgun Gothic");
  size-adjust: 102%; ascent-override: 90%; descent-override: 22%;
}
```

도구 [Fallback metrics generator](https://screenspan.net/fallback) 가
size-adjust 값 자동 출력 → CLS score 0.

**Source:** [Simon Hearne — fallback metrics](https://simonhearne.com/2021/layout-shifts-webfonts/),
[MDN — size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust).

---

## § 8. Loading 전략

| `font-display` | 동작 | Use case |
|---|---|---|
| `swap` | 즉시 fallback, webfont 로드되면 swap | **Default 권장** — body, ui |
| `optional` | 100ms 미로드 시 fallback 으로 끝 | 모바일 뉴스, low-bandwidth |
| `block` | 3초 invisible 후 fallback | hero display, brand identity |
| `fallback` | 100ms invisible + 3초 swap window | swap+optional 절충 |

`preconnect` (DNS+TLS 미리) + `preload` (critical font fetch) 순서:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/pretendard.var.woff2" crossorigin>
```

Subset (`unicode-range`) — Hangul ≈ 250KB / Latin ≈ 30KB. 순차 fetch.

**Source:** [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display),
[Google Fonts API](https://developers.google.com/fonts/docs/getting_started).

---

## § 9. anti-pattern (cross-link to 06)

- **#8 Inter only, body to footer** — § 1 결정트리에서 single super-family
  + 200/800/900 weight 강제, 또는 § 3/4 매트릭스에서 페어 선택.
- **(신규 cross-link)** voice contrast 없는 페어 — § 2 Rule 1 위반. 두
  폰트가 같은 humanist sans 면 페어 무용.

---

## Self-audit checklist

- [ ] § 1 결정트리로 single vs pair 결정 명시 (design 메모 1줄)
- [ ] § 2 Rule 1 — 두 폰트의 voice 카테고리가 다름
- [ ] § 2 Rule 2 — x-height ratio gap ≤ 5% (또는 borderline 인정 1줄)
- [ ] § 2 Rule 3 — display/body weight gap ≥ 300
- [ ] § 3 또는 § 4 매트릭스 row 와 매핑 명시 (예: "L-1 row 차용")
- [ ] 매트릭스에 없으면 ad-hoc 검증 후 새 row 등록
- [ ] Variable font 1개로 정적 weight 다수 대체 (payload 1/3 이하)
- [ ] § 7 fallback stack 이 KR+Latin 양쪽 OS 커버
- [ ] `size-adjust` / `ascent-override` 로 CLS 0
- [ ] `font-display: swap` (또는 명시적 다른 값 + 근거)
- [ ] `preconnect` 가 webfont 도메인에 적용
- [ ] subset (latin / korean) 또는 woff2 사용

12 items. ≤ 2 fails 통과.

---

## Sources

- [Fontpair — pairing matrix](https://www.fontpair.co/)
- [Practical Typography — Butterick](https://practicaltypography.com/)
- [Refactoring UI — Typography](https://www.refactoringui.com/)
- [Utopia.fyi — Type Calculator](https://utopia.fyi/type/calculator)
- [Pretendard 공식](https://github.com/orioncactus/pretendard)
- [Naver Typography](https://naver.github.io/fontface/typography.html)
- [Google Fonts API](https://developers.google.com/fonts/docs/getting_started)
- [MDN — font-display](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display)
- [MDN — size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust)
- [Wakamai Fondue — font metrics analyzer](https://wakamaifondue.com/)
- [Simon Hearne — fallback metrics](https://simonhearne.com/2021/layout-shifts-webfonts/)
- [Fallback metrics generator](https://screenspan.net/fallback)
- [Vercel Geist — typography](https://vercel.com/geist/typography)

## Refresh policy

분기 1회 검토. 변경 트리거: 신규 super-family 출시 (예: Inter v4),
Variable font 신규 axis 채택, 한국 폰트 라이선스 변경 (Pretendard 업데이트).

**Last updated:** 2026-04-29
