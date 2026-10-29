import os
import urllib.parse
import hashlib
import json
import shutil

# 1. 사이트 기본 설정
SITE_ORIGIN = "https://daejeon-slimtherapy.netlify.app"
SITE_NAME = "S슬림테라피"
DEFAULT_PHONE = "0507-1280-3358"

# 2. 지정 단일 제휴 업체
PARTNER_SHOPS = [
    {
        "name": "S슬림테라피",
        "phone": "0507-1280-3358",
        "category": "S케어 VIP",
        "price": "건식 60분 50,000원~",
        "img": "01"
    }
]

# 3. 대전·청주·세종·천안·아산 충청권 시구동 데이터셋
REGION_DATA = {
    "daejeon": {
        "name": "대전광역시", "short": "대전",
        "districts": {
            "유성구": ["봉명동", "온천동", "구암동", "장대동", "상대동", "원신흥동", "도룡동", "신성동", "전민동", "관평동", "송강동", "노은동", "지족동", "반석동", "덕명동", "학하동", "진잠동"],
            "서구": ["둔산동", "탄방동", "월평동", "갈마동", "만년동", "괴정동", "용문동", "가장동", "내동", "변동", "도마동", "정림동", "복수동", "가수원동", "도안동", "관저동", "기성동"],
            "중구": ["은행동", "선화동", "대흥동", "문창동", "석교동", "대사동", "부사동", "용두동", "오류동", "태평동", "유천동", "문화동", "산성동"],
            "동구": ["중앙동", "신인동", "효동", "판암동", "용운동", "대동", "자양동", "가양동", "용전동", "성남동", "홍도동", "삼성동", "대청동", "산내동"],
            "대덕구": ["오정동", "대화동", "회덕동", "비래동", "송촌동", "중리동", "법동", "신탄진동", "석봉동", "덕암동", "목상동"]
        }
    },
    "cheongju": {
        "name": "청주시", "short": "청주",
        "districts": {
            "흥덕구": ["가경동", "복대동", "봉명동", "송정동", "강서동", "운천동", "신봉동", "오송읍", "강내면", "옥산면"],
            "청원구": ["율량동", "사천동", "오창읍", "내수읍", "우암동", "내덕동", "북이면"],
            "상당구": ["용암동", "금천동", "영운동", "탑대성동", "성안동", "중앙동", "용담동", "남일면", "문의면", "가덕면"],
            "서원구": ["사직동", "사창동", "모충동", "산남동", "분평동", "수곡동", "성화동", "개신동", "죽림동", "남이면", "현도면"]
        }
    },
    "sejong": {
        "name": "세종특별자치시", "short": "세종",
        "districts": {
            "세종시": ["나성동", "어진동", "새롬동", "다정동", "종촌동", "고운동", "아름동", "도담동", "보람동", "대평동", "소담동", "반곡동", "조치원읍", "장군면", "금남면", "부강면", "연서면"]
        }
    },
    "cheonan": {
        "name": "천안시", "short": "천안",
        "districts": {
            "서북구": ["불당동", "백석동", "두정동", "성정동", "쌍용동", "부성동", "성환읍", "직산읍", "성거읍", "입장면"],
            "동남구": ["신부동", "청수동", "청당동", "신방동", "원성동", "봉명동", "일봉동", "문성동", "중앙동", "목천읍"]
        }
    },
    "asan": {
        "name": "아산시", "short": "아산",
        "districts": {
            "아산시": ["배방읍", "탕정면", "온양동", "모종동", "용화동", "풍기동", "신창면", "음봉면", "둔포면", "염치읍"]
        }
    }
}

def render_cards_html(area_label, dong_name=""):
    seed = int(hashlib.md5(f"{area_label}_{dong_name}".encode('utf-8')).hexdigest(), 16)
    s = PARTNER_SHOPS[0]

    prefixes = [
        f"{dong_name} 직영 " if dong_name else "",
        f"{dong_name} " if dong_name else "",
        "프라이빗 S케어 ",
        "100% 후불 안심 ",
        "VIP 힐링 "
    ]
    prefix = prefixes[seed % len(prefixes)]
    display_name = f"{prefix}{s['name']}".strip()

    return f"""
    <article class="shop-card single-feature-card">
      <a class="card-media" href="tel:{s['phone']}" aria-label="{display_name} 전화 문의">
        <span class="media-fallback">{s['category']}</span>
        <picture class="card-picture">
  <source media="(max-width: 680px)" srcset="/assets/cards/therapist-card-01-240.webp">
  <img class="card-photo" src="/assets/cards/therapist-card-01-512.webp" alt="{display_name} 대표 이미지" width="512" height="320" loading="lazy">
</picture>
      </a>
      <div class="card-body">
        <div style="display:flex; justify-content:space-between; width:100%; align-items:center; margin-bottom: 6px;">
          <span class="category-tag">{s['category']}</span>
          <span style="font-size: 0.8rem; color: #f59e0b; font-weight: 850;">★ 4.9 (고객 후기 {92 + (seed % 45)}개)</span>
        </div>
        <h3 style="font-size: 1.35rem; margin: 4px 0 8px;"><a class="card-title-link" href="tel:{s['phone']}">{display_name}</a></h3>
        <p class="address">{area_label} 전 지역 1:1 방문 맞춤 케어 · 25분 내 신속 도착</p>
        <p style="font-size: 0.88rem; color: #64748b; margin: 0 0 16px;">선입금·예약금 없는 100% 안심 후불제 | 호텔·자택·오피스텔 프라이빗 방문 테라피</p>
        <div class="card-bottom">
          <div><span class="price-label">대표 코스 요금</span><strong class="price">{s['price']}</strong></div>
          <div class="card-actions">
            <a class="detail-link" href="sms:{s['phone']}">문자예약</a>
            <a class="phone-link" href="tel:{s['phone']}" aria-label="{display_name} 전화하기">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              <span>전화문의</span>
            </a>
          </div>
        </div>
      </div>
    </article>"""

def generate_page(title_area, page_path, breadcrumbs, related_links, current_city="daejeon", current_district="", current_dong=""):
    full_url = f"{SITE_ORIGIN}{page_path}"
    
    # 요청하신 타이틀 & 메타디스크립션 양식 적용
    page_title = f"{title_area} 대전 청주 출장 S케어 마사지 | 지역별 이용 가이드 - {SITE_NAME}"
    meta_desc = f"{SITE_NAME} 선입금없는 후불제 {title_area} 청주 대전 출장 마사지 안내! 대전시 일정과 공간에 맞춰 제휴업체 선택지와 후기 등을 확인하세요."
    
    seed = int(hashlib.md5(f"{title_area}_{page_path}".encode('utf-8')).hexdigest(), 16)
    review_count = str(98 + (seed % 60))
    rating_val = "4.9"

    # 네이버 별점 스니펫용 LocalBusiness Schema
    structured_data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"{title_area} 출장 S케어 마사지 - {SITE_NAME}",
        "description": meta_desc,
        "url": full_url,
        "telephone": DEFAULT_PHONE,
        "priceRange": "50,000원 ~ 150,000원",
        "image": f"{SITE_ORIGIN}/assets/banner.jpg",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": current_district or title_area,
            "addressRegion": REGION_DATA[current_city]["name"],
            "addressCountry": "KR"
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": REGION_DATA[current_city]["name"]},
            {"@type": "AdministrativeArea", "name": title_area}
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating_val,
            "reviewCount": review_count,
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    json_ld_string = json.dumps(structured_data, ensure_ascii=False, indent=2)

    nav_chips = "".join([
        f'<a class="area-chip{" is-active" if link.get("active") else ""}" href="{link["path"]}">{link["name"]}</a>'
        for link in related_links
    ])

    card_html = render_cards_html(title_area, current_dong)

    district_options = "".join([
        f'<option value="/{current_city}/{urllib.parse.quote(d)}/" {"selected" if d==current_district else ""}>{d}</option>'
        for d in REGION_DATA[current_city]["districts"].keys()
    ])

    dong_options = "".join([
        f'<option value="/{current_city}/{urllib.parse.quote(current_district)}/{urllib.parse.quote(dong)}/" {"selected" if dong==current_dong else ""}>{dong}</option>'
        for dong in REGION_DATA[current_city]["districts"].get(current_district, [])
    ]) if current_district else ""

    map_query = urllib.parse.quote(f"{title_area} 마사지")

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="naver-site-verification" content="035c40a92813479740412aa9cb31a765d613d031" />
  <title>{page_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{title_area} 출장마사지, {title_area} 타이마사지, {title_area} 아로마마사지, {title_area} 스웨디시, {SITE_NAME}, 대전출장마사지, 청주출장마사지">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#1e1b4b">
  <link rel="canonical" href="{full_url}">

  <!-- Open Graph -->
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="{full_url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:image" content="{SITE_ORIGIN}/assets/banner.jpg">
  <meta name="twitter:image" content="{SITE_ORIGIN}/assets/banner.jpg">
  <!-- 네이버 별점 및 구조화 데이터 -->
  <script type="application/ld+json">
{json_ld_string}
  </script>

  <style>
    :root {{
      --ink: #0f172a; --ink-soft: #475569; --primary: #6366f1; --primary-dark: #4338ca;
      --primary-pale: #eef2ff; --line: #e2e8f0; --radius-lg: 16px; --radius-md: 20px;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: var(--ink); font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f8fafc; line-height: 1.6; }}
    a {{ color: inherit; text-decoration: none; }}
    .app-header {{ position: sticky; top: 0; z-index: 20; background: rgba(255,255,255,.94); backdrop-filter: blur(12px); border-bottom: 1px solid var(--line); }}
    .header-inner, .page-shell {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; }}
    .brand-row {{ display: flex; align-items: center; justify-content: space-between; height: 68px; }}
    .brand {{ font-size: 1.25rem; font-weight: 850; display: inline-flex; align-items: center; gap: 8px; color: var(--primary-dark); }}
    
    .filter-bar {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; padding-bottom: 14px; }}
    .select-wrap select {{ width: 100%; height: 44px; padding: 0 14px; border: 1px solid var(--line); border-radius: 12px; background: #fff; font-size: .88rem; font-weight: 750; cursor: pointer; }}
    
    main {{ padding: 24px 0 48px; }}
    .intro {{ padding: clamp(24px, 4vw, 42px); border-radius: var(--radius-lg); background: #1e1b4b; color: #fff; text-align: center; border-top: 5px solid var(--primary); }}
    h1 {{ font-size: clamp(1.8rem, 3.6vw, 2.6rem); margin: 10px 0; word-break: keep-all; }}
    .intro-copy {{ color: #e0e7ff; margin-top: 8px; font-size: 1.05rem; word-break: keep-all; }}
    
    .rating-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); padding: 4px 14px; border-radius: 999px; color: #f59e0b; font-size: 0.88rem; font-weight: 850; margin-top: 8px; }}
    
    .nearby-row {{ display: flex; gap: 8px; overflow-x: auto; padding: 18px 0; justify-content: center; scrollbar-width: none; }}
    .nearby-row::-webkit-scrollbar {{ display: none; }}
    .area-chip {{ padding: 8px 14px; border: 1px solid var(--line); border-radius: 999px; background: #fff; font-size: .88rem; font-weight: 750; flex: 0 0 auto; transition: .18s; }}
    .area-chip:hover {{ border-color: var(--primary); }}
    .area-chip.is-active {{ background: var(--primary-pale); border-color: var(--primary); color: var(--primary-dark); }}
    
    .single-feature-card {{ max-width: 720px; margin: 20px auto 0; border: 1px solid var(--line); border-radius: var(--radius-md); background: #fff; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
    .card-media {{ aspect-ratio: 16/9; position: relative; background: #eee; display: block; }}
    .card-photo {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .card-body {{ padding: 22px; text-align: center; display: flex; flex-direction: column; }}
    .category-tag {{ padding: 4px 10px; border-radius: 6px; background: #ede9fe; color: #6d28d9; font-size: .78rem; font-weight: 850; }}
    .address {{ color: var(--ink-soft); font-size: .9rem; margin: 0 0 6px; }}
    .card-bottom {{ margin-top: 10px; padding-top: 14px; border-top: 1px solid #f1f5f9; display: flex; justify-content: space-between; align-items: center; }}
    .price {{ font-weight: 900; font-size: 1.05rem; color: var(--primary-dark); }}
    .phone-link {{ padding: 9px 18px; border-radius: 12px; background: var(--ink); color: #fff; font-size: .88rem; font-weight: 800; display: inline-flex; align-items: center; gap: 6px; }}
    .phone-link svg {{ width: 15px; height: 15px; }}
    .detail-link {{ padding: 9px 15px; border-radius: 12px; border: 1px solid var(--line); font-size: .88rem; margin-right: 6px; }}
    
    .content-box {{ margin-top: 36px; padding: clamp(20px, 3.5vw, 32px); background: #fff; border: 1px solid var(--line); border-radius: var(--radius-md); }}
    .content-box h2 {{ margin-top: 0; font-size: 1.35rem; color: var(--primary-dark); }}
    .content-box p {{ font-size: 0.94rem; color: #334155; line-height: 1.8; margin-bottom: 12px; }}
    
    /* 5대 코스 카드 그리드 스타일 */
    .course-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin-top: 16px; }}
    .course-card {{ border: 1px solid var(--line); border-radius: 14px; padding: 18px; background: #fafafa; display: flex; flex-direction: column; justify-content: space-between; }}
    .course-card.highlight {{ background: #fdf4ff; border-color: #f0abfc; }}
    .course-card h3 {{ margin: 0 0 4px; font-size: 1.1rem; color: #1e1b4b; }}
    .course-tag {{ font-size: 0.76rem; font-weight: 800; color: #7c3aed; margin-bottom: 8px; display: inline-block; }}
    .course-desc {{ font-size: 0.85rem; color: #64748b; margin: 0 0 14px; line-height: 1.5; }}
    .course-price-list {{ list-style: none; padding: 0; margin: 0; border-top: 1px dashed #cbd5e1; padding-top: 10px; }}
    .course-price-list li {{ display: flex; justify-content: space-between; font-size: 0.88rem; padding: 4px 0; }}
    .course-price-list li strong {{ color: var(--primary-dark); font-weight: 850; }}

    .map-box {{ margin-top: 24px; border-radius: 16px; overflow: hidden; border: 1px solid var(--line); height: 320px; }}
    .site-footer {{ margin-top: 40px; padding: 36px 0; background: #fff; border-top: 1px solid var(--line); text-align: center; color: var(--ink-soft); font-size: .88rem; }}
  </style>
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand" href="/" aria-label="{SITE_NAME} 홈">✨ {SITE_NAME}</a>
        <div style="font-size: .88rem; font-weight: 700; color: var(--ink-soft);">대전·청주 24시 출장 S케어 플랫폼</div>
      </div>
      <div class="filter-bar">
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;">
            <option value="/daejeon/" {'selected' if current_city=='daejeon' else ''}>대전광역시</option>
            <option value="/cheongju/" {'selected' if current_city=='cheongju' else ''}>청주시</option>
            <option value="/sejong/" {'selected' if current_city=='sejong' else ''}>세종특별자치시</option>
            <option value="/cheonan/" {'selected' if current_city=='cheonan' else ''}>천안시</option>
            <option value="/asan/" {'selected' if current_city=='asan' else ''}>아산시</option>
          </select>
        </div>
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;">
            <option value="/{current_city}/">구/시 선택 전체</option>
            {district_options}
          </select>
        </div>
        <div class="select-wrap">
          <select onchange="if(this.value) window.location.href=this.value;" {'disabled' if not current_district else ''}>
            <option value="/{current_city}/{urllib.parse.quote(current_district)}/">동 선택 전체</option>
            {dong_options}
          </select>
        </div>
      </div>
    </div>
  </header>

  <main class="page-shell">
    <section class="intro">
      <p style="color: #a5b4fc; font-weight: 800; letter-spacing: .08em;">24H S-CARE PRIVATE HOME THERAPY</p>
      <h1>{title_area} 대전 청주 출장 S케어 마사지<br>선입금 없는 안심 후불제 안내</h1>
      <p class="intro-copy">{title_area} 고객님의 일정과 공간에 맞춘 1:1 방문 맞춤 테라피! 선입금 요구 없이 도착 후 100% 결제하는 정직한 S슬림테라피입니다.</p>
      <div class="rating-badge">★ {rating_val} 점 / 5.0 만점 (실시간 고객 후기 {review_count}개 기준)</div>
    </section>

    <!-- 빠른 구 / 동 칩 링크 -->
    <nav class="nearby-row" aria-label="지역 바로가기">
      {nav_chips}
    </nav>

    <!-- 지정 단독 제휴 업체 카드 -->
    <section>
      <div style="text-align: center; margin: 24px 0 12px;">
        <h2 style="margin: 0; font-size: 1.45rem;">{title_area} 추천 공식 제휴 센터</h2>
        <p style="margin: 6px 0 0; color: var(--ink-soft); font-size: .9rem;">실력파 베테랑 테라피스트의 프라이빗 힐링을 정찰제 요금으로 만나보세요.</p>
      </div>

      {card_html}
    </section>

    <!-- 요청하신 5대 코스 세부 가격표 -->
    <section class="content-box">
      <h2>🔮 {title_area} S슬림테라피 코스별 상세 프로그램 요금표</h2>
      <p>{title_area} 전 지역에서 동일하게 적용되는 정찰 기준 가격입니다. 선입금 요구 없이 관리사 도착 후 결제하며, 추가 출장비가 발생하지 않습니다.</p>
      
      <div class="course-grid">
        <!-- 1. 건식 코스 -->
        <div class="course-card">
          <div>
            <h3>🔮 개운한 꾹꾹 건식</h3>
            <span class="course-tag">기본 힐링</span>
            <p class="course-desc">뭉치고 굳은 전신 근육을 시원하고 개운하게 풀어주는 정통 건식 수기 테라피</p>
          </div>
          <ul class="course-price-list">
            <li><span>⏱️ 60분</span><strong>50,000원</strong></li>
            <li><span>⏱️ 90분</span><strong>70,000원</strong></li>
            <li><span>⏱️ 120분</span><strong>80,000원</strong></li>
          </ul>
        </div>

        <!-- 2. 아로마 코스 -->
        <div class="course-card">
          <div>
            <h3>🔮 촉촉한 아로마</h3>
            <span class="course-tag">릴렉스 추천</span>
            <p class="course-desc">고급 천연 오일로 피부를 부드럽게 감싸고 긴장된 전신을 이완시키는 아로마 코스</p>
          </div>
          <ul class="course-price-list">
            <li><span>⏱️ 60분</span><strong>60,000원</strong></li>
            <li><span>⏱️ 90분</span><strong>80,000원</strong></li>
            <li><span>⏱️ 120분</span><strong>90,000원</strong></li>
          </ul>
        </div>

        <!-- 3. 스페셜 코스 -->
        <div class="course-card highlight">
          <div>
            <h3>🔮 스페셜 코스</h3>
            <span class="course-tag" style="color:#c026d3;">★BEST 인기</span>
            <p class="course-desc">아로마와 타이 스트레칭, 그리고 발관리까지 체계적으로 묶은 집중 프로그램</p>
          </div>
          <ul class="course-price-list">
            <li><span>⏱️ 120분 (아로마60+타이60)</span><strong>90,000원</strong></li>
            <li><span>⏱️ 150분 (+발관리30분)</span><strong>120,000원</strong></li>
            <li><span>⏱️ 180분 (+발관리60분)</span><strong>150,000원</strong></li>
          </ul>
        </div>

        <!-- 4. 힐링 코스 -->
        <div class="course-card">
          <div>
            <h3>🔮 힐링 코스</h3>
            <span class="course-tag">감성 릴렉싱</span>
            <p class="course-desc">심신의 안정과 깊은 휴식을 유도하는 섬세한 테라피스트의 감성 힐링 프로그램</p>
          </div>
          <ul class="course-price-list">
            <li><span>⏱️ 60분</span><strong>90,000원</strong></li>
            <li><span>⏱️ 90분</span><strong>100,000원</strong></li>
            <li><span>⏱️ 120분</span><strong>120,000원</strong></li>
            <li><span>⏱️ 150분</span><strong>150,000원</strong></li>
          </ul>
        </div>

        <!-- 5. VIP 스웨디시 -->
        <div class="course-card highlight">
          <div>
            <h3>🔮 VIP 스웨디시</h3>
            <span class="course-tag" style="color:#d97706;">👑 VIP 시그니처</span>
            <p class="course-desc">부드럽고 감각적인 터치로 림프 순환을 돕고 피로를 말끔히 비워내는 프리미엄 코스</p>
          </div>
          <ul class="course-price-list">
            <li><span>⏱️ 60분</span><strong>100,000원</strong></li>
            <li><span>⏱️ 90분</span><strong>120,000원</strong></li>
            <li><span>⏱️ 120분</span><strong>150,000원</strong></li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 네이버 검색 누락 방지용 지역 본문 -->
    <section class="content-box">
      <h2>✨ {title_area} S슬림테라피 이용 안내 및 고객 안심 수칙</h2>
      <p>
        지친 일상의 피로와 누적된 근육 뭉침을 해소하고자 하시는 고객님을 위해 <strong>{title_area}</strong> 출장 S케어 마사지 서비스를 제공합니다. 
        계신 자택, 오피스텔, 호텔 등 프라이빗한 공간에서 전화 한 통으로 품격 있는 전문 테라피를 편안하게 경험하실 수 있습니다.
      </p>
      <p>
        <strong>1. 100% 선입금 없는 후불 결제 원칙:</strong> 최근 빈번하게 발생하는 예약금 및 보증금 사기 피해를 원천 차단하기 위해, 
        {SITE_NAME}는 관리사가 현장에 도착한 후 직접 결제가 이루어지는 <strong>100% 안심 후불제</strong>만을 엄격히 고수합니다.
      </p>
      <p>
        <strong>2. 신속한 맞춤 방문 시스템:</strong> {title_area} 주요 교통축과 주거 상권을 기반으로 관리사가 대기하고 있어, 
        예약 통화 후 평균 25분 내외로 계신 곳까지 지체 없이 신속하게 방문합니다.
      </p>
      <p>
        <strong>3. 최고급 위생 용품 및 맞춤 프로그램:</strong> 1회용 청결 소모품과 최고급 천연 수용성 아로마 오일을 사용하여 쾌적하게 진행되며, 
        건식 압 조절부터 스웨디시 림프 케어까지 고객님의 신체 컨디션에 맞춘 1:1 집중 관리를 선사합니다.
      </p>
    </section>

    <!-- 동적 구글 지도 -->
    <section class="content-box">
      <h2>📍 {title_area} 출장 S케어 방문 권역</h2>
      <p>{title_area} 전 지역과 인접 도로망을 기반으로 신속한 방문 출장 관리가 가능합니다.</p>
      <div class="map-box">
        <iframe
          width="100%"
          height="100%"
          style="border:0;"
          loading="lazy"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q={map_query}&t=&z=14&ie=UTF8&iwloc=&output=embed">
        </iframe>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="header-inner">
      <p style="font-weight: 850; font-size: 1.15rem; color: var(--primary-dark); margin: 0 0 8px;">{SITE_NAME}</p>
      <p style="margin: 0 0 12px;">대전·청주·세종·충청권 24시 출장 S케어 마사지 플랫폼</p>
      <p style="font-size: .78rem; color: #64748b;">{SITE_NAME}는 예약금을 요구하지 않는 100% 안심 후불제 제휴 정보 사이트입니다.<br>© 2026 {SITE_NAME}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""

def main():
    sitemap_urls = [SITE_ORIGIN + "/"]
    os.makedirs("dist", exist_ok=True)

    # 1. 메인 홈페이지 생성 (대전 유성, 서구 및 청주 주요 거점 칩 링크)
    home_links = [
        {"name": "대전 유성구", "path": f"/daejeon/{urllib.parse.quote('유성구')}/"},
        {"name": "대전 서구", "path": f"/daejeon/{urllib.parse.quote('서구')}/"},
        {"name": "대전 중구", "path": f"/daejeon/{urllib.parse.quote('중구')}/"},
        {"name": "청주 흥덕구", "path": f"/cheongju/{urllib.parse.quote('흥덕구')}/"},
        {"name": "청주 청원구", "path": f"/cheongju/{urllib.parse.quote('청원구')}/"},
        {"name": "세종시", "path": f"/sejong/{urllib.parse.quote('세종시')}/"},
        {"name": "천안 불당", "path": f"/cheonan/{urllib.parse.quote('서북구')}/"},
        {"name": "아산시", "path": f"/asan/{urllib.parse.quote('아산시')}/"}
    ]
    home_bc = [{"name": "홈", "path": "/"}]
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(generate_page("대전 청주", "/", home_bc, home_links, current_city="daejeon"))
    print("✓ S슬림테라피 메인 페이지(dist/index.html) 생성 완료")

    # 2. 시·도, 구, 동 폴더 및 개별 정적 index.html 생성
    for city_key, city_info in REGION_DATA.items():
        city_path = f"/{city_key}/"
        sitemap_urls.append(SITE_ORIGIN + city_path)
        city_dir = os.path.join("dist", city_key)
        os.makedirs(city_dir, exist_ok=True)

        dist_links = [{"name": d, "path": f"/{city_key}/{urllib.parse.quote(d)}/"} for d in list(city_info["districts"].keys())[:12]]
        city_bc = [{"name": "홈", "path": "/"}, {"name": city_info["short"], "path": city_path}]
        with open(os.path.join(city_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(generate_page(city_info["name"], city_path, city_bc, dist_links, current_city=city_key))

        for district_name, dongs in city_info["districts"].items():
            encoded_dist = urllib.parse.quote(district_name)
            dist_path = f"/{city_key}/{encoded_dist}/"
            sitemap_urls.append(SITE_ORIGIN + dist_path)

            dist_dir = os.path.join(city_dir, district_name)
            os.makedirs(dist_dir, exist_ok=True)

            dong_links = [{"name": d, "path": f"/{city_key}/{encoded_dist}/{urllib.parse.quote(d)}/"} for d in dongs]
            dist_bc = city_bc + [{"name": district_name, "path": dist_path}]

            with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(generate_page(f"{city_info['short']} {district_name}", dist_path, dist_bc, dong_links, current_city=city_key, current_district=district_name))

            for dong_name in dongs:
                encoded_dong = urllib.parse.quote(dong_name)
                dong_path = f"/{city_key}/{encoded_dist}/{encoded_dong}/"
                sitemap_urls.append(SITE_ORIGIN + dong_path)

                dong_dir = os.path.join(dist_dir, dong_name)
                os.makedirs(dong_dir, exist_ok=True)

                dong_bc = dist_bc + [{"name": dong_name, "path": dong_path}]
                sibling_dongs = [
                    {"name": d, "path": f"/{city_key}/{encoded_dist}/{urllib.parse.quote(d)}/", "active": (d == dong_name)}
                    for d in dongs
                ]

                with open(os.path.join(dong_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(generate_page(
                        f"{city_info['short']} {district_name} {dong_name}",
                        dong_path,
                        dong_bc,
                        sibling_dongs,
                        current_city=city_key,
                        current_district=district_name,
                        current_dong=dong_name
                    ))

    # 3. sitemap.xml 생성
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap_content += f"  <url><loc>{url}</loc><priority>0.8</priority></url>\n"
    sitemap_content += "</urlset>"
    with open("dist/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    print(f"✓ sitemap.xml 생성 완료 (총 {len(sitemap_urls)}개 URL)")

    # 4. robots.txt 생성
    with open("dist/robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_ORIGIN}/sitemap.xml\n")
    print("✓ robots.txt 생성 완료")

    # 5. assets 복사
    if os.path.exists("assets"):
        shutil.copytree("assets", "dist/assets", dirs_exist_ok=True)
        print("✓ assets 폴더 복사 완료")

if __name__ == "__main__":
    main()