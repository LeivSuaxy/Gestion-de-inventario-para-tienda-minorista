import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-post_warehouse',
  templateUrl: './post_warehouse.component.html',
  styleUrls: ['./post_warehouse.component.css'],
  standalone: true,
  imports: [
    FormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
  ],
})
export class Post_warehouseComponent {

  name? : string;
  location? : string

  constructor(private http : HttpClient, private router: Router) {}

  ngOnInit() {}

  // FIXME Adriano, has que cuando again == true reinicie las variables
  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_warehouse/';
    const formData = new FormData();
    formData.append('name', this.name!);
    formData.append('location', this.location!);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data);
      this.name = this.location = undefined;

      if (!again) {
        this.router.navigate(['/tables/warehouse_table']);
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
    }
  }

  cancel(): void {
    this.router.navigate(['/tables/warehouse_table']);
  }

}
