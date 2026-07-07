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

macOS CV generation app for job seekers. The icon uses a bold `CV` monogram, a tailored document shape, professional navy/blue, and a sunrise amber accent for hope.

<img src="TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png" alt="TailrCV icon" width="220">

Files:

- iOS/macOS master: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-IconComposer-iOS-macOS-Default-1024.png`
- App Store opaque PNG: `TailrCVIcon/HopeWhite/SourceLayers/TailrCV-HopeWhite-AppStore-1024-opaque.png`
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

For modern Xcode projects, the `.icon` document is the preferred production handoff. The PNG masters remain useful for visual review, README showcase images, fallback asset catalogs, and generating resized PNG sets.

Current saved `.icon` document:

- `NativeMobileIcon/ProjectThemeWhiteAccent/SourceLayers/Native Mobile.icon`

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
10. Verify with a contact sheet at 16, 32, 64, 128, and 256 px.
11. Add the `.icon` file to Xcode and verify in Simulator or on device when working inside an app project.

See `Agent.md` for the detailed future-session rules and tool notes.
