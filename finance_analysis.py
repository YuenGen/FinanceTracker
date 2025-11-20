import pandas as pd
import matplotlib.pyplot as plt
import os


def set_chinese_font():
    """設定中文字型（根據你的系統調整）"""
    try:
        # macOS
        plt.rcParams["font.sans-serif"] = ["PingFang TC", "Heiti TC"]
        # Windows: plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams["axes.unicode_minus"] = False
        return True
    except:
        return False


def generate_charts():
    """生成分析圖表"""
    if not os.path.exists("expenses.csv"):
        print("找不到支出記錄檔案，請先新增一些支出")
        return

    df = pd.read_csv("expenses.csv")
    if df.empty:
        print("目前沒有任何支出記錄")
        return

    # 設定中文字型
    chinese_available = set_chinese_font()

    # 按類別分組計算總金額
    category_totals = df.groupby("類別")["金額"].sum()

    # 圖表 1: 圓餅圖 - 各類別花費比例
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    colors = [
        "#ff9999",
        "#66b3ff",
        "#99ff99",
        "#ffcc99",
        "#ff99cc",
        "#c2c2f0",
        "#ffb3e6",
        "#c4e17f",
    ]
    wedges, texts, autotexts = plt.pie(
        category_totals.values,
        labels=(
            category_totals.index
            if chinese_available
            else [f"Category {i+1}" for i in range(len(category_totals))]
        ),
        autopct="%1.1f%%",
        colors=colors[: len(category_totals)],
    )

    # 美化文字
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    plt.title("各類別花費比例")

    # 圖表 2: 長條圖 - 各類別總金額
    plt.subplot(1, 2, 2)
    bars = plt.bar(
        range(len(category_totals)),
        category_totals.values,
        color=colors[: len(category_totals)],
    )

    if chinese_available:
        plt.xticks(range(len(category_totals)), category_totals.index, rotation=45)
    else:
        plt.xticks(
            range(len(category_totals)),
            [f"Cat{i+1}" for i in range(len(category_totals))],
            rotation=45,
        )

    plt.title("各類別總金額")
    plt.ylabel("金額 ($)")

    # 在長條圖上顯示金額
    for bar, amount in zip(bars, category_totals.values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(category_totals.values) * 0.01,
            f"${amount:.0f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig("expense_analysis.png", dpi=300, bbox_inches="tight")
    plt.show()

    print("分析圖表已生成並儲存為 'expense_analysis.png'")

    # 顯示統計資訊
    print("\n=== 詳細統計 ===")
    total_spent = df["金額"].sum()
    avg_daily = df.groupby("日期")["金額"].sum().mean()
    most_expensive_category = category_totals.idxmax()

    print(f"總花費: ${total_spent:.2f}")
    print(f"平均每日花費: ${avg_daily:.2f}")
    print(f"花費最多的類別: {most_expensive_category} (${category_totals.max():.2f})")
    print(f"總記錄數: {len(df)} 筆")


if __name__ == "__main__":
    generate_charts()
