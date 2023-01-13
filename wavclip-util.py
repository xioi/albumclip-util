from pydub import AudioSegment
import os
import argparse
import yaml
import taglib

def time_to_second( t):
    return t[0] * 3600 + t[1] * 60 + t[2]

def clip_audio( src, dst, t1, t2, format):
    rt1 = t1 * 1000
    rt2 = t2 * 1000
    new_audio = src[rt1:rt2]
    new_audio.export( dst, format = format)

def load_configure( filename):
    with open( filename, 'r', encoding = 'UTF-8') as file:
        yml_dat = yaml.safe_load( file)
    return yml_dat

def parse_time( str):
    processed = str.split( ':')
    hour = 0
    minute = 0
    second = 0

    if( len( processed) == 3):
        hour = processed[0]
        minute = processed[1]
        second = processed[2]
    else:
        minute = processed[0]
        second = processed[1]

    return ( int( hour), int( minute), int( second))

parser = argparse.ArgumentParser( 
    prog = 'wavclip-util',
    description = 'Utility program to clip a wav file into several ones, using a yaml as cinfiguration.',
    usage = 'wavclip-util <configure>.yaml [-d|--directory <outpur directory>]')

parser.add_argument( 'filename')
parser.add_argument( '-d', '--directory', default = '.', required = False)
args = parser.parse_args()
# print( args.filename)

cfg = load_configure( args.filename)
output_dir = args.directory

format = cfg['format'] if ('format' in cfg) else 'wav'
global_album_artist = cfg['album_artist'] if ('album_artist' in cfg) else ''
global_album_year = cfg['year'] if ('year' in cfg) else 0
# album_title = cfg['album'] if ('album' in cfg) else ''
# album_artist = cfg['artist'] if ('artist' in cfg) else ''

# will_add_metadata = (album_artist != '') or (album_title != '')

def export_album( source, album, global_last_point):
    cur_track = 1
    wav_parts = album['parts']
    
    last_point = global_last_point

    album_title = album['title'] if ('title' in album) else ''
    album_artist = album['album_artist'] if ('album_artist' in album) else global_album_artist
    album_year = album['year'] if ('year' in album) else global_album_year
    for part in wav_parts:
        start_point = parse_time( part['from']) if ('from' in part) else last_point
        end_point = parse_time( part['to'])

        name = part['name']
        basename = (part['file'] if ('file' in part) else name) + '.' + format
        filename = os.path.join( output_dir, basename)
        artist = part['artist'] if ('artist' in part) else ''

        last_point = end_point
        print( ' ', name, 'by', album_artist if (artist == '') else artist, '-->', filename)
        # print( name, filename, start_point, end_point)
        clip_audio( origin_wav, filename, time_to_second( start_point), time_to_second( end_point), format)

        tfile = taglib.File( filename)
        tfile.tags['TITLE'] = name
        tfile.tags['TRACKNUMBER'] = str( cur_track)
        if( artist != ''):
            tfile.tags['ARTIST'] = artist
        if( album_artist != ''):
            tfile.tags['ALBUMARTIST'] = album_artist
        if( album_title != ''):
            tfile.tags['ALBUM'] = album_title
        if( album_year != 0):
            tfile.tags['DATE'] = str( album_year)
        tfile.save()
        tfile.close()

        cur_track += 1
    return last_point

wav_source = cfg['origin']
# wav_parts = cfg['parts']

print( 'Loading packed file', wav_source)
origin_wav = AudioSegment.from_file( wav_source)

last_point = (0, 0)
# current_track = 0

# Create output directory if doesn't exist
if( not os.path.exists( output_dir)):
    os.makedirs( output_dir)

albums = cfg['albums']
for album in albums:
    album_title = album['title']
    print( 'Exporting "' + album_title + '"')
    last_point = export_album( origin_wav, album, last_point)
