//import { ChatService } from './chat.service';

import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {CommonModule} from '@angular/common';
import {HttpClient} from "@angular/common/http";
import Pusher from 'pusher-js';

 
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
  standalone: true,
  imports: [FormsModule,CommonModule]
})
export class AppComponent implements OnInit {
  
  username = 'username';
  message = '';
  messages: { username: string, message: string }[] = [];
  
  constructor(private http: HttpClient) { }
  
  
  // Inside your component class
  ngOnInit(): void {
    Pusher.logToConsole = true;

    Pusher.logToConsole = true;

    const pusher = new Pusher('25291c0752d6089a660c', {
      cluster: 'eu'
    });

    const channel = pusher.subscribe('chat');
    channel.bind('message', (data: never) => { // Specify the type of 'data'
      this.messages.push(data);
    });
  }
  



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
      console.log(response);
  
      // Clear the message input field after the request
      this.message = '';
    }, (error: any) => {
      console.error(error);  // Log any errors
    });
  }
  
  
}
