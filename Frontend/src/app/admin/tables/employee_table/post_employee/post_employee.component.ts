import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import {MatCheckboxModule} from '@angular/material/checkbox';

@Component({
  selector: 'app-post_employee',
  templateUrl: './post_employee.component.html',
  styleUrls: ['./post_employee.component.css'],
  standalone: true,
  imports: [
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    RouterLink,
    RouterLinkActive,
    MatCheckboxModule
  ],
})
export class Post_employeeComponent {

  name? : string;
  ci? : string;
  salary? : number;
  ci_boss? : string;

  constructor(private http : HttpClient, private router: Router) {
  }

  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_employee/';
    const employeeData = {
      employee: { // Añadir este nivel para encapsular los datos del empleado
        ci: this.ci ? this.ci : '',
        name: this.name ? this.name : '',
        salary: this.salary?.toString() ?? '',
        id_boss: this.ci_boss ? this.ci_boss : ''
      }
    };
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(employeeData)
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      console.log(data);
      this.ci = this.name = this.salary = this.ci_boss = undefined;
  
      if (!again) {
        this.router.navigate(['/tables/employee_table']);
      } else {
        this.name = "";
        this.ci = "";
        this.salary = undefined;
        this.ci_boss = "";
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
    }
  }

  cancel(): void {
    this.router.navigate(['/tables/employee_table']);
  }

}