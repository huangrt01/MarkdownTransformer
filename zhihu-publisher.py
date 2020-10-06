

# Usage: This program aims to transfer your markdown file into a way zhihu.com can recognize correctly.
#        It will mainly deal with your local images and the formulas inside.

import os, re
import argparse
import codecs
import subprocess
import chardet
import functools
import time

from urllib.parse import quote

from PIL import Image
from pathlib2 import Path
from shutil import copyfile

###############################################################################################################
## Please change the GITHUB_REPO_PREFIX value according to your own GitHub user name and relative directory. ##
###############################################################################################################
# Your image folder remote link
GITHUB_REPO_PREFIX = "https://raw.githubusercontent.com/huangrt01/Markdown-Transformer-and-Uploader/mynote/Notes/"
COMPRESS_THRESHOLD = 5e5 # The threshold of compression

# The main function for this program
def process_for_zhihu():
    if args.compress:
        reduce_image_size()
    with open(str(curfile), 'rb') as f:
        s = f.read()
        chatest = chardet.detect(s)
    print(chatest)
    with open(str(curfile),"r",encoding=chatest["encoding"]) as f:
        lines = f.read()
        lines = image_ops(lines)
        lines = formula_ops(lines)
        lines = table_ops(lines)
        with open(curfile.parent/"Output"/(curfile.stem+".md"), "w+", encoding=chatest["encoding"]) as fw:
            fw.write(lines)
        if not args.only_generate:
            git_ops()

# Deal with the formula and change them into Zhihu original format
def formula_ops(_lines):
     # _lines = re.sub('((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n',
    #                 '\n<img src="http://latex.codecogs.com/gif.latex?\\4" alt="\\4" class="ee_img tr_noresize" eeimg="1">\n', _lines)
    # _lines = re.sub('(\$)(?!\$)(.*?)(\$)',
    #                 ' <img src="http://latex.codecogs.com/gif.latex?\\2" alt="\\2" class="ee_img tr_noresize" eeimg="1"> ', _lines)

    # pattern=re.compile('')
    # pattern.findall(_lines)

    _lines = re.sub('((.*?)\$\$)(\s*)?([\s\S]*?)(\$\$)\n',
                    '\n<img src="https://www.zhihu.com/equation?tex=\\4" alt="\\4" class="ee_img tr_noresize" eeimg="1">\n', _lines)
    _lines = re.sub('(\$)(?!\$)(.*?)(\$)',
                    ' <img src="https://www.zhihu.com/equation?tex=\\2" alt="\\2" class="ee_img tr_noresize" eeimg="1"> ', _lines)
    _lines = re.sub(
        '<img src="https://www.zhihu.com/equation\?tex=([\s\S]*?)" alt', rename_image_ref1, _lines)
   
    
    return _lines


def rename_image_ref1(m):
    result = '<img src="https://www.zhihu.com/equation?tex='+quote(m.group(1))+'" alt'
    return result

# The support function for image_ops. It will take in a matched object and make sure they are compatible
def rename_image_ref(m, original=True):
    global image_folder_path
    if not (Path(image_folder_path.parent/m.group(1)).is_file() or Path(image_folder_path.parent/m.group(2)).is_file()):
        return m.group(0)
    if args.compress and os.path.getsize(image_folder_path.parent/m.group(1+int(original)))>COMPRESS_THRESHOLD:
        if original:
            image_ref_name = Path(m.group(2)).stem+".jpg"
        else:
            image_ref_name = Path(m.group(1)).stem+".jpg"
    else:
        if original:
            image_ref_name = Path(m.group(2)).name
        else:
            image_ref_name = Path(m.group(1)).name
    if original:
        return "!["+m.group(1)+"]("+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/"+image_ref_name+")"
    else:
        return '<img src="'+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/" +image_ref_name +'"'

# Search for the image links which appear in the markdown file. It can handle two types: ![]() and <img src="LINK" alt="CAPTION" style="zoom:40%;" />.
# The second type is mainly for those images which have been zoomed.
def image_ops(_lines):
    # if args.compress:
    #     _lines = re.sub(r"\!\[(.*?)\]\((.*?)\)",lambda m: "!["+m.group(1)+"]("+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/"+Path(m.group(2)).stem+".jpg)", _lines)
    #     _lines = re.sub(r'<img src="(.*?)"',lambda m:'<img src="'+GITHUB_REPO_PREFIX+str(image_folder_path.name)+"/"+Path(m.group(1)).stem+'.jpg"', _lines)
    # else:
    _lines = re.sub(r"\!\[(.*?)\]\((.*?)\)",functools.partial(rename_image_ref, original=True), _lines)
    _lines = re.sub(r'<img src="(.*?)"',functools.partial(rename_image_ref, original=False), _lines)
    return _lines

# Deal with table. Just add a extra \n to each original table line
def table_ops(_lines):
    return re.sub("\|\n",r"|\n\n", _lines)

# Reduce image size and compress. It the image is bigger than threshold, then resize, compress, and change it to jpg.
def reduce_image_size():
    global image_folder_path
    image_folder_new_path = curfile.parent/(curfile.stem+"_for_zhihu")
    if not os.path.exists(str(image_folder_new_path)): 
        os.mkdir(str(image_folder_new_path))
    for image_path in [i for i in list(image_folder_path.iterdir()) if not i.name.startswith(".") and i.is_file()]:
        print(image_path)
        if os.path.getsize(image_path)>COMPRESS_THRESHOLD:
            img = Image.open(str(image_path))
            if(img.size[0]>img.size[1] and img.size[0]>1920):
                img=img.resize((1920,int(1920*img.size[1]/img.size[0])),Image.ANTIALIAS)
            elif(img.size[1]>img.size[0] and img.size[1]>1080):
                img=img.resize((int(1080*img.size[0]/img.size[1]),1080),Image.ANTIALIAS)
            img.convert('RGB').save(str(image_folder_new_path/(image_path.stem+".jpg")), optimize=True,quality=85)
        else:
            copyfile(image_path, str(image_folder_new_path/image_path.name))
    image_folder_path = image_folder_new_path

# Push your new change to github remote end
def git_ops():
    subprocess.run(["git","add","-A"])
    subprocess.run(["git", "commit", "-m", "update file "+curfile.stem])
    subprocess.run(["git","push", "-u", "origin", "master"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Please input the file path you want to transfer using --input=""')

    # RGB arguments
    parser.add_argument(
        '--compress', action='store_true', help='Compress the image which is too large')

    parser.add_argument(
        '--input',
        type=str,
        help='Path to the file you want to transfer.')

    parser.add_argument('--only_generate', action='store_true', default=False)

    args = parser.parse_args()
    if args.input is None:
        raise FileNotFoundError("Please input the file's path to start!")
    elif args.input == 'all' or args.input =='update' :
        cwd=os.getcwd()+'/Notes'
        files = os.listdir(cwd)
        files = [f for f in files if f.endswith(('md'))]
        for file in files:
            curfile="Notes"/Path(file)
            image_folder_path = curfile.parent/(curfile.stem)
            mtime = os.stat(curfile).st_mtime
            outputfile=Path(curfile.parent/"Output"/(curfile.stem+".md"))
            if args.input == 'all' or ((not outputfile.is_file())or mtime > os.stat(outputfile).st_mtime):
                process_for_zhihu()
    else:
        curfile = Path(args.input)
        image_folder_path = curfile.parent/(curfile.stem)
        process_for_zhihu()

        
