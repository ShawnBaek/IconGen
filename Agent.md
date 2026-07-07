# IconGen Agent Guide

Use this file as the working memory for future Codex sessions that design Apple-platform app icons in this repo.

## Goal

Create polished iOS, macOS, and watchOS app icons with a typography-first Apple look:

- Strong monogram or short wordmark, usually SF Pro Display Black/Bold.
- Concept-aware color palette from the app, country, domain, or brand.
- Layered source artwork that can be imported into Apple Icon Composer.
- Saved `.icon` files as the preferred Xcode handoff when possible.
- Final Icon Composer preview/export PNGs for iOS/macOS and watchOS.
- Resized PNG sets generated only from the approved Icon Composer master.

Best examples in this repo:

- CityCommuter Singapore transit icon: `CityCommuterIcon/SingaporeTransitClean/`
- ShadowTeep Thailand flag white icon: `ShadowTeepIcon/ThailandFlagWhite/`
- TailrCV hope white icon: `TailrCVIcon/HopeWhite/`

## Tools

Use these tools in this order.

1. Local code/search tools
   - `rg`, `find`, `sed`, and `git status` to inspect projects and existing assets.
   - Read app theme files before choosing colors.

2. Python + Pillow
   - Generate precise 1024 x 1024 transparent PNG layers.
   - Resize final masters into AppIcon sizes.
   - Build contact sheets for small-size visual QA.
   - PNG is acceptable for this typography workflow; use SVG for scalable vector source when a design starts in a vector editor.

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
   - Save a `.icon` file for the target project whenever the save flow is reliable.
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
- Prefer a saved `.icon` file as the production artifact for modern Xcode projects. Keep PNG masters for review, README showcase, App Store handoff checks, and fallback asset catalogs.
- App Store 1024 PNGs must be fully opaque. Flatten onto the intended background and remove the alpha channel before App Store or asset-catalog handoff.
- Do not export a canvas mask into Icon Composer; Apple applies the icon crop automatically.
- Keep imported layers numbered from back to front so Icon Composer's alphabetical ordering stays predictable.

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
      AppName-Variant.icon
      AppName-Variant-IconComposer-iOS-macOS-Default-1024.png
      AppName-Variant-IconComposer-watchOS-Default-1088.png
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

The `.icon` file is the preferred production handoff for Xcode. If a `.icon` package is not saved, the canonical review artifacts are the exported PNG masters named `*-IconComposer-*.png`.

## Apple Xcode Guidance

Apple's current app icon documentation changes how to think about final delivery:

- Icon Composer creates a single multilayer `.icon` file that Xcode can use for iOS, iPadOS, macOS, watchOS, and App Store icon rendering.
- Add the `.icon` file to the Xcode project bundle before building. In the target's General pane, the App Icon field must match the `.icon` filename without the extension.
- In current Xcode, an Icon Composer file can replace an existing `AppIcon` asset catalog for the app icon. Xcode can generate similar-looking assets for older OS releases from the `.icon` file. If an app must keep its previous icon on older OS releases, continue using asset catalogs.
- Use Icon Composer's Document inspector to hide platforms the app does not support. For this repo, usually keep iOS/macOS and watchOS; disable unrelated platforms.
- Icon Composer previews platform and appearance variants: iOS/macOS Default, Dark, Mono, clear/tinted options, and watchOS. Always inspect the variants that the app will ship.
- Organize imported artwork into no more than four groups where possible. Groups are the depth layers the system renders.
- For source artwork from vector tools, prefer SVG. Convert text to outlines because SVG does not preserve fonts. For this repo's generated typography PNG layers, keep the Python source script so the type remains reproducible.
- Remove baked blurs, shadows, translucency, background gradients, and similar effects before importing when possible; apply those effects in Icon Composer where they can be previewed with Liquid Glass.
- For non-Icon-Composer fallback asset catalogs, Xcode can generate many icon variations from a single high-resolution image for iOS, iPadOS, tvOS, and watchOS. macOS app icon sets still need explicit sizes when using an asset catalog.
- App Store 1024 PNG artwork must not contain transparency. Use an RGB/sRGB, fully opaque 1024 x 1024 PNG with the background already flattened into the image.
- iOS and iPadOS asset catalogs support Light, Dark, and Tinted icon appearances. Tinted icons should be grayscale; dark icons should use transparent backgrounds so the system background can show through.
- Always test the icon in Simulator or on a real device for the supported platforms and appearances.

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
   - If using SVG source from a vector tool, convert text to outlines before import.
   - Keep source effects minimal; let Icon Composer handle Liquid Glass, shadow, opacity, translucency, and appearance variations where possible.

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
   - Save the document as `SourceLayers/AppName-Variant.icon`.
   - Use the Document inspector to keep only the supported platforms visible.
   - Organize layers into meaningful groups, with a practical maximum of four groups.
   - Check iOS/macOS and watchOS preview.
   - Check Default, Dark, and Mono appearances for iOS/macOS when applicable.
   - Keep Liquid Glass on layers where it adds depth.
   - Disable Liquid Glass on flat flag/ribbon layers if it creates edge jitter.
   - Inspect the small preview chips at the bottom of Icon Composer.

7. Export
   - Use `File -> Export...`.
   - Export iOS/macOS `Default` at `1024pt 1x`.
   - Export watchOS `Default` at `1088pt 1x`.
   - Save beside source layers with explicit names.
   - For any App Store or fallback asset-catalog `1024.png`, flatten onto a solid background and remove alpha. Do not submit transparent PNGs to App Store Connect.

8. Resize from final master
   - Use the Icon Composer 1024 iOS/macOS PNG as the resize source.
   - Standard sizes:
     - `16, 20, 29, 32, 40, 58, 60, 64, 76, 80, 87, 120, 128, 152, 167, 180, 256, 512, 1024`
   - Save into `Exports/IconComposerSized/`.
   - If the resize source has alpha, create a separate flattened opaque App Store PNG instead of reusing the transparent master.

9. Verify
   - Verify image dimensions with Pillow.
   - View the contact sheet.
   - Confirm the icon reads at 32 px and 64 px.
   - Confirm no unwanted edge artifacts after Icon Composer export.
   - Add the `.icon` file to an Xcode target when possible and test in Simulator or on device.

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

### TailrCV, Hope White

Purpose: macOS app for generating CVs for job seekers.

Design:

- Monogram: `CV`
- Background: white with a subtle blue/amber wash
- Hope color: sunrise amber `#FFB540`
- Trust/professional color: blue `#246BFE` and navy ink
- Concept cue: real SF Symbol `doc.text.fill` as the CV document, plus a sunrise base for optimism.
- App Store note: the 1024 PNG is intentionally RGB/opaque with no alpha.

Key files:

- Source layers: `TailrCVIcon/HopeWhite/SourceLayers/`
- iOS/macOS master: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png`
- App Store opaque PNG: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-AppStore-1024-opaque.png`
- watchOS master: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-watchOS-Default-1088.png`
- Contact sheet: `TailrCVIcon/HopeWhite/Exports/TailrCV-HopeWhite-contact-sheet.png`
- Resized set: `TailrCVIcon/HopeWhite/Exports/IconComposerSized/`

## Icon Composer Notes

- Save `.icon` packages whenever possible, ideally beside source layers:
  - `SourceLayers/AppName-Variant.icon`
- The `.icon` package is the production handoff for modern Xcode projects.
- If the save flow is unreliable, do not block the work. Exported Icon Composer PNG masters remain the dependable visual deliverables and fallback source for resized PNG sets.
- The current repo contains a saved `.icon` package for Native Mobile:
  - `NativeMobileIcon/ProjectThemeWhiteAccent/SourceLayers/Native Mobile.icon`
- CityCommuter and ShadowTeep are currently represented by source layers plus Icon Composer exported PNG masters.

## Xcode Handoff Checklist

- Add the saved `.icon` file to the Xcode project.
- In target settings, open General -> App Icons and Launch Screen.
- Set App Icon to the `.icon` filename without `.icon`.
- If the project still uses an asset catalog fallback, add the 1024 px master or explicit sizes as required by the target platform.
- For App Store Connect, provide a 1024 x 1024 opaque PNG: no alpha channel and no transparent pixels.
- Run on Simulator or device and verify Default, Dark, Mono/tinted, and watchOS appearances as applicable.

## Known Issues And Fixes

- Problem: noisy/jittery edge around a flat flag or ribbon after Icon Composer export.
  - Fix: select that layer, turn off `Liquid Glass -> Effects`, re-export masters, regenerate resized PNGs.

- Problem: file picker will not multi-select PNGs reliably.
  - Fix: import one layer at a time using `Cmd+Shift+G` and exact file paths.

- Problem: save field appends filename text after an overwrite prompt.
  - Fix: cancel the save panel, reopen Export, and type the filename into a fresh selected default field.

- Problem: watchOS preview crops or amplifies side glow.
  - Fix: switch to watchOS preview before export and adjust the layer scale or rim effects.
