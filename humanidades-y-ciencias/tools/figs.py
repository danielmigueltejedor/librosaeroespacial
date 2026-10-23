"""TikZ generators for figures that are drawn from data given in the chapter file."""

def timeline(events, width=15.0, label_width=3.0):
    """Ordinal timeline: events = [(year_text, label)], equally spaced, labels alternate above/below."""
    n = len(events)
    dx = width / max(n - 1, 1)
    out = [r"\draw[->, thick] (-0.5,0) -- (%.2f,0);" % (width + 0.6)]
    for i, (year, label) in enumerate(events):
        x = i * dx
        up = i % 2 == 0
        sign = 1 if up else -1
        out.append(r"\draw[thick] (%.2f,-0.1) -- (%.2f,0.1);" % (x, x))
        out.append(r"\draw[gray] (%.2f,0) -- (%.2f,%.2f);" % (x, x, sign * 0.55))
        anchor = 'south' if up else 'north'
        out.append(r"\node[anchor=%s, align=center, text width=%.2fcm, font=\scriptsize] at (%.2f,%.2f) {\textbf{%s}\\ %s};" % (anchor, label_width, x, sign * 0.55, year, label))
    return "\n".join(out)
