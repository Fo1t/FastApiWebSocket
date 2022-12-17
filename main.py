from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import uvicorn

host = str(input('External server ip address:'))
port = int(input('Enter port:'))

app = FastAPI()

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Сообщение</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    </head>
    <body>
        <form action="" onsubmit="sendMessage(event)" style="margin-top: 25%;">
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text" id="inputGroup-sizing-default">Сообщение</span>
                </div>
            <input type="text" id="messageText" autocomplete="off" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default"/>
            <button>Отправить</button>
            </div>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://{host}:{port}/ws");
            """ + """ws.onmessage = function(event) {
                var jso = JSON.parse(event.data);
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(jso.index + ': ' + jso.msg)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = JSON.stringify({ "msg": document.getElementById("messageText").value});
                ws.send(input)
                var inp = document.getElementById("messageText")
                inp.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    index = 1
    try:
        while True:
            data = await websocket.receive_json()
            await websocket.send_json({
                'index': index,
                'msg': data['msg']
                })
            index += 1
    except WebSocketDisconnect:
        pass
        
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)