# IconGen

Typography-first Apple app icon experiments for iOS, macOS, and watchOS.

This repo keeps the source layers, Icon Composer files/exports, and resized PNG sets for side-project app icons. The current strongest designs are CityCommuter, ShadowTeep, and TailrCV.

Apple guidance used for this workflow:

- [Creating your app icon using Icon Composer](https://developer.apple.com/documentation/xcode/creating-your-app-icon-using-icon-composer)
- [Configuring your app icon using an asset catalog](https://developer.apple.com/documentation/xcode/configuring-your-app-icon)

## Showcase

### CityCommuter

Singapore transit routing app. The icon combines a bold `CC` monogram, Singapore red/white, CityCommuter route blue, and real SF Symbols for transit cues.

<img src="CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png" alt="CityCommuter icon" width="220">

Files:

- iOS/macOS master: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png`
- watchOS master: `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-watchOS-Default-1088.png`
- Contact sheet: `CityCommuterIcon/SingaporeTransitClean/Exports/CityCommuter-SingaporeTransitClean-NoJitter-IconComposer-contact-sheet.png`
- Resized set: `CityCommuterIcon/SingaporeTransitClean/Exports/IconComposerSized/`

Notes:

- The top Singapore ribbon has Liquid Glass disabled to avoid edge jitter.
- The main typography and route layers keep the polished Icon Composer depth.

### ShadowTeep

English practice app inspired by the Muay Thai teep. The icon uses a bold `ST` monogram on a white base with Thailand flag colors.

<img src="ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png" alt="ShadowTeep icon" width="220">

Files:

- iOS/macOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png`
- watchOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-watchOS-Default-1088.png`
- Preview: `ShadowTeepIcon/ThailandFlagWhite/Exports/ShadowTeep-ThaiWhite-preview-1024.png`
- Resized set: `ShadowTeepIcon/ThailandFlagWhite/Exports/IconComposerSized/`

### TailrCV

macOS CV generation app for job seekers. The icon uses a bold `CV` monogram, the `doc.text.fill` SF Symbol, professional navy/blue, and a sunrise amber accent for hope.

<img src="TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png" alt="TailrCV icon" width="220">

Files:

- Icon Composer package: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite.icon`
- iOS/macOS master: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png`
- Dark appearance: `TailrCVIcon/HopeWhite/Exports/AppearanceVariants/TailrCV-HopeWhite-IconComposer-iOS-macOS-Dark-1024.png`
- Mono appearance: `TailrCVIcon/HopeWhite/Exports/AppearanceVariants/TailrCV-HopeWhite-IconComposer-iOS-macOS-Mono-1024.png`
- Tinted grayscale source: `TailrCVIcon/HopeWhite/Exports/AppearanceVariants/TailrCV-HopeWhite-IconComposer-iOS-macOS-Tinted-Grayscale-1024.png`
- App Store opaque PNG: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-AppStore-1024-opaque.png`
- macOS AppIcon set: `TailrCVIcon/HopeWhite/Exports/MacOSAppIcon.appiconset/`
- macOS icns: `TailrCVIcon/HopeWhite/Exports/TailrCV-HopeWhite-AppIcon.icns`
- watchOS master: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-watchOS-Default-1088.png`
- Contact sheet: `TailrCVIcon/HopeWhite/Exports/TailrCV-HopeWhite-contact-sheet.png`
- Resized set: `TailrCVIcon/HopeWhite/Exports/IconComposerSized/`

## Repository Layout

```text
Agent.md
README.md
CityCommuterIcon/
  SingaporeTransitClean/
    SourceLayers/
    Exports/
      IconComposerSized/
      RawSized/
ShadowTeepIcon/
  ThailandFlagWhite/
    SourceLayers/
    Exports/
      IconComposerSized/
      RawSized/
TailrCVIcon/
  HopeWhite/
    SourceLayers/
    Exports/
      IconComposerSized/
      RawSized/
      AppearanceVariants/
NativeMobileIcon/
  ProjectThemeWhiteAccent/
    SourceLayers/
    Exports/
```

## Icon Composer Artifacts

Each finished variant should keep:

- Source PNG layers in `SourceLayers/`
- Saved Icon Composer `.icon` document in `SourceLayers/` whenever possible
- iOS/macOS Icon Composer master PNG in `SourceLayers/*-IconComposer-iOS-macOS-Default-1024.png`
- watchOS Icon Composer master PNG in `SourceLayers/*-IconComposer-watchOS-Default-1088.png`
- For macOS fallback projects, a full `Exports/MacOSAppIcon.appiconset/`
  ladder and a matching `Exports/*-AppIcon.icns`

For modern Xcode projects, the `.icon` document is the preferred production handoff. The PNG masters remain useful for visual review, README showcase images, fallback asset catalogs, and generating resized PNG sets.
When the target still uses `CFBundleIconFile = AppIcon`, update both
`AppIcon.icns` and every mac idiom image in `AppIcon.appiconset`; a single 1024
PNG is not enough for macOS fallback delivery.

Current saved `.icon` document:

- `NativeMobileIcon/ProjectThemeWhiteAccent/SourceLayers/Native Mobile.icon`
- `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite.icon`

Current best Icon Composer PNG masters:

- `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png`
- `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png`
- `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png`

## Workflow

1. Read app context and color theme.
2. Design a large SF Pro monogram.
3. Add one or two concept cues with restrained color.
4. Generate 1024 x 1024 PNG source layers.
5. Import layers into Apple Icon Composer.
6. Save a `.icon` document when possible.
7. Preview iOS/macOS, watchOS, and appearance variants.
8. Export Icon Composer masters.
9. Generate resized PNGs from the final 1024 master.
10. For macOS fallback handoff, generate the explicit AppIcon ladder:
    `16x16`, `16x16@2x`, `32x32`, `32x32@2x`, `128x128`, `128x128@2x`,
    `256x256`, `256x256@2x`, `512x512`, and `512x512@2x`, plus `.icns`.
11. Verify with a contact sheet at 16, 32, 64, 128, and 256 px.
12. Add the `.icon` file or macOS fallback assets to Xcode and verify in Simulator or on device when working inside an app project.

See `Agent.md` for the detailed future-session rules and tool notes.
