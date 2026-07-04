# SmartCalc Pro

A calculator with basic, scientific, statistics, finance/economics, and
utility tools. This repo contains **two versions** of the same app:

| Version | Where | Runs on |
|---|---|---|
| 🖥️ Desktop app | `main.py` + `calculator_engine.py` + `themes.py` + `history.py` | Windows / macOS / Linux, via Python + Tkinter |
| 📱 Web / installable app | `web/` folder (`index.html`, `manifest.json`, `sw.js`, icons) | Any phone or browser, as an installable PWA |

Both share the same feature set — Basic, Scientific, Statistics, Finance,
and Utility calculators — but the web version is a self-contained
rewrite (HTML/CSS/JS) so it can run without Python or a desktop.

---

## 🖥️ Desktop version (Tkinter)

**Requirements:** Python 3.10+

```bash
python main.py
```

No extra packages needed — it only uses the standard library
(`tkinter`, `math`, `statistics`, `datetime`).

Files:
- `main.py` — GUI and layout
- `calculator_engine.py` — all calculation logic
- `themes.py` — light/dark color definitions
- `history.py` — saves calculations to `history.txt`

---

## 📱 Web version (installable app)

Lives in the `web/` folder. It's a static site — no build step, no
backend, no dependencies.

**Files:**
- `index.html` — the entire app (UI + calculator logic)
- `manifest.json` — tells the browser this is an installable app (name, icons, colors)
- `sw.js` — service worker, caches the app so it works offline
- `icon-192.png`, `icon-512.png` — app icons

### Run it locally
Just open `web/index.html` in a browser — no server required for basic use.
(The install prompt and offline support only activate once it's served over HTTPS — see below.)

### Publish it with GitHub Pages
1. Push this repo to GitHub (if not already).
2. Go to **Settings → Pages**.
3. Under "Source," select your branch and the `/web` folder as the root.
4. Save. GitHub will give you a URL like:
   `https://<your-username>.github.io/<repo-name>/`

### Install it on your phone
- **Android (Chrome):** open the URL → tap **"Install app"** when prompted (or menu → Install app).
- **iPhone (Safari):** open the URL → Share → **Add to Home Screen**.

Once installed, it opens full-screen like a native app and keeps working
offline thanks to the service worker.

---

## Feature overview (both versions)

- **Basic** — add, subtract, multiply, divide, modulus, power, square, cube, percentage
- **Scientific** — square root, cube root, factorial, ln, log10, eˣ, sin/cos/tan (degrees)
- **Statistics** — count, mean, median, mode, range, standard deviation, variance
- **Finance** — simple interest, compound interest, EMI, CAGR, % change, inflation adjustment
- **Utility** — BMI, age calculator, temperature/length/weight unit conversion

## Notes

- The web version keeps calculation history in the browser's local
  storage for that installed app — it isn't synced anywhere.
- The two versions are independent; changes to one don't affect the other.
