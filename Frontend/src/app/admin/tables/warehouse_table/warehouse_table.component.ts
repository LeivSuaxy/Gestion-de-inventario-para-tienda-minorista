import { Component, OnInit, ViewChild } from '@angular/core';
import {SelectionModel} from '@angular/cdk/collections';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TablesComponent } from '../tables.component';
import { StockComponent } from '../../../views/stock/stock.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { ButtonsComponent } from '../buttons/buttons.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTable } from '@angular/material/table';
import { forkJoin } from 'rxjs';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

export interface Almacen {
  id_warehouse: number;
  name: string;
  location: string;
}

@Component({
  selector: 'app-warehouse_table',
  templateUrl: './warehouse_table.component.html',
  styleUrls: ['./warehouse_table.component.css'],
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
    CommonModule,
    RouterLink,
    RouterLinkActive
  ],
})
export class Warehouse_tableComponent implements OnInit {

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
    this.deleteInventory();
  }

  @ViewChild(MatTable) table!: MatTable<any>;

  eliminarElemento(id: number) {
    // Eliminar el elemento de la fuente de datos
    const index = this.dataSource.data.findIndex(item => item.id_warehouse === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }

  data: any;
  almacenes: Almacen[] = []
  dataSource: MatTableDataSource<Almacen> = new MatTableDataSource<Almacen>(this.almacenes);
  displayedColumns: string[] = ['select', 'id_warehouse', 'name', 'location'];
  selection = new SelectionModel<Almacen>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/warehouses/'

  constructor(private http: HttpClient, private router: Router) { 
    
  }

  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Almacen>(this.almacenes);
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
    this.almacenes.push(...this.data['elements'].map((element: any) => ({
      id_warehouse: element.id_warehouse,
      name: element.name,
      location: element.location
    })));
  }

  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.id_warehouse);
    });
  
    return ids;
  }

  eliminarAlmacen(ids: string[]) {
    const observables = ids.map(id => 
      this.http.post('http://localhost:8000/api/admin/delete_warehouse/', { id_warehouse: id }),
    );
    return forkJoin(observables);
  }

  deleteInventory() {
    this.eliminarAlmacen(this.getSelectedRowsData()).subscribe({
      next: (response) => console.log('Inventarios eliminados', response),
      error: (error) => console.error('Error al eliminar inventarios', error)
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
  checkboxLabel(row?: Almacen): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id_warehouse + 1}`;
  }

}
