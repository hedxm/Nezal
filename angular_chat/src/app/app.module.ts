import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
//import {CommonModule} from '@angular/common';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import {HttpClientModule} from "@angular/common/http";


@NgModule({
  declarations: [
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserModule
  ],
  providers: [],
  
})
export class AppModule {
}
