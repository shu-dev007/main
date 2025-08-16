from datetime import datetime, timedelta
import lunardate
import os

def generate_lunar_events(year_start, year_end):
    """
    指定した期間の旧暦1日と15日の新暦日付リストを生成
    """
    events = []
    for year in range(year_start, year_end + 1):
        for month in range(1, 13):
            for lunar_day in [1, 15]:
                try:
                    d = lunardate.LunarDate(year, month, lunar_day).toSolarDate()
                    events.append(d)
                except ValueError:
                    # 存在しない日付（閏月など）はスキップ
                    pass
    return events

def create_ics(dates):
    """
    日付リストからICSファイルを生成
    イベント名は「ウチャトー」、通知は当日7:00に設定
    出力先は固定
    """
    filename = "/Users/shu/vscode/main/Python/lunar calendar_1_15/lunar_uchato.ics"

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    header = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n"
    footer = "END:VCALENDAR"
    events_str = ""

    for d in dates:
        dtstart = datetime(d.year, d.month, d.day, 7, 0, 0)  # 当日7:00
        dt_str = dtstart.strftime("%Y%m%dT%H%M%S")
        events_str += (
            "BEGIN:VEVENT\n"
            f"DTSTART:{dt_str}\n"
            "SUMMARY:ウチャトー\n"
            "BEGIN:VALARM\n"
            "TRIGGER:-PT0H\n"
            "ACTION:DISPLAY\n"
            "DESCRIPTION:ウチャトー\n"
            "END:VALARM\n"
            "END:VEVENT\n"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + events_str + footer)

if __name__ == "__main__":
    # 生成期間を指定
    dates = generate_lunar_events(2025, 2030)
    create_ics(dates)
    print("lunar_uchato.ics を作成しました（通知：当日7:00）。")