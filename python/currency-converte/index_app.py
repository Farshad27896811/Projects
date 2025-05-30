# currency_converter_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import requests

# نگاشت کد ارز به نام فارسی
CURRENCY_NAMES_FA = {
    "USD": "دلار آمریکا",
    "EUR": "یورو",
    "GBP": "پوند انگلیس",
    "JPY": "ین ژاپن",
    "CAD": "دلار کانادا",
    "AUD": "دلار استرالیا",
    "CHF": "فرانک سوئیس",
    "CNY": "یوان چین",
    "IRR": "ریال ایران"
}

# تابع گرفتن نرخ از Frankfurter API
SUPPORTED_CURRENCIES = []

def fetch_supported_currencies():
    global SUPPORTED_CURRENCIES
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        if response.status_code == 200:
            SUPPORTED_CURRENCIES = list(response.json().keys())
    except:
        SUPPORTED_CURRENCIES = list(CURRENCY_NAMES_FA.keys())


def fetch_conversion_rate(base, target):
    if base.upper() not in SUPPORTED_CURRENCIES or target.upper() not in SUPPORTED_CURRENCIES:
        raise ValueError("کد ارز نامعتبر یا پشتیبانی‌نشده است.")
    url = f"https://api.frankfurter.app/latest?from={base.upper()}&to={target.upper()}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'rates' in data and target.upper() in data['rates']:
            return data['rates'][target.upper()]
        else:
            raise ValueError("کد ارز نامعتبر است.")
    except requests.RequestException:
        raise ConnectionError("خطا در اتصال به API")

# تابع تبدیل ارز
def convert():
    try:
        amount = float(entry_amount.get())
        base = combo_base.get()
        target = combo_target.get()

        if not base or not target:
            raise ValueError("لطفاً ارز مبدا و مقصد را انتخاب کنید.")

        rate = fetch_conversion_rate(base, target)
        result = amount * rate
        base_name = CURRENCY_NAMES_FA.get(base, base)
        target_name = CURRENCY_NAMES_FA.get(target, target)
        lbl_result.config(
            text=f"{amount:.2f} {base} ({base_name}) = {result:.2f} {target} ({target_name})\nنرخ تبدیل: {rate:.4f}"
        )
    except ValueError as ve:
        messagebox.showerror("خطا", str(ve))
    except ConnectionError as ce:
        messagebox.showerror("خطا", str(ce))

# ساخت رابط گرافیکی
fetch_supported_currencies()

root = tk.Tk()
root.title("مبدل ارز پیشرفته")
root.geometry("500x360")
root.resizable(False, False)
root.configure(bg="#f0f4f7")

CURRENCIES = SUPPORTED_CURRENCIES.copy()
if "IRR" not in CURRENCIES:
    CURRENCIES.append("IRR")  # اضافه فقط برای نمایش در لیست در صورتی که Frankfurter پشتیبانی نمی‌کند

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Vazir", 12), padding=6)
style.configure("TCombobox", padding=5, font=("Vazir", 11))

lbl_title = tk.Label(root, text="مبدل ارز آنلاین", font=("Vazir", 18, "bold"), bg="#f0f4f7", fg="#2c3e50")
lbl_title.pack(pady=15)

frame = tk.Frame(root, bg="#f0f4f7")
frame.pack(pady=10)

entry_amount = tk.Entry(frame, width=10, font=("Vazir", 14), justify='center')
entry_amount.grid(row=0, column=0, padx=5)

combo_base = ttk.Combobox(frame, values=CURRENCIES, width=7, font=("Vazir", 12))
combo_base.grid(row=0, column=1, padx=5)
combo_base.set("USD")

combo_target = ttk.Combobox(frame, values=CURRENCIES, width=7, font=("Vazir", 12))
combo_target.grid(row=0, column=2, padx=5)
combo_target.set("EUR")

btn_convert = ttk.Button(root, text="تبدیل", command=convert)
btn_convert.pack(pady=15)

lbl_result = tk.Label(root, text="", font=("Vazir", 14), fg="#27ae60", bg="#f0f4f7")
lbl_result.pack(pady=10)

footer = tk.Label(root, text="استفاده از API رایگان Frankfurter", font=("Vazir", 9), bg="#f0f4f7", fg="#7f8c8d")
footer.pack(side="bottom", pady=10)

root.mainloop()