# desk-sm — a small monitor for my desk

A custom PCB that sits on my desk and shows the album art of whatever I'm playing on Spotify, spinning like a vinyl while the song plays and freezing when it's paused. It also doubles as a weather display and a daily calendar view, controlled with two push buttons and a rotary encoder.

![3D render, front](images/render-front.png)
*Front: display, two push buttons, and the rotary encoder.*

![3D render, back detail](images/render-back-detail.png)
*Back: mounting holes and through-hole pads for the controls.*

## What it does

- **Now playing**: pulls the current track from the Spotify API and shows the album art. The art rotates like a vinyl record while the song plays, and stops when it's paused.
- **Weather**: a dedicated screen, because it's Seattle and I need to know if it's raining or not raining.
- **Calendar**: shows the day's schedule, class times, office hours, extracurriculars, meetings, whatever's on deck.
- **Controls**: two push buttons handle skip and play/pause. The rotary encoder cycles between the three screens (now playing, weather, calendar).

## Why I built this

I listen to a lot of music and love album art, so a little screen dedicated to it felt like an easy yes. Weather and calendar earned their spot because they're the two things I actually check every morning in college, class times, meetings, and whether Seattle is doing its usual thing.

Mostly, though, I wanted to build something I hadn't done before, hardware end to end, and use the last 10 days of summer break to do it. I also had a free trial of GitHub Copilot's agent and wanted to see what it could actually do: it handled the schematic well when I gave it clear specs, but the KiCad MCP fell apart at placement and routing. I ended up doing that part by hand, which the small scale of this board made manageable, and honestly more satisfying.

## Hardware

- **MCU**: Seeed Studio XIAO ESP32-S3
- **Display**: Adafruit 1.3" 240x240 IPS TFT (ST7789)
- **Controls**: 2x 6mm tactile switches, 1x EC11 rotary encoder
- **PCB**: 2-layer, hand-routed in KiCad

## Status

- [x] Schematic (Copilot-assisted)
- [x] PCB layout and hand-routing
- [x] DRC clean
- [x] Fab files generated, PCB ordered via JLCPCB
- [x] Display ordered from Adafruit
- [x] MCU sourced from Amazon
- [ ] Firmware (display driver, Spotify/weather/calendar integration)
- [ ] Solder and bring-up once the PCB arrives
- [ ] 3D-printed enclosure, designed in FreeCAD, printed on campus at UW

## Next steps

Once the display and MCU land, I'll write and test the firmware, display driving, Spotify polling, weather and calendar pulls, before any of it touches the actual board. When the PCB arrives, I'll solder everything on, take careful measurements, and design an enclosure in FreeCAD to print at one of UW's shops.

There's also a v2 in the back of my mind, more sophisticated, but v1 has to actually work first.

## Want one?

If you see this running and like it, let me know. I can put together a few more, up to 4, you'd just need to source a display and MCU (easy, both off-the-shelf), and I'll get the switches and encoder, solder the board, and flash the firmware. Plug and play from there.
