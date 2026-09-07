import json
from datetime import datetime, timezone

def generate_ics():
    with open('/Users/akashx/ai-fellowships-timeline/data/fellowships.json', 'r') as f:
        fellowships = json.load(f)

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Fellowships Timeline//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:AI Fellowships Deadlines (UK & USA)",
        "X-WR-TIMEZONE:UTC",
        "X-WR-CALDESC:Comprehensive calendar of upcoming AI Fellowship deadlines in the UK and USA"
    ]

    for f in fellowships:
        iso_date = f.get("deadline_iso", "")
        if not iso_date or "2027-12-31" in iso_date:  # skip rolling placeholders
            continue
        try:
            dt = datetime.strptime(iso_date, "%Y-%m-%d")
            dt_str = dt.strftime("%Y%m%d")
            dt_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            
            summary = f"DEADLINE: {f['name']} ({f['country']})"
            desc = f"Fellowship: {f['name']}\\nHost: {f['organization']}\\nCountry: {f['country']}\\nCategory: {f['category']}\\nDeadline: {f['deadline']}\\nStipend: {f['stipend_funding']}\\nOfficial URL: {f['url']}"
            
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:{f['id']}-{dt_str}@ai-fellowships-timeline",
                f"DTSTAMP:{dt_stamp}",
                f"DTSTART;VALUE=DATE:{dt_str}",
                f"DTEND;VALUE=DATE:{dt_str}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{desc}",
                f"URL:{f['url']}",
                "STATUS:CONFIRMED",
                "TRANSP:TRANSPARENT",
                "END:VEVENT"
            ])
        except Exception as e:
            print(f"Error parsing date for {f['id']}: {e}")

    ics_lines.append("END:VCALENDAR")
    ics_content = "\r\n".join(ics_lines) + "\r\n"

    with open('/Users/akashx/ai-fellowships-timeline/data/fellowships.ics', 'w') as f:
        f.write(ics_content)
    print("Successfully generated /Users/akashx/ai-fellowships-timeline/data/fellowships.ics")

if __name__ == "__main__":
    generate_ics()
