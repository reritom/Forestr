'''
This module contains tools for dealing with the Media directory
'''
import os, shutil, stat
from django.conf import settings

def get_temp_media_path():
    return os.path.join(settings.MEDIA_ROOT, 'temp')


def delete_dir(identifier):
    '''
        This method checks if the url dir is present
        and deletes it if it is.
    '''
    if 'temp' in os.listdir(settings.MEDIA_ROOT):
        if identifier in os.listdir(os.path.join(settings.MEDIA_ROOT, 'temp')):
            identifier_dir = os.path.join(settings.MEDIA_ROOT, 'temp', identifier)

            os.chmod(identifier_dir, stat.S_IWUSR)
            shutil.rmtree(identifier_dir)

def make_dir(identifier):
    '''
        This method makes a directory for an identifier in the media directory
    '''

    if not 'temp' in os.listdir(os.path.join(settings.MEDIA_ROOT)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'temp'))

    if not identifier in os.listdir(os.path.join(settings.MEDIA_ROOT, 'temp')):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'temp', identifier))

    media_path = os.path.join(settings.MEDIA_ROOT, 'temp', identifier)

    return media_path

def delete_file(name):
    os.remove(name)
