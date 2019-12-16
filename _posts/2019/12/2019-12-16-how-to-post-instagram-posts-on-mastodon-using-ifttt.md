---
title: How to post Instagram posts on Mastodon using IFTTT
layout: post
excerpt_separator: "<!--more-->"
tags: code geek mastadon ifttt instagram
categories: Geek
---

*This post was originally published on my old [Tumblr](https://alephnaughtpix.tumblr.com/post/177232593842/how-to-post-instagram-posts-on-mastodon-using), but it seemed more appropriate for this place, so...*

A lot of people are starting to join **[Mastodon](https://joinmastodon.org/)** these days as an alternative to Twitter, because of it’s perceived benefits of community and local moderation over Twitter’s centralised structure and problems with moderating hate speech and harrasment. (Although, as **[Sage Sharp](https://twitter.com/_sagesharp_)** notes on Twitter, [this is dependent on picking the right community, or “instance” in Mastodon, that supports you](https://twitter.com/_sagesharp_/status/1030112338836221953).)

I’m currently on [one](https://mastodon.cloud/@alephnaughtpix) of the main active instance of Mastodon to try a few things out before moving to another instance, and one of the things that I been trying out is seeing if I can post my latest Instagrams on Mastodon the way I can on Twitter.
<!--more-->
For Twitter, I use a service called **[If This, Then That](https://ifttt.com/)** (IFTTT). On IFTTT, you can set up “applets” that carry out operations, such as *“I post a picture on Instagram, publish it on Twitter”*. Now IFTTT directly supports both Instagram and Twitter, so it’s easy to set up such an operation. However, it doesn’t support Mastodon directly, so it is possible to post Instagram posts on Mastadon? Well, yes it is. (I want to thank [**Kelson Vibber**’s article](https://www.hyperborea.org/journal/2017/12/mastodon-ifttt/) for pointing me in the right direction.)

Here’s how you do it:

1. Log into into IFTTT, and go to Webhook Settings, make sure it’s turned on.
2. Log onto Mastadon, go to “Edit Profile”.
3. On the left hand menu, select “Development”.
4. Select “Your applications”, and then the “New Application” button.
5. Fill in the application name (eg “IFTTT Instagram”), and “https://maker.ifttt.com/” for Application website.
6. Under "scope", make sure only “write:statuses” is ticked.
7. Select “Submit”.
8. Select the application you created, and copy the access token labelled “**Your access token**”. You’ll need this later.
9. Go back onto IFTTT, and click “New applet”.
10. For “If this”, select “Instagram”. (There’s a dynamic search at the top, so you just need to type in “ins” there, and Instagram will be at the top.)
11. For “Choose trigger”, select “Any new photo by you”.
12. For “Then That” select “Webhooks”, and then “Make a web request”.
13. For “URL” use “https://**[YOUR MASTADON INSTANCE]**/api/v1/statuses?access_token=**[YOUR ACCESS TOKEN]**”
14. For “Method” use “POST”.
15. For “Content-type” use “application/x-www-form-urlencoded”.
16. For “Body” use “status=**[TEXT TO POST TO MASTADON]**” for example, I use “status=New on Instagram: **{% raw %}{{Caption}} {{Url}}{% endraw %}**”. The stuff in curly brackets are “ingredients” In IFTTT, which in this case are the title of the photo and the URL to the Instagram page it’s on. You can find other “ingredients” by clicking on the “Add ingredient” button. Note that the “EmbedCode” doesn’t work on Mastadon.
17.  Select “Create Action”.
18.  At this point, IFTTT will ask you to log into Mastodon, and approve the applet from Mastodon.
19.  Give the applet a nice sensible name.

And that should be that! Now you can test it out by posting a pic to Instagram, go into your newly created app in IFTTT, and clicking “Check now”, and then checking on Mastadon to see it has posted your pic.