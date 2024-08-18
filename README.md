# HANA

Holographic, Artifical, Nerual networking, Assistant

## Features

- QR detection
- Projection Mapping - https://www.npmjs.com/package/react-projection-mapping
- Modular system using multi-threading and multi-processing

### TODO - Upcomming features (Ordered list)

- [ ] QR Spotlight - Highlighting detected QR's allowing the webcam to easily read QR codes
- [ ] Four point QR mapping -  Using four QR's in each corner, it will correctly projection map the work area.
- [ ] Saving projection map settings in data
- [ ] Improve QR code performance
- [ ] Add UI wide notification handler (routes and datahandler)
- [ ] Hand guesture recognition
  - Certain hand guestures trigger certain functions
- [ ] Real world size 3D model viewer
  - https://github.com/google/model-viewer/issues/1038
  - Default view is in units where 1 unit is 1 meter
- [ ] Projects Vault
- [ ] Locally running LLM (Large Language Model (AI))
- [ ] Modular API's?

#### QR Features:

- [ ] Projects Vault
  - Acessing the data using QR's
- [ ] Page control
  - Navigating pages using Qr codes
- [ ] Modes - Different features based on mode QR
  - NO mode QR: Normal, colour is blue
  - DEBUG QR: Shows logs, updates colour to Orange
  - Project Mode: updates colours to red, access to vault data

#### Hand detection Features:

- [ ] Guesture recognition
  - Performing actions based on how many fingers are held up
- [ ] Mouse control
  - Controlling the system based on thumb and index positioning

## Later on features

Theses are a list of features which would be cool to have:

- Octopus Energy
  - Using their API I could make something that integrates features to notifiy of electric usage?

## Requirements

- Python 3
- Node
- C++
- Build tools:
  - winget install --id Microsoft.VisualStudio.2022.BuildTools --override "--passive --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"
