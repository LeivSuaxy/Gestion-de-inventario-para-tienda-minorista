import { Component } from '@angular/core';
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-registro',
  standalone: true,
    imports: [
        FormsModule,
        NgIf,
        ReactiveFormsModule,
        RouterLink
    ],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})
export class RegistroComponent {


  constructor(private http: HttpClient, private router: Router) {
  }

  registerForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
    cpassword: new FormControl('')
  });

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
