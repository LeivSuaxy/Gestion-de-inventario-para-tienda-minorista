import { Component } from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import {NgIf} from "@angular/common";
import {Router, RouterLink} from '@angular/router';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {LogintokenService} from "../../logintoken.service";

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [ReactiveFormsModule, NgIf, RouterLink, HttpClientModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {
  isCorrect: boolean = true;

  loginForm = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
  });

  constructor(private http: HttpClient,private router: Router, private login:LogintokenService) { }

  loginAccount():void {
    const username = this.loginForm.value.username;
    const password = this.loginForm.value.password;

    if(username && password) {
      this.login.loginAPI(username, password);
    } else {
      console.log('Error making login');
    }
  }
}
