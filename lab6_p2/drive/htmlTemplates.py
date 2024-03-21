css = '''
<style>
.stApp {
    background-color:#f4faeb;
}

.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex
}
.chat-message.user {
    background-color: #d6c44b
}
.chat-message.bot {
    background-color: #88a9db
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #000;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn1.vectorstock.com/i/thumb-large/85/85/robot-face-icon-smiling-laugh-emotion-robotic-vector-15868585.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://st3.depositphotos.com/16138592/18728/v/450/depositphotos_187280770-stock-illustration-smiling-face-emoji-large-ear.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
