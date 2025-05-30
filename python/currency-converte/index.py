# currency_converter.py
import argparse
import requests
import sys
import json
from datetime import datetime
import os
from tabulate import tabulate

# استثناءهای سفارشی
class CurrencyConversionError(Exception):
    pass

class InvalidCurrencyCodeError(CurrencyConversionError):
    pass

class APIConnectionError(CurrencyConversionError):
    pass

# مسیر فایل تاریخچه
HISTORY_FILE = "conversion_history.json"

# گرفتن نرخ تبدیل از API جایگزین (Frankfurter)
def fetch_conversion_rate(base: str, target: str):
    url = f"https://api.frankfurter.app/latest?from={base.upper()}&to={target.upper()}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'rates' in data and target.upper() in data['rates']:
            return data['rates'][target.upper()]
        else:
            raise InvalidCurrencyCodeError("کد ارز نامعتبر است.")
    except requests.RequestException:
        raise APIConnectionError("خطا در اتصال به API")

# محاسبه مقدار تبدیل شده
def convert_currency(amount: float, base: str, target: str):
    rate = fetch_conversion_rate(base, target)
    converted = amount * rate
    return rate, converted

# ذخیره‌سازی تاریخچه
def save_conversion(amount, base, target, rate, result):
    record = {
        "datetime": datetime.now().isoformat(),
        "amount": amount,
        "base": base.upper(),
        "target": target.upper(),
        "rate": rate,
        "result": result
    }

    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []

    history.append(record)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=2, ensure_ascii=False)

# نمایش تاریخچه
def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("هیچ سابقه‌ای برای نمایش وجود ندارد.")
        return

    with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
        try:
            history = json.load(file)
            table = [[item['datetime'], f"{item['amount']} {item['base']}", f"{item['result']:.2f} {item['target']}", item['rate']] for item in history]
            print(tabulate(table, headers=["تاریخ", "مقدار اولیه", "مقدار تبدیل‌شده", "نرخ"], tablefmt="fancy_grid"))
        except json.JSONDecodeError:
            print("خطا در خواندن فایل تاریخچه.")

# لیست نرخ‌های یک ارز پایه
def list_all_rates(base: str):
    url = f"https://api.frankfurter.app/latest?from={base.upper()}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'rates' in data:
            rates = data['rates']
            table = [[k, f"{v:.4f}"] for k, v in sorted(rates.items())]
            print(tabulate(table, headers=["ارز", "نرخ"], tablefmt="fancy_grid"))
        else:
            print("نرخ‌ها یافت نشدند.")
    except requests.RequestException:
        raise APIConnectionError("خطا در اتصال به API")

# تابع اصلی CLI
def main():
    parser = argparse.ArgumentParser(description="مبدل ارز حرفه‌ای با پشتیبانی از API و تاریخچه")
    parser.add_argument("amount", type=float, nargs='?', help="مقدار ارز")
    parser.add_argument("base", type=str, nargs='?', help="کد ارز مبدا")
    parser.add_argument("target", type=str, nargs='?', help="کد ارز مقصد")
    parser.add_argument("--list", type=str, help="نمایش نرخ‌ها نسبت به یک ارز مثلاً --list USD")
    parser.add_argument("--history", action="store_true", help="نمایش تاریخچه تبدیل‌ها")
    args = parser.parse_args()

    try:
        if args.list:
            list_all_rates(args.list)
        elif args.history:
            show_history()
        elif args.amount and args.base and args.target:
            rate, converted = convert_currency(args.amount, args.base, args.target)
            save_conversion(args.amount, args.base, args.target, rate, converted)
            table = [[
                f"{args.amount} {args.base.upper()}",
                f"نرخ تبدیل: {rate:.4f}",
                f"نتیجه: {converted:.2f} {args.target.upper()}"
            ]]
            print(tabulate(table, headers=["مقدار ورودی", "نرخ تبدیل", "مقدار تبدیل‌شده"], tablefmt="grid"))
        else:
            parser.print_help()
    except CurrencyConversionError as e:
        print(f"خطا: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()