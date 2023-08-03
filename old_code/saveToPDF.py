import os
import configuration_file as config

os.system(f"/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to ods {config.OUTPUTEXCEL}")

