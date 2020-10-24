import os
import wget

file = 'Last24_tro2a.gif'
if os.path.exists(file):
    os.remove(file)

url = 'https://flux.phys.uit.no/Last24/Last24_tro2a.gif'
wget.download(url)
