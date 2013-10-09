# Youtube Lookup #

## A scripted lookup that gets the information for a video by its video-id ##

How it works:
---------------------------------------------------------
This Splunk App provides a scripted lookup that take the video-id from a youtube URL, and uses the youtube API to get information about the video such as title, duration, description, etc.

Simply define which splunk field is your 'video-id' from the extracted data, and call it 'video-id' and then pass that to the lookup

` | eval video-id=v`
` | lookup youtube video-id `

With it all together

`index=proxy_logs  request=*www.youtube.com/watch?v* | eval video-id=v | lookup youtube video-id`

Where is the video-id in the youtube URL?
-----------------------------------------------------------

The video id in the url it typically - "http://www.youtube.com/watch?v=<video-id>", "http://www.youtube.com/watch?v=oHg5SJYRHA0"

Splunk might already be extracting the "v" since it does so automatically with key=value pairs in URLs


What fields are available for me after the lookup?
------------------------------------------------------------

1. video-title  --   The title of the video
2. video-category -- The category of the video on youtube
3. video-description -- The description of the video on youtube
4. video-duration-seconds -- The duration of the video in seconds on youtube
5. video-published -- The date the video was published to youtube
6. video-view-count -- How many times the video has been viewed on youtube


 

