# IconGen Agent Guide

Use this file as the working memory for future Codex sessions that design Apple-platform app icons in this repo.

## Goal

Create polished iOS, macOS, and watchOS app icons with a typography-first Apple look:

- Strong monogram or short wordmark, usually SF Pro Display Black/Bold.
- Concept-aware color palette from the app, country, domain, or brand.
- Layered source PNGs that can be imported into Apple Icon Composer.
- Final Icon Composer exports for iOS/macOS and watchOS.
- Resized PNG sets generated only from the approved Icon Composer master.

Best examples in this repo:

- CityCommuter Singapore transit icon: `CityCommuterIcon/SingaporeTransitClean/`
- ShadowTeep Thailand flag white icon: `ShadowTeepIcon/ThailandFlagWhite/`

## Tools

Use these tools in this order.

1. Local code/search tools
   - `rg`, `find`, `sed`, and `git status` to inspect projects and existing assets.
   - Read app theme files before choosing colors.

2. Python + Pillow
   - Generate precise 1024 x 1024 transparent PNG layers.
   - Resize final masters into AppIcon sizes.
   - Build contact sheets for small-size visual QA.

3. AppKit / PyObjC
   - Render real SF Symbols when the design needs Apple system symbols.
   - Example symbols used for CityCommuter: `tram.fill`, `bus.fill`, `location.fill`, `arrow.triangle.turn.up.right.diamond.fill`.

4. Apple SF fonts
   - Prefer installed Apple fonts:
     - `/Library/Fonts/SF-Pro-Display-Black.otf`
     - `/Library/Fonts/SF-Pro-Display-Bold.otf`
     - `/Library/Fonts/SF-Pro-Text-Semibold.otf`
     - `/System/Library/Fonts/SFNS.ttf`

5. SF Symbols app
   - App path: `/Applications/SF Symbols.app`
   - Check symbol names and the Transportation / Maps sections when icons need transit, route, location, or mobility cues.

6. Icon Composer
   - App path: `/Applications/Icon Composer.app`
   - Use it for final Liquid Glass preview and export.
   - Export static PNG masters:
     - iOS/macOS: `1024pt 1x`
     - watchOS: `1088pt 1x`

7. Computer Use
   - Required for Icon Composer and SF Symbols GUI work.
   - Always call `get_app_state` before clicking, typing, or pressing keys in an app.

## Design Rules

- Do not use a full app name unless the name is extremely short.
- Prefer a bold monogram: `ST`, `CC`, `NM`, etc.
- Use SF Pro Display Black/Bold for the main letters.
- Keep the monogram large enough to read at 32 px.
- Use concept color, not decoration color.
- Design with the app's actual theme first, then add one contextual accent.
- Keep source layers separated and named with numeric prefixes.
- Use SF Symbols only when they add meaning and remain readable.
- Use real SF Symbols via AppKit/PyObjC instead of manually redrawing Apple symbols.
- Avoid tiny text inside the icon. If a label is used, it must be optional detail at large sizes.
- Verify at 16, 32, 64, 128, and 256 px before calling it done.
- If Icon Composer creates noisy/jittery edges, turn off Liquid Glass effects for that specific layer.
- Keep the final master export and the raw source layers. Do not only keep resized outputs.

## Folder Structure

Use this structure for every icon concept:

```text
AppNameIcon/
  VariantName/
    SourceLayers/
      01-background.png
      02-meaningful-accent.png
      03-secondary-shape-or-route.png
      04-symbols.png
      05-type.png
      06-glass-highlights.png
      AppName-Variant-IconComposer-iOS-macOS-Default-1024.png
      AppName-Variant-IconComposer-watchOS-Default-1088.png
      AppName-Variant.icon            # optional, when saved from Icon Composer
    Exports/
      AppName-Variant-preview-1024.png
      AppName-Variant-IconComposer-contact-sheet.png
      IconComposerSized/
        AppName-Variant-IconComposer-16.png
        AppName-Variant-IconComposer-32.png
        ...
        AppName-Variant-IconComposer-1024.png
      RawSized/
        AppName-Variant-Raw-16.png
        ...
```

If a `.icon` package is not saved, the canonical Icon Composer artifacts are the exported PNG masters named `*-IconComposer-*.png`.

## Workflow

1. Understand the product
   - Read the user's concept.
   - If a local app repo exists, inspect its theme files, design tokens, asset catalogs, and existing app icon.
   - Extract exact hex colors.

2. Choose the mark
   - Pick a short monogram.
   - Choose one semantic visual cue.
   - Example: CityCommuter uses `CC`, Singapore red/white, a blue route line, and transit SF Symbols.
   - Example: ShadowTeep uses `ST`, Thailand flag colors, and an energetic steep/kick-like shadow.

3. Generate source layers
   - Use Python and Pillow for deterministic geometry.
   - Use AppKit/PyObjC for SF Symbols.
   - Use SF fonts for typography.
   - Save all layer PNGs at 1024 x 1024.

4. Make a raw preview
   - Composite the source layers into `Exports/*-preview-1024.png`.
   - Generate a contact sheet with small sizes.
   - Iterate before opening Icon Composer if the mark is not readable.

5. Import into Icon Composer
   - Create a new document.
   - Add each layer via `+` -> `New Image...`.
   - Use `Cmd+Shift+G` in the file picker to jump to the source folder.
   - Import layers from bottom to top:
     - background first
     - accents/shapes
     - symbols
     - type
     - highlights last

6. Tune Icon Composer
   - Check iOS/macOS and watchOS preview.
   - Keep Liquid Glass on layers where it adds depth.
   - Disable Liquid Glass on flat flag/ribbon layers if it creates edge jitter.
   - Inspect the small preview chips at the bottom of Icon Composer.

7. Export
   - Use `File -> Export...`.
   - Export iOS/macOS `Default` at `1024pt 1x`.
   - Export watchOS `Default` at `1088pt 1x`.
   - Save beside source layers with explicit names.

8. Resize from final master
   - Use the Icon Composer 1024 iOS/macOS PNG as the resize source.
   - Standard sizes:
     - `16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024`
   - Save into `Exports/IconComposerSized/`.

9. Verify
   - Verify image dimensions with Pillow.
   - View the contact sheet.
   - Confirm the icon reads at 32 px and 64 px.
   - Confirm no unwanted edge artifacts after Icon Composer export.

## Current Best Icons

### CityCommuter, Singapore Transit Clean

Purpose: Singapore-only commuter routing app.

Design:

- Monogram: `CC`
- Main color: CityCommuter blue `#0066CC`
- Context accent: Singapore red/white
- Symbols: real SF Symbols for tram, bus, route, and location
- Important fix: Liquid Glass is disabled on `02-singapore-red-ribbon.png` to avoid top flag edge jitter.

Key files:

- Source layers: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/`
- iOS/macOS master: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png`
- watchOS master: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-watchOS-Default-1088.png`
- No-jitter explicit copy: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-NoJitter-IconComposer-iOS-macOS-Default-1024.png`
- Contact sheet: `CityCommuterIcon/SingaporeTransitClean/Exports/CityCommuter-SingaporeTransitClean-NoJitter-IconComposer-contact-sheet.png`
- Resized set: `CityCommuterIcon/SingaporeTransitClean/Exports/IconComposerSized/`

### ShadowTeep, Thailand Flag White

Purpose: English practice app using TTS, note writing, playback, and a Muay Thai "teep" inspiration.

Design:

- Monogram: `ST`
- Background: white
- Accent: Thailand flag red/blue/white
- Style: bold SF typography, energetic diagonal shadow, clean Apple icon padding.

Key files:

- Source layers: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/`
- iOS/macOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png`
- watchOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-watchOS-Default-1088.png`
- Contact preview: `ShadowTeepIcon/ThailandFlagWhite/Exports/ShadowTeep-ThaiWhite-preview-1024.png`
- Resized set: `ShadowTeepIcon/ThailandFlagWhite/Exports/IconComposerSized/`

## Icon Composer Notes

- Save `.icon` packages when possible, ideally beside source layers:
  - `SourceLayers/AppName-Variant.icon`
- If the save flow is unreliable, do not block the work. The exported Icon Composer PNG masters are the dependable deliverables.
- The current repo contains a saved `.icon` package for Native Mobile:
  - `NativeMobileIcon/ProjectThemeWhiteAccent/SourceLayers/Native Mobile.icon`
- CityCommuter and ShadowTeep are currently represented by source layers plus Icon Composer exported PNG masters.

## Known Issues And Fixes

- Problem: noisy/jittery edge around a flat flag or ribbon after Icon Composer export.
  - Fix: select that layer, turn off `Liquid Glass -> Effects`, re-export masters, regenerate resized PNGs.

- Problem: file picker will not multi-select PNGs reliably.
  - Fix: import one layer at a time using `Cmd+Shift+G` and exact file paths.

- Problem: save field appends filename text after an overwrite prompt.
  - Fix: cancel the save panel, reopen Export, and type the filename into a fresh selected default field.

- Problem: watchOS preview crops or amplifies side glow.
  - Fix: switch to watchOS preview before export and adjust the layer scale or rim effects.
