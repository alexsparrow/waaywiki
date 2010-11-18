waaywiki
==================

**waaywiki** is a very simple **distributed** wiki. It is intended for use by
small teams or individuals looking for the organisational power of a wiki
without the hassle/expense of setting up a central server. For easy deployment,
the software itself consists of a single python file plus markmin for text
formatting and [[itty https://github.com/toastdriven/itty]] for web serving. The
wiki pages themselves are stored in flat files and [[git
http://www.git-scm.com]] is used for recording history as well as synchronising
users of the wiki.

Note that currently **waaywiki** is not able to push or pull from other git
repositories. For the moment, this needs to be done outside the waaywiki
interface.


WARNING: waaywiki is neither feature complete nor bug-free. Please feel free to
fork and improve :-)
