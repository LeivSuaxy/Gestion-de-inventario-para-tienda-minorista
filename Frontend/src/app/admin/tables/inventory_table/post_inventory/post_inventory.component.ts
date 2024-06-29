import { Component } from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatFormFieldModule} from '@angular/material/form-field';
import {ChangeDetectionStrategy} from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-post_inventory',
  templateUrl: './post_inventory.component.html',
  styleUrls: ['./post_inventory.component.css'],
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
export class Post_inventoryComponent {

  category? : string;
  storage_id? : number;

  constructor(private http : HttpClient, private router: Router) {}

  ngOnInit() {}

  // FIXME Adriano, haz que cuando again == true reinicie las variables
  async posMethod(again: boolean): Promise<void> {
    let url = 'http://localhost:8000/api/admin/insert_inventory/';
    const formData = new FormData();
    formData.append('category', this.category!);
    formData.append('storage_id', this.storage_id!.toString());

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
      this.category = this.storage_id = undefined;

      if (!again) {
        this.router.navigate(['/tables/inventory_table']);
      }
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
      // Manejar el error adecuadamente en la UI
    }
  }

  cancel(): void {
    this.router.navigate(['/tables/inventory_table']);
  }

}


