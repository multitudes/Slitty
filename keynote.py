import sys
import json
import os
import termios
import tty
import time

COLORS = {
    "black": "\033[30m", "red": "\033[31m", "green": "\033[32m",
    "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
    "cyan": "\033[36m", "white": "\033[37m", "reset": "\033[0m"
}

# 5x5 Banner Font
BANNER_GLYPHS = {
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '?': ["▓▓▓▓ ", "    ▓", "  ▓▓ ", "     ", "  ▓  "],
    'A': [" ▓▓▓ ", "▓   ▓", "▓▓▓▓▓", "▓   ▓", "▓   ▓"],
    'B': ["▓▓▓▓ ", "▓   ▓", "▓▓▓▓ ", "▓   ▓", "▓▓▓▓ "],
    'C': [" ▓▓▓▓", "▓    ", "▓    ", "▓    ", " ▓▓▓▓"],
    'D': ["▓▓▓▓ ", "▓   ▓", "▓   ▓", "▓   ▓", "▓▓▓▓ "],
    'E': ["▓▓▓▓▓", "▓    ", "▓▓▓▓ ", "▓    ", "▓▓▓▓▓"],
    'F': ["▓▓▓▓▓", "▓    ", "▓▓▓▓ ", "▓    ", "▓    "],
    'G': [" ▓▓▓▓", "▓    ", "▓  ▓▓", "▓   ▓", " ▓▓▓ "],
    'H': ["▓   ▓", "▓   ▓", "▓▓▓▓▓", "▓   ▓", "▓   ▓"],
    'I': ["▓▓▓▓▓", "  ▓  ", "  ▓  ", "  ▓  ", "▓▓▓▓▓"],
    'J': ["▓▓▓▓▓", "    ▓", "    ▓", "▓   ▓", " ▓▓▓ "],
    'K': ["▓   ▓", "▓  ▓ ", "▓▓▓  ", "▓  ▓ ", "▓   ▓"],
    'L': ["▓    ", "▓    ", "▓    ", "▓    ", "▓▓▓▓▓"],
    'M': ["▓   ▓", "▓▓ ▓▓", "▓ ▓ ▓", "▓   ▓", "▓   ▓"],
    'N': ["▓   ▓", "▓▓  ▓", "▓ ▓ ▓", "▓  ▓▓", "▓   ▓"],
    'O': [" ▓▓▓ ", "▓   ▓", "▓   ▓", "▓   ▓", " ▓▓▓ "],
    'P': ["▓▓▓▓ ", "▓   ▓", "▓▓▓▓ ", "▓    ", "▓    "],
    'Q': [" ▓▓▓ ", "▓   ▓", "▓ ▓ ▓", "▓  ▓ ", " ▓▓ ▓"],
    'R': ["▓▓▓▓ ", "▓   ▓", "▓▓▓▓ ", "▓  ▓ ", "▓   ▓"],
    'S': [" ▓▓▓▓", "▓    ", " ▓▓▓ ", "    ▓", "▓▓▓▓ "],
    'T': ["▓▓▓▓▓", "  ▓  ", "  ▓  ", "  ▓  ", "  ▓  "],
    'U': ["▓   ▓", "▓   ▓", "▓   ▓", "▓   ▓", " ▓▓▓ "],
    'V': ["▓   ▓", "▓   ▓", "▓   ▓", " ▓ ▓ ", "  ▓  "],
    'W': ["▓   ▓", "▓   ▓", "▓ ▓ ▓", "▓▓ ▓▓", "▓   ▓"],
    'X': ["▓   ▓", " ▓ ▓ ", "  ▓  ", " ▓ ▓ ", "▓   ▓"],
    'Y': ["▓   ▓", " ▓ ▓ ", "  ▓  ", "  ▓  ", "  ▓  "],
    'Z': ["▓▓▓▓▓", "   ▓ ", "  ▓  ", " ▓   ", "▓▓▓▓▓"],
    '0': [" ▓▓▓ ", "▓   ▓", "▓   ▓", "▓   ▓", " ▓▓▓ "],
    '1': ["  ▓  ", " ▓▓  ", "  ▓  ", "  ▓  ", "▓▓▓▓▓"],
    '2': [" ▓▓▓ ", "▓   ▓", "   ▓ ", "  ▓  ", "▓▓▓▓▓"],
    '3': ["▓▓▓▓ ", "    ▓", " ▓▓▓ ", "    ▓", "▓▓▓▓ "],
    '4': ["▓   ▓", "▓   ▓", "▓▓▓▓▓", "    ▓", "    ▓"],
    '5': ["▓▓▓▓▓", "▓    ", "▓▓▓▓ ", "    ▓", "▓▓▓▓ "],
    '6': [" ▓▓▓ ", "▓    ", "▓▓▓▓ ", "▓   ▓", " ▓▓▓ "],
    '7': ["▓▓▓▓▓", "    ▓", "   ▓ ", "  ▓  ", " ▓   "],
    '8': [" ▓▓▓ ", "▓   ▓", " ▓▓▓ ", "▓   ▓", " ▓▓▓ "],
    '9': [" ▓▓▓ ", "▓   ▓", " ▓▓▓▓", "    ▓", " ▓▓▓ "]
}


def load_slides(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def clear_screen():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def get_banner_lines(text):
    text = text.upper()
    lines = ["", "", "", "", ""]
    for char in text:
        glyph = BANNER_GLYPHS.get(char, BANNER_GLYPHS['?'])
        for i in range(5):
            lines[i] += glyph[i] + " "
    return lines


def render_progress_bar(current, total, width=32):
    filled = int(((current + 1) / total) * width)
    return "█" * filled + "░" * (width - filled)


def render_slide(slide, current, total):
    clear_screen()

    try:
        term_size = os.get_terminal_size()
        term_rows = term_size.lines
    except OSError:
        term_rows = 24

    reset = COLORS["reset"]
    s_color = COLORS.get(
        slide.get("subtitle_color", "cyan").lower(), COLORS["cyan"])

    title = slide.get('title', '')
    banner_text = slide.get('banner', '')
    subtitle = slide.get('subtitle', '')
    typewriter = slide.get('typewriter', False)

    content_height = 5 if banner_text else (1 if title else 0)
    if subtitle:
        content_height += 2

    # Calculate padding, but guarantee we don't accidentally exceed the terminal height
    vertical_padding = max(0, (term_rows // 2) - (content_height // 2))
    if vertical_padding + content_height >= term_rows - 1:
        vertical_padding = max(0, term_rows - content_height - 2)

    sys.stdout.write("\n" * vertical_padding)

    if banner_text:
        b_color = COLORS.get(
            slide.get("banner_color", "white").lower(), COLORS["white"])
        banner_lines = get_banner_lines(banner_text)
        for line in banner_lines:
            sys.stdout.write(f"  {b_color}{line}{reset}\n")
    elif title:
        t_color = COLORS.get(
            slide.get("title_color", "white").lower(), COLORS["white"])
        sys.stdout.write(f"  {t_color}{title}{reset}\n")

    if subtitle:
        sys.stdout.write("\n")
        sys.stdout.write(f"  {s_color}")
        if typewriter:
            for char in subtitle:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.02)
            # Notice there is no \n here anymore! This stops the jump.
            sys.stdout.write(reset)
        else:
            # Removed \n from here too.
            sys.stdout.write(f"{subtitle}{reset}")

    # STRICTLY lock the footer exactly 1 line from the absolute bottom of the window
    footer_row = max(2, term_rows - 1)

    prog_bar = render_progress_bar(current, total)
    footer = f" {prog_bar}  |  Slide {current + 1} of {total}  |  [<-] [->]  |  [q] Quit "

    # Teleport cursor straight to the bottom row
    sys.stdout.write(f"\033[{footer_row};1H")
    sys.stdout.write(f"  \033[90m{footer}\033[0m")
    sys.stdout.flush()


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch1 + ch2 + ch3
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run keynote.py slides.json")
        sys.exit(1)

    slides = load_slides(sys.argv[1])
    current_idx = 0
    total_slides = len(slides)

    sys.stdout.write("\033[?25l")
    clear_screen()

    try:
        # Render the very first slide normally
        render_slide(slides[current_idx], current_idx, total_slides)

        while True:
            key = get_key()
            prev_idx = current_idx

            if key == '\x1b[C' or key == ' ':
                if current_idx < total_slides - 1:
                    current_idx += 1
            elif key == '\x1b[D':
                if current_idx > 0:
                    current_idx -= 1
            elif key.lower() == 'q' or key == '\x03':
                break

            # Only re-render if the slide actually changed
            if current_idx != prev_idx:
                render_slide(slides[current_idx], current_idx, total_slides)
    finally:
        sys.stdout.write("\033[?25h")
        clear_screen()


if __name__ == '__main__':
    main()
