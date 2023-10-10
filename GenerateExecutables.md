# Generate Executables from Codebase


## Generate WAS Display
`python -m PyInstaller src/main.py --add-data src\config.yml;. --add-data src\assets;assets --splash --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" project_assets/splashscreen.png --noconsole --name WASDisplay --version-file=project_assets/version-file.txt --icon project_assets/Feuerwehr.ico`

## Generate TEST WAS Display
`python -m PyInstaller src/main.py --add-data src\config.yml;. --add-data src\assets;assets --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --name WASDisplayTEST --version-file=project_assets/version-file.txt --icon project_assets/Feuerwehr.ico`



## Generate TesterSystem
`python -m PyInstaller -F test-sender/test_was_sender.py --splash project_assets/splashscreen.png --add-data "venv/Lib/site-packages/customtkinter;customtkinter/"  --noconsole --name WASDisplayTester --version-file=project_assets/version-file.txt --icon project_assets/Feuerwehr.ico`

## Generate TESt TesterSystem
`python -m PyInstaller -F  test-sender/test_was_sender.py --name WASDisplayTesterTEST --add-data "venv/Lib/site-packages/customtkinter;customtkinter/" --version-file=project_assets/version-file.txt --icon project_assets/Feuerwehr.ico`