from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import sys
import uvicorn
from path import Path
import os
from BotWriter import botWriter

path = Path(__file__).parent
template_path = path/'templates'

print(os.listdir(path/'templates'))
app = Starlette(debug=True)
templates = Jinja2Templates(directory=template_path)

# index page
@app.route("/")
async def index(request):
    return templates.TemplateResponse('index.html', {'request': request})
    #html_file = path/'templates'/'index.html'
    #return HTMLResponse(html_file.open().read())

@app.route("/liveWriterForm")
async def liveWriterForm(request):
    content = {'request': request}
    return templates.TemplateResponse("liveWriterForm.html", content)

@app.route("/trainingResults")
async def trainingResult(request):
    content = {'request': request}
    return templates.TemplateResponse("trainingResult.html", content)
    #html = template_path/'trainingResult.html'
    #return HTMLResponse(html.open().read())

@app.route("/liveWriter", methods = ["POST"])
async def liveWriter(request):
    form = await request.form()
    usersline = form.get("usersline")
    num_lines = int(form.get("usersnumlines"))
    num_chars = int(form.get("usersnumchars"))
    botline = []
    for i in range(num_lines):
        #botline.append("hahahaha")
        botline.append(botWriter(usersline,num_chars))
    
    return templates.TemplateResponse("botReply.html", 
    {"request": request,"usersline": usersline, "botline": botline})

'''
@app.route('/error')
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)
'''
if __name__ == "__main__":
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")