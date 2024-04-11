import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // The content could be dynamic as well, based on the user interaction or other logic
  chatContent = [
    {
      message: "Hi I want to know if grades for HW1 has been released?",
      time: "10:10 AM, Today",
      sender: "other"
    },
    {
      message: "Hi, we are still in the progress of grading and we will release the grades once we finish.",
      time: "10:12 AM, Today",
      sender: "mine"
    },
    {
      message: "Ok, thank you.",
      time: "10:14 AM, Today",
      sender: "other"
    }
  ];

  // Method to simulate changing the chat when clicking on a different user
  changeChat(): void {
    // This method could be expanded to change the chat content based on the user clicked
    console.log('Chat changed');
  }
}
