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
import axios from 'axios';

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
  category? : string;

  constructor(private http : HttpClient, private router: Router) {
  }

  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_product/';
    const formData = new FormData();
    formData.append('name', this.name ? this.name : '');
    formData.append('price', this.price?.toString() ?? '');
    formData.append('stock', this.stock?.toString() ?? '');
    formData.append('description', this.description ? this.description : '');
    formData.append('category', this.category ? this.category : '');
    if (this.image) {
      formData.append('image', this.image ? this.image : '');
    }
  
    console.log(formData.get('name'), formData.get('category'), formData.get('image'), formData.get('price'), formData.get('description'), formData.get('stock'));
    try {
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
  
      console.log(response.data);
      this.name = this.price = this.description = this.image = this.stock = this.category = undefined;
  
      if (!again) {
        this.router.navigate(['/tables/product_table']);
      } else {
        this.name = "";
        this.stock = undefined;
        this.price = undefined;
        this.description = "";
        this.image = undefined;
      }
    } catch (error) {
      console.error('There was a problem with your axios operation:', error);
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
