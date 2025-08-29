import matplotlib.pyplot as plt


# Initial guess mappings (to be refined by trial and error)
lane_map = {
    0x17: 0,
    0x2F: 1,
    0x47: 2,
    0x5F: 3,
}

event_types = {
    0x00: "tap",
    0x01: "hold",
    0x02: "slide",
}

slide_directions = {
    0x00: "up",
    0x01: "down",
    0x02: "left",
    0x03: "right",
    0x04: "up-left",
    0x05: "up-right",
    0x06: "down-left",
    0x07: "down-right",
}


def parse_chart(raw_bytes: bytes):
    data = list(raw_bytes)
    events = []
    time = 0

    i = 0
    while i < len(data):
        if i + 2 < len(data) and data[i] == 0x00 and data[i+1] == 0x60:
            lane_code = data[i+2]
            lane = lane_map.get(lane_code, None)

            if lane is not None:
                # Try to peek ahead for type/direction
                etype_code = data[i+3] if i+3 < len(data) else None
                etype = event_types.get(etype_code, "unknown")
                direction = None

                if etype == "slide" and i+4 < len(data):
                    dir_code = data[i+4]
                    direction = slide_directions.get(dir_code, f"0x{dir_code:02X}")

                events.append({
                    "time": time,
                    "lane": lane,
                    "etype": etype,
                    "raw": data[i:i+6],
                    "direction": direction
                })

            time += 1
            i += 6  # assume events ~6 bytes for now
        else:
            i += 1

    return events


def plot_chart(events, title="Rhythm Game Chart"):
    colors = {"tap": "blue", "hold": "green", "slide": "red", "unknown": "gray"}

    plt.figure(figsize=(6, 10))

    for e in events:
        c = colors.get(e["etype"], "black")
        plt.scatter(e["lane"], e["time"], color=c, marker="s", s=30)

        if e["etype"] == "slide" and e["direction"]:
            plt.text(e["lane"]+0.1, e["time"], e["direction"], fontsize=6)

    plt.gca().invert_yaxis()
    plt.xticks(range(4))
    plt.xlabel("Lane")
    plt.ylabel("Time (steps)")
    plt.title(title)
    plt.show()
