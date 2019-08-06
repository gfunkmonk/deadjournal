# Deadjournal
### It's Livejournal, but not as we know it

[Deadjournal](https://alephnaughtpix.github.io/deadjournal/) is a recreation of my old Livejournal blog, but not on 
Livejournal, (as that's now on a Russian server) as well as an ongoing experiment into the delights of maintaining a blog based 
on the Jekyll system and hosted on GitHub pages.

The site uses [Jekyll](https://github.com/jekyll), and incorporates 
[Jekyll Admin](https://github.com/jekyll/jekyll-admin) and [Jekyll Feed](https://github.com/jekyll/jekyll-feed). 
My old Livejournal posts (2006-2011) were extracted from my LJ account using 
[LJDump](https://hewgill.com/ljdump/). I'm using [Bootstrap](https://getbootstrap.com/) for formatting, 
[Jquery](https://jquery.com/) for extra UI tasks, [JSCookie](https://github.com/js-cookie/js-cookie) for cookie handling, 
and [Bootstrap 4 Toggle](https://gitbrent.github.io/bootstrap4-toggle/) for the Night Mode switch. The actual Night Mode 
styling is based on the [Slate](https://bootswatch.com/slate/) theme from [Bootswatch](https://bootswatch.com/).

## Requirements
* [Ruby](https://www.ruby-lang.org/en/)
* [Git](https://git-scm.com/) (I also use [GitKraken Git Client](https://www.gitkraken.com/) on top of this, but you can use any GUI, or none at all, if you're a hardcore command line type.)
* [Bundler](https://bundler.io/) (You can install this via Ruby- see below.)

## Install and Build
* If you have Ruby installed, but not Bundler, you can install Bundler from the command line:
  ```gem install bundler```
* Create a directory for your local copy of the site, and navigate to it in the command line.
* Clone the site from GitHub:
  ```git clone https://github.com/alephnaughtpix/deadjournal.git```
* Install Jekyll and additional software:
  ```bundle install```

## Running locally
I've included scripts for running and building the site locally in `scripts/windows` and `scripts/linux`. (Which also works on MacOS) the two scripts are:
* `build`: Run a full build of the Jekyll site, including generating tags and categories pages. The site is saved to the folder `_site`. Note that this folder is not under source control.
* `runserver_dev`: Run an incremental build, and start a local web server serving the built site. 

To browse the site, go to http://localhost:4000/. The port number can be configured in the `_config.yml` setting `port`. 

The admin can be accessed at http://localhost:4000/admin . Note that the admin only can run locally as a dev site- it will not appear on the published website. (Thank goodness!)

## Publishing
You have two options:
1. Manual:
   * Run a full build.
   * Transfer all the files from the `_site` folder to your website host via FTP.
2. Host your published site on [GitHub pages](https://pages.github.com/). 
   * Set up an account at GitHub. (Which you probably already have, if you're reading this!)
   * Set up your own Git repository, and copy the files from this repo into it.
   * Now all you need to do, each time you want to publish, is push the changes to your repository, and GitHub will automatically publish your website to GitHub pages! You can find out more about setting up GitHub pages [here](https://pages.github.com/).

