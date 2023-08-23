# Generate Executables from Codebase


## Generate WAS Display
`python -m PyInstaller -F --add-data src/utils/config.yml;. --splash project_assets/splashscreen.png src/main.py --noconsole`



## Generate TesterSystem
`python -m PyInstaller -F --splash project_assets/splashscreen.png test-sender/test_was_sender.py --noconsole`