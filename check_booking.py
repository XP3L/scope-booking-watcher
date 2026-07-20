#!/usr/bin/env python3
"""
Checks the Scope Cinemas movie page for SPIDER-MAN: BRAND NEW DAY to see
if online booking has opened, and sends a push notification via ntfy.sh
the moment it detects the "BUY TICKETS" button.

How it detects "open":
  - The movie page shows a "BUY TICKETS" button once bookings are live.
  - Before that, the page only shows a "Coming Soon" tag and no button.

State is kept in state.txt so we only notify ONCE (not on every run).
"""

import sys
import urllib.request

MOVIE_URL = "https://www.scopecinemas.com/movies/spider-man-brand-new-day"
SHOWTIMES_URL = "https://www.scopecinemas.com/movies/spider-man-brand-new-day/showtimes"

# Set this to a unique, hard-to-guess topic name. Anyone who knows this
# topic name can read your notifications, so keep it non-obvious.
NTFY_TOPIC = "spiderman-bnd-booking-alert-lk-8f2k1"

STATE_FILE = "state.txt"


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def is_booking_open(html: str) -> bool:
    # "BUY TICKETS" appears once the button is live on the movie page.
    return "BUY TICKETS" in html.upper().replace("&nbsp;", " ")


def is_showtimes_active(html: str) -> bool:
    # The showtimes page is a JS-rendered app, so the actual showtimes never
    # appear in the raw HTML we fetch here. BUT once a movie has showtimes
    # configured, the server also renders the "All Experiences" / "All
    # Locations" filter widgets into the initial HTML. Confirmed by
    # comparing this same page for a movie with live bookings (The Odyssey,
    # which shows these filters) vs Spider-Man (which shows neither).
    return "All Experiences" in html


def send_notification():
    message = (
        "Booking is OPEN for SPIDER-MAN: BRAND NEW DAY at Scope Cinemas! "
        f"Go book now: {MOVIE_URL}"
    )
    req = urllib.request.Request(
        url=f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": "Spider-Man tickets are live!",
            "Priority": "urgent",
            "Tags": "spider,tickets",
        },
        method="POST",
    )
    urllib.request.urlopen(req, timeout=15)


def read_state() -> str:
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "not_open"


def write_state(value: str):
    with open(STATE_FILE, "w") as f:
        f.write(value)


def main():
    try:
        movie_html = fetch(MOVIE_URL)
    except Exception as e:
        print(f"Error fetching movie page: {e}")
        movie_html = ""

    try:
        showtimes_html = fetch(SHOWTIMES_URL)
    except Exception as e:
        print(f"Error fetching showtimes page: {e}")
        showtimes_html = ""

    if not movie_html and not showtimes_html:
        # Both fetches failed (transient network issue) - skip this run.
        sys.exit(0)

    buy_button_present = is_booking_open(movie_html)
    showtimes_present = is_showtimes_active(showtimes_html)
    open_now = buy_button_present or showtimes_present
    previous_state = read_state()

    print(f"BUY TICKETS button present: {buy_button_present}")
    print(f"Showtimes filters present: {showtimes_present}")

    print(f"Booking open now: {open_now} | previous state: {previous_state}")

    if open_now and previous_state != "open":
        print("Booking just opened! Sending notification...")
        send_notification()
        write_state("open")
    elif not open_now and previous_state != "not_open":
        # In case the movie gets pulled again, reset state (unlikely, but safe).
        write_state("not_open")
    else:
        print("No change.")


if __name__ == "__main__":
    main()