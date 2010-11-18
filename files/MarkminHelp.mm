## Examples

### Bold, italic, code and links

--------------------------------------------------
**SOURCE**                 | **OUTPUT**
``# title``                | **title**
``## section``             | **section**
``### subsection``         | **subsection**
``**bold**``               | **bold**
``''italic''``             | ''italic''
``!`!`verbatim`!`!``       | ``verbatim``
``http://google.com``      | http://google.com
``[[click me #myanchor]]`` | [[click me #myanchor]]
---------------------------------------------------

### More on links

The format is always ``[[title link]]``. Notice you can nest bold, italic and code inside the link title.

### Anchors [[myanchor]]

You can place an anchor anywhere in the text using the syntax ``[[name]]`` where ''name'' is the name of the anchor.
You can then link the anchor with [[link #myanchor]], i.e. ``[[link #myanchor]]``.

### Images

[[some image http://www.web2py.com/examples/static/web2py_logo.png right 200px]]
This paragraph has an image aligned to the right with a width of 200px. Its is placed using the code

``[[some image http://www.web2py.com/examples/static/web2py_logo.png right 200px]]``.

### Unordered Lists

``
- Dog
- Cat
- Mouse
``

is rendered as
- Dog
- Cat
- Mouse

Two new lines between items break the list in two lists.

### Ordered Lists

``
+ Dog
+ Cat
+ Mouse
``

is rendered as
+ Dog
+ Cat
+ Mouse


### Tables

Something like this
``
---------
**A** | **B** | **C**
0 | 0 | X
0 | X | 0
X | 0 | 0
-----:abc
``
is a table and is rendered as
---------
**A** | **B** | **C**
0 | 0 | X
0 | X | 0
X | 0 | 0
-----:abc
Four or more dashes delimit the table and | separates the columns.
The ``:abc`` at the end sets the class for the table and it is optional.

### Blockquote

A table with a single cell is rendered as a blockquote:

-----
Hello world
-----

### Code, ``<code>``, escaping and extra stuff

``
def test():
    return "this is Python code"
``:python

Optionally a ` inside a ``!`!`...`!`!`` block can be inserted escaped with !`!.
The ``:python`` after the markup is also optional. If present, by default, it is used to set the class of the <code> block.
The behavior can be overridden by passing an argument ``extra`` to the ``render`` function. For example:

``
>>> markmin2html("!`!!`!aaa!`!!`!:custom",
       extra=dict(custom=lambda text: 'x'+text+'x'))
``:python

generates

``'xaaax'``:python

(the ``!`!`...`!`!:custom`` block is rendered by the ``custom=lambda`` function passed to ``render``).


### Html5 support

Markmin also supports the <video> and <audio> html5 tags using the notation:
``
[[title link video]]
[[title link audio]]
``

### Latex and other extensions

Formulas can be embedded into HTML with ``$````$``formula``$````$``.
You can use Google charts to render the formula:

``
>>> LATEX = '<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" align="ce\
nter"/>'
>>> markmin2html(text,{'latex':lambda code: LATEX % code.replace('"','\"')})
``

### Code with syntax highlighting

This requires a syntax highlighting tool, such as the web2py CODE helper.

``
>>> extra={'code_cpp':lambda text: CODE(text,language='cpp').xml(),
           'code_java':lambda text: CODE(text,language='java').xml(),
           'code_python':lambda text: CODE(text,language='python').xml(),
           'code_html':lambda text: CODE(text,language='html').xml()}
>>> markmin2html(text,extra=extra)
``

Code can now be marked up as in this example:

``
!`!`
<html><body>example</body></html>
!`!`:code_html
``

### Citations and References

Citations are treated as internal links in html and proper citations in latex if there is a final section called "References". Items like

``
- [[key]] value
``

in the References will be translated into Latex

``
\\bibitem{key} value
``

Here is an example of usage:

``
As shown in Ref.!`!`mdipierro`!`!:cite

## References
- [[mdipierro]] web2py Manual, 3rd Edition, lulu.com
``

### Caveats
``<ul/>``, ``<ol/>``, ``<code/>``, ``<table/>``, ``<blockquote/>``, ``<h1/>``, ..., ``<h6/>`` do not have ``<p>...</p>`` around them.
