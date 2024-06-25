import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {ChangeDetectionStrategy} from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-postcar',
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
    RouterLinkActive
  ],
  templateUrl: './postcar.component.html',
  styleUrl: './postcar.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PostcarComponent {
  name? : string;
  price? : number;
  description? : string;
  image? : File;
  stock? : number;
  
  constructor(private http : HttpClient, private router: Router) {
  }

  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_product/';
    const formData = new FormData();
    formData.append('image', this.image ? this.image : '');
    formData.append('name', this.name?.toString() ?? '');
    formData.append('price', this.price?.toString() ?? '');
    formData.append('description', this.description?.toString() ?? '');
    formData.append('stock', this.stock?.toString() ?? '');
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json(); // Asumiendo que el servidor responde con JSON
      console.log(data); // Manejar la respuesta del servidor
      this.name = this.price = this.description = this.image = this.stock = undefined;
  
      if (!again) {
        this.router.navigate(['/tables/product_table']);
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
      // Manejar el error adecuadamente en la UI
    }
  }

  onFileSelected(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target && target.files && target.files.length > 0) {
      this.image = target.files[0];
    }
  }

  cancel(): void {
    this.router.navigate(['/tables/product_table']);
  }
}
