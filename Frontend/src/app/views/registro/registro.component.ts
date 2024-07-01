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
  isValid : boolean = true;
  ci: string = '';
  username: string = '';
  password: string = '';
  cpassword: string = '';


  constructor(private http: HttpClient, private router: Router) {
  }

  registerForm = new FormGroup({
    username: new FormControl(''),
    ci: new FormControl(''),
    password: new FormControl(''),
    cpassword: new FormControl('')
  });

  createAccount(): void {
    console.log(this.registerForm.value);
  
    const account = {
      ci: this.registerForm.value.ci,
      username: this.registerForm.value.username,
      password: this.registerForm.value.password
    };
  
    this.http.post<any>('http://localhost:8000/api/auth/register/', account).subscribe(
      response => {
        console.log('Success', response);
        // Asumiendo que el token viene en un campo llamado 'token' en la respuesta
        const token = response.token;
        // Almacenar el token en el almacenamiento local
        localStorage.setItem('authToken', token);
        // Navegar a la página de inicio
        this.router.navigate(['/home']);
      },
      error => console.error('Error', error)
    );
  }

  onSubmit(): number {
    if(this.registerForm.value.password === this.registerForm.value.cpassword) {
      this.isValid = true;
      this.createAccount();
      return 200;
    } else {
      this.isValid = false;
      return 400;
    }
  }
}
