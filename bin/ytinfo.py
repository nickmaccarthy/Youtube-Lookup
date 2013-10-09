import json
import os,sys
import urllib, urllib2
import csv
import logger
import traceback

DEBUG_MODE = False 

def process_csv_stream( input, output ):

    global DEBUG_MODE

    reader = csv.DictReader( input )
    headers = reader.fieldnames
    if not headers: return

    output_headers = ['video-id', 'video-title', 'video-description', 'video-published', 'video-category', 'video-duration-seconds', 'video-view-count']
    writer = csv.DictWriter(output,fieldnames=output_headers)
    # output our headers
    writer.writeheader()

    # make the API call to youtube and get the video info
    for row in reader:

        if DEBUG_MODE:
            logger.info('in row: %s' % ( row ))

        vid_info = get_video_info( row['video-id'] )

        writer.writerow(vid_info)

    

def get_video_info( video_id ):

    global DEBUG_MODE 

    if DEBUG_MODE:
        logger.info('video_id given in get_video_info(): %s' % ( video_id ))

    try:

        response = urllib2.urlopen(('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % ( video_id )), timeout=2)

        myjson = json.load(response)

        title = myjson['entry']['title']['$t']
        description = myjson['entry']['media$group']['media$description']['$t']
        published = myjson['entry']['published']['$t']
        category_label = myjson['entry']['category'][1]['label']
        duration = myjson['entry']['media$group']['yt$duration']['seconds']
        view_count = myjson['entry']['yt$statistics']['viewCount']
    
        my_dict = { 'video-id': video_id, 'video-title': title, 'video-description' : description, 'video-published' : published, 'video-category': category_label, 'video-duration-seconds' : duration, 'video-view-count' : view_count }

    except Exception, e:

        error = "error getting JSON from youtube: %s " % ( e )

        my_dict = { 'video-id': video_id, 'video-title': error, 'video-description' : error, 'video-published' : error, 'video-category' : error, 'video-duration-seconds': error, 'video-view-count' : error }


    if DEBUG_MODE:
        logger.info('output_dict: %s' % ( my_dict))

    return my_dict      

# Get the party started
if __name__ == "__main__":

    logging = logger.logger()
    logger = logging.get_logger('youtube_lookup')

    if DEBUG_MODE:
        logger.info('sys argv: %s' % ( sys.argv ))
        logger.info('sys.stdin: %s' % ( sys.stdin))
        
    ## CSV will come from splunk via STDIN, and we will output ours via STDOUT
    process_csv_stream(sys.stdin, sys.stdout)

    sys.exit(0)
