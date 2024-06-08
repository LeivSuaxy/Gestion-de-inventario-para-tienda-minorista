import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, FormGroup } from '@angular/forms';
import {NgIf} from "@angular/common";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import { Router } from '@angular/router';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [ReactiveFormsModule, NgIf, HttpClientModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {
  isCorrect: boolean = true;

  constructor(private hhtp: HttpClient, private router: Router) {
  }

  registerForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
    confirmpassword: new FormControl('')

  });

  createAccount():void {
    console.log(this.registerForm.value);

    const account = {
      username: this.registerForm.value.username,
      password: this.registerForm.value.password
    };


    this.hhtp.post('http://localhost:8000/api/auth/register/', account).subscribe(
      response => {
        console.log('Succes', response)
        this.router.navigate(['/main']);
      },
      error => console.error('Error', error)
    );
  }

  onSubmit(): number {
    if(this.registerForm.value.password == this.registerForm.value.confirmpassword) {
      this.createAccount();
      return 200;
    } else {
      this.isCorrect = false;
      return 400;
    }
  }
}
