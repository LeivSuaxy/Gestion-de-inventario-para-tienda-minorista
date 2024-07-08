import { Component } from '@angular/core';
import { FormsModule } from "@angular/forms";
import {HttpClientModule } from "@angular/common/http";
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { SharedService } from '../shared.service';
import { CartService } from '../cartservice.service';

@Component({
  selector: 'app-post_client',
  templateUrl: './post_client.component.html',
  styleUrls: ['./post_client.component.css'],
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
export class Post_clientComponent {
  name? : string;
  ci? : string;
  email? : string;
  phone? : number;

  constructor(private router: Router, private sharedService: SharedService, private cartService: CartService) { }

  async posMethod(): Promise<void> {
    let url = 'http://localhost:8000/api/public/purchaseproducts/';
    const clientData = {
      client: { // Añadir este nivel para encapsular los datos del empleado
        ci: this.ci ? this.ci : '',
        name: this.name ? this.name : '',
        email: this.email ? this.name : '',
        phone: this.phone?.toString() ?? '',
      },
      products: this.cartService.cartJson()
    };
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(clientData)
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      console.log(data);
      this.ci = this.name = this.email = this.phone = undefined;
  
      this.sharedService.triggerFunction('closeDialog');
 
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
    }
  }

  camposLlenos(): boolean {
    return (this.ci ?? '').trim().length > 0 && 
           (this.name ?? '').trim().length > 0 && 
           this.isValidEmail(this.email) && 
           (this.phone ?? '').toString().trim().length > 0;
  }

  isValidEmail(email: string | undefined): boolean {
    if (email === undefined) {
      return false;
    }
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return regex.test(email);
  }

  cancel(): void {
    this.sharedService.triggerFunction('closeDialog');
  }

}
