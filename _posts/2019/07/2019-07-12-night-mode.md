---
title: Night mode
layout: post
excerpt_separator: "<!--more-->"
tags: geek jekyll javascript css technotes
categories: Geek
date: '2019-07-12 12:30:00'
---

I've used Night Mode in various web applications, and it's even supported on my MacOS desktop computer, so I thought: can I implement it in this website? Well, you might have noticed a new switch on the top right of this page, which switches Night mode on or off, and that it remembers your choice when going to another page. So, how did I do this?<!--more-->

The first piece of the puzzle was to have a Night Mode stylesheet to overlay the existing stylesheet, so as the existing site was using [Bootstrap](https://getbootstrap.com/) for styling, I looked for any Bootstrap themes that would be suitable for a Night Mode. I found one on [Bootswatch](https://bootswatch.com/) called [Slate](https://bootswatch.com/slate/). Now, the way Bootswatch does themes is that you can download a precompiled Bootstrap CSS file with the theme baked in. (You can also get the source files for the theme if you want to compile the Bootstrap CSS yourself.) You can also get a minimised version of this, which I didn't, for reasons I will explain later.

The styling works in this site in the following order:
1. The original *Minima* styling
2. Bootstrap styling
3. My own customised styling

The Night Mode styling would have to come between steps 2 & 3.

Jekyll is able to compile [SCSS](https://sass-lang.com/) files from the `_sass` folder into a site CSS file, and I used this a lot for my own customised styling, and I wanted to use this for any tweaks I need to make to the Night Mode styling. As this was overlaying the existing Bootstrap styles, I decided to bring the existing Bootstrap CSS file, which was a separate file, into the `_sass` folder, and have it part of the compile site CSS. This is pretty easy as SCSS is backwards compatible with CSS, so I just have to rename the file as a SCSS file, and `@import` it as a partial into the main file. 

The next partials to be imported would be the Night Mode version of Bootstrap, and my tweaks to the theme. Most of the tweaks were basically colour changes for things like the links, although there were the odd bits where the theme changed some of the formatting, so I just commented those out. One good thing about importing the Bootstrap CSS as SCSS beforehand in the compilation process was that I had access to its styling classes, and could use `@extend` in my SCSS to re-use the styles in my own tweaks. One example is me setting the colours of the "Deadjournal" heading, using the existing Bootstrap text "warning" colour class:

```
.site-title {
    @extend .text-warning;
}
```

When I was satisfied with the Night Mode theme, I started implementing a way to switch it on and off. I already had a good idea of how I could do this quite easily: have the Night Mode CSS dependent on the `<body>` tag of the web page having the class `night_mode`. Having brought the Bootstrap and Night Mode theme into SCSS, this was quite easy. All I had to do was put the Night mode SCSS inside `body.night_mode` eg:

```
body.night_mode {

    [... existing SCSS ...]
		
}
```

As you can see, doing it this way in SCSS is far easier than if it was being done in CSS- in CSS, you would have to prepend `body.night_mode` to every blummin' CSS selector! Also, this is why I didn't get the minimised version of the theme, as I need to do some alterations to get this to work. As I've already set SCSS minifying in the `_config.yml` anyway, the final resulting site will have minified CSS, so it doesn't matter if the source is minified or not, but it certainly makes it easier for me! If you haven't turned on SCSS minifying on your site, you can do it by putting the following in your `_config.yml` file.

```
sass:
  style: compressed
```

There is one thing to watch out for: if the theme SCSS contains selectors for `body` tag itself. (Which sets the base background and foreground colours for the web page.) But that's easy to fix: just replace `body` with `&`, and SCSS will interpret that as styling for `body.night_mode`.

So now the site had Night Mode styling that only kicked in when the `<body>` of the web page had the class `night_mode`. (I was able to test this on Chrome browser using the development tools, by going into the *Elements* tab, and adding `class="night_mode`, and checking the Night Mode was kicking, then removing the class, and checking the default styling returned.) The next step was to add functionality to web page to switch the Night Mode on and off.

I already had a good idea I wanted to do a sliding switch, which I had implemented in a previous project. This had used a Bootstrap extension which styled a checkbox as a sliding switch. So the first I did was put a checkbox on the top navigation and give it an id `night_mode_toggle`. So it was quite easy to add to the main site Javascript:

```
var body = $('body');

[...]

$('#night_mode_toggle').click( toggleNightMode );

[...]

function toggleNightMode() {
  if ($(body).hasClass('night_mode')) 
    nightModeOff();
  else 
    nightModeOn();
}

function nightModeOff() {
  $(body).removeClass('night_mode');
}

function nightModeOn() {
  $(body).addClass('night_mode');
}
```

You can see I'm using [Jquery](https://jquery.com/) here to manipulate the `body` tag, and set the even for the checkbox. Anyway, this worked, and I was able to turn the Night Mode on and off using the checkbox. Next was making sure the browser remembers this choice, and the obvious choice here is to use cookies: send the browser a cookie if in Night Mode, and check for a cookie coming back that specified Night Mode was switched on. Again, this was fairly easy. I used the [JS Cookie](https://github.com/js-cookie/js-cookie) library for this, which made it much easier to handle and check for cookies.

```
var mode = Cookies.get('night_mode');
if (mode != undefined)
if (mode == "true") {
  [...]
}
	
[...]
	
function nightModeOff() {
  $(body).removeClass('night_mode');
  Cookies.set('night_mode', 'false');	
}

function nightModeOn() {
  $(body).addClass('night_mode');
  Cookies.set('night_mode', 'true');
}
```

So now the browser was remembering Night Mode between pages, all I had to do was style the checkbox. For this I used [Bootstrap 4 Toggle](https://gitbrent.github.io/bootstrap4-toggle/), a variation on a toggle slider I had used before. Rather bizarrely this caused the most difficulties. Firstly, I found the click event was broken. This was because the toggle appeared on top of the checkbox, obscuring it, so I had to the set the click event for *that* element, which was the parent element of the checkbox. This would mean some alterations to the Javascript, which took a lot less effort than tracking down the actual problem. eg

```
$('#night_mode_toggle').parent().click( toggleNightMode );
```

I also had to hack around a bit to get the styling right. Some of it was partly because of formatting issues that had crept into the CSS via the Night Mode styling, so I had to go around turning various styles on and off before I finally found what was messing things up, and turn that off for the Night Mode style. I also set the visibility of the original checkbox to hidden, so that the checkbox wouldn't appear only to disappear and be replaced by toggle.

So that is that! I now have a Night Mode switch for this website.

There are a couple of things I think I could improve about it. Most obvious is that if Night has been selected, the next you load another page, it starts in default mode, then switches to Night Mode, leading to a flash at the start of each page as it goes from default to Night Mode. If you were running this off a server generated page, you could set the body class to Night Mode as the page is being served, but on a static site like you don't have that option. I've got a possible idea about how to achieve this, and if I actually get it to work, I'll let you know! Other improvements would be small things like making the transition between modes more smooth (I've already added a transistion to the colour changes.), and maybe changing the text on the toggle to icons to make it smaller, but we'll see what happens.

**UPDATE**: I've actually been able to fix the "flash" issue. I describe how I did it in [this post]({{"/2019/07/12/a-better-night.html"|relative_url}}).