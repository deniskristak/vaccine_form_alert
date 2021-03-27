import time
import requests
from pywebcopy import save_webpage
import logging
import os

def get_valid_input():
    # dont bother with security rn
    website_question = "Do you wish to save the registration website once"
    website_question += "there is a new available registration date? Please type 'yes' or 'no'\n"
    should_save_website = input(website_question)
    if should_save_website != 'yes' and should_save_website != 'no':
        get_valid_input()
    else:
        local_project_folder = False
        if should_save_website == 'yes':
            folder_input_msg = "Please provide a complete path where the downloaded "
            folder_input_msg += "website should be saved.\n"
            local_project_folder = input(folder_input_msg)
        return should_save_website, local_project_folder

should_save_website, local_project_folder = get_valid_input()

url = "https://www.old.korona.gov.sk/covid-19-vaccination-form.php"
refreshed = 0
html = ""
count = 0

while refreshed != -1:
    try:
        count += 1
        time.sleep(0.1)

        html = requests.get(url).text

        # we dont know what the next (actual registration) page looks like and what to look for, so this is the best we can get
        refreshed = html.find("Momentálne sú všetky kapacity obsadené.")
        print(count)
    except:
        logging.basicConfig(filename='log_download_html.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        logging.warning('==============================GOT DISCONNECTED, RESETING COUNTER AND RUNNING AGAIN=================================')
        count = 0
        pass

# some Stephen Hawking stuff
os.system('spd-say "\
    alert! there are new dates available for registration! \
"')

if should_save_website == 'yes':
    kwargs = {'project_name': 'vacc'}
    save_webpage(
        url='https://www.old.korona.gov.sk/covid-19-vaccination-form.php',
        project_folder=local_project_folder,
        **kwargs
    )

print("Attempts before successful: ", str(count))
print('To exit, press CTRL+C')
duration = 2838240000  # in seconds...90 years should be enough for someone to notice the sound
freq = 1000  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
