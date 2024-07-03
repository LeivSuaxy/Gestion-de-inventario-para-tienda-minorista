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
import { StyleManagerService } from '../../../styleManager.service';

export interface Inventario {
  id_inventario: number;
  categoria: string;
  id_almacen: string;
}

@Component({
  selector: 'app-inventory_table',
  templateUrl: './inventory_table.component.html',
  styleUrls: ['./inventory_table.component.css'],
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
export class Inventory_tableComponent implements OnInit {
  showConfirmDialog = false; // Controla la visibilidad del diálogo

  openConfirmDialog() {
    this.showConfirmDialog = true;
    const body = document.getElementById("contain");
  
    if (body instanceof HTMLElement) {
      body.classList.add('blur-background');
    }
    this.styleManager.setBlurBackground(true);
  }
  
  closeConfirmDialog() {
    this.showConfirmDialog = false;
    const body = document.getElementById("contain");
  
    if (body instanceof HTMLElement) {
      body.classList.remove('blur-background');
    }
    this.styleManager.setBlurBackground(false);
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
    const index = this.dataSource.data.findIndex(item => item.id_inventario === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }

  data: any;
  inventarios: Inventario[] = []
  dataSource: MatTableDataSource<Inventario> = new MatTableDataSource<Inventario>(this.inventarios);
  displayedColumns: string[] = ['select', 'id_inventario', 'categoria', 'id_almacen'];
  selection = new SelectionModel<Inventario>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/inventories/'

  constructor(private http: HttpClient, private router: Router, private styleManager: StyleManagerService) { 
    
  }

  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Inventario>(this.inventarios);
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
    this.inventarios.push(...this.data['elements'].map((element: any) => ({
      id_inventario: element.id_inventory,
      categoria: element.category,
      id_almacen: element.id_warehouse
    })));
  }

  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.id_inventario);
    });
  
    return ids;
  }

  eliminarInventario(ids: string[]) {
    const observables = ids.map(id => 
      this.http.post('http://localhost:8000/api/admin/delete_inventory/', { id: id }),
    );
    return forkJoin(observables);
  }

  deleteInventory() {
    this.eliminarInventario(this.getSelectedRowsData()).subscribe({
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
    console.log(this.getSelectedRowsData());
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
  checkboxLabel(row?: Inventario): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id_inventario + 1}`;
  }

}
