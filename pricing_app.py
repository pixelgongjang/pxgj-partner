import streamlit as st
from num2words import num2words

def calculate_settlement(amount, vat_type, payment_method):
    if amount == 0:
        return {"기존 결제금액": "0 원", "최종 결제금액": "0 원", "최종 정산금액": "0 원", "세전 정산액": "0 원", "공급가액": "0 원", "부가세": "0 원", "카드수수료": "0 원", "결제대행료": "0 원", "원천징수액": "0 원", "결제 방법": ""}

    if vat_type == "included":
        supply_amount = round(amount / 1.1)  
        vat = amount - supply_amount
    else:
        supply_amount = amount
        vat = round(amount * 0.1)
        amount += vat  

    card_fee = round(amount * 0.02) + 3300 if payment_method == "card" else 0
    service_fee = round(supply_amount * 0.09)
    pre_tax_settlement = amount - vat - card_fee - service_fee
    withholding_tax = round(pre_tax_settlement * 0.033)
    final_settlement = pre_tax_settlement - withholding_tax

    return {
        "기존 결제금액": f"{amount:,} 원",
        "최종 결제금액": f"{amount:,} 원",
        "최종 정산금액": f"{final_settlement:,} 원",
        "세전 정산액": f"{pre_tax_settlement:,} 원",
        "공급가액": f"{supply_amount:,} 원",
        "부가세": f"{vat:,} 원",
        "카드수수료": f"{card_fee:,} 원",
        "결제대행료": f"{service_fee:,} 원",
        "원천징수액": f"{withholding_tax:,} 원",
        "결제 방법": "💳 카드 결제" if payment_method == "card" else "📄 계산서 발행"
    }

st.set_page_config(page_title="파트너 정산 계산기", layout="centered", initial_sidebar_state="collapsed", page_icon="💰")

# --- 스타일 적용 ---
st.markdown("""
    <style>
        body {background-color: #263238 !important; color: #F5F5F5 !important;}
        .stApp {background-color: #263238 !important;}
        .stButton button {width: 100%; border-radius: 8px; font-size: 16px; padding: 12px; font-weight: bold; transition: 0.3s;
                          background-color: #FF5722; color: white; border: none;}
        .stButton button:hover {background-color: #37474F !important; color: #F5F5F5 !important;}
        .stRadio div[role=radiogroup] {gap: 10px; color: #F5F5F5 !important;}
        .stMarkdown, .stText, .stCaption, .stNumberInput label, .stTable {font-size: 16px; line-height: 1.4; color: #F5F5F5 !important;}
        .stSubheader {font-size: 24px !important; font-weight: bold; margin-bottom: 10px; color: #DC143C;}
        .stMarkdown h3 {font-size: 20px !important; font-weight: 700;}
        .stNumberInput input {border: 2px solid #F5F5F5; border-radius: 5px; padding: 8px; width: 100%; color: #FFFFFF !important;}
        .stContainer {padding: 20px; background: #37474F; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2);}
        .stTable {border: 1px solid #F5F5F5 !important;}
        hr {border: 1px solid #F5F5F5 !important;}
        .highlight {font-size: 24px; font-weight: bold; color: #FFC107 !important;} /* 노란색 강조 */
        .small-text {font-size: 20px; color: #FFC107 !important;} /* 세전 정산액 */
    </style>
    """, unsafe_allow_html=True)

# 🔹 로고 이미지 추가 (크기 조정하여 50% 축소)
st.image("https://cdn.imweb.me/upload/S202503127b0bff1a15646/4ba6f0afeb76b.png", width=150)

st.title("💰 파트너 정산 계산기")

amount = st.number_input("💰 결제금액을 입력하세요:", min_value=0, step=10000, format="%d")
st.caption(f"🔢 {amount:,} 원 ({num2words(amount, lang='ko')} 원)")

vat_type = st.radio("💡 부가세 포함 여부:", ["included", "excluded"], format_func=lambda x: "✅ 포함 (10%)" if x == "included" else "❌ 미포함 (10% 추가됨)")
payment_method = st.radio("💳 결제 방식 선택:", ["card", "invoice"], format_func=lambda x: "💳 카드 결제" if x == "card" else "📄 계산서 발행")

if st.button("🔍 정산 계산"):
    result = calculate_settlement(amount, vat_type, payment_method)

    if amount == 0:
        st.warning("🚨 결제금액이 0원이므로 정산 내역이 없습니다.")
    elif vat_type == "excluded":
        st.warning("⚠️ 입력된 결제금액에는 부가세가 포함되지 않았습니다. 최종 결제금액이 자동으로 조정되었습니다.")

    st.subheader("✅ 정산 내역")
    
    # 🔹 최종 결제금액 & 최종 정산금액을 강조 색상으로 변경
    st.markdown(f"### 💰 최종 결제금액: <span class='highlight'>{result['최종 결제금액']}</span>", unsafe_allow_html=True)
    st.markdown(f"### 📌  최종 정산금액: <span class='highlight'>{result['최종 정산금액']}</span>", unsafe_allow_html=True)

    data = {
        "구분": ["공급가액", "부가세", "카드수수료", "결제대행료", "원천징수액"],
        "금액": [result["공급가액"], result["부가세"], result["카드수수료"], result["결제대행료"], result["원천징수액"]]
    }
    st.table(data)

    # 🔹 세전 정산액 강조
    st.markdown(f"<p class='small-text'>세전 정산액: {result['세전 정산액']}</p>", unsafe_allow_html=True)

    if st.button("🔝 처음으로"):
        st.experimental_rerun()
