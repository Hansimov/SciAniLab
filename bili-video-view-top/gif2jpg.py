import os
from shutil import copyfile
# if not os.path.exists('pics'):
#     os.mkdir('pics')

def convertGIFToJPG(rootpath):
    for filename in os.listdir(rootpath):
        if filename.endswith('.gif'):
            # print(filename)
            filename_body = os.path.splitext(filename)[0]
            # print(filename_body)
            if os.path.exists('./{}/{}.jpg'.format(rootpath,filename_body)):
                print('Existed: {}.jpg'.format(filename_body))
                pass
            else:
                print('Converting {} to {}.jpg ...'.format(filename, filename_body))
                os.system('F:/Technology/ImageMagick/convert.exe -monitor ./{}/{}[0] ./{}/{}.jpg'.format(rootpath, filename, rootpath, filename_body))
                # Some up has no face image
                # You can get the noface.gif from the mid with an 'failed' gif,
                #   then convert the noface.gif to noface.jpg.
                if not os.path.exists('./{}/{}.jpg'.format(rootpath, filename_body)):
                    print('Copying noface.jpg to {}.jpg ...'.format(filename_body))
                    copyfile(f'./{rootpath}/noface.jpg', './{}/{}.jpg'.format(rootpath, filename_body))

if __name__ == '__main__':
    convertGIFToJPG('pic')
    convertGIFToJPG('face')