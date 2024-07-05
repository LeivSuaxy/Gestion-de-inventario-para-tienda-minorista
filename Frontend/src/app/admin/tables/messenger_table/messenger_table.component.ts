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
import { forkJoin, Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { StyleManagerService } from '../../../styleManager.service';

export interface Messenger {
  ci: string;
  vehicle: string;
  salary_per_km: number;
}

@Component({
  selector: 'app-messenger_table',
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
    RouterLink
  ],
  templateUrl: './messenger_table.component.html',
  styleUrl: './messenger_table.component.css'
})
export class Messenger_tableComponent implements OnInit{
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
      this.eliminarElemento(element);
    });
    this.deleteEmployees();
  }

  @ViewChild(MatTable) table!: MatTable<any>;

  eliminarElemento(id: string) {
    // Eliminar el elemento de la fuente de datos
    const index = this.dataSource.data.findIndex(item => item.ci === id);
    if (index > -1) {
      this.dataSource.data.splice(index, 1);
      // Actualizar el dataSource
      this.dataSource.data = [...this.dataSource.data];
      // Refrescar la tabla, si es necesario
      // this.table.renderRows();
    }
  }

  // Datos para configurar la tabla
  data: any;
  messengers: Messenger[] = []
  dataSource: MatTableDataSource<Messenger> = new MatTableDataSource<Messenger>(this.messengers);
  displayedColumns: string[] = ['select' ,'ci', 'vehicle', 'salary_per_km'];
  selection = new SelectionModel<Messenger>(true, []);
  apiUrl: string = 'http://localhost:8000/api/admin/messengers/'

  constructor(private http: HttpClient, private router: Router, private styleManager: StyleManagerService) {}

  // Llamada a la API para extraer los datos y guardarlos en dataSource
  async ngOnInit() {
    await this.apicall();
    this.dataSource = new MatTableDataSource<Messenger>(this.messengers);
  }

  // Extracción de datos de la API
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

  // Traducción de los datos obtenidos de la API
  traslate(): void {
    this.messengers.push(...this.data['elements'].map((element: any) => ({
      ci: element.ci,
      vehicle: element.vehicle,
      salary_per_km: element.salary_per_km
    })));
  }

  // Busqueda de datos en la tabla
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  // Devuelve si estan todas las filas seleccionadas
  isAllSelected() {
    console.log(this.getSelectedRowsData());
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  // Selecciona todas las filas, si ya todas estan seleccionadas las deselecciona
  toggleAllRows() {
    if (this.isAllSelected()) {
      this.selection.clear();
      return;
    }

    this.selection.select(...this.dataSource.data);
  }

  // Devuelve en un arreglo todas las filas seleccionadas
  getSelectedRowsData(): string[] {
    let ids: any[] = [];

    this.selection.selected.forEach((element) => {
      ids.push(element.ci);
    });

    return ids;
  }

  eliminarEmpleados(carnetIds: string[]) {
    const observables = this.http.post('http://localhost:8000/api/admin/delete_messenger/', { messenger: carnetIds })

    return forkJoin(observables);
  }

  deleteEmployees() {
    this.eliminarEmpleados(this.getSelectedRowsData()).subscribe({
      next: (response) => console.log('Empleados eliminados', response),
      error: (error) => console.error('Error al eliminar empleados', error)
    });
    this.closeConfirmDialog();
  }

  // Muestra en consola las filas seleccionadas
  showSelectedRowsData(): void {
    const selectedRows = this.getSelectedRowsData();
    console.log('Filas seleccionadas:', selectedRows);
  }

  // Selecciona una casilla
  checkboxLabel(row?: Messenger): string {
    if (!row) {
      return `${this.isAllSelected() ? 'deselect' : 'select'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.ci + 1}`;
  }
}
