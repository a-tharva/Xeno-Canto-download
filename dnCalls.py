import sys
import os
import re
import urllib.request

MAXPAGES = 1


def get_number_of_download_links(searchTerm):
    # Function to return links from searchTerm page  
    i = 1
    numbers = []
    
    while True:
        print(f'Featching links from page {i} with term {searchTerm}')
        page = urllib.request.urlopen(f'http://www.xeno-canto.org/explore?pg={i}&query={searchTerm}')
        newResults = re.findall(b'/(\d+)/download', page.read())
        if(len(newResults) > 0):
            numbers.extend(newResults)
        
        if(len(newResults) < 30 or i >= MAXPAGES):
            break
        else:
            i += 1
    
    return numbers


def get_filenames(searchTerm):
    # Function to return names from links
    # Get the filename from website for storage
    i = 1
    filenames = []
    while True:
        page = urllib.request.urlopen(f'http://www.xeno-canto.org/explore?pg={i}&query={searchTerm}')
        newResults = re.findall(b"data-xc-filepath=\'(\S+)\'", page.read())
        if(len(newResults) > 0):
            filenames.extend(newResults)
        
        if(len(newResults) < 30 or i >= MAXPAGES):
            break
        else:
            i += 1

    return filenames


def download(searchTerm):
    # Main function for download audio files
    if not os.path.exists(f'{searchTerm}'):
        print(f'Creating folder \{searchTerm}')
        os.makedirs(f'{searchTerm}')
    filename = get_filenames(searchTerm)
    
    if len(filename) == 0:
        print("No search result")
        sys.exit()
    numbers = get_number_of_download_links(searchTerm)
    
    fileFinder = re.compile('\S+/+(\S+)')
    print(f'Total {len(filename)} files will be downloaded')
    
    for i in range(len(filename)):
        # Iterate through files
        localFilename = f"{numbers[i].decode('utf-8')}" + '_' + fileFinder.findall(f"{filename[i].decode('utf-8')}")[0]
        
        if(len(f'{searchTerm}/'+ localFilename) > 255):
            localFilename = numbers[i]
        print(f'Downloading {localFilename}')
        filenameCon = str(filename[i])
        filenameCon = filenameCon[4:-1]
        print(f'filenameCon : http://{filenameCon}')
        urllib.request.urlretrieve(f'https://{filenameCon}', f'{searchTerm}/' + localFilename)
        

        
def main(args):
    
    print('Xeno canto downloader')
    birdName = args[1]
    print(birdName)
    
    download(birdName)
    

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("To use type: python dnXeno.py BirdName")
    main(sys.argv)