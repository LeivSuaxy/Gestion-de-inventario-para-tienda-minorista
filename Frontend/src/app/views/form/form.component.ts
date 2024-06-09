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

  registerForm = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
  });

  constructor(private http: HttpClient,private router: Router) { }

  createAccount():void {
    console.log(this.registerForm.value);

    const account = {
      username: this.registerForm.value.username,
      password: this.registerForm.value.password
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
