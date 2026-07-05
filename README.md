# IconGen

Typography-first Apple app icon experiments for iOS, macOS, and watchOS.

This repo keeps the source layers, Icon Composer exports, and resized PNG sets for side-project app icons. The current strongest designs are CityCommuter and ShadowTeep.

## Showcase

### CityCommuter

Singapore transit routing app. The icon combines a bold `CC` monogram, Singapore red/white, CityCommuter route blue, and real SF Symbols for transit cues.

![CityCommuter icon](CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png)

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

![ShadowTeep icon](ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png)

Files:

- iOS/macOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png`
- watchOS master: `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-watchOS-Default-1088.png`
- Preview: `ShadowTeepIcon/ThailandFlagWhite/Exports/ShadowTeep-ThaiWhite-preview-1024.png`
- Resized set: `ShadowTeepIcon/ThailandFlagWhite/Exports/IconComposerSized/`

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
NativeMobileIcon/
  ProjectThemeWhiteAccent/
    SourceLayers/
    Exports/
```

## Icon Composer Artifacts

Each finished variant should keep:

- Source PNG layers in `SourceLayers/`
- iOS/macOS Icon Composer master PNG in `SourceLayers/*-IconComposer-iOS-macOS-Default-1024.png`
- watchOS Icon Composer master PNG in `SourceLayers/*-IconComposer-watchOS-Default-1088.png`
- Optional saved `.icon` document in the same `SourceLayers/` folder

Current saved `.icon` document:

- `NativeMobileIcon/ProjectThemeWhiteAccent/SourceLayers/Native Mobile.icon`

Current best Icon Composer PNG masters:

- `CityCommuterIcon/SingaporeTransitClean/SourceLayers/CityCommuter-SingaporeTransitClean-IconComposer-iOS-macOS-Default-1024.png`
- `ShadowTeepIcon/ThailandFlagWhite/SourceLayers/ShadowTeep-ThaiWhite-IconComposer-iOS-macOS-Default-1024.png`

## Workflow

1. Read app context and color theme.
2. Design a large SF Pro monogram.
3. Add one or two concept cues with restrained color.
4. Generate 1024 x 1024 PNG source layers.
5. Import layers into Apple Icon Composer.
6. Preview iOS/macOS and watchOS.
7. Export Icon Composer masters.
8. Generate resized PNGs from the final 1024 master.
9. Verify with a contact sheet at 16, 32, 64, 128, and 256 px.

See `Agent.md` for the detailed future-session rules and tool notes.
