import pandas as pd
import os
from datetime import datetime


class FinanceTracker:
    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        self.categories = [
            "飲食",
            "交通",
            "娛樂",
            "購物",
            "房租",
            "水電",
            "教育",
            "醫療",
            "其他",
        ]
        self.init_file()

    def init_file(self):
        """初始化CSV檔案，如果不存在就建立"""
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=["日期", "類別", "金額", "備註"])
            df.to_csv(self.filename, index=False, encoding="utf-8-sig")
            print(f"已建立新的記帳檔案: {self.filename}")

    def add_expense(self):
        """新增一筆支出"""
        print("\n=== 新增支出 ===")

        # 取得使用者輸入
        date = input("請輸入日期 (YYYY-MM-DD，直接Enter使用今天): ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # 顯示類別選項
        print("\n可選類別:")
        for i, category in enumerate(self.categories, 1):
            print(f"{i}. {category}")

        try:
            category_choice = int(input("請選擇類別 (輸入數字): ")) - 1
            category = self.categories[category_choice]
        except (ValueError, IndexError):
            print("無效的選擇，使用預設類別: 其他")
            category = "其他"

        try:
            amount = float(input("請輸入金額: "))
        except ValueError:
            print("無效的金額，請重新開始")
            return

        note = input("請輸入備註 (可選): ").strip()

        # 建立新記錄
        new_expense = {"日期": date, "類別": category, "金額": amount, "備註": note}

        # 添加到CSV檔案
        df = pd.read_csv(self.filename)
        df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
        df.to_csv(self.filename, index=False, encoding="utf-8-sig")

        print(f"✓ 已成功記錄: {date} | {category} | ${amount} | {note}")

    def view_expenses(self):
        """查看所有支出記錄"""
        try:
            df = pd.read_csv(self.filename)
            if df.empty:
                print("目前沒有任何支出記錄")
                return

            print("\n=== 所有支出記錄 ===")
            print(df.to_string(index=False))

            # 顯示總花費
            total = df["金額"].sum()
            print(f"\n總花費: ${total:.2f}")

        except FileNotFoundError:
            print("找不到記帳檔案，請先新增一筆支出")

    def show_summary(self):
        """顯示簡單摘要"""
        try:
            df = pd.read_csv(self.filename)
            if df.empty:
                print("目前沒有任何支出記錄")
                return

            print("\n=== 支出摘要 ===")
            category_sum = df.groupby("類別")["金額"].sum()

            for category, amount in category_sum.items():
                print(f"{category}: ${amount:.2f}")

            total = df["金額"].sum()
            print(f"\n總花費: ${total:.2f}")

        except FileNotFoundError:
            print("找不到記帳檔案")


def main():
    tracker = FinanceTracker()

    while True:
        print("\n=== 個人記帳系統 ===")
        print("1. 新增支出")
        print("2. 查看所有記錄")
        print("3. 顯示摘要")
        print("4. 生成分析圖表")
        print("5. 退出")

        choice = input("請選擇功能 (1-5): ").strip()

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.show_summary()
        elif choice == "4":
            # 調用分析程式
            try:
                from finance_analysis import generate_charts

                generate_charts()
            except ImportError:
                print("請確保 finance_analysis.py 在同一目錄下")
        elif choice == "5":
            print("感謝使用個人記帳系統！")
            break
        else:
            print("無效的選擇，請輸入 1-5")


if __name__ == "__main__":
    main()
