<!-- Header: Blog Engine Description -->
<!-- Tag: python -->
<!-- Tag: cpp -->
<!-- Summary: Overview of this blog engine functional description (what's it for?) -->
<!-- Summary: and explanation of its structure (how one could use it?). -->

## What Is It For?

This "blog engine" is supposed to be a transparent tool for:

1. building a big _vision_ from small strokes in incremental manner
2. collecting random _observations_

One could think about this engine as a hybrid between blog and wiki.

### Building

When one is doing a long lasting project with either complicated or
not fully invented structure, it is necessary to have a communication
tool which would help to accumulate gained vision of the structure.

Since vision doesn't fully appear in a moment, engine should be flexible
enough to suffer from compulsory transformations. It should also track all
changes since creation is messy and rewritten versions can contain valuable
information.

### Collecting

In traditional blogging one is supposed to generate "linear increment"
of stuff by pushing completed postings at the top of the "postings line".
Such an approach is convenient for a model where posting value is bound to
time.

This engine is oriented on "random, locally convergent, increment" of stuff.
By locally convergent it is meant that frequency of posting updates is
decreasing with time. So basically it is like wiki for articles which are
supposed to become pretty finished in a small number of updates.

### Aesthetics

Engine is supposed to be a "mentally thin thing". It should minimally bother
a user. No web-interfaces for editing, no data bases for storage. Just a
directory with a bunch of text files which are stored in a git repository.
One could `grep` them, `sed` them and use his favorite editor to update them.

Every text file is basically just a
[markdown](https://help.github.com/articles/markdown-basics/) file with
support for TeX and syntax highlighting. Tags are supported for more
convenient visual representation. See **Design:** sections for more detail.

## How One Could Use It?

In order to set up blog engine, one need a server with
[**django**](https://www.djangoproject.com/) and
[**git**](http://git-scm.com/).

### Set Up

Installation consists of

1. installation of
   [dango application](https://github.com/kishmakov/blog_engine/tree/master/blog)
   on the server
2. installation of a git server
3. installation of markdown
   [python package](https://github.com/waylan/Python-Markdown)
4. configuration of the
   [hook file](https://github.com/kishmakov/blog_engine/blob/master/post-receive)
   which should be added to the git server

Configuration is just a setting of four paths, which is better understood
through work cycle.

### How Does It Work?

1. each entry of the form _yyyymmdd_name.txt_ is extracted and kept in
   `BLOG_ENTRIES` directory altogether with 3 additional description files of
   the form: _yyyymmdd_name.header_, _yyyymmdd_name.summary_ and
   _yyyymmdd_name.tags_
2. part of the entry is also kept compiled from markdown into
   _yyyymmdd_name.html_ and stored in `BLOG_TEMPLATES` directory, which is used
   by django application
3. when freshly updated entries are commited to git server, hook would update
   corresponding description files and recompile django template
4. after updates were finished hook would assemble `entry_tools.py` and
   `list_tools.py` (examples provided below) based on description files and
   would put them into `BLOG_COMMON` directory
5. finally hook would restart django with command via `RESTART_CMD`

**`entry_tools.py`**
<pre class='brush: py'>
descriptions = {
    '20150109_blog_conception': {
        'id': '20150109_blog_conception',
        'header': 'Blog Engine Conception',
        'updated': '2015-01-09 @ 20:57',
        'summary': ["Overview of this blog engine functional description.",],
        'navi_tags': ['programming tools'],
        'syntax_tags': ['python'],
    },
    '20141217_macros_explosion': {
        'id': '20141217_macros_explosion',
        'header': 'Explosive Macros Example',
        'updated': '2015-01-07 @ 19:45',
        'summary': ['A small code which demonstrates C++ compiler constraints.',],
        'navi_tags': ['fun'],
        'syntax_tags': ['cpp'],
    },
}
</pre>

**`list_tools.py`**
<pre class='brush: py'>
search_ids = [
    '20150109_blog_conception',
    '20141217_macros_explosion',
]
search_tags = {
    'fun': [1, ],
    'programming tools': [0, ],
}
</pre>

### Design: Format

Each file should consist of 4 sections: `Tags`, `Header`, `Summary`
and `Body`. Each section name line should look like `=== Header ===` with
at least 3 `=` characters from each side.

`Tags` section consists of technical tags. Tags are divided into navigational,
syntactical and referential. Tags from two last groups must match specific
patterns. First group tags could be arbitrary with natural restriction not to
fall into other groups patterns. All tags are supposed to be separated by `;`.

1. Navigational tags are used for external tagging of entries. Through these
   tags selection of specific entries is possible.
2. Syntactical tags control
   [syntax highlighting](http://alexgorbatchev.com/SyntaxHighlighter/) brushes
   and [mathjax](http://mathjax.org) support. Tags `syntax cpp`, `syntax js`,
   `syntax python` and `syntax xml` turn on support for C++, JavaScript, Python
   and XML (HTML) highlighting correspondingly. MathJax support could be turn
   on via `syntax mathjax`.
3. Referential tags include references into entry context. Mentioning of the
   reference in tags section is necessary for enabling subsequent citations.
   These tags must match pattern `ref S ID` where S stands for type of source
   (see section **Design: Reference System** for detail) and ID stands for
   identifier.

### Design: Syntax Higlighting

Code syntax higlighting is currently supported for C++, JavaScript, Python and
XML (HTML). One need to turn on corresponding functionality through syntactical
tags (see **Design: Format** section for more detail). Once it is done,
code snippets could be inserted into file as

<pre>
&lt;pre class='brush: cpp'>
void print(ostream * out, int num)
{
    *out &amp;lt;&amp;lt; num;
}
&lt;/pre>
</pre>

with all `<` characters replaced by `&lt;` within inserted snippet due to
SyntaxHiglighter requirements. Such a snippet produces result as follows

<pre class='brush: cpp'>
void print(ostream * out, int num)
{
    *out &lt;&lt; num;
}
</pre>

### Design: Math Typesetting

Math Typesetting could be turned on via syntactical tags (see
**Design: Format** section). MathJax supports Latex code insertion in a
number of ways:

* with <span style="color:#C7254E">\(</span> and <span style="color:#C7254E">\)</span> paired delimiters for in-line formulas
* with `$$` and `$$` delimeters for displayed unnumbered formulas
* with `\begin{equation}` and `\end{equation}` for displayed numbered formulas

In case of numbered formulas, it is convenient to insert `\label{label_name}`
instruction somewhere inside formula code and to invoke this equation number
with `\eqref{label_name}` in arbitrary part of the file.

### Design: References System

All references are stored in the file `references.json`. At the top level it
consists of 4 sections: _book_, _paper_, _link_ and _other_. Sections are
basically maps which map items ids to its descriptions. An example of paper
with id `hughes_1989` is provided below (see a
[work copy](https://github.com/kishmakov/blog/blob/master/references.json) for
more examples).

<pre>
{
    "paper": {
        ...
        "hughes_1989" : {
            "authors": ["John Hughes"],
            "year": 1989,
            "journal": {
                "title": "The Computer Journal",
                "volume": 32,
                "issue": 2,
                "pages": [98, 107],
                "doi": "10.1093/comjnl/32.2.98"
            },
            "title": "Why Functional Programming Matters",
            "link": "http://www.cse.chalmers.se/~rjmh/Papers/whyfp.pdf"
        },
        ...
    },
}
</pre>

Once record is specified in reference file, it could be invoked in any entry.
In order to do it one need to mention it in referential tags (see
**Design: Format** section). The order of appearance of referential tags
specifies references numeration in the list at the bottom of the page.

Occurrences of the form <span>[</span>ref paper hughes_1989<span>]</span>
turn into cross-links to the detailed references description list at the bottom
of the page.
