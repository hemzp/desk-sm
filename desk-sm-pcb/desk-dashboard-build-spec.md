# Desk Dashboard — KiCad Build Spec

Instruction set for GitHub Copilot + KiCad MCP. Build the schematic and PCB
from this. Do not export fabrication files or push to any manufacturer until
the human reviews the schematic pin-by-pin against this document.

## 1. What this board is

A small desk display driven by a Seeed XIAO ESP32-S3 (SMD module). It shows
Spotify now-playing, weather, and calendar on an Adafruit 1.3" 240x240 IPS TFT
(ST7789, product 4313). Two mechanical keys and one rotary encoder provide
control. Firmware is out of scope for this spec; this is the hardware only.

## 2. Components

- U1: Seeed XIAO ESP32-S3 (SMD module). Use the Seeed XIAO symbol/footprint
  library. If not present, generate a custom symbol + footprint for the XIAO
  ESP32-S3 SMD (castellated module).
- J1: display connection to the Adafruit 4313. Two options, pick per section 4.
- SW1, SW2: two momentary tactile push switches (SPST).
- ENC1: rotary encoder with push switch (EC11 type: pins A, B, common, plus
  an integral push button with its own two terminals).
- Power symbols: +3V3 and GND.
- Decoupling: one 100nF ceramic across the display's Vin/GND, placed close to
  the connector. Optional second 100nF near the XIAO 3V3 pad.

## 3. Verified display netlist (XIAO <-> Adafruit 4313)

The 4313 breakout header is 11 pads. Signal order confirmed from the board
silkscreen. Wire these signals (by name, not by guessed pad number):

- Vin        -> XIAO 3V3
- Gnd        -> XIAO GND
- SCK        -> XIAO D8   (hardware SPI clock)
- SI (MOSI)  -> XIAO D10  (hardware SPI data)
- TCS        -> XIAO D1   (TFT chip select)
- D/C        -> XIAO D2   (data/command)
- RST        -> XIAO D3   (optional; board has auto-reset, may be left open)
- Lite       -> XIAO 3V3  (backlight on; or route to a free GPIO for dimming)
- SO (MISO)  -> no connection (SD card only, unused)
- CCS        -> no connection (SD card chip select, unused)
- 3v3 (out)  -> no connection (regulator output, unused)

Note: the display's onboard regulator and level shifter mean Vin can take 3.3V
directly from the XIAO. Do not connect the display's 3v3 output pin to anything.

## 4. Display connector choice (human decides before layout)

Option A — EYESPI (recommended, deterministic, no soldering to display):
  Place an 18-pin 0.5mm-pitch EYESPI FPC connector on the board. Use the
  published EYESPI standard footprint. Connect via EYESPI flex cable to the
  4313's onboard EYESPI socket. Only the power + SPI signals in section 3 are
  used; the rest of the 18 pins are unconnected per the EYESPI standard.

Option B — Solder header:
  Place a 1x11 2.54mm header (J1) matching the 4313's solder header. Use
  Adafruit's official footprint for this board if available. Physical pad order
  left-to-right is: Lite, CCS, D/C, RST, TCS, SI, SO, SCK, Gnd, 3v3, Vin.

Default to Option A unless the human says otherwise.

## 5. Controls netlist

Assign each to a free XIAO GPIO. Avoid strapping and USB pins. On the XIAO
ESP32-S3 the broken-out pads are D0-D10; D8/D10 are taken by SPI clock/data,
D1/D2/D3 by the display. Use the remaining free pads (e.g. D0, D4, D5, D6, D7,
D9) for the controls. Final pin choice is the assistant's to make from the free
set; record whatever is chosen.

- SW1: one terminal -> free GPIO, other terminal -> GND. Use internal pull-up
  (active low). No external resistor.
- SW2: one terminal -> free GPIO, other terminal -> GND. Internal pull-up.
- ENC1 A  -> free GPIO
- ENC1 B  -> free GPIO
- ENC1 common -> GND
- ENC1 push switch -> free GPIO, other terminal -> GND. Internal pull-up.
  (An encoder press is just another button.)

Encoder needs two GPIOs for rotation (A, B) plus one for its push = three
GPIOs. Two keys = two GPIOs. Total controls = five free GPIOs, which the XIAO
has after SPI + display.

## 6. Power

- The XIAO is powered over its USB-C. Its 3V3 pad supplies the display and any
  pull-ups. Confirm the display's current draw (backlight included) is within
  the XIAO 3V3 regulator budget; the 1.3" panel is light, this is fine.
- Tie all grounds common.

## 7. Steps for the tool, in order

1. Create the KiCad project.
2. Ensure/generate symbols + footprints for: XIAO ESP32-S3 SMD, the display
   connector (EYESPI 18-pin or 1x11 header per section 4), tactile switch,
   EC11 encoder.
3. Place components and wire every net in sections 3 and 5.
4. Add the decoupling cap(s) from section 2.
5. Add +3V3 and GND power symbols and connect.
6. Run ERC. Report all warnings and errors back to the human. Do not silence
   or auto-fix power/pin warnings without flagging them.
7. Stop. Do not lay out copper, route, generate Gerbers, or contact any fab
   until the human reviews the schematic against this spec.

## 8. Review checklist (human does this before fab)

- Every signal in section 3 lands on the correct XIAO pad.
- No control or display signal sits on a strapping pin (GPIO0/45/46 on the raw
  chip) or the USB pins — verify against the XIAO's actual pad mapping.
- Display Vin goes to 3V3, not 5V (XIAO 3V3 is the supply).
- SO, CCS, and the display 3v3-out pin are left unconnected.
- Footprints match the real parts being ordered (measure or check datasheets).
- ERC is clean or every remaining warning is understood and intentional.
