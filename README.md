# Spider-Man: Brand New Day — Booking Monitor

Checks https://www.scopecinemas.com/movies/spider-man-brand-new-day every 15 minutes
and sends you a free push notification the moment the "BUY TICKETS" button appears.

## Setup (takes ~5 minutes, all free)

### 1. Get the notification app (do this first, on your phone)
- Install **ntfy** from the App Store / Google Play (it's a free, open-source push notification app — no account needed).
- Open the app, tap "+", and subscribe to this topic name exactly:
  ```
  spiderman-bnd-booking-alert-lk-8f2k1
  ```
- That's it — any device subscribed to that topic name gets the alert.
- ⚠️ Optional but recommended: change the topic name in `check_booking.py` (the `NTFY_TOPIC` variable) to something more random/unique to you, since anyone who guesses the topic name could also see the notification (it's not private data, just avoids noise from other ntfy users picking the same name). If you change it, subscribe to your new name in the app instead.

### 2. Put this code on GitHub
1. Create a new **private** GitHub repository (e.g. `spiderman-monitor`).
2. Upload all the files in this folder (`check_booking.py`, `state.txt`, `.github/workflows/check-booking.yml`, this README) to the repo, keeping the folder structure.
3. Go to the repo's **Settings → Actions → General → Workflow permissions**, and make sure "Read and write permissions" is selected (needed so the workflow can save its state between runs).

### 3. Done
- GitHub Actions will now automatically run the check every 15 minutes for free.
- You can watch it run under the **Actions** tab in your repo.
- You can also trigger a manual check any time via **Actions → Check Spider-Man Booking Status → Run workflow**.
- The moment "BUY TICKETS" appears on the page, you'll get a push notification on your phone, and the script stops notifying repeatedly after that (it only fires once, on the transition to "open").

## Notes
- GitHub Actions' free tier gives public repos unlimited minutes, and private repos 2,000 free minutes/month — this job takes a few seconds per run, so 15-minute checks use well under 1% of that.
- If Scope Cinemas changes their page design later (unlikely soon), the "BUY TICKETS" text check might need updating — just let me know and I can adjust the script.
- If you'd rather not use GitHub, the same `check_booking.py` script can run via `cron` (Mac/Linux) or Task Scheduler (Windows) on your own computer instead — I can give you those setup steps if you want to switch later.
