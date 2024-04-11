import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private messageSubject = new BehaviorSubject<string[]>([]);
  public messages = this.messageSubject.asObservable();

  constructor() {}

  sendMessage(message: string): void {
    const currentMessages = this.messageSubject.value;
    this.messageSubject.next([...currentMessages, `You: ${message}`, `Bot: Echoing "${message}"`]);
  }
}
