

import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {CommonModule} from '@angular/common';
import {HttpClient} from "@angular/common/http";
//import Pusher from 'pusher-js';

 
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
  imports: [FormsModule,CommonModule]
})
export class AppComponent{
  
  username = 'username';
  message = '';
  messages: { username: string, message: string }[] = [];
  response = ''; // Initialize the 'response' variable
  chatbotName = 'Nezal'; // Initialize the chatbot's name
  chatbotResponses: string[] = []; // Initialize an empty array
  
  constructor(private http: HttpClient) { }
  
  

  



  // submit(): void {
  //   console.log("Llegue a submit")
  //   this.http.post('http://localhost:8000/api/messages', {
  //     username: this.username,
  //     message: this.message
  //   }).subscribe(() => this.message = '');
  // }

  

  submit(): void {
    console.log("Llegué a submit");
    console.log(this.message);  // Log the message before sending it
  
    // Push the new message to the messages array
    this.messages.push({
      username: this.username,
      message: this.message
    });
  
    this.http.post('http://localhost:8000/api/messages', {
      username: this.username,
      message: this.message
    }).subscribe((response: any) => {
      this.message = '';
      console.log(response);
      this.response = response;
      this.chatbotResponses.push(response);
      // Clear the message input field after the request
    }, (error: any) => {
      console.error(error);  // Log any errors
    });
  }
  
  
}
