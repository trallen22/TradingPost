import os
import configurationFile as config

os.system(f"/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to ods {config.OUTPUTEXCEL}")

