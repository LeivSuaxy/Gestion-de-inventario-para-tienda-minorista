import { Component } from '@angular/core';
import { FormControl, ReactiveFormsModule, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {
  registerForm = new FormGroup({
    name: new FormControl(''),
    password: new FormControl(''),
    confirmpassword: new FormControl('')

  });

  onSubmit(): number {
    if(this.registerForm.value.password == this.registerForm.value.confirmpassword) {
      console.log(this.registerForm.value)
      console.log('Form submitted');
      return 200;
    } else {
      console.log('Error');
      return 400;
    }
  }
}
