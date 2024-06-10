import { Component } from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import {NgIf} from "@angular/common";
import {Router, RouterLink} from '@angular/router';
import {HttpClient, HttpClientModule} from "@angular/common/http";

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

  constructor(private http: HttpClient,private router: Router) { }

  loginAccount():void {
    console.log(this.loginForm.value);

    const account = {
      username: this.loginForm.value.username,
      password: this.loginForm.value.password
    };


    this.http.post('http://localhost:8000/api/auth/register/', account).subscribe(
      response => {
        console.log('Succes', response)
        this.router.navigate(['/main']);
      },
      error => console.error('Error', error)
    );
  }
}
