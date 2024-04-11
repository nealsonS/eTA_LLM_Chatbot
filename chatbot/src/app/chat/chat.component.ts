import { Component, OnInit } from '@angular/core';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  currentMessage = '';
  messages: string[] = [];

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    this.chatService.messages.subscribe(messages => {
      this.messages = messages;
    });
  }

  sendMessage() {
    if (!this.currentMessage.trim()) return;
    this.chatService.sendMessage(this.currentMessage);
    this.currentMessage = '';
  }
}
