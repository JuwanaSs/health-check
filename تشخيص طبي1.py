import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# دالة حفظ النتائج في ملف نصي
def save_results_to_file(result_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="احفظ نتيجة الفحص")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("نتيجة الفحص الصحي:\n\n")
            file.write(result_text)

# دالة عرض نافذة النتائج مع الرسم البياني
def show_results_window(result_text, data_dict):
    result_window = ctk.CTkToplevel()
    result_window.title("نتيجة الفحص الصحي")
    result_window.geometry("580x700")

    title = ctk.CTkLabel(result_window, text="نتائج الفحص الصحي", font=("Arial", 22, "bold"))
    title.pack(pady=10)

    result_box = ctk.CTkLabel(result_window, text=result_text, font=("Arial", 14), wraplength=500, justify="right")
    result_box.pack(pady=10, padx=20)

    # الرسم البياني
    figure = plt.Figure(figsize=(5, 3.3), dpi=100)
    ax = figure.add_subplot(111)

    categories = list(data_dict.keys())
    values = list(data_dict.values())
    ideal = [22, 8, 7, 6, 3]  # ideal values for BMI, sleep, water, activity, meals

    x = np.arange(len(categories))
    ax.bar(x - 0.2, values, width=0.4, label='قيمك')
    ax.bar(x + 0.2, ideal, width=0.4, label='المثالي')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=15, ha='right')
    ax.set_ylabel("القيم")
    ax.set_title("مقارنة بين قيمك والقيم المثالية")
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    canvas = FigureCanvasTkAgg(figure, master=result_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    button_frame = ctk.CTkFrame(result_window)
    button_frame.pack(pady=10)

    save_button = ctk.CTkButton(button_frame, text="💾 حفظ النتيجة كملف", command=lambda: save_results_to_file(result_text))
    save_button.pack(pady=6)

    close_button = ctk.CTkButton(button_frame, text="إغلاق النافذة", command=result_window.destroy)
    close_button.pack(pady=6)

# دالة التحليل

def analyze():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — وزنك أقل من الطبيعي.\n💡 نصيحة: زد السعرات بتوازن وركّز على البروتينات."
        elif 18.5 <= bmi < 25:
            bmi_result = f"✅ مؤشر كتلة الجسم: {bmi:.1f} — وزنك طبيعي.\n😊 استمر على نمطك الصحي."
        elif 25 <= bmi < 30:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — زيادة في الوزن.\n💡 قلل السعرات وابدأ مشي يومي."
        else:
            bmi_result = f"⚠️ مؤشر كتلة الجسم: {bmi:.1f} — سمنة مفرطة.\n💡 استشر أخصائي وابدأ نظام غذائي."

        sleep_hours = float(sleep_entry.get())
        if sleep_hours < 6:
            sleep_result = "⚠️ نومك أقل من الطبيعي.\n💡 حاول النوم بين 7-8 ساعات لتحسين الصحة العامة."
        elif 6 <= sleep_hours <= 9:
            sleep_result = "✅ عدد ساعات النوم جيد.\n😊 حافظ على انتظام النوم."
        else:
            sleep_result = "⚠️ نومك أطول من المعتاد.\n💡 حاول النوم باعتدال 7-9 ساعات."

        water = int(water_entry.get())
        if water < 5:
            water_result = "⚠️ شرب الماء قليل.\n💡 حاول شرب 6 إلى 8 أكواب يوميًا."
        elif 5 <= water <= 8:
            water_result = "✅ معدل شرب الماء جيد.\n😊 استمر على هذا المستوى."
        else:
            water_result = "👍 شربك للماء ممتاز.\n💡 حافظ عليه ووازن مع الإلكتروليتات."

        meals = int(meals_entry.get())
        if meals < 2:
            meals_result = "⚠️ عدد وجباتك قليل جدًا.\n💡 حاول تناول 3 وجبات يوميًا."
        elif 2 <= meals <= 3:
            meals_result = "✅ عدد الوجبات مناسب.\n😊 حافظ على التوازن."
        else:
            meals_result = "⚠️ عدد الوجبات مرتفع.\n💡 تأكد أن تكون الوجبات خفيفة ومتوازنة."

        level = activity_option.get()
        if level == "منخفض - أقل من 20 دقيقة يوميًا":
            activity_minutes = 10
        elif level == "متوسط - 30 إلى 60 دقيقة":
            activity_minutes = 45
        else:
            activity_minutes = 75

        if activity_minutes < 20:
            activity_result = "⚠️ نشاطك البدني منخفض.\n💡 ابدأ بمشي خفيف 20-30 دقيقة يوميًا."
        elif 20 <= activity_minutes <= 60:
            activity_result = "✅ نشاطك مناسب.\n😊 استمر في ممارسة الرياضة."
        else:
            activity_result = "⚠️ نشاطك عالي جدًا.\n💡 تأكد من الراحة الكافية والتغذية."

        result = "\n\n".join([bmi_result, sleep_result, activity_result, water_result, meals_result])

        # البيانات للرسم البياني
        data_for_chart = {
            "BMI": round(bmi, 1),
            "النوم (س)": sleep_hours,
            "الماء (أكواب)": water,
            "النشاط (د)": activity_minutes / 15,  # تحويل لدلالة عددية
            "الوجبات": meals
        }

        show_results_window(result, data_for_chart)

    except ValueError:
        result_label.configure(text="❌ تأكد من إدخال البيانات بشكل صحيح.", text_color="red")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("نموذج الفحص الصحي")
app.geometry("460x780")

title_label = ctk.CTkLabel(app, text="الفحص الصحي الشامل", font=("Arial", 24, "bold"))
title_label.pack(pady=20)

form_frame = ctk.CTkFrame(app, corner_radius=20)
form_frame.pack(pady=10, padx=20, fill="both", expand=True)

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

activity_option = ctk.CTkOptionMenu(
    form_frame,
    values=["منخفض - أقل من 20 دقيقة يوميًا", "متوسط - 30 إلى 60 دقيقة", "مرتفع - أكثر من 60 دقيقة"]
)
activity_option.set("اختر مستوى النشاط")
activity_option.pack(pady=10, padx=20)

analyze_button = ctk.CTkButton(app, text="تحليل الفحص الصحي", command=analyze, font=("Arial", 16, "bold"))
analyze_button.pack(pady=20)

result_label = ctk.CTkLabel(app, text="", font=("Arial", 14), wraplength=420, justify="right")
result_label.pack(pady=10)

app.mainloop()

