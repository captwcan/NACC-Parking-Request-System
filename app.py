import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 1. ข้อมูลตั้งต้น (Pre-defined Data Variables)
# ==========================================
nacc_departments = [
    "สำนักกิจการคณะกรรมการ ป.ป.ช.", "สำนักการประชุม", "สำนักบริหารงานกลาง", 
    "สำนักตรวจสอบภายใน", "สำนักตรวจราชการ", "สำนักสืบสวนและกิจการพิเศษ", 
    "สำนักไต่สวนคดีพิเศษ", "กลุ่มที่ปรึกษาสำนักงาน ป.ป.ช.", 
    "สำนักพัฒนาวิชาการด้านการศึกษาและกระบวนการมีส่วนร่วมต้านทุจริต",
    "สำนักประเมินคุณธรรม ความโปร่งใส และส่งเสริมธรรมาภิบาล",
    "สำนักมาตรการป้องกันการทุจริต", "สำนักป้องกันการขัดกันแห่งผลประโยชน์และกำกับจริยธรรมภาครัฐ",
    "สำนักพัฒนาระบบตรวจสอบทรัพย์สิน", "สำนักตรวจสอบทรัพย์สินภาคการเมือง",
    "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๑", "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๒",
    "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๓", "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๔",
    "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๕", "สำนักตรวจสอบทรัพย์สินภาครัฐและรัฐวิสาหกิจ ๖",
    "สำนักไต่สวนการทุจริตคดีการเมืองการปกครอง ๑", "สำนักไต่สวนการทุจริตคดีการเมืองการปกครอง ๒",
    "สำนักไต่สวนการทุจริตคดีการเมืองการปกครอง ๓", "สำนักไต่สวนการทุจริตคดีเศรษฐกิจ ๑",
    "สำนักไต่สวนการทุจริตคดีเศรษฐกิจ ๒", "สำนักไต่สวนการทุจริตคดีเศรษฐกิจ ๓",
    "สำนักไต่สวนการทุจริตคดีของหน่วยงานที่ขึ้นตรงต่อนายกรัฐมนตรี",
    "สำนักไต่สวนการทุจริตคดีความมั่นคงของรัฐ",
    "สำนักไต่สวนการทุจริตคดีความมั่นคงด้านทรัพยากรธรรมชาติและสิ่งแวดล้อม",
    "สำนักกฎหมาย", "สำนักพัฒนาระบบกฎหมาย", "สำนักพันธกรณีและความร่วมมือระหว่างประเทศ",
    "สำนักคดี ๑", "สำนักคดี ๒", "สำนักคดี ๓",
    "สำนักยุทธศาสตร์ด้านการป้องกันและปราบปรามการทุจริต",
    "สำนักวิเคราะห์แผนและงบประมาณ", "สำนักบริหารงานคลัง", "สำนักบริหารทรัพย์สิน",
    "สำนักสื่อสารองค์กร", "สำนักบริหารทรัพยากรบุคคล",
    "สถาบันการป้องกันและปราบปรามการทุจริตแห่งชาติ สัญญา ธรรมศักดิ์",
    "สำนักวิจัยและบริการวิชาการด้านการป้องกันและปราบปรามการทุจริต",
    "สำนักเทคโนโลยีสารสนเทศ", "สำนักนวัตกรรม เทคโนโลยี และภูมิสารสนเทศ"
]

parking_spots = [
    "ข้างอาคาร 1 ฝั่งกองสลาก", "ข้างอาคาร 1 ฝั่ง ATM", "หน้าอาคาร 3", "หน้าอาคาร 2", "บริเวณอาคารสถาบันฯ",
    "หน้าอาคาร 4", "ชั้นใต้ดินอาคาร 4", "อาคาร 4", "อาคาร 7", "อาคาร 8", "อื่นๆ (ระบุเพิ่มเติม)"
]

security_officers = [
    "นายธวัชชัย สุขศิริผล", "นายถิรายุ สมานสินธุ์", "นายวันพิทักษ์ วงค์มูล", 
    "นายทรงพล เล็กพูนศักดิ์", "ร.ต.อ. วรดร ใสสุชล", "นายปริวรรตน์ จารุเศวตรัศมี", 
    "นายไกรฤทธิ์ ศรีสูงเนิน", "นายวีรพจน์ สรรพากิจวัฒนา", "นางสาวปาณิชา ใจมุข", 
    "นางสาวพลชา กองจันทร์", "นายณัฐนันท์ อำม์พรพันธ์", "นายกมลนัทธ์ ศักดิ์สุวรรณ", 
    "นายกฤตภาส เอี่ยมศรี"
]

# ==========================================
# 2. ตั้งค่าหน้าเพจและเชื่อมต่อ Database
# ==========================================
st.set_page_config(page_title="ระบบขอที่จอดรถ ป.ป.ช.", page_icon="📝", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันดึงข้อมูลจาก Google Sheets
@st.cache_data(ttl=5) # Cache data for 5 seconds to prevent spamming API
def get_data():
    try:
        df = conn.read(worksheet="ชีต1")
        # สร้าง DataFrame ว่างถ้า Sheet ว่างเปล่า
        if df.empty or 'เลขหนังสือ' not in df.columns:
            return pd.DataFrame(columns=[
                "วันที่รับเรื่อง", "สำนัก", "เลขหนังสือ", "วันที่จอด", 
                "เวลาที่จอด", "จำนวนรถ", "อาคารที่จอด", "เจ้าหน้าที่ผู้รับเรื่อง"
            ])
        return df
    except Exception:
        # กรณี Sheet ไม่มีอยู่ หรืออ่านไม่ได้
        return pd.DataFrame(columns=[
            "วันที่รับเรื่อง", "สำนัก", "เลขหนังสือ", "วันที่จอด", 
            "เวลาที่จอด", "จำนวนรถ", "อาคารที่จอด", "เจ้าหน้าที่ผู้รับเรื่อง"
        ])

if 'last_saved_doc' not in st.session_state:
    st.session_state.last_saved_doc = None

st.title("📝 ระบบรวบรวมข้อมูลการขอที่จอดรถ สำนักงาน ป.ป.ช.")
st.markdown("---")

# ==========================================
# 3. ส่วนรับข้อมูล (Input Form)
# ==========================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📋 ข้อมูลการรับเรื่อง")
    receive_date = st.date_input("วันที่รับเรื่อง", value=date.today(), format="DD/MM/YYYY")
    department = st.selectbox("สำนัก", options=nacc_departments)
    doc_number = st.text_input("เลขหนังสือ (ห้ามซ้ำ)")
    officer = st.selectbox("เจ้าหน้าที่ผู้รับเรื่อง", options=security_officers)

with col_right:
    st.subheader("🚗 รายละเอียดการขอที่จอด")
    parking_date = st.date_input("วันที่จอด", value=date.today(), format="DD/MM/YYYY")
    parking_time = st.text_input("เวลาที่จอด (เช่น 08.30 น.)")
    car_count = st.number_input("จำนวนรถ", min_value=1, step=1)
    parking_spot = st.selectbox("อาคารที่จอด", options=parking_spots)
    
    # เงื่อนไขเมื่อเลือกจุดจอดอื่นๆ
    parking_spot_other = ""
    if parking_spot == "อื่นๆ (ระบุเพิ่มเติม)":
        parking_spot_other = st.text_input("ระบุจุดจอดอื่นๆ (โปรดระบุ)")

# ==========================================
# 4. ปุ่มบันทึกและปุ่มยกเลิก
# ==========================================
btn_col1, btn_col2 = st.columns([4, 1])

with btn_col1:
    if st.button("💾 บันทึกข้อมูล", use_container_width=True):
        # 4.1 ตรวจสอบความครบถ้วนของข้อมูล
        if not doc_number.strip():
            st.error("❌ กรุณาระบุเลขหนังสือ")
        elif parking_spot == "อื่นๆ (ระบุเพิ่มเติม)" and not parking_spot_other.strip():
            st.error("❌ กรุณาระบุจุดจอดอื่นๆ")
        else:
            final_parking_spot = parking_spot_other if parking_spot == "อื่นๆ (ระบุเพิ่มเติม)" else parking_spot
            df = get_data()
            
            # 4.2 ตรวจสอบเลขหนังสือซ้ำ (Duplicate Check)
            if not df.empty and doc_number in df['เลขหนังสือ'].astype(str).values:
                st.error(f"❌ มีเลขหนังสือ {doc_number} ในระบบแล้ว ไม่สามารถบันทึกซ้ำได้")
            else:
                # 4.3 เตรียมข้อมูลใหม่
                new_row = pd.DataFrame([{
                    "วันที่รับเรื่อง": receive_date.strftime("%d/%m/%Y"),
                    "สำนัก": department,
                    "เลขหนังสือ": doc_number,
                    "วันที่จอด": parking_date.strftime("%d/%m/%Y"),
                    "เวลาที่จอด": parking_time,
                    "จำนวนรถ": int(car_count),
                    "อาคารที่จอด": final_parking_spot,
                    "เจ้าหน้าที่ผู้รับเรื่อง": officer
                }])
                
                # นำข้อมูลใหม่ไปต่อท้ายข้อมูลเดิม
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # อัปเดตลง Google Sheets
                conn.update(worksheet="ชีต1", data=updated_df)
                
                # ล้าง Cache เพื่อให้ดึงข้อมูลล่าสุด และเก็บ Session ว่าเพิ่งบันทึกรายการอะไรไป
                get_data.clear()
                st.session_state.last_saved_doc = doc_number
                st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว!")
                st.rerun()

with btn_col2:
    # 4.4 ระบบยกเลิกรายการล่าสุด (Undo Action)
    if st.session_state.last_saved_doc:
        if st.button("🗑️ ยกเลิกรายการล่าสุด", use_container_width=True):
            df = get_data()
            if not df.empty:
                # กรองเอาเลขหนังสือที่ตรงกับอันล่าสุดออก
                updated_df = df[df['เลขหนังสือ'].astype(str) != str(st.session_state.last_saved_doc)]
                
                # อัปเดตตารางกลับไปที่ Google Sheets
                conn.update(worksheet="ชีต1", data=updated_df)
                get_data.clear()
                
                # ลบ Session การจำเลขหนังสือล่าสุดทิ้ง
                st.session_state.last_saved_doc = None
                st.success("🗑️ ยกเลิกรายการล่าสุดสำเร็จ!")
                st.rerun()

st.markdown("---")

# ==========================================
# 5. ฟังก์ชันสรุปยอดรถรายวัน
# ==========================================
st.subheader("📊 ฟังก์ชันสรุปยอดรวมจำนวนรถขอเข้าจอดวันนี้ (แยกตามสำนัก)")

df_display = get_data()
today_str = date.today().strftime("%d/%m/%Y")

if not df_display.empty:
    df_display['วันที่จอด'] = df_display['วันที่จอด'].astype(str)
    # คัดกรองจาก วันที่จอด == วันปัจจุบัน
    today_parking = df_display[df_display['วันที่จอด'] == today_str]
    
    if not today_parking.empty:
        # แปลงจำนวนรถเป็นตัวเลขเพื่อคำนวณ
        today_parking['จำนวนรถ'] = pd.to_numeric(today_parking['จำนวนรถ'], errors='coerce').fillna(0)
        # จัดกลุ่มและรวมยอด
        summary_df = today_parking.groupby('สำนัก')['จำนวนรถ'].sum().reset_index()
        summary_df.columns = ['สำนัก', 'รวมจำนวนรถ (คัน)']
        
        # แสดงผล
        st.dataframe(summary_df, use_container_width=True)
        
        # ยอดรวมทั้งหมดของวันนี้
        total_cars = int(summary_df['รวมจำนวนรถ (คัน)'].sum())
        st.info(f"**ยอดรวมจำนวนรถขอเข้าจอดวันนี้ทั้งหมด: {total_cars} คัน**")
    else:
        st.info("ยังไม่มีการขอเข้าจอดสำหรับวันที่จอดในวันนี้")
else:
    st.info("ยังไม่มีข้อมูลในระบบ")

st.markdown("---")

# ==========================================
# 6. ตารางรายละเอียดรายวัน (Data Visibility)
# ==========================================
st.subheader("📋 รายละเอียดรายการคำขอที่รับเรื่องในวันนี้")

if not df_display.empty:
    df_display['วันที่รับเรื่อง'] = df_display['วันที่รับเรื่อง'].astype(str)
    # คัดกรองจาก วันที่รับเรื่อง == วันปัจจุบัน
    today_records = df_display[df_display['วันที่รับเรื่อง'] == today_str]
    
    if not today_records.empty:
        st.dataframe(today_records, use_container_width=True)
    else:
        st.info("ไม่มีรายการคำขอที่รับเรื่องในวันนี้")
else:
    st.info("ยังไม่มีข้อมูลในระบบ")
