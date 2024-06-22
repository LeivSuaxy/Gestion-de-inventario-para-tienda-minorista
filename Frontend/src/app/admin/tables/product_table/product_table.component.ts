import { Component, OnInit, Input } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import { Venta} from "../../../views/stock/cartservice.service";
import {CartService} from "../../../views/stock/cartservice.service";
import {HttpClient, HttpClientModule} from "@angular/common/http";

export interface PeriodicElement {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {position: 1, name: 'Hydrogen', weight: 1.0079, symbol: 'H'},
  {position: 2, name: 'Helium', weight: 4.0026, symbol: 'He'},
  {position: 3, name: 'Lithium', weight: 6.941, symbol: 'Li'},
  {position: 4, name: 'Beryllium', weight: 9.0122, symbol: 'Be'},
  {position: 5, name: 'Boron', weight: 10.811, symbol: 'B'},
  {position: 6, name: 'Carbon', weight: 12.0107, symbol: 'C'},
  {position: 7, name: 'Nitrogen', weight: 14.0067, symbol: 'N'},
  {position: 8, name: 'Oxygen', weight: 15.9994, symbol: 'O'},
  {position: 9, name: 'Fluorine', weight: 18.9984, symbol: 'F'},
  {position: 10, name: 'Neon', weight: 20.1797, symbol: 'Ne'},
];

@Component({
  selector: 'app-product_table',
  templateUrl: './product_table.component.html',
  styleUrls: ['./product_table.component.css'],
  standalone: true,
  imports: [HttpClientModule, MatTableModule, MatCheckboxModule, TablesComponent, StockComponent],
})
export class Product_tableComponent implements OnInit {

  data: any;
  products: Venta[] = []
  aux: Venta[] = []
  counterPage: number = 0;

  constructor(private http: HttpClient) { 
    
  }

  ngOnInit() {
    this.apicall();
    this.comprobar();
  }

  private async apicall(): Promise<void> {
    let nextPage = true;
    while (nextPage) {
      try {
        const response = await this.http.get(`http://localhost:8000/api/objects/?page=${this.counterPage}`).toPromise();
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

  comprobar(): void {
    let arreglo: string[][] = [['pepe', 'antonio', 'patricia'], ['rolando', 'jose', 'luis'], ['maria', 'laura', 'lucia']];

    console.log(this.products);
    
    for (let i = 0; i < this.products.length; i++) {
      console.log(this.products[i])
    }
    console.log(this.aux)
  }

  displayedColumns: string[] = ['select', 'position', 'name', 'weight', 'symbol'];
  dataSource = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  selection = new SelectionModel<PeriodicElement>(true, []);

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
  checkboxLabel(row?: PeriodicElement): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.position + 1}`;
  }

}
