#!/usr/bin/env python
from itty.itty import *
from markmin2html import markmin2html

######################################################
# Configuration
config = {}
config["wikiname"] = "waaywiki"
#######################################################

html_layout = """
<html>
<head>
<title> %(title)s </title>
<link rel='stylesheet' href='/css/extra.css?v=2'>
<link rel='stylesheet' href='/css/table.css?v=2'>
<script type="text/javascript">
function prompt_restore(page, commit){
if(window.confirm("Revert to revision " + commit+" ?"))
  window.location = "/revert/"+page+"/" + commit;
}
</script>
</head>
<body>
<h1>waaywiki</h1>
%(header)s
<hr>
<div id='main'>
%(body)s
</div>
</body>
</html>
"""

html_log_line = """
<tr>
<td align='left'><a href='/view/%(page)s?version=%(commit)s'>%(commit)s</a></td>
<td align='left' width='10%%'>%(date)s</td>
<td align='left' width='20%%'>%(author)s</td>
<td align='left' >%(message)s</td>
<td width=10%%><a href='#' onclick="prompt_restore('%(page)s','%(commit)s')"'>Restore</a></td>
</tr>
"""

html_edit = """
<div class='error'>%(error)s</div>
<div>
<form action='/edit/%(page)s' method=post name='f1'>
<textarea name='text' cols=80 rows=25>%(text)s</textarea><br>
<p><input type=text name='msg' value='Log Message' size=50/>
<p><input type=submit value='submit'>
<input type=submit value='Preview'

onclick="this.form.target='_blank';
f1.action='/preview/%(page)s'; return true;">
</form>
</div>
<a href='/view/%(page)s'>View Page</a> | <a href='/view/MarkminHelp'>Editing Help</a>
"""

html_view_footer = """
<hr>
<a href='/edit/%(page)s'>Edit</a> | <a href='/log/%(page)s'>History</a> | (@%(version)s)
"""

def git_head(file):
    try:
        return git_log(file, 1)[0]["commit"]
    except IndexError:
        return "Unknown"

def git_add_commit(file, msg):
    import subprocess as sub
    try:
        sub.check_call(["git", "add", file], cwd="./files")
        sub.check_call(["git", "commit", "-m", msg], cwd = "./files")
    except sub.CalledProcessError,e:
        print e
        return False
    return True

def git_show(fname, version):
    import subprocess as sub
    p = sub.Popen(["git", "show", "%s:%s" % (version, fname)], cwd = "./files", stdout=sub.PIPE)
    (out, err) = p.communicate()
    if p.returncode == 0:
        return out
    else:
        return "Version does not exist"


def git_log(file, max=None):
    import subprocess as sub
    cmd = ["git", "log", "--pretty=medium", "--relative-date", "-z", "--abbrev-commit"]
    if max is not None:
        cmd += ["-n", str(max)]
    cmd += [file]
    print cmd
    p = sub.Popen(cmd, cwd = "./files", stderr=sub.PIPE, stdout=sub.PIPE)
    (out, err) = p.communicate()
    print out
    l = out.split("\0")
    logs = []
    for k in l:
        m = {}
        l2 = k.split("\n")
        if len(l2) < 4:
            continue
        m["commit"] = l2[0].split()[1].strip().rstrip()
        m["author"] = l2[1].split(":")[1].strip().rstrip()
        m["date"] = "".join(l2[2].split(":")[1:]).strip().rstrip()
        m["message"] = l2[4].strip().rstrip()
        logs.append(m)
    return logs

def git_restore(file, commit):
    import subprocess as sub
    try:
        sub.check_call(["git", "checkout", commit, file], cwd="./files")
        sub.check_call(["git", "commit", "-m", "Reverting to commit %s" % commit], cwd="./files")
    except sub.CalledProcessError,e:
        print e
        return False
    return True

def render_html(page, body, **kwargs):
    opts = kwargs
    kwargs.update({
        "title" : "%s : %s" % (config["wikiname"], page),
        "header":"<a href='/' class='header'>%(wiki)s</a> // <a href='/view/%(page)s' class='header'>%(page)s</a>" % {"wiki":config["wikiname"],
                                                                                       "page":page},
                   "body":body,
                   "page": page})
    kwargs.update(config)
    return html_layout % opts

@get('/')
def index(request):
    raise Redirect("/view/Home")

@get('/view/(?P<page>\w+)')
def view(request, page):
    version = request.GET.get("version", None)
    if version is not None:
        return render_page_git(page, version)
    elif not os.path.exists("files/%s.mm" % page):
        return render_html(page, "This page does not exist. <a href='/edit/%s'>Create?" % page)
    else:
        return render_page_file(page)

def render_page_file(page):
    body = markmin2html(open("files/%s.mm" % page).read())
    body += html_view_footer % {"page":page ,
                                "version":git_head("%s.mm" % page)}
    return render_html(page,  body)

def render_page_git(page, version):
    body = markmin2html(git_show("%s.mm" % page, version))
    body += html_view_footer % {"page":page , "version":version}
    return render_html(page,  body)

def render_page_string(page, s):
    body = markmin2html(s)
    body += html_view_footer % {"page":page , "version":"PREVIEW"}
    return render_html(page,  body)

@get('/edit/(?P<page>\w+)')
def edit(request, page):
    if os.path.exists("files/%s.mm" % page):
        text = open("files/%s.mm" % page).read()
    else:
        text = ""
    body = html_edit % {"page": page, "text": text, "error":request.GET.get("error", "")}
    return render_html("Editing %s" % page,
                       body)

@post('/edit/(?P<page>\w+)')
def edit(request, page):
    open("files/%s.mm" % page, "w").write(request.POST.get("text"))
    if git_add_commit("%s.mm" % page,
                      request.POST.get("msg", "Empty log")):
        raise Redirect("/view/%s" % page)
    else:
        raise Redirect("/edit/%s?error='Could not add'" % page)

@post('/preview/(?P<page>\w+)')
def preview(request, page):
    s = request.POST.get("text")
    return render_page_string(page, s)

@get("/log/(?P<page>\w+)")
def log(request, page):
    log = git_log("%s.mm" % page)
    error = request.GET.get("error", "")
    print log
    for l in log:
        l["page"] = page
    loghtml = [html_log_line % l for l in log]
    body = """<h1>History of <a href='/view/%s'>%s</a></h1> <div class='error'>%s</div> <div class='centered'>
    <table><tr><th width=10%%>Version</th><th>Date</th><th>Author</th><th>Message</th><th></th>""" % (page, page, error)
    body += "\n".join(loghtml)+"</table></div><hr>"
    body +="<a href='/view/%s'>View Latest</a>" % page
    return render_html(page,
                       body)

@get("/revert/(?P<page>\w+)/(?P<commit>\w+)")
def revert(request, page, commit):
    if git_restore("%s.mm" % page, commit):
        raise Redirect("/view/%s" % page)
    else:
        raise Redirect("/log/%s?error='Could not revert'" % page)

@get('/css/(?P<filename>.+)')
def css(request, filename):
    return serve_static_file(request, filename, root="./css")

run_itty()

