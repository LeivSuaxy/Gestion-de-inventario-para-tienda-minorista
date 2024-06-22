import { Component, OnInit, Input } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import { Venta} from "../../../views/stock/cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';

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
    ButtonsComponent
  ],
})
export class Product_tableComponent implements OnInit {

  data: any;
  products: Venta[] = []
  aux: Venta[] = []
  counterPage: number = 0;

  dataSource: MatTableDataSource<Venta> = new MatTableDataSource<Venta>(this.products);
  displayedColumns: string[] = ['select', 'id_producto', 'nombre', 'categoria', 'stock', 'precio'];
  selection = new SelectionModel<Venta>(true, []);

  constructor(private http: HttpClient) { 
    
  }

  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Venta>(this.products);
  }

  private async apicall(): Promise<void> {
    let nextPage = true;
    while (nextPage) {
      try {
        const response = await this.http.get(`http://localhost:8000/api/public/objects/?page=${this.counterPage}`).toPromise();
        this.data = response;
        this.traslate();
        this.counterPage++;
        nextPage = !!this.data['urls'].next; // Continúa si hay una siguiente página
      } catch (error) {
        console.error(error);
        nextPage = false; // Detiene el bucle si hay un error
      }
    }
  }
  
  traslate(): void {
    this.products.push(...this.data['elements'].map((element: any) => ({
      nombre: element.nombre,
      id_producto: element.id_producto,
      precio: element.precio,
      stock: element.stock,
      categoria: element.categoria,
      descripcion: element.descripcion,
      imagen: element.imagen
    })));
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
