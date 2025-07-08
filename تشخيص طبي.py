# health_check_gui_advanced.py

import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageTk

# دالة حفظ النتائج

def save_results_to_file(result_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="احفظ نتيجة الفحص")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("نتيجة الفحص الصحي:\n\n")
            file.write(result_text)

# دالة إنشاء رسم بياني بسيط للمخاطر

def create_risk_chart(risks):
    fig, ax = plt.subplots(figsize=(4.5, 2.2))
    labels = [r[0] for r in risks]
    values = [r[1] for r in risks]
    bars = ax.barh(labels, values, color=["#f39c12" if v > 0 else "#2ecc71" for v in values])
    ax.set_xlim(0, 1)
    ax.set_title("مؤشرات المخاطر الصحية")
    ax.axis('off')

    for bar, value in zip(bars, values):
        ax.text(value + 0.01, bar.get_y() + bar.get_height()/2, f"{int(value*100)}%", va='center')

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# نافذة عرض النتائج

def show_results_window(result_text, risk_data):
    result_window = ctk.CTkToplevel()
    result_window.title("نتائج الفحص الصحي")
    result_window.geometry("550x750")

    title = ctk.CTkLabel(result_window, text="نتائج الفحص الصحي الشامل", font=("Arial", 22, "bold"))
    title.pack(pady=15)

    result_box = ctk.CTkTextbox(result_window, font=("Arial", 14), wrap="word", height=380)
    result_box.insert("1.0", result_text)
    result_box.configure(state="disabled")
    result_box.pack(pady=10, padx=20, fill="both", expand=False)

    # عرض الرسم البياني
    chart_img = create_risk_chart(risk_data)
    chart_photo = ImageTk.PhotoImage(chart_img)
    img_label = ctk.CTkLabel(result_window, image=chart_photo, text="")
    img_label.image = chart_photo  # keep reference
    img_label.pack(pady=10)

    button_frame = ctk.CTkFrame(result_window)
    button_frame.pack(pady=15)

    save_button = ctk.CTkButton(button_frame, text="💾 حفظ النتيجة", command=lambda: save_results_to_file(result_text))
    save_button.pack(pady=6)

    close_button = ctk.CTkButton(button_frame, text="إغلاق النافذة", command=result_window.destroy)
    close_button.pack(pady=6)

# التحليل

def analyze():
    try:
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        sleep_hours = float(sleep_entry.get())
        water = int(water_entry.get())
        meals = int(meals_entry.get())

        level = activity_option.get()
        if level == "منخفض - أقل من 20 دقيقة يوميًا":
            activity_minutes = 10
        elif level == "متوسط - 30 إلى 60 دقيقة":
            activity_minutes = 40
        else:
            activity_minutes = 75

        # تحليل BMI
        if bmi < 18.5:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — وزنك أقل من الطبيعي.\n💡 زد السعرات وركّز على البروتينات."
        elif 18.5 <= bmi < 25:
            bmi_result = f"✅ مؤشر كتلة الجسم: {bmi:.1f} — وزنك طبيعي.\n😊 استمر على نمطك الصحي."
        elif 25 <= bmi < 30:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — زيادة في الوزن.\n💡 قلل السعرات وابدأ مشي يومي."
        else:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — سمنة مفرطة.\n💡 استشر أخصائي وابدأ برنامج صحي."

        # تحليل النوم
        if sleep_hours < 6:
            sleep_result = "⚠️ نومك أقل من الطبيعي.\n💡 حاول النوم بين 7-8 ساعات."
        elif 6 <= sleep_hours <= 9:
            sleep_result = "✅ عدد ساعات النوم جيد.\n😊 حافظ على انتظام النوم."
        else:
            sleep_result = "⚠️ نومك أطول من المعتاد.\n💡 توازن النوم ضروري للصحة العامة."

        # تحليل النشاط
        if activity_minutes < 20:
            activity_result = "⚠️ نشاطك البدني منخفض.\n💡 ابدأ بالمشي 20-30 دقيقة يوميًا."
        elif 20 <= activity_minutes <= 60:
            activity_result = "✅ نشاطك مناسب.\n😊 استمر بممارسة الرياضة."
        else:
            activity_result = "🔁 نشاطك مرتفع جدًا.\n💡 تأكد من الراحة الكافية."

        # شرب الماء
        if water < 5:
            water_result = "⚠️ شرب الماء قليل.\n💡 اشرب 6-8 أكواب يوميًا."
        elif 5 <= water <= 8:
            water_result = "✅ شربك للماء جيد.\n😊 استمر عليه."
        else:
            water_result = "👍 شربك ممتاز.\n💡 وازن مع الإلكتروليتات."

        # عدد الوجبات
        if meals < 2:
            meals_result = "⚠️ عدد وجباتك قليل جدًا.\n💡 تناول 3 وجبات متوازنة."
        elif 2 <= meals <= 3:
            meals_result = "✅ عدد الوجبات مناسب.\n😊 حافظ على توازنها."
        else:
            meals_result = "⚠️ عدد الوجبات مرتفع.\n💡 اجعلها خفيفة ومتوازنة."

        # تحليل المخاطر الصحية
        risk_report = "\n\n🧠 تحليل المخاطر الصحية المحتملة\n"
        risk_data = []

        # تحليل ضغط الدم
        bp_risk = int(bmi > 30 or sleep_hours < 6 or water < 5 or activity_minutes < 20)
        if bp_risk:
            risk_report += "\n⚠️ خطر ارتفاع ضغط الدم.\n💡 قلل وزنك، نم جيدًا واشرب ماء كافٍ."
        risk_data.append(("ضغط الدم", bp_risk))

        # تحليل السكري
        diabetes_risk = int(bmi >= 27 and meals > 3 and activity_minutes < 30)
        if diabetes_risk:
            risk_report += "\n⚠️ خطر الإصابة بالسكري.\n💡 قلل السكر والخبز الأبيض، وزد نشاطك."
        risk_data.append(("السكري النوع 2", diabetes_risk))

        # تحليل الكوليسترول
        chol_risk = int(meals > 3 and activity_minutes < 30 and bmi >= 27)
        if chol_risk:
            risk_report += "\n⚠️ خطر ارتفاع الكوليسترول.\n💡 ابتعد عن الدهون المشبعة ومارس الرياضة."
        risk_data.append(("الكوليسترول", chol_risk))

        # متلازمة الأيض
        metabolic_risk = int(sum([bmi > 27, sleep_hours < 6, meals > 3, activity_minutes < 20]) >= 3)
        if metabolic_risk:
            risk_report += "\n⚠️ احتمال الإصابة بمتلازمة الأيض.\n💡 غيّر نمط حياتك لتجنب مشاكل القلب."
        risk_data.append(("متلازمة الأيض", metabolic_risk))

        # تجميع النتائج
        full_result = "\n\n".join([bmi_result, sleep_result, water_result, meals_result, activity_result]) + risk_report
        show_results_window(full_result, risk_data)

    except ValueError:
        result_label.configure(text="❌ تأكد من إدخال البيانات بشكل صحيح.", text_color="red")

# إعداد الثيم
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("نموذج الفحص الصحي")
app.geometry("520x790")

# العنوان
title_label = ctk.CTkLabel(app, text="نموذج الفحص الصحي الشامل", font=("Arial", 22, "bold"))
title_label.pack(pady=20)

form_frame = ctk.CTkFrame(app, corner_radius=15)
form_frame.pack(pady=10, padx=20, fill="both", expand=True)

# المدخلات
age_entry = ctk.CTkEntry(form_frame, placeholder_text="العمر (بالسنوات)", font=("Arial", 14))
age_entry.pack(pady=8, padx=20)

weight_entry = ctk.CTkEntry(form_frame, placeholder_text="الوزن (كجم)", font=("Arial", 14))
weight_entry.pack(pady=8, padx=20)

height_entry = ctk.CTkEntry(form_frame, placeholder_text="الطول (سم)", font=("Arial", 14))
height_entry.pack(pady=8, padx=20)

sleep_entry = ctk.CTkEntry(form_frame, placeholder_text="عدد ساعات النوم يوميًا", font=("Arial", 14))
sleep_entry.pack(pady=8, padx=20)

water_entry = ctk.CTkEntry(form_frame, placeholder_text="كم كوب ماء تشرب يوميًا؟", font=("Arial", 14))
water_entry.pack(pady=8, padx=20)

meals_entry = ctk.CTkEntry(form_frame, placeholder_text="عدد الوجبات الرئيسية يوميًا", font=("Arial", 14))
meals_entry.pack(pady=8, padx=20)

activity_option = ctk.CTkOptionMenu(form_frame, values=[
    "منخفض - أقل من 20 دقيقة يوميًا",
    "متوسط - 30 إلى 60 دقيقة",
    "مرتفع - أكثر من 60 دقيقة"
])
activity_option.set("اختر مستوى النشاط")
activity_option.pack(pady=10, padx=20)

analyze_button = ctk.CTkButton(app, text="🔎 تحليل الفحص الصحي", command=analyze, font=("Arial", 16, "bold"))
analyze_button.pack(pady=15)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 14), wraplength=440, justify="right")
result_label.pack(pady=10)

app.mainloop()
