from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
import sys
import uvicorn
from path import Path
import os
from BotWriter import botWriter

path = Path(__file__).parent
template_path = path/'templates'

app = Starlette(debug=True)
templates = Jinja2Templates(directory=template_path)

# index page
@app.route("/")
async def index(request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.route("/liveWriterForm")
async def liveWriterForm(request):
    content = {'request': request}
    return templates.TemplateResponse("liveWriterForm.html", content)

@app.route("/trainingResults")
async def trainingResult(request):
    content = {'request': request}
    return templates.TemplateResponse("trainingResult.html", content)

@app.route("/liveWriter", methods = ["POST"])
async def liveWriter(request):
    form = await request.form()
    usersline = form.get("usersline")
    num_lines = int(form.get("usersnumlines"))
    num_chars = int(form.get("usersnumchars"))
    botline = []
    for i in range(num_lines):
        botline.append(botWriter(usersline,num_chars))
    
    return templates.TemplateResponse("botReply.html", 
    {"request": request,"usersline": usersline, "botline": botline})

if __name__ == "__main__":
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8080, log_level="info")