# SLITTY - Present your slides in the terminal

![slitty-header.png](slitty-header.png)

You can run Slitty in any standard terminal (like iTerm2), but it looks especially good in Ghostty since you can easily hide the window borders. 

Here is a quick command to launch Ghostty as a clean, borderless presentation window:

```bash
/Applications/Ghostty.app/Contents/MacOS/ghostty --window-decoration=false --window-width=182 --window-height=25 --font-size=24 --background-opacity=1.0  -e bash -c "cd ~/Dev/terminal-keynote && uv run keynote.py slides.json"
```
