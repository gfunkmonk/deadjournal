---
title: The Shipping Forecast in Python
layout: post
excerpt_separator: "<!--more-->"
tags: python shippingforecast code speech radio geek
categories: Geek
---

No, that's not a cute *look at me!* headline, I really am going to talk about your actual [Shipping Forecast](https://en.wikipedia.org/wiki/Shipping_Forecast) in [Python](https://www.python.org/). I told you I was super-geeky<!--more-->...

Now, I listen to a number of podcasts, all spoken word ones, so it's a bit like I have my own custom made [Radio 4](https://en.wikipedia.org/wiki/BBC_Radio_4). So why not round it off with one of Radio 4's most famous and quirky features, the [Shipping Forecast](https://en.wikipedia.org/wiki/Shipping_Forecast)? 

Well, that's a problem, as you can't get the Shipping Forecast as a podcast. You *can* get it on [iPlayer](https://www.bbc.co.uk/programmes/b006qfvv/episodes/player), but it tends to be bookended by adverts for other Radio 4 programmes. Even more crucially, due to copyright issues, the replay of the nightime broadcast misses out the beautiful *"Sailing By"* by Ronald Binge, which is used to fill in time before the actual forecast, which has to start on the dot at 2348h.

After reading about [this Raspberry PI based project](https://www.instructables.com/id/Pi-Zero-Talking-Radio/), which used an old converted radio as a kind of simplified Alexa, I thought about doing something similar, gathering notifications from the internet, but also reading articles from RSS feeds, and maybe even podcasts. The idea of reading articles in a text-to-speech format made me wonder: can I do something similar with Shipping Forecast? Since I would be control of the sound, maybe even add in *"Sailing By"* beforehand?

It turns out the Shipping Forecast does have an [RSS feed](https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest) on the [Met Office](https://www.metoffice.gov.uk/)'s website.  If you go to it, you see something like this:

```xml
<report xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" creation-time="2019-10-21T11:27:00">
<title>Shipping forecast</title>
<issue date="2019-10-21" time="1030"/>
<gales>
<shipping-area>Viking</shipping-area>
<shipping-area>North Utsire</shipping-area>
<shipping-area>Rockall</shipping-area>
<shipping-area>Hebrides</shipping-area>
<shipping-area>Bailey</shipping-area>
<shipping-area>Fair Isle</shipping-area>
<shipping-area>Faeroes</shipping-area>
<shipping-area>Southeast Iceland</shipping-area>
</gales>
<general-synopsis>
<valid time="0600"/>
<gs-text>
Low Iceland 989 moving steadily northeast expected 250 miles north of Norwegian Basin 967 by 0600 tomorrow. Low France 1010 losing its identity. New high expected France 1024 by same time
</gs-text>
</general-synopsis>
<area-forecasts period="24" total-num="17">
<area-forecast>
<all>Viking, North Utsire</all>
<wind>Southwesterly 4 or 5, increasing 6 to gale 8.</wind>
<seastate>
Slight or moderate, becoming rough, then occasionally very rough later in north.
</seastate>
<visibility>Moderate or good, occasionally poor</visibility>
<weather>Rain at times.</weather>
<area>
<seastate>
Slight or moderate, becoming rough, then occasionally very rough later in north.
</seastate>
<visibility>Moderate or good, occasionally poor.</visibility>
<weather>Rain at times.</weather>
<wind>Southwesterly 4 or 5, increasing 6 to gale 8.</wind>
<main>Viking</main>
<sub/>
</area>
<area>
<seastate>
Slight or moderate, becoming rough, then occasionally very rough later in north.
</seastate>
<visibility>Moderate or good, occasionally poor.</visibility>
<weather>Rain at times.</weather>
<wind>Southwesterly 4 or 5, increasing 6 to gale 8.</wind>
<main>North Utsire</main>
<sub/>
</area>
</area-forecast>
<!-- ... And so on ... ->
```

That might look very different to what your hear on Radio 4, but as [explained here](https://en.wikipedia.org/wiki/Shipping_Forecast#Broadcast_format), the broadcast format of the Shipping Forecast is tightly regulated, so it's actually very easy to parse the RSS into the broadcast script.

As the RSS feed is an [XML](https://en.wikipedia.org/wiki/XML) file, I figured the best way to parse it would be to use [XSLT](xslt w3schools) to tranform it into human readable text. That way, I could later use different XSLT stylesheets for different RSS feeds without having to change the underlying code. Also, I could download an example RSS file, and link it to my stylesheet, and then I could load the RSS file into my browser, and test the XSLT stylesheet without having to write a line of code. 

To link the XSLT file to the RSS file, add the `xml-stylesheet` directive, with the filename of the stylesheet, to the RSS file just after XML declaration at the top.

```xml
<?xml version="1.0" ?>
<?xml-stylesheet type="text/xsl" href="convert.xsl"?><!-- Change to whatever the stylesheet file is called --->
```

### The XSLT stylesheet

In XSL, you can take an XML file, and parse various elements of it. There are also various basic workflow and and conditional statements. With complex XML data, this can lead to a lot of fiddly code in XSL, but thankfully the Met Office's RSS feed for the Shipping forecast is not complex, and has all the data we need, with minimal faffing about.

Everything in the forecast is contained within the tag `report`, so we start by matching that:

```xml
<xsl:template match="/report">
```

Now can start the forecast and insert the time of the forecast, which contained in the `time` attribute of the tag `issue`.

```xml
And now the Shipping Forecast, issued by the Met Office on behalf of the Maritime and Coastguard Agency at <xsl:value-of select="issue/@time"></xsl:value-of> today.
```

The next part of the forecast involves gale warnings, if there are any. These are contained within the tag `gales`, which contains a list of one or more `shipping-area` tags. This is probably the most fiddly part of the parsing, as you have to cope with the conditions if there no gale warnings, or whether there are one, two or more areas in the warning.

The first part is easy. First, check if there are any `gales` tags, and check there are `shipping-area` tags within that. (Note that `&gt;` means `>`. eg `count(gales) > 0`.  We have to use `&gt;` and `&lt;` instead of `<` and `>` because XML.)

```xml
<xsl:if test="count(gales) &gt; 0">
	<xsl:if test="count(gales/shipping-area) &gt; 0">
		...
	</xsl:if>
</xsl:if>
```

If there is one `shipping-area` tag, say "There **is** a gale warning for `shipping-area`." (Note that XML element indexing starts at 1.)

```xml
<xsl:if test="count(gales/shipping-area) = 1"> 
	There is a gale warning for <xsl:value-of select="gales/shipping-area[1]"></xsl:value-of>.
</xsl:if>
```

If there are more than one `shipping-area` tags, say "There **are** gale warning for `shipping-area` [1], `shipping-area` [2], [... and the rest before the second last...] `shipping-area` [second-last] and  `shipping-area` [last]." This covers if there's just two areas, or if there's more.

```xml
<xsl:if test="count(gales/shipping-area) &gt; 1">
	There are gale warnings for 
	<xsl:for-each select="gales/shipping-area[position() &lt; last() - 1]">
		<xsl:value-of select="."></xsl:value-of>, 
	</xsl:for-each>
	<xsl:value-of select="gales/shipping-area[last() - 1 ]"></xsl:value-of> 
	and 
	<xsl:value-of select="gales/shipping-area[last()]"></xsl:value-of>.
</xsl:if>
```

Next is the general synopsis. This is quite easy, as we just have to extract the time for the synopsis (In the `time` attribute of the tag `general-synopsis/valid`), and the text. (in `general-synopsis/gs-text`.)

```xml
The General Synopsis at <xsl:value-of select="general-synopsis/valid/@time"></xsl:value-of>:
<xsl:value-of select="general-synopsis/gs-text"></xsl:value-of>.
```

Finally, the area forecasts. These are contained within the `area-forecasts` tag, which contains a series of `area-forecast` tags. As with the broadcast version, areas with similar conditions are grouped together, which makes our job easier. (You *can* isolate individual areas if you want, as these are included as `area` tags within the `area-forecast` tag, but that's not how Radio 4 does it, so we don't need to worry about it here.)

The `area-forecast` contains the following tags that we need:
1. `all` contains the area names.
2. `wind` contains the wind conditions.
3. `weather`- guess.
4. `visibility`- again, guess.

The `area-forecast` also contains `seastate`, but this is not used in the broadcast version.

So all we need to do now is for a XSL for loop on all the `area-forecast` tags.

```xml
<xsl:for-each select="area-forecasts/area-forecast">
	<xsl:value-of select="all"></xsl:value-of>: 
	<xsl:value-of select="wind"></xsl:value-of>.
	<xsl:value-of select="weather"></xsl:value-of>.
	<xsl:value-of select="visibility"></xsl:value-of>.
</xsl:for-each>
```

And then, to complete the translation, I added a sign-off. This is not strictly part of the broadcast version, but most presenters do it, and it's better than suddenly stopping dead.

```xml
And that's the Shipping Forecast.
```

### Saving to a human readable text file

Now that my XSLT stylesheet was working, I needed a way to save to a human readable text file for further processing. As I was looking to eventually get it working on a Raspberry Pi, I figured Python 3 would be a good bet. I used the python library [lxml](https://lxml.de/) and the inbuilt [requests](https://realpython.com/python-requests/) library to download the RSS from the Met Office website, translate it, and output as human-readable text. You'll notice that after downloading, I strip any excess spaces, and remove the XML header that gets added as part of the translation. The filename of the XSLT stylesheet is contained within the variable `xsl_filename`.

```python
import requests
import lxml.etree as ET
import os
import os.path

source_url = 'https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest'    # URL of Shipping Forecast feed
xml_filename = 'source.xml'         # Saved RSS of Shipping Forecast
xsl_filename = 'translate.xsl'      # Translates RSS to human readable text
script_filename = 'script.txt'      # Human readable version of Shipping Forecast

# Get Shipping Forecast RSS
response = requests.get(source_url)
source_text = response.text

# Save on local system
file = open(xml_filename,'w')
file.write(source_text)
file.close()

# Translate Shipping forecast RSS to human readable text for Text to Speech
dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
output = " ".join(str(newdom).split())                  # Strip extra spaces
output = output.replace('<?xml version="1.0"?>', '')    # Remove XML header.
file = open(script_filename,'w')
file.write(output)
file.close()
```

Running this script will create a file called `script.txt`, which will contain something like the following.

```
 And now the Shipping Forecast, issued by the Met Office on behalf of the Maritime and Coastguard Agency at 1030 today. There are gale warnings for Viking, North Utsire, Rockall, Hebrides, Bailey, Fair Isle, Faeroes and Southeast Iceland. The General Synopsis at 0600: Low Iceland 989 moving steadily northeast expected 250 miles north of Norwegian Basin 967 by 0600 tomorrow. Low France 1010 losing its identity. New high expected France 1024 by same time. The Area Forecasts for the next 24 hours: Viking, North Utsire: Southwesterly 4 or 5, increasing 6 to gale 8.. Rain at times.. Moderate or good, occasionally poor. South Utsire, Forties, Cromarty, Forth: Variable 3, becoming southwesterly 4 to 6, increasing 7 at times in Cromarty and Forth.. Mainly fair.. Good. Tyne, Dogger: Northeast backing west, 4 or 5, occasionally 6 later.. Fair.. Good. Fisher: Variable 2 to 4, becoming southwest 4 to 6 later.. Fair.. Good. German Bight, Humber, Thames: Northeast becoming cyclonic, then becoming west later, 4 to 6, occasionally 7 at first.. Occasional rain.. Good, occasionally poor. Dover, Wight: Cyclonic 5 to 7, becoming north 3 or 4, then becoming variable later.. Occasional rain.. Good, occasionally poor. Portland, Plymouth: Northeast 3 or 4, becoming variable 3 or less later.. Showers.. Good. Biscay: Cyclonic in south, otherwise northeasterly, 3 to 5.. Thundery showers.. Good, occasionally poor. South Fitzroy: Northerly 4 to 6.. Thundery showers.. Good, occasionally poor. North Fitzroy, Sole, Lundy, Fastnet: Northerly 4 to 6, becoming variable 3 or 4.. Showers.. Good. Irish Sea: North backing west or southwest, 3 to 5.. Fair.. Good. Shannon, Southeast Rockall: Variable 4, becoming southwesterly 5 to 7.. Fair.. Good. Northwest Rockall: Southwesterly 6 to gale 8.. Rain.. Good, occasionally poor. Malin: Southwest 4 or 5, increasing 6 or 7.. Fair.. Good. Hebrides, Bailey: Southwesterly, veering northeasterly later in north, 6 to gale 8, occasionally severe gale 9 at first.. Rain.. Moderate or poor. Fair Isle: Southwesterly 6 to gale 8, occasionally severe gale 9 at first, then veering northeasterly 4 to 6 later in north.. Rain.. Good occasionally poor. Faeroes, Southeast Iceland: Southwesterly, veering northerly, then veering northeasterly later, 6 to gale 8, occasionally severe gale 9 at first.. Occasional rain.. Good, occasionally poor. Trafalgar: North 4 to 6.. Thundery showers.. Good, occasionally moderate.. And that's the Shipping Forecast.
```

### Turning the text into speech

Now that we have a human readable version, how about getting a voice to read it? I investiagted the options for text to speech in Python through [this article](https://pythonprogramminglanguage.com/text-to-speech/), and tried out a few things. Firstly, I tried [Pyttsx3](https://github.com/nateshmbhat/pyttsx3), but I found that a bit robotic, and as it depends on the system speech engine, it can be variable across different systems. [IBM Watson](https://text-to-speech-demo.ng.bluemix.net/) has a more natural sound, but it requires a lot of faffing about to get going, and has a limitation on the number of requests, after which you have to pay IBM. In the end I settled on Google Text to Speech through the [gTTS](https://github.com/pndurette/gTTS) library. This only has once choice of voice, but is very natural sounding.

Getting the text saved as speech turned out to be very simple.

```python
from gtts import gTTS 

source_mp3 = "speech.mp3"           # Text to speech result

'''

Translate the file- remember that the translated text is already contained in the variable 'output'!

'''

# Google Text to speech
engine = gTTS(text=output, lang='en-UK', slow=False) 
engine.save(source_mp3)
```

So now we have the Shipping Forecast saved as a spoken word MP3 file. You might notice that the voice, although very natural sounding can have a bit of an [uncanny valley](https://en.wikipedia.org/wiki/Uncanny_valley) effect. For example, I find the gale warnings sound a bit sarcastic, any mentions of gale force 8 sound a bit like Chris Morris on *The Day Today*, the use of the word "rain" sounds a bit strange, and for some reason Google appears to find *"Fair Isle"* a bit chuckleworthy! More about the voice later...

### Adding the the theme tune
But what would the Shipping Forecast be without having Ronald Binge's *Sailing By* to start it off? What I wanted was to have an MP3 that started off with *Sailing By*, and then had the Forecast begin just as the song ended. After a bit of searching around, I settled on [PyDub](https://github.com/jiaaro/pydub) to do the deed.

```python
from pydub import AudioSegment
```

Next I obtained an MP3 of *Sailing By*, which can be obtained from various sources. Using PyDub, the two MP3s can be loaded into `Audiosegment` objects. You might notice I'm using PyDub's `normalise` function to even up the levels of both files. The significance of this will come later...

```python
source_mp3 = "speech.mp3"           # Text to speech result
theme_mp3 = "sailingby.mp3"         # "Sailing By" by Ronald Binge.
combined_file = "output_with_theme.mp3"

# ... Process RSS, save as MP3 etc ...

theme_src = AudioSegment.from_mp3(theme_mp3).normalize() 
feature_src = AudioSegment.from_mp3(source_mp3).normalize() 
```

Next, I wanted to combine the two. PyDub allows you to overlay two or more Audiosegments onto another. As Audiosegments are immutable objects, this means you have to create a blank Audiosegment object to overlay them to, and the tricky bit is that you have to specify the length of that blank object in advance. Usually that just means adding the length of the two MP3 files together. However, I wanted the Forecast to start just as *Sailing By* ends. After a bit of testing, I found that this point was 6 seconds before that MP3 ended, so I would have to determine where that point was in time, and factor that into the combined length calculations. (Note that Audiosegment lengths are measured in milliseconds.)

```python
programme_start = len(theme_src) - (6 * 1000)                   # Speech starts 6 seconds before the theme is complete
programme_length = programme_start + len(feature_src)           # Combined length of two files minus 6 seconds
```

Now I had the length and where the Forecast started, it was easy to create a new blank Audiosegment, and overlay the two MP3 files onto it.

```python
playlist = AudioSegment.silent( duration=programme_length )     # New blank segment with programme length
programme = playlist.overlay(theme_src).overlay(feature_src, position=programme_start)  # Overlay theme and speech onto blank segment
```
After that, exporting the combined result to an MP3 file was easy:

```python
programme.export(combined_file, format="mp3")
```

### But- that voice!

Now I had Python code that could generate the Shipping Forecast complete with theme music, was there anything I could about the voice? After experimenting around with the results in [Audacity](https://www.audacityteam.org/), I found that it sounded much better pitch-shifted down 4 semitones, which gave a more plummy and camp tone to it. Now all I had to was work out how to do the pitch-shifting in Python. The bad news was that PyDub had a number of inbuilt effects, but pitch-shifting was not one of them. I would have to look elsewhere.

After a lot of faffing about trying to look for a solution, (Why do so many people think pitch-shifting is the same as speeding a sample up or down?) I settled on using [PyRubberband](https://pyrubberband.readthedocs.io/), which also uses [Numpy](https://numpy.org/) and [PySoundfile](https://pysoundfile.readthedocs.io/). 

Slotting the pitch-shift code inbetween the generation of the forecast speech MP3 and merging the speech with the theme was a little onerous. PySoundfile does not load MP3 files, which is a bit of a problem as that's what Google Text to Speech outputs! So what I had to do was load the MP3 file using PyDub, which luckily can output the file data for third party data manipulation, and then convert to a Numpy array, which PyRubberband can handle, then use PySoundfile to output the result as a FLAC file. (Which PyDub *can* load.) Also as part of the process the sample rate of the speech file needs to be determined, but PyDub can handle this.

```python
import numpy as np
import pyrubberband as pyrb
import soundfile as sf

source_mp3 = "speech.mp3"           # Text to speech result
pitch_file = "output_pitch.flac"    # Pitch-shifted Text to speech result

# ... Translate RSS, Generate speech, etc ...

word_src = AudioSegment.from_mp3(source_mp3)
sample_rate = word_src.frame_rate
samples = np.array(word_src.get_array_of_samples())
pitched_down = pyrb.pitch_shift(samples, sample_rate, n_steps=-4)
sf.write(pitch_file, pitched_down, sample_rate)

# ... Merge results with theme music etc ...
```

If you listen to the FLAC generated, you'll notice the volume is way down compared to the source file, but don't worry, we'll fix that in the next step!

Now that the pitch-shifted speech file has been generated, all that needs to be done is change the line which loads the speech (Before being merged with the theme), as the input file is now a FLAC file rather then an MP3 file. 

```python
feature_src = AudioSegment.from_file(pitch_file).normalize()
```
The `normalize` bit at the end now makes more sense now, doesn't it? Once it's normalised, the speech file's volume will have been restored.

### And that, finally, is that!
After that, I did some cleaning up of the code, and added a few options. You can view the completed code on my GitHub account [here](https://github.com/alephnaughtpix/shippingforecast). The code is in the file `process.py`. Although this is  "just" the Shipping Forecast, in the process I learned a lot of about audio manipulation in Python, and the code I've written could easily be refactored to work with other RSS feeds to become a more generic text to speech reader, and then... Who knows?