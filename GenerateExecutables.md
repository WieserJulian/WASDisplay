# Generate Executables from Codebase


## Generate WAS Display
`python -m PyInstaller -F src/main.py --add-data src/utils/config.yml;. --splash project_assets/splashscreen.png --noconsole --name WASDisplay --version-file=project_assets/version-file.txt`

## Generate TEST WAS Display
`python -m PyInstaller -F src/main.py --add-data src/utils/config.yml;. --name WASDisplayTEST --version-file=project_assets/version-file.txt`



## Generate TesterSystem
`python -m PyInstaller -F test-sender/test_was_sender.py --splash project_assets/splashscreen.png  --noconsole --name WASDisplayTester --version-file=project_assets/version-file.txt`

## Generate TESt TesterSystem
`python -m PyInstaller -F  test-sender/test_was_sender.py --name WASDisplayTesterTEST --version-file=project_assets/version-file.txt`