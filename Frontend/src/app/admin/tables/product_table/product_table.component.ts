import { Component, OnInit, ViewChild } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import { MatTable } from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Venta } from '../../../views/stock/cartservice.service'
import { CommonModule } from '@angular/common';
import { forkJoin, Observable } from 'rxjs';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-product_table',
  templateUrl: './product_table.component.html',
  styleUrls: ['./product_table.component.css'],
  standalone: true,
  imports: [
    HttpClientModule,
    MatTableModule,
    MatCheckboxModule,
    TablesComponent,
    StockComponent,
    MatIconModule,
    MatButtonModule,
    ButtonsComponent,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    HttpClientModule,
    CommonModule,
    RouterLink,
    RouterLinkActive
  ],
})
export class Product_tableComponent implements OnInit {
  showConfirmDialog = false; // Controla la visibilidad del diálogo

  // Otros métodos y propiedades...
  openConfirmDialog() {
    this.showConfirmDialog = true;
  }

  deleteConfirmed() {
    this.showConfirmDialog = false;
    let filas: string[] = this.getSelectedRowsData();
    filas.forEach((element) => {
      this.eliminarElemento(parseInt(element));
    });
    this.deleteProducts();
  }

  @ViewChild(MatTable) table!: MatTable<any>;

  eliminarElemento(id: number) {
    // Eliminar el elemento de la fuente de datos
    const index = this.dataSource.data.findIndex(item => item.id_producto === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }


  data: any;
  products: Venta[] = []

  dataSource: MatTableDataSource<Venta> = new MatTableDataSource<Venta>(this.products);
  displayedColumns: string[] = ['select', 'id_producto', 'nombre', 'categoria', 'stock', 'precio'];
  selection = new SelectionModel<Venta>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/products/'

  constructor(private http: HttpClient) {

  }

  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Venta>(this.products);
  }

  private async apicall(): Promise<void> {
    if (this.apiUrl) {
      try {
        const response = await this.http.get(this.apiUrl).toPromise();
        this.data = response;
        this.traslate();
      } catch (error) {
        console.error(error);
      }
    }
  }

  traslate(): void {
    this.products.push(...this.data['elements'].map((element: any) => ({
      nombre: element.name,
      id_producto: element.id_product,
      precio: element.price,
      stock: element.stock,
      categoria: element.category,
      descripcion: element.description,
      imagen: element.image,
    })));
  }

  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.id_producto);
    });

    return ids;
  }

  eliminarProductos(ids: string[]): Observable<any[]> {
    // Mapea cada id a una petición HTTP individual
    const observables = ids.map(id =>
      this.http.post('http://localhost:8000/api/admin/delete_product', { id: id }),
    );

    // forkJoin espera a que todos los observables se completen y luego emite los valores de todos ellos
    return forkJoin(observables);
  }

  deleteProducts() {
    this.eliminarProductos(this.getSelectedRowsData()).subscribe({
      next: (response) => console.log('Productos eliminados', response),
      error: (error) => console.error('Error al eliminar productos', error)
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Venta): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id_producto + 1}`;
  }

}

