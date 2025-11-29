# Monthly Expenses - Kivy Mobile App

This repository contains a Kivy-based mobile expenses tracker and a GitHub Actions workflow
that runs Buildozer to compile an Android APK automatically.

## How to use (GitHub automatic build)

1. Create a **new GitHub repository**, e.g. `expenses-mobile`.
2. Upload all files and folders from this ZIP to the repository root.
3. Commit and push to the `main` branch.
4. Go to the repository **Actions** tab and open the workflow **Android Build (Buildozer)**.
5. Run the workflow or wait for GitHub to trigger it on push.
6. When finished, check **Artifacts** in the workflow run and download the APK (`app-apk` artifact).

Notes:
- Build may take 20–60 minutes on GitHub runner.
- If the build fails due to missing Android SDK/NDK versions, adjust `buildozer.spec` android.api/android.ndk values.
- For release builds and Play Store uploads, you will need to set signing keys and change `buildozer.spec` accordingly.

Generated from your original desktop Tkinter code. See original file reference: expenses_pro.py
