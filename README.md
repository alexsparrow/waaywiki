waaywiki
==================

Description
-------------------
**waaywiki** is a very simple git-based **distributed** wiki. It is intended for
use by small teams or individuals looking for the organisational power of a wiki
without the hassle/expense of setting up a central server. For easy deployment,
the software itself consists of a single python file plus markmin for text
formatting and [itty](https://github.com/toastdriven/itty) for web serving. The
wiki pages are stored in flat files within a [git](http://www.git-scm.com)
repository.

Getting it
-----------------
**waaywiki** should be able to run out of the box:
     git clone git@github.com:alexsparrow/waaywiki.git
     # Fetch itty
     git submodule init
     git submodule update

Status
------------------
**WARNING:** waaywiki is neither feature complete nor bug-free. Please feel free
to fork and improve :-)

Here are the currently supported features:
*  Basic wiki functionality: create/edit pages
*  Markup with markmin
*  Versioning with git
*  View history, revert and view previous versions

Here are some things in particular that need doing:
*  Delete pages
*  Add attachments
*  Improve the interface
*  git push/pull and diff/merge interface
*  Themes/customisation
*  Markdown/reStructured text support
*  PDF export
*  Search/tags/index etc.

